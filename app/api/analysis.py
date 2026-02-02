from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.analysis_service import AnalysisService
from app.schemas.analysis import (
    AnalysisSummaryResponse, 
    GenreAnalysisResponse, 
    TimeAnalysisResponse
)
from app.api.deps import get_current_user

router = APIRouter()

# 1. 요약 정보 (시청 수, 평점, 최근 장르)
@router.get("/summary", response_model=AnalysisSummaryResponse)
def get_summary(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user) # 여기서 진짜 유저 ID를 받습니다!
):
    return AnalysisService.get_summary(db, current_user_id)

# 2. 장르 분포 (파이 차트용 및 AI 분석 텍스트)
@router.get("/genre", response_model=GenreAnalysisResponse)
def get_genre_analysis(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    return AnalysisService.get_genre_analysis(db, current_user_id)

# 3. 취향 분석 벡터 전용 API
@router.get("/preference")
def get_preference_analysis(db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user)):
    data = AnalysisService.get_preference_analysis(db, current_user_id)
    if isinstance(data, str):
        import json
        return json.loads(data)
    return data

# 4. 시계열 지표 (라인 그래프 및 덕질 분석)
@router.get("/time", response_model=TimeAnalysisResponse)
def get_time_analysis(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    return AnalysisService.get_time_analysis(db, current_user_id)