from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    clerk_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    username: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


class UserLessonProgress(Base):
    __tablename__ = "user_lesson_progress"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True
    )

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lessons.id"),
        primary_key=True
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )