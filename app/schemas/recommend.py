from pydantic import BaseModel
from typing import List, Optional

# 1. 유사한 애니메이션 응답 규격
class RecommendedAnime(BaseModel):
    anime_id: int
    title_en: str
    image_url: Optional[str] = None
    similarity_score: float  # 얼마나 비슷한지 (0.0 ~ 1.0)
    reason: Optional[str] = None # "정우님이 좋아하시는 '액션' 장르라 추천해요!"

    class Config:
        from_attributes = True

# 2. 최종 추천 API 응답
class RecommendationListResponse(BaseModel):
    user_id: int
    recommendations: List[RecommendedAnime]


# 명대사 분석 
# 1. 클라이언트 -> 서버 (명대사 텍스트 리스트)
class QuoteAnalysisRequest(BaseModel):
    quotes: List[str]  # 예: ["포기하면 그 시합은 종료야", "왼손은 거들 뿐"]

# 2. 서버 -> 클라이언트 (분석 결과 문장)
class QuoteAnalysisResponse(BaseModel):
    analysis: str