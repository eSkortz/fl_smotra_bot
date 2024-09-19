import aiohttp
from config import DISCORD_CAPTION


async def post_with_images(
    authorization: str, text: str, images: list, channel_id: str
) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"authorization": authorization}

        images = [[f"file{index}.jpg", images[index]] for index in range(len(images))]
        form_data = aiohttp.FormData()
        for file_name, file_content in images:
            form_data.add_field(
                "files",
                file_content,
                filename=file_name,
                content_type="application/octet-stream",
            )
        form_data.add_field("content", f"{text}\n\n{DISCORD_CAPTION}")

        async with session.post(
            url=f"https://discord.com/api/v9/channels/{channel_id}/messages",
            headers=headers,
            data=images,
        ) as response:
            return await response.json()


async def post_without_images(authorization: str, text: str, channel_id: str) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"authorization": authorization}
        body = {"content": f"{text}\n\n{DISCORD_CAPTION}"}
        async with session.post(
            url=f"https://discord.com/api/v9/channels/{channel_id}/messages",
            headers=headers,
            json=body,
        ) as response:
            return await response.json()


async def delete_message(authorization: str, channel_id: str, message_id: str) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": authorization}
        async with session.delete(
            url=f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}",
            headers=headers,
        ) as response:
            return await response.json()


async def get_messages(authorization: str, channel_id: str, before: str = None) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": authorization}
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=100"
        if before:
            url = url + f"&before={before}"
        async with session.get(url=url, headers=headers) as response:
            return await response.json()


async def put_reaction(
    authorization: str, reaction: str, channel_id: str, message_id: str
) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": authorization}
        async with session.put(
            url=f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{reaction}",
            headers=headers,
        ) as response:
            return response.status
