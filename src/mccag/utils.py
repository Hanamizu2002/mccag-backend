from io import BytesIO
import httpx


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
