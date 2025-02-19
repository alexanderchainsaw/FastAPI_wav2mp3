import os

from fastapi.exceptions import HTTPException
from pydub import AudioSegment

from .. import config
from .models import RecordCreate


def construct_download_link(record_id: str, user_id: str) -> str:
    return f"http://{config.APP_HOST}:{config.APP_PORT}/record?record_id={record_id}&user_id={user_id}"


def _wav_to_mp3(record_create: RecordCreate, path_to_file: str):
    # Создаём папку для пользователя если её нет
    if not os.path.exists(f"media/{record_create.user_id}"):
        os.makedirs(f"media/{record_create.user_id}")

    with open(f"{path_to_file}.wav", "wb") as file:
        file.write(record_create.wav_file.file.read())
    mp3_file = AudioSegment.from_wav(f"{path_to_file}.wav")
    mp3_file.export(f"{path_to_file}.mp3", format="mp3")
    os.remove(f"{path_to_file}.wav")


def _validate_wav(filename: str) -> bool:
    if not filename.endswith(".wav"):
        return False
    return True


def process_audio(record_create: RecordCreate, path_to_file: str) -> None:
    """Save WAV file, convert it to MP3, then return a link to download it"""
    if not _validate_wav(record_create.wav_file.filename):
        raise HTTPException(status_code=415, detail="Wrong file format")
    _wav_to_mp3(record_create, path_to_file)
