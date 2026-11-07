from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..models import User


def get_or_create_user(
    db: Session,
    clerk_id: str
) -> User:

    user = db.scalar(
        select(User).where(User.clerk_id == clerk_id)
    )

    if user is not None:
        return user

    user = User(clerk_id=clerk_id)

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
        return user

    except IntegrityError:
        db.rollback()

        existing_user = db.scalar(
            select(User).where(User.clerk_id == clerk_id)
        )

        if existing_user is not None:
            return existing_user

        raise