from pydantic import BaseModel



class LessonCompletionResponse(BaseModel):
    lesson_id: int
    completed: bool
    xp_reward: int
    already_completed: bool


