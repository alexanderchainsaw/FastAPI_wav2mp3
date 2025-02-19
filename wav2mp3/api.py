from fastapi import APIRouter

from .records.views import records_router
from .users.views import users_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["users"])

api_router.include_router(records_router, prefix="/record", tags=["records"])
