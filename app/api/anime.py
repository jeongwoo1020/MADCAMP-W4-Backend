from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.anime import AnimeResponse
from app.crud import animes as crud_anime

router = APIRouter()

@router.get("/", response_model=List[AnimeResponse])
def read_animes(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud_anime.get_animes(db, skip=skip, limit=limit)