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
    score_story: Optional[int] = Field(None, ge=1, le=5)
    score_character: Optional[int] = Field(None, ge=1, le=5)
    score_art: Optional[int] = Field(None, ge=1, le=5)
    score_music: Optional[int] = Field(None, ge=1, le=5)
    
    comment: Optional[str] = None

# API 응답 결과
class ReviewResponse(BaseModel):
    id: int
    anime_id: int
    status: str
    
    watching_start: Optional[date] = None
    watching_end: Optional[date] = None
    
    score_story: Optional[int] = Field(None, ge=1, le=5)
    score_character: Optional[int] = Field(None, ge=1, le=5)
    score_art: Optional[int] = Field(None, ge=1, le=5)
    score_music: Optional[int] = Field(None, ge=1, le=5)
    score: Optional[float] = None
    
    comment: Optional[str] = None
    updated_at: datetime

    class Config:
        from_attributes = True # SQLAlchemy 모델을 Pydantic으로 자동 변환