import requests
from .base import BasePlugin

API_KEY = "b7804ca"


class Plugin(BasePlugin):

    name = "OMDbPlugin"

    def search(self, query):

        url = f"http://www.omdbapi.com/?s={query}&apikey={API_KEY}"

        response = requests.get(url)

        data = response.json()

        results = []

        if data.get("Response") == "True":

            movies = data.get("Search", [])

            for movie in movies[:5]:

                results.append({
                    "title": movie.get("Title"),
                    "year": movie.get("Year"),
                    "poster": movie.get("Poster"),
                    "imdbID": movie.get("imdbID")
                })

        return results


    async def get_movie(self, imdb_id):

        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={API_KEY}"

        response = requests.get(url)

        movie = response.json()

        return {
            "title": movie.get("Title"),
            "year": movie.get("Year"),
            "genre": movie.get("Genre"),
            "plot": movie.get("Plot"),
            "poster": movie.get("Poster"),
            "runtime": movie.get("Runtime"),
            "rating": movie.get("imdbRating")
        }


    async def get_stream(self, imdb_id):

        # Placeholder streams (test links)

        return [
            {
                "quality": "720p",
                "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
            },
            {
                "quality": "1080p",
                "url": "https://test-streams.mux.dev/test_001/stream.m3u8"
            }
        ]