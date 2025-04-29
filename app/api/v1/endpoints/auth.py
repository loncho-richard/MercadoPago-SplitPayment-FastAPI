from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
import jwt
from jwt.exceptions import PyJWTError

from app.core.security import (
    create_access_token,
    create_refresh_token,
    Token
)
from app.core.hashing import verify_password
from app.core.config import settings
from app.api.deps import get_db
from app.repositories.user_repository import UserRepository


router = APIRouter()

@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: Session = Depends(get_db)
) -> Token:
    user = UserRepository(db).get_user_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )

    refresh_token = create_refresh_token(
        data={"sub": user.email},
        expires_delta=refresh_token_expires
    )
    return Token(
        access_token=access_token, 
        refresh_token=refresh_token,
        token_type="bearer")


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db)
) -> Token:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Verificar tipo de token
        if payload.get("type") != "refresh":
            raise credentials_exception
            
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except PyJWTError:
        raise credentials_exception
    
    user = UserRepository(db).get_user_by_email(email)
    if user is None:
        raise credentials_exception
    
    # Generar nuevo access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=new_access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )