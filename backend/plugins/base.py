class BasePlugin:

    name = "BasePlugin"

    # ⭐ New Category Field
    category = "movies"

    async def search(self, query):
        return []

    async def get_movie(self, url):
        return {}

    async def get_stream(self, url):
        return []