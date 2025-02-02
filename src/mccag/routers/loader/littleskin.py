from typing import Annotated, Optional

from fastapi import APIRouter, Path, Query, Response
from fastapi.responses import FileResponse
from mccag.common import COMMON_404_RESPONSE, PNG_200_RESPONSE, generate_response_by_fetch_profile
from mccag.core import AvatarTypes
from yggdrasil_mc.client import YggdrasilMC

LITTLESKIN_API = "https://littleskin.cn/api/yggdrasil"

router = APIRouter(prefix="/littleskin.cn")


@router.get(
    "/player/{player}",
    summary="Get texture from LittleSkin.cn",
    responses={**PNG_200_RESPONSE, **COMMON_404_RESPONSE},
    response_class=FileResponse,
    tags=["LittleSkin.cn"],
)
async def get_from_littleskin(
    player: Annotated[str, Path(description="LittleSkin player name", example="SerinaNya")],
    avatar_type: AvatarTypes = "full",
):
    profile = await YggdrasilMC(LITTLESKIN_API).by_name_async(player)
    return await generate_response_by_fetch_profile(profile, avatar_type)


@router.get(
    "/uuid/{uuid}",
    summary="Get texture from LittleSkin.cn by UUID",
    responses={**PNG_200_RESPONSE, **COMMON_404_RESPONSE},
    response_class=FileResponse,
    tags=["LittleSkin.cn"],
)
async def get_from_littleskin_uuid(
    uuid: Annotated[str, Path(description="LittleSkin player UUID", example="a6abd9a95e4b4fe18f60777d1ab94ebb")],
    avatar_type: AvatarTypes = "full",
) -> Response:
    profile = await YggdrasilMC(LITTLESKIN_API).by_uuid_async(uuid)
    return await generate_response_by_fetch_profile(profile, avatar_type)
