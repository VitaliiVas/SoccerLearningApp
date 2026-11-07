from pydantic import BaseModel, Field, ConfigDict, field_validator

# Limits mirror the column sizes in models.Lesson so bad input is a 422, not a DB error.
TITLE_MAX = 255
DESCRIPTION_MAX = 1024
CONTENT_MAX = 4096


class LessonCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=TITLE_MAX, description="The title of the lesson")
    description: str = Field(..., max_length=DESCRIPTION_MAX, description="The description of the lesson")
    content: str = Field(..., min_length=1, max_length=CONTENT_MAX, description="The content of the lesson")
    xp_reward: int = Field(..., ge=0, description="The XP reward for completing the lesson")

class LessonUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=TITLE_MAX, description="The title of the lesson")
    description: str | None = Field(None, max_length=DESCRIPTION_MAX, description="The description of the lesson")
    content: str | None = Field(None, min_length=1, max_length=CONTENT_MAX, description="The content of the lesson")
    xp_reward: int | None = Field(None, ge=0, description="The XP reward for completing the lesson")

    # Fields are optional (omit to leave unchanged), but every column is NOT NULL.
    @field_validator("title", "description", "content", "xp_reward")
    @classmethod
    def not_null(cls, value):
        if value is None:
            raise ValueError("may be omitted but cannot be null")
        return value

class LessonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    content: str
    xp_reward: int
