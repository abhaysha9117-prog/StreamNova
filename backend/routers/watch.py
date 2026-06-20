from fastapi import APIRouter
from pydantic import BaseModel
import json
import os

# ⭐ Multi Provider Loader
from plugins.providers.providers_loader import load_all_streams

router = APIRouter()

WATCH_FILE = "watch_history.json"


# ================================
# ⭐ Data Model
# ================================
class WatchItem(BaseModel):

    imdbID: str
    title: str
    poster: str
    progress: int


# ================================
# ⭐ Load History
# ================================
def load_history():

    if not os.path.exists(WATCH_FILE):

        return []

    try:

        with open(WATCH_FILE, "r") as f:

            return json.load(f)

    except:

        return []


# ================================
# ⭐ Save History
# ================================
def save_history(data):

    with open(WATCH_FILE, "w") as f:

        json.dump(data, f, indent=2)


# ================================
# ⭐ Save Progress
# ================================
@router.post("/save")
async def save_watch(item: WatchItem):

    data = load_history()

    found = False

    for m in data:

        if m["imdbID"] == item.imdbID:

            m["progress"] = item.progress
            m["title"] = item.title
            m["poster"] = item.poster

            found = True

    if not found:

        data.append(item.dict())

    save_history(data)

    return {
        "message": "Progress saved"
    }


# ================================
# ⭐ Get Continue Watching List
# ================================
@router.get("/list")
async def list_watch():

    return load_history()


# ================================
# ⭐ MULTI PROVIDER STREAMS
# ================================
@router.get("/streams/{movie_id}")
async def streams(movie_id: str):

    try:

        print("Loading streams for:", movie_id)

        streams = load_all_streams(movie_id)

        # ⭐ Safety check
        if not streams:

            return {
                "streams": []
            }

        # ⭐ Ensure provider exists
        fixed_streams = []

        for s in streams:

            if "provider" not in s:

                s["provider"] = "unknown"

            fixed_streams.append(s)

        return {
            "streams": fixed_streams
        }

    except Exception as e:

        print("Stream error:", e)

        return {
            "streams": []
        }