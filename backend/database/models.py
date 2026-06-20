from sqlalchemy import Column, Integer, String
from database.db import Base


# Existing User Model

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True)

    password = Column(String)


# ⭐ Favorites Model (NEW)

class Favorite(Base):

    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)

    imdbID = Column(String, unique=True, index=True)

    title = Column(String)

    poster = Column(String)

    year = Column(String)
    # ⭐ Watch History Table

class WatchHistory(Base):

    __tablename__ = "watch_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    imdbID = Column(String)

    title = Column(String)

    poster = Column(String)

    progress = Column(Integer)  # seconds