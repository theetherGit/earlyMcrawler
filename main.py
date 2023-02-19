import asyncio
import aiohttp
import aioredis
from datetime import datetime
from prisma import Client
from dotenv import load_dotenv
from os import getenv

load_dotenv()

api_client = None


async def get_manga(new_manga):
    print('Manga', new_manga)
    async with api_client.get('/api/manga/'+new_manga['slug']) as manga_response:
        new_manga_data = await manga_response.json()
        print(new_manga_data)


async def main():
    global api_client
    async with aiohttp.ClientSession('https://earlym.org') as session:
        api_client = session
        redis = await aioredis.from_url('redis://localhost:6379')
        # prisma = Client()

        async with api_client.get('/api/home') as response:
            data = await response.json()
            latest_updates = data['latestUpdates']

            for new_manga in latest_updates:
                print('Manga', new_manga)
                await get_manga(new_manga)

        await redis.close()
        await session.close()
        # await prisma.disconnect()


asyncio.run(main())
