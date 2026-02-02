from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models
from app.db.session import get_db
from app.schemas.anime import AnimeResponse
from app.crud import animes as crud_anime

router = APIRouter()

@router.get("/", response_model=List[AnimeResponse])
def read_animes(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud_anime.get_animes(db, skip=skip, limit=limit)

@router.get("/{anime_id}", response_model=AnimeResponse) 
def get_anime_detail(anime_id: int, db: Session = Depends(get_db)):
    anime = db.query(models.Anime).filter(models.Anime.id == anime_id).first()
    
    if not anime:
        raise HTTPException(status_code=404, detail="애니메이션 정보를 찾을 수 없습니다.")
    return anime