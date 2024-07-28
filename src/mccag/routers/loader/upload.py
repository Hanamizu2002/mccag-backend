from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse
from loguru import logger
from mccag.common import COMMON_417_RESPONSE, PNG_200_RESPONSE
from mccag.core import AvatarRenderer, AvatarTypes

router = APIRouter(prefix="/custom")


@router.post(
    "/upload",
    summary="Get the texture from user upload",
    responses={**PNG_200_RESPONSE, **COMMON_417_RESPONSE},
    response_class=FileResponse,
    tags=["Custom"],
)
async def from_upload(
    file: Annotated[UploadFile, File(description="PNG file, <= 64KB", media_type="image/png")],
    avatar_type: AvatarTypes = "full",
) -> Response:
    logger.info(f"Receive file: {file.content_type=}, {file.size=}")

    if file.size and file.size > 65536:  # 64KB
        raise HTTPException(status_code=413, detail="File too large, should be <= 64KB")

    image = AvatarRenderer(BytesIO(await file.read())).render(avatar_type=avatar_type)

    return Response(
        content=image.getvalue(),
        media_type="image/png",
    )
