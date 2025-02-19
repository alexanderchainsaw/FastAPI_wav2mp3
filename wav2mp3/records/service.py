from uuid import uuid4

from fastapi.concurrency import run_in_threadpool
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Record, RecordCreate
from .utils import process_audio


async def create_record(session: AsyncSession, record_create: RecordCreate):
    filename_without_ext = "".join(record_create.wav_file.filename.rsplit(".", 1)[:-1])
    path_to_file = f"media/{record_create.user_id}/{filename_without_ext}"
    await run_in_threadpool(  # внутри блокирующий I/O, поэтому в тредпуле
        process_audio, record_create, path_to_file
    )
    record = Record(
        id=str(uuid4()),
        user_id=str(record_create.user_id),
        path_to_mp3=f"{path_to_file}.mp3",
    )

    if await session.scalar(
        select(Record).where(Record.path_to_mp3 == record.path_to_mp3)
    ):
        raise HTTPException(
            status_code=409, detail="Record with the same name already exists"
        )

    session.add(record)

    return record


async def get_record(session: AsyncSession, record_id: str, user_id: str):
    record = await session.get(Record, record_id)
    if not record or user_id != record.user_id:
        raise HTTPException(status_code=404, detail="Record not found")
    return record
