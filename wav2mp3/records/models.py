from typing import Annotated

from fastapi import File, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from ..database.core import Base


class RecordCreate(BaseModel):
    wav_file: Annotated[UploadFile, File(description="A file read as UploadFile")] = (
        File(...)
    )


class Record(Base):
    __tablename__ = "records"

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column()
    path_to_mp3: Mapped[str] = mapped_column()
