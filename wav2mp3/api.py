from fastapi import APIRouter
from wav2mp3.users.views import users_router
from wav2mp3.records.views import records_router

api_router = APIRouter()

api_router.include_router(
    users_router, prefix="/users", tags=["users"]
)

api_router.include_router(
    records_router, prefix="/record", tags=["records"]
)
