from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserOut
from fastapi import HTTPException, status


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user (self, user_create: UserCreate) -> UserOut:
        existing_user = self.user_repository.get_user_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        return self.user_repository.create_user(user_create)