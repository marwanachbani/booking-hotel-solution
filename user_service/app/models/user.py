from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class User(BaseModel):
    user_id: UUID
    email: EmailStr
    hashed_password: str
    full_name: str
    role: str  # Add this field (e.g., "user", "admin")
    created_at: datetime
