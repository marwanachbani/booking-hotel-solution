from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.config.security import get_password_hash, verify_password, create_access_token
from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, email: str, password: str, full_name: str, role: str = "user") -> User:
        hashed_password = get_password_hash(password)
        user = User(
            user_id=uuid4(),
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
            created_at=datetime.utcnow()
        )
        self.repository.create_user(user)
        return user

    def authenticate_user(self, email: str, password: str) -> Optional[str]:
        user = self.repository.get_user_by_email(email)
        if user and verify_password(password, user.hashed_password):
            access_token = create_access_token({"sub": user.email, "role": user.role})
            return access_token
        return None

    def get_user(self, user_id: UUID) -> Optional[User]:
        return self.repository.get_user_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.repository.get_user_by_email(email)
