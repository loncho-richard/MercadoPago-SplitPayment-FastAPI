from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from fastapi import Depends


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
    )


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))