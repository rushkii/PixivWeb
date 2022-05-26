from PixivWeb import Client
import asyncio

pixiv = Client()

async def main():
    art = await pixiv.get_artworks(98541854)
    print(art)

asyncio.get_event_loop().run_until_complete(main())