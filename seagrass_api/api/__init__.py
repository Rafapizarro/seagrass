from fastapi import APIRouter
from .fast import router as fast_router

api_router = APIRouter()

api_router.include_router(fast_router)
# api_router.include_router(fast_router, prefix="/users", tags=["Users"])
