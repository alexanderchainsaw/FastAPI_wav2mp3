import os
import shutil
from tempfile import NamedTemporaryFile
from typing import IO

from fastapi import UploadFile
from fastapi.exceptions import HTTPException
from pydub import AudioSegment

from .. import config
from ..users.models import User
from .models import MAX_WAV_SIZE, MAX_WAV_SIZE_MB


def construct_download_link(record_id: str, user_id: str) -> str:
    return f"http://{config.APP_HOST}:{config.APP_PORT}/record?id={record_id}&user_id={user_id}"


def _wav_to_mp3(wav_file, user, path_to_file: str):
    # Создаём папку для пользователя если её нет
    if not os.path.exists(f"media/{user.id}"):
        os.makedirs(f"media/{user.id}")

    # Читаем файл кусками, если превышает лимит то выбрасываем 413, если ок - сохраняем
    current_file_size = 0
    temp: IO = NamedTemporaryFile(delete=False)
    for chunk in wav_file.file:
        current_file_size += len(chunk)
        if current_file_size > MAX_WAV_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large, must be below {MAX_WAV_SIZE_MB} MB",
            )
        temp.write(chunk)
    temp.close()
    shutil.move(temp.name, f"{path_to_file}.wav")

    mp3_file = AudioSegment.from_wav(f"{path_to_file}.wav")
    mp3_file.export(f"{path_to_file}.mp3", format="mp3")
    os.remove(f"{path_to_file}.wav")


def _validate_wav(filename: str) -> bool:
    if not filename.endswith(".wav"):
        return False
    return True


def process_audio(wav_file: UploadFile, user: User, path_to_file: str) -> None:
    """Save WAV file, convert it to MP3, then return a link to download it"""
    if not _validate_wav(wav_file.filename):
        raise HTTPException(status_code=415, detail="Wrong file format")
    _wav_to_mp3(wav_file, user, path_to_file)
