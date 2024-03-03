from utils.discord_utils import post_without_images
import asyncio


async def main() -> None:
    response = await post_without_images(
        authorizartion="NDE0MDM1OTUyODIzMTczMTIw.GC4BJ_.S5s0pdpz4w15IlWIvIiNExEYxfnUT8VkiVc1kI",
        text="test assistant",
        channel_id="1065420115484614656",
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
