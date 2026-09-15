"""User repository – pure data-access layer."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.db.scalars(stmt).first()

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def update_password(self, user: User, hashed: str) -> User:
        user.password = hashed
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user