from io import BytesIO

import httpx
from fastapi import HTTPException, Response
from yggdrasil_mc.client import PlayerProfile

from mccag.core import AvatarRenderer

PNG_200_RESPONSE = {
    200: {
        "content": {"image/png": {}},
        "description": "The rendered image",
    },
}

COMMON_404_RESPONSE = {
    404: {"description": "Texture not found"},
}

COMMON_417_RESPONSE = {
    417: {"description": "File too large"},
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


async def generate_response_by_fetch_profile(profile: PlayerProfile) -> Response:
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
