from wav2mp3.database.core import Base
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel
from uuid import UUID
from fastapi import UploadFile, File
from typing import Annotated


class RecordCreate(BaseModel):
    user_id: UUID
    token: UUID
    wav_file: Annotated[UploadFile, File(description="A file read as UploadFile")] = File(...)


class RecordGet(BaseModel):
    record_id: UUID
    user_id: UUID


class Record(Base):
    __tablename__ = "records"

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column()
    path_to_mp3: Mapped[str] = mapped_column()
