from app.models import Lesson


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

    # First completion
    response = client.post(f"/lessons/{lesson_id}/complete")
    assert response.status_code == 200

    data = response.json()
    assert data["completed"] is True
    assert data["already_completed"] is False
    assert data["lesson_id"] == lesson_id
    assert data["xp_reward"] == 20

    # Completing the same lesson again is idempotent
    response = client.post(f"/lessons/{lesson_id}/complete")
    assert response.status_code == 200

    data = response.json()
    assert data["completed"] is True
    assert data["already_completed"] is True
