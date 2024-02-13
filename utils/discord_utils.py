import aiohttp


async def post_with_images(
    authorizartion: str, text: str, images: list, channel_id: str
) -> None:
    async with aiohttp.ClientSession() as session:
        headers = {"authorizartion": authorizartion}
        async with session.post(url=f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, files=images) as response:
            response = await response.json()
            message_id = response['id']
        body = {'content': f'{text}\n\n*Sent by Smotra Assistant* <:pUwu:760501989532237844>'}
        async with session.patch(url=f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}', headers=headers, json=body) as response:
            response = await response.json()


async def post_without_images(authorizartion: str, text: str, channel_id: str) -> None:
    async with aiohttp.ClientSession() as session:
        headers = {"authorizartion": authorizartion}
        body = {'content': f'{text}\n\n*Sent by Smotra Assistant* <:pUwu:760501989532237844>'}
        async with session.post(url=f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=body) as response:
            response = await response.json()