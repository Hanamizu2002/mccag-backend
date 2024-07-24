from fastapi import APIRouter

from . import littleskin, official, upload

router = APIRouter(prefix="/loader")

# Define routers

# from Minecraft.net
router.include_router(official.router)

# from LittleSkin.cn
router.include_router(littleskin.router)

# from user upload
router.include_router(upload.router)
