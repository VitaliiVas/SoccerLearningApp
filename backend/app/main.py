from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from .auth import get_current_user
from .database import get_db
from .models import Lesson

from .schemas.Lesson import LessonCreate, LessonResponse, LessonUpdate

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/me")
def get_me(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/lessons")
def get_lessons(db: Session = Depends(get_db)):
    return db.execute(select(Lesson)).scalars().all()

@app.get("/lessons/{lesson_id}", status_code=200, response_model=LessonResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson



@app.post("/lessons", status_code=201)
def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db)):
    new_lesson = Lesson(
        title=lesson.title,
        description=lesson.description,
        content=lesson.content,
        xp_reward=lesson.xp_reward
    )
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson


@app.patch("/lessons/{lesson_id}", status_code=200, response_model=LessonResponse)
def update_lesson(lesson_id: int, lesson_update: LessonUpdate, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    for field, value in lesson_update.dict(exclude_unset=True).items():
        setattr(lesson, field, value)
    
    db.commit()
    db.refresh(lesson)
    return lesson

@app.delete("/lessons/{lesson_id}", status_code=204)
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    db.delete(lesson)
    db.commit()

