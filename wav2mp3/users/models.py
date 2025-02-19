from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from ..database.core import Base


class UserCreate(BaseModel):
    name: str


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
