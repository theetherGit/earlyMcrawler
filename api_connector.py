class EarlyMApiClient:
    def __init__(self, session):
        self.session = session

    async def get(self, path):
        async with self.session.get('https://earlym.org/api/' + path) as response:
            self.session.close()
            return await response.json()
