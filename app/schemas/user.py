from pydantic import BaseModel, EmailStr
from app.models.role import Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role


class UserOut(BaseModel):
    id: int
    email: str
    role: Role


class UserTokens(BaseModel):
    access_token: str
    refresh_token: str
