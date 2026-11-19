from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from .auth import AUTHORIZED_PARTIES, get_current_user, require_admin
from .database import get_db
from .models import Lesson, UserLessonProgress
from .services.users import get_or_create_user

from .schemas.Lesson import LessonCreate, LessonResponse, LessonUpdate
from .schemas.LessonCompletion import LessonCompletionResponse
from .schemas.UserProgress import UserProgressResponse

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # The frontend origins are the same set Clerk tokens are accepted from.
    allow_origins=sorted(AUTHORIZED_PARTIES),
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/me")
def get_me(
    clerk_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = get_or_create_user(db, clerk_id)
    return {"id": user.id, "clerk_id": user.clerk_id}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/lessons", response_model=list[LessonResponse])
def get_lessons(db: Session = Depends(get_db)):
    return db.execute(select(Lesson).order_by(Lesson.id)).scalars().all()

@app.get("/lessons/{lesson_id}", status_code=200, response_model=LessonResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson



def commit_lesson(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A lesson with this title already exists"
        )


@app.post("/lessons", status_code=201, response_model=LessonResponse)
def create_lesson(
    lesson: LessonCreate,
    db: Session = Depends(get_db),
    _admin: str = Depends(require_admin)
):
    new_lesson = Lesson(
        title=lesson.title,
        description=lesson.description,
        content=lesson.content,
        xp_reward=lesson.xp_reward
    )
    db.add(new_lesson)
    commit_lesson(db)
    db.refresh(new_lesson)
    return new_lesson


@app.patch("/lessons/{lesson_id}", status_code=200, response_model=LessonResponse)
def update_lesson(
    lesson_id: int,
    lesson_update: LessonUpdate,
    db: Session = Depends(get_db),
    _admin: str = Depends(require_admin)
):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    for field, value in lesson_update.model_dump(exclude_unset=True).items():
        setattr(lesson, field, value)

    commit_lesson(db)
    db.refresh(lesson)
    return lesson

@app.delete("/lessons/{lesson_id}", status_code=204)
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    _admin: str = Depends(require_admin)
):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Progress rows reference the lesson, so remove them first.
    db.execute(
        delete(UserLessonProgress)
        .where(UserLessonProgress.lesson_id == lesson_id)
    )
    db.delete(lesson)
    db.commit()

@app.post(
    "/lessons/{lesson_id}/complete",
    response_model=LessonCompletionResponse
)
def complete_lesson(
    lesson_id: int,
    clerk_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Verify the lesson exists
    lesson = db.get(Lesson, lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    # 2. Retrieve the internal PostgreSQL user
    user = get_or_create_user(db, clerk_id)

    # 3. Check whether the lesson is already completed
    progress = db.get(
        UserLessonProgress,
        (user.id, lesson_id)
    )

    if progress is not None:
        return {
            "lesson_id": lesson_id,
            "completed": True,
            "xp_reward": lesson.xp_reward,
            "already_completed": True
        }

    # 4. Create the completion record
    new_progress = UserLessonProgress(
        user_id=user.id,
        lesson_id=lesson_id
    )

    db.add(new_progress)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        # Check whether a concurrent request created the completion
        existing_progress = db.get(
            UserLessonProgress,
            (user.id, lesson_id)
        )

        if existing_progress is None:
            # Unexpected integrity error — don't hide it
            raise

        return {
            "lesson_id": lesson_id,
            "completed": True,
            "xp_reward": lesson.xp_reward,
            "already_completed": True
        }

    # 5. New completion was saved successfully
    return {
        "lesson_id": lesson_id,
        "completed": True,
        "xp_reward": lesson.xp_reward,
        "already_completed": False
    }




@app.get(
    "/me/progress",
    response_model=UserProgressResponse
)
def get_my_progress(
    clerk_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = get_or_create_user(db, clerk_id)

    completed_lessons = db.execute(
        select(Lesson.id, Lesson.xp_reward)
        .join(
            UserLessonProgress,
            UserLessonProgress.lesson_id == Lesson.id
        )
        .where(UserLessonProgress.user_id == user.id)
    ).all()

    completed_lesson_ids = [lesson.id for lesson in completed_lessons]
    total_xp = sum(lesson.xp_reward for lesson in completed_lessons)

    return {
        "completed_lessons": completed_lesson_ids,
        "total_completed": len(completed_lesson_ids),
        "total_xp": total_xp
    }
