from pydantic import BaseModel
from typing import List, Dict

# 취향 분석 요약 정보 (/api/analysis/summary)
class AnalysisSummaryResponse(BaseModel):
    total_watched_count: int  # 시청한 애니 수 (WATCHED + REVIEWED)
    total_reviewed_count: int # 기록된 애니 수 (REVIEWED)
    avg_score: float          # 전체 평균 평점
    recent_genres: List[str]  # 최근 시청한 장르 상위 3개
    
    class Config:
        from_attributes = True

# 장르 분포 (예: {"label": "이세계물", "value": 70})
class GenreDistItem(BaseModel):
    label: str
    value: float

# (/api/analysis/genre)
class GenreAnalysisResponse(BaseModel):
    genre_distribution: List[GenreDistItem]
    analysis_text: str  # "당신은 '이세계물'에 70% 편향되어 있습니다..."
    
    class Config:
        from_attributes = True
    
# 시청 타임라인 (예: {"date": "2025-01", "count": 5})
class TimelineItem(BaseModel):
    date: str   # "2025-01"
    count: int  # 해당 월 기록 수

# (/api/analysis/time)
class TimeAnalysisResponse(BaseModel):
    timeline_data: List[TimelineItem]
    most_active_month: str      # 가장 활발했던 달
    weekly_avg_records: float   # 주간 평균 기록 수
    total_watching_time: int    # 누적 시청 시간 (분 단위)
    consecutive_days: int       # 연속 기록 일수
    
    class Config:
        from_attributes = True
    
class RecommendationResponse(BaseModel):
    anime_id: int
    title_en: str
    image_url: str
    similarity_score: float # 유저 벡터와의 유사도
    
    class Config:
        from_attributes = True
    
class QuoteAnalysisResponse(BaseModel):
    keywords: List[str]  # ["희생", "신념", "고독"]
    persona_report: str  # LLM이 생성한 맞춤형 코멘트
    
    class Config:
        from_attributes = True