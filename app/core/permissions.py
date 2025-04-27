from fastapi import HTTPException, status, Depends
from app.models.user import User, Role
from app.core.security import get_current_active_user


class PermissionChecker:
    def __init__(self, allowed_roles: tuple[Role]):
        self.allowed_roles = allowed_roles

    
    def __call__(self, user: User = Depends(get_current_active_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You needs permisions for this route"
            )
        return user