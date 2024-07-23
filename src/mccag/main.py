from importlib.metadata import metadata
from typing import Annotated

from fastapi import FastAPI, Path
from fastapi.responses import FileResponse, Response
from yggdrasil_mc.client import PlayerProfile, YggdrasilMC

from mccag.core import AvatarRenderer
from mccag.utils import fetch_skin

app_metadata = metadata("mccag")

app = FastAPI(
    title="MCCAG API",
    summary=app_metadata.get("Summary", ""),
    version=app_metadata.get("Version", ""),
    license_info={"name": app_metadata.get("License", "")},
)


LITTLESKIN_API = "https://littleskin.cn/api/yggdrasil"
PNG_RESPONSE = {
    200: {
        "content": {"image/png": {}},
        "description": "The rendered image",
    }
}


async def generate_response(profile: PlayerProfile) -> Response:
    skin_texture = await fetch_skin(str(profile.skin.url))
    image = AvatarRenderer(skin_texture).render()
    return Response(
        content=image.getvalue(), headers={"X-Minecraft-Texture-Hash": profile.skin.hash}, media_type="image/png"
    )


@app.get(
    "/minecraft.net/player/{player}",
    summary="Get texture from Minecraft.net",
    responses={**PNG_RESPONSE},
    response_class=FileResponse,
    tags=["Minecraft.net"],
)
async def get_from_official(
    player: Annotated[str, Path(description="Minecraft player name")],
):
    profile = await YggdrasilMC().by_name_async(player)
    return await generate_response(profile)


@app.get(
    "/minecraft.net/uuid/{uuid}",
    summary="Get texture from Minecraft.net by UUID",
    responses={**PNG_RESPONSE},
    response_class=FileResponse,
    tags=["Minecraft.net"],
)
async def get_from_official_uuid(
    uuid: Annotated[str, Path(description="Minecraft player UUID")],
) -> Response:
    profile = await YggdrasilMC().by_uuid_async(uuid)
    return await generate_response(profile)


@app.get(
    "/littleskin.cn/player/{player}",
    summary="Get texture from LittleSkin.cn",
    responses={**PNG_RESPONSE},
    response_class=FileResponse,
    tags=["LittleSkin.cn"],
)
async def get_from_littleskin(
    player: Annotated[str, Path(description="LittleSkin player name")],
):
    profile = await YggdrasilMC(LITTLESKIN_API).by_name_async(player)
    return await generate_response(profile)


@app.get(
    "/littleskin.cn/uuid/{uuid}",
    summary="Get texture from LittleSkin.cn by UUID",
    responses={**PNG_RESPONSE},
    response_class=FileResponse,
    tags=["LittleSkin.cn"],
)
async def get_from_littleskin_uuid(
    uuid: Annotated[str, Path(description="LittleSkin player UUID")],
) -> Response:
    profile = await YggdrasilMC(LITTLESKIN_API).by_uuid_async(uuid)
    return await generate_response(profile)
