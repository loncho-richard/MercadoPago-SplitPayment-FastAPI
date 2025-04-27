# user_repository.py (mejorado)
from sqlmodel import select, Session
from app.models.user import User
from app.schemas.user import UserCreate, UserTokens
from app.core.hashing import get_password_hash

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_create: UserCreate) -> User:
        hashed_password = get_password_hash(user_create.password)
        db_user = User(**user_create.model_dump(exclude={"password"}), hashed_password=hashed_password)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str) -> User | None:
        return self.session.exec(select(User).where(User.email == email)).first()

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.session.exec(select(User).where(User.id == user_id)).first()

    def update_tokens(self, user: User, tokens: dict):
        user.mercadopago_access_token = tokens["access_token"]
        user.mercadopago_refresh_token = tokens.get("refresh_token")
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user