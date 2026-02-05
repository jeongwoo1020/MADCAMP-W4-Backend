from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime

# 온보딩 시 여러 애니를 한꺼번에 선택할 때 사용
class OnboardingCreate(BaseModel):
    anime_ids: List[int]

# 상세 리뷰 작성 및 수정 (Upsert용)
class ReviewCreate(BaseModel):
    anime_id: int
    watching_start: Optional[date] = None
    watching_end: Optional[date] = None
    
    # 1~5점 사이로 제한
    score_story: Optional[float] = Field(None, ge=0, le=5, multiple_of=0.5)
    score_character: Optional[float] = Field(None, ge=0, le=5, multiple_of=0.5)
    score_art: Optional[float] = Field(None, ge=0, le=5, multiple_of=0.5)
    score_music: Optional[float] = Field(None, ge=0, le=5, multiple_of=0.5)
    
    comment: Optional[str] = None

# --- [1] 기초 정보 응답용 스키마 (하위 모델) ---

class GenreResponse(BaseModel):
    genre_id: int
    genre_name: str

    class Config:
        from_attributes = True

class TitleKrResponse(BaseModel):
    title_kr: str

    class Config:
        from_attributes = True

# --- [2] 애니메이션 상세 정보 (리뷰 응답에 포함될 용도) ---

class AnimeInReview(BaseModel):
    anime_id: int
    title_en: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    
    # 모델의 relationship 이름과 정확히 일치해야 함
    korean_titles: List[TitleKrResponse] = []
    genres: List[GenreResponse] = []

    class Config:
        from_attributes = True

# --- [3] 최종 API 응답용 스키마 (Response) ---

class ReviewResponse(BaseModel):
    id: int
    anime_id: int
    status: str
    
    watching_start: Optional[date] = None
    watching_end: Optional[date] = None
    
    score_story: Optional[float] = Field(None, ge=0, le=5, multiple_of=0.5)
    score_character: Optional[float] = Field(None, ge=0, le=5, multiple_of=0.5)
    score_art: Optional[float] = Field(None, ge=0, le=5, multiple_of=0.5)
    score_music: Optional[float] = Field(None, ge=0, le=5, multiple_of=0.5)
    score: Optional[float] = None
    
    comment: Optional[str] = None
    updated_at: datetime
    
    anime: Optional[AnimeInReview] = None

    class Config:
        from_attributes = True # SQLAlchemy 모델을 Pydantic으로 자동 변환