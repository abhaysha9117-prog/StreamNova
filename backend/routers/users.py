from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import SessionLocal, engine
from database import models

from auth.schemas import (
    UserCreate,
    UserLogin
)

from auth.auth import (
    hash_password,
    verify_password,
    create_access_token
)

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    hashed = hash_password(user.password)

    new_user = models.User(
        email=user.email,
        hashed_password=hashed
    )

    db.add(new_user)

    db.commit()

    return {"message": "User created"}


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(
        models.User
    ).filter(
        models.User.email == user.email
    ).first()

    if not db_user:
        return {"error": "User not found"}

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        return {"error": "Wrong password"}

    token = create_access_token(
        {"sub": user.email}
    )

    return {"access_token": token}