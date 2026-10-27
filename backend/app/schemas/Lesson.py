from pydantic import BaseModel, Field, ConfigDict

class LessonCreate(BaseModel): 
    title: str = Field(..., description="The title of the lesson")
    description: str | None = Field(None, description="The description of the lesson")
    content: str = Field(..., description="The content of the lesson")
    xp_reward: int = Field(..., description="The XP reward for completing the lesson")

class LessonUpdate(BaseModel):
    title: str | None = Field(None, description="The title of the lesson")
    description: str | None = Field(None, description="The description of the lesson")
    content: str | None = Field(None, description="The content of the lesson")
    xp_reward: int | None = Field(None, description="The XP reward for completing the lesson") 

class LessonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None 
    content: str
    xp_reward: int



