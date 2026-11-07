from pydantic import BaseModel


class UserProgressResponse(BaseModel):
    completed_lessons: list[int]
    total_xp: int
    total_completed: int
