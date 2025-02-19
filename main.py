import os
from fastapi import FastAPI
from wav2mp3.api import api_router
from wav2mp3.database.core import engine, Base
import uvicorn

# Папка для mp3
if not os.path.exists('media'):
    os.makedirs('media')

app = FastAPI(title='WAV2MP3')


@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router)

