from urllib import response

from app.models import Lesson
from sqlalchemy import select, func
from app.models import User, UserLessonProgress


def create_test_lesson(db_session) -> int:
    lesson = Lesson(
        title="Test Soccer Lesson",
        description="A lesson used for automated testing",
        content="Soccer fundamentals",
        xp_reward=20,
    )
    db_session.add(lesson)
    db_session.commit()
    db_session.refresh(lesson)
    return lesson.id


def test_complete_lesson_first_and_second_time(client, db_session):
    lesson_id = create_test_lesson(db_session)

    
    response = client.post(f"/lessons/{lesson_id}/complete")
    assert response.status_code == 200

    data = response.json()
    assert data["completed"] is True
    assert data["already_completed"] is False
    assert data["lesson_id"] == lesson_id
    assert data["xp_reward"] == 20

    
    response = client.post(f"/lessons/{lesson_id}/complete")
    assert response.status_code == 200

    data = response.json()
    assert data["completed"] is True
    assert data["already_completed"] is True

    user = db_session.scalar(
        select(User).where(User.clerk_id == "test_clerk_user_123")
    )

    completion_count = db_session.scalar(
        select(func.count())
        .select_from(UserLessonProgress)
        .where(
            UserLessonProgress.user_id == user.id,
            UserLessonProgress.lesson_id == lesson_id,
        )
    )
    assert completion_count == 1

    response = client.get("/me/progress")

    assert response.json()["total_xp"] == 20
    assert response.json()["total_completed"] == 1
