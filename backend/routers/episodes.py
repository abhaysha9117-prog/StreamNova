from fastapi import APIRouter

router = APIRouter()


@router.get("/episodes/{imdbID}")
async def get_episodes(imdbID: str):

    # ⭐ Demo Episode Data

    return {
        "seasons": [
            {
                "season": 1,
                "episodes": [
                    {
                        "episode": 1,
                        "title": "Pilot",
                        "imdbID": imdbID,
                        "stream": {
                            "quality": "720p",
                            "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
                        }
                    },
                    {
                        "episode": 2,
                        "title": "Cat's in the Bag",
                        "imdbID": imdbID,
                        "stream": {
                            "quality": "720p",
                            "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8"
                        }
                    }
                ]
            }
        ]
    }