from fastapi import APIRouter, Depends, status

from app.api.deps import (
    get_user_service,
)
from app.core.security import get_current_active_user
from app.schemas.user import (
    UserCreate,
    UserOut
)
from app.models.user import User
from app.services.user_service import UserService


router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> UserOut:
    return user_service.create_user(user_create)


@router.get("/me")
async def read_user_me(
    current_user: User = Depends(get_current_active_user)
) -> UserOut:
    return current_user