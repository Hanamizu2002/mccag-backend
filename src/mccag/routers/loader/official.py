from typing import Annotated

from fastapi import APIRouter, Path, Response
from fastapi.responses import FileResponse
from mccag.common import COMMON_404_RESPONSE, PNG_200_RESPONSE, generate_response_by_fetch_profile
from mccag.core import AvatarTypes
from yggdrasil_mc.client import YggdrasilMC

router = APIRouter(prefix="/minecraft.net")


@router.get(
    "/player/{player}",
    summary="Get texture from Minecraft.net",
    responses={**PNG_200_RESPONSE, **COMMON_404_RESPONSE},
    response_class=FileResponse,
    tags=["Minecraft.net"],
)
async def get_from_official(
    player: Annotated[str, Path(description="Minecraft player name", example="w84")],
    avatar_type: AvatarTypes = "full",
):
    profile = await YggdrasilMC().by_name_async(player)
    return await generate_response_by_fetch_profile(profile, avatar_type)


@router.get(
    "/uuid/{uuid}",
    summary="Get texture from Minecraft.net by UUID",
    responses={**PNG_200_RESPONSE, **COMMON_404_RESPONSE},
    response_class=FileResponse,
    tags=["Minecraft.net"],
)
async def get_from_official_uuid(
    uuid: Annotated[str, Path(description="Minecraft player UUID", example="ca244462f8e5494791ec98f0ccf505ac")],
    avatar_type: AvatarTypes = "full",
) -> Response:
    profile = await YggdrasilMC().by_uuid_async(uuid)
    return await generate_response_by_fetch_profile(profile, avatar_type)
