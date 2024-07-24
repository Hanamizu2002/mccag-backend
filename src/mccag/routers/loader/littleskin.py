from typing import Annotated

from fastapi import APIRouter, Path, Response
from fastapi.responses import FileResponse
from mccag.common import COMMON_RESPONSE, generate_response
from yggdrasil_mc.client import YggdrasilMC

LITTLESKIN_API = "https://littleskin.cn/api/yggdrasil"


router = APIRouter(prefix="/littleskin.cn")


@router.get(
    "/player/{player}",
    summary="Get texture from LittleSkin.cn",
    responses={**COMMON_RESPONSE},
    response_class=FileResponse,
    tags=["LittleSkin.cn"],
)
async def get_from_littleskin(
    player: Annotated[str, Path(description="LittleSkin player name")],
):
    profile = await YggdrasilMC(LITTLESKIN_API).by_name_async(player)
    return await generate_response(profile)


@router.get(
    "/uuid/{uuid}",
    summary="Get texture from LittleSkin.cn by UUID",
    responses={**COMMON_RESPONSE},
    response_class=FileResponse,
    tags=["LittleSkin.cn"],
)
async def get_from_littleskin_uuid(
    uuid: Annotated[str, Path(description="LittleSkin player UUID")],
) -> Response:
    profile = await YggdrasilMC(LITTLESKIN_API).by_uuid_async(uuid)
    return await generate_response(profile)
