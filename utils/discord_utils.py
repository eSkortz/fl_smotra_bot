import aiohttp
from config import DISCORD_CAPTION


async def post_with_images(
    authorization: str, text: str, images: list, channel_id: str
) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"authorization": authorization}
        async with session.post(
            url=f"https://discord.com/api/v9/channels/{channel_id}/messages",
            headers=headers,
            files=images,
        ) as response:
            response = await response.json()
            message_id = response["id"]
        body = {
            "content": f"{text}\n\n{DISCORD_CAPTION}"
        }
        async with session.patch(
            url=f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}",
            headers=headers,
            json=body,
        ) as response:
            response = await response.json()
            return response


async def post_without_images(authorization: str, text: str, channel_id: str) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"authorization": authorization}
        body = {
            "content": f"{text}\n\n{DISCORD_CAPTION}"
        }
        async with session.post(
            url=f"https://discord.com/api/v9/channels/{channel_id}/messages",
            headers=headers,
            json=body,
        ) as response:
            response = await response.json()
            return response


async def delete_message(authorization: str, channel_id: str, message_id: str) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": authorization}
        async with session.delete(
            url=f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}",
            headers=headers,
        ) as response:
            response = await response.json()
            return response
