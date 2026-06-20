from fastapi import APIRouter
from pydantic import BaseModel

from database.db import SessionLocal
from database.models import Favorite

router = APIRouter()


# ⭐ Schema
class FavoriteCreate(BaseModel):

    imdbID: str
    title: str
    poster: str
    year: str


# ⭐ Add Favorite (No duplicates)
@router.post("/favorites/add")
def add_favorite(movie: FavoriteCreate):

    db = SessionLocal()

    existing = db.query(Favorite).filter(
        Favorite.imdbID == movie.imdbID
    ).first()

    if existing:

        db.close()
        return {"message": "Already exists"}

    new_movie = Favorite(
        imdbID=movie.imdbID,
        title=movie.title,
        poster=movie.poster,
        year=movie.year
    )

    db.add(new_movie)
    db.commit()

    db.close()

    return {"message": "Added"}


# ⭐ List Favorites
@router.get("/favorites/list")
def list_favorites():

    db = SessionLocal()

    movies = db.query(Favorite).all()

    db.close()

    return movies


# ⭐ Remove Favorite
@router.delete("/favorites/remove/{imdb_id}")
def remove_favorite(imdb_id: str):

    db = SessionLocal()

    movie = db.query(Favorite).filter(
        Favorite.imdbID == imdb_id
    ).first()

    if movie:

        db.delete(movie)
        db.commit()

    db.close()

    return {"message": "Removed"}