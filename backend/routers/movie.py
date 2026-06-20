from fastapi import APIRouter
from plugins.loader import get_plugins

router = APIRouter()


@router.get("/movie/{imdb_id}")
async def get_movie(imdb_id: str):

    plugins = get_plugins()

    for plugin in plugins:

        try:

            movie = await plugin.get_movie(imdb_id)

            if movie:
                return movie

        except Exception as e:

            print(f"Plugin error: {e}")

    return {"error": "Movie not found"}