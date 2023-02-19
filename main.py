import asyncio
import json

import aiohttp
import aioredis
from datetime import datetime
from prisma import Prisma
from dotenv import load_dotenv
from os import getenv

load_dotenv()

api_client = None
redis_client = None
db = None


async def get_manga(new_manga):
    print('Manga', new_manga)
    async with api_client.get('/api/manga/' + new_manga['slug']) as manga_response:
        new_manga_data = await manga_response.json()
        print(new_manga_data)


async def main():
    global api_client, redis_client, db
    async with aiohttp.ClientSession('https://earlym.org') as session:
        api_client = session
        redis_client = await aioredis.from_url('redis://localhost:6379')
        db = Prisma()
        await db.connect()

        async with api_client.get('/api/home') as response:
            data = await response.json()
            latest_updates = data['latestUpdates']

            for new_manga in latest_updates:
                print('Manga', new_manga)
                await get_manga(new_manga)
                await db.newmanga.create(
                    data={'slug': new_manga['slug']}
                )

        await redis_client.close()
        await session.close()
        await db.disconnect()


asyncio.run(main())
