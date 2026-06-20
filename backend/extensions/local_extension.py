from plugins.base import BasePlugin


class Plugin(BasePlugin):

    name = "LocalRepoExtension"

    async def search(self, query):

        return [
            {
                "title": f"Repo Movie for {query}",
                "url": "https://example.com/movie"
            }
        ]

    async def get_movie(self, url):

        return {
            "title": "Repo Movie",
            "description": "Loaded from repository."
        }

    async def get_stream(self, url):

        return [
            {
                "quality": "720p",
                "url": "https://test-stream.m3u8"
            }
        ]