from PixivWeb import Client
import asyncio, time

pixiv = Client()

async def main():
    art = await pixiv.get_artworks(94267660)
    print(await art.download())

asyncio.get_event_loop().run_until_complete(main())