from sqlmodel import Field, SQLModel
from .role import Role


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    role: Role = Field(default=Role.BUYER)
    mercadopago_access_token: str | None = Field(default=None)
    mercadopago_refresh_token: str | None = Field(default=None)