from wav2mp3.database.core import Base
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


class UserCreate(BaseModel):
    name: str


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
