from typing import Annotated, Optional

from fastapi import APIRouter, Path, Query, Response
from fastapi.responses import FileResponse
from mccag.common import COMMON_404_RESPONSE, PNG_200_RESPONSE, generate_response_by_fetch_profile
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
    player: Annotated[str, Path(description="Minecraft player name")],
    avatar_type: Annotated[Optional[str], Query(description="Type of avatar to generate: 'full' or 'head'", regex="^(full|head)$")] = 'full',
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
    uuid: Annotated[str, Path(description="Minecraft player UUID")],
    avatar_type: Annotated[Optional[str], Query(description="Type of avatar to generate: 'full' or 'head'", regex="^(full|head)$")] = 'full',
) -> Response:
    profile = await YggdrasilMC().by_uuid_async(uuid)
    return await generate_response_by_fetch_profile(profile, avatar_type)