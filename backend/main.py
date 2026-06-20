from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# ⭐ Import Routers
from routers import users
from routers import search
from routers import movie
from routers import stream
from routers import favorites
from routers import watch
from routers import extensions
from routers import episodes

# ⭐ Import Plugin Loader
from plugins.loader import load_plugins


# ⭐ Create app FIRST (very important)
app = FastAPI()


# ⭐ Static files
app.mount(
    "/repo_test",
    StaticFiles(directory="repo_test"),
    name="repo_test"
)


# ⭐ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ⭐ Load Plugins
load_plugins()


# ⭐ Users Router
app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)


# ⭐ Episodes Router
app.include_router(
    episodes.router,
    tags=["Episodes"]
)


# ⭐ Search Router
app.include_router(
    search.router,
    tags=["Search"]
)


# ⭐ Movie Router
app.include_router(
    movie.router,
    tags=["Movie"]
)


# ⭐ Stream Router
app.include_router(
    stream.router,
    tags=["Stream"]
)


# ⭐ Favorites Router
app.include_router(
    favorites.router,
    tags=["Favorites"]
)


# ⭐ Watch Router
app.include_router(
    watch.router,
    prefix="/watch",
    tags=["Watch"]
)
from routers import torrent

app.include_router(
    torrent.router,
    prefix="/torrent",
    tags=["Torrent"]
)


# ⭐ Extensions Router
app.include_router(
    extensions.router,
    prefix="/extensions",
    tags=["Extensions"]
)


# ⭐ Root Endpoint
@app.get("/")
def root():

    return {
        "message": "StreamNova Backend Running 🚀"
    }

from routers import provider

app.include_router(
    provider.router,
    tags=["Provider"]
)