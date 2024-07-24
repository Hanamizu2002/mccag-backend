from fastapi import APIRouter

from . import littleskin, official

router = APIRouter(prefix="/loader")

# Define routers

router.include_router(official.router)
router.include_router(littleskin.router)
