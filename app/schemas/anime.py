from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class GenreResponse(BaseModel):
    genre_id: int
    genre_name: str
    class Config: from_attributes = True

class KoreanTitleResponse(BaseModel):
    title_kr: str
    class Config: from_attributes = True

class AnimeResponse(BaseModel):
    anime_id: int
    anilist_id: int
    title_en: str
    image_url: Optional[str]
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    
    genres: List[GenreResponse] # M:N 관계 반영
    korean_titles: List[KoreanTitleResponse]

    class Config:
        from_attributes = True