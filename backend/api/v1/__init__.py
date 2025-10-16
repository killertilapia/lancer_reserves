from fastapi import APIRouter
from backend.api.v1 import reserves

api_router = APIRouter()
api_router.include_router(reserves.router, prefix="/reserves", tags=["reserves"])

__all__ = ["api_router"]


