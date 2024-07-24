from io import BytesIO

import httpx
from fastapi import HTTPException, Response
from yggdrasil_mc.client import PlayerProfile

from mccag.core import AvatarRenderer

COMMON_RESPONSE = {
    200: {
        "content": {"image/png": {}},
        "description": "The rendered image",
    },
    400: {"description": "Texture not found"},
}


async def fetch_skin(url: str) -> BytesIO:
    """
    通过 URL 获取皮肤材质，并返回 `BytesIO` 对象

    ---

    Args:
        url (str): 皮肤材质的 URL

    Returns:
        BytesIO: 皮肤材质的 `BytesIO` 对象
    """
    async with httpx.AsyncClient(http2=True, follow_redirects=True) as client:
        resp = await client.get(url)

    resp.raise_for_status()
    print(len(resp.content))
    return BytesIO(resp.content)


async def generate_response(profile: PlayerProfile) -> Response:
    if profile.skin:
        skin_texture = await fetch_skin(str(profile.skin.url))
        image = AvatarRenderer(skin_texture).render()

        return Response(
            content=image.getvalue(),
            headers={"X-Minecraft-Texture-Hash": str(profile.skin.hash)},
            media_type="image/png",
        )

    else:
        raise HTTPException(status_code=404, detail="Skin not found")
