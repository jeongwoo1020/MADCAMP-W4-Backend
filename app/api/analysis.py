from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.analysis_service import AnalysisService
from app.schemas.analysis import (
    AnalysisSummaryResponse, 
    GenreAnalysisResponse, 
    TimeAnalysisResponse
)

router = APIRouter()

# 1. 요약 정보 (시청 수, 평점, 최근 장르)
@router.get("/summary", response_model=AnalysisSummaryResponse)
def get_summary(db: Session = Depends(get_db)):
    current_user_id = 1  # 임시 사용자 ID
    return AnalysisService.get_summary(db, current_user_id)

# 2. 장르 분포 (파이 차트용 및 AI 분석 텍스트)
@router.get("/genre", response_model=GenreAnalysisResponse)
def get_genre_analysis(db: Session = Depends(get_db)):
    current_user_id = 1
    return AnalysisService.get_genre_analysis(db, current_user_id)

# 3. 시계열 지표 (라인 그래프 및 덕질 분석)
@router.get("/time", response_model=TimeAnalysisResponse)
def get_time_analysis(db: Session = Depends(get_db)):
    current_user_id = 1
    return AnalysisService.get_time_metrics(db, current_user_id)