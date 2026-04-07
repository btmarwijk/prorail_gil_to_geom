from datetime import datetime
from typing import Optional

from models import User  # Adjust import based on your file structure
from sqlalchemy import select
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user from the database by their email.
        """
        query = select(User).where(User.email == email)
        return self.db.execute(query).scalar_one_or_none()

    def user_exists(self, email: str) -> bool:
        """
        Returns True if a user with the given email already exists.
        """
        user = self.get_user_by_email(email)
        return user is not None

    def create_user(
        self,
        email: str,
        validation_code: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> User:
        """
        Creates a new user record if they don't already exist.
        """
        if self.user_exists(email):
            raise ValueError(f"User with email {email} already exists.")

        new_user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            validation_code=validation_code,
            created_at=datetime.utcnow(),
        )

        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_or_create_user(self, email: str, **kwargs) -> User:
        """
        Logic to either find an existing user or create them.
        """
        user = self.get_user_by_email(email)
        if user:
            return user

        return self.create_user(email=email, **kwargs)
