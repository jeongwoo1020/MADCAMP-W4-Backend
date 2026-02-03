from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import recommends as crud
from app.services import recommend_service as service
from app.schemas.recommend import RecommendationListResponse # 정우님이 만든 스키마

router = APIRouter()

@router.get("/{user_id}", response_model=RecommendationListResponse)
def get_anime_recommendations(user_id: int, db: Session = Depends(get_db)):
    # 1. 유저 벡터 조회
    user_vector = crud.get_user_preference_vector(db, user_id)
    if not user_vector:
        raise HTTPException(status_code=404, detail="유저 분석 데이터가 없습니다.")
    
    # 2. 후보군(스탯 + 이미지 포함) 조회
    # CRUD에서 Anime.main_image도 select에 포함되어 있어야 합니다!
    candidates = crud.get_anime_stats_candidates(db, user_id)
    
    # 3. 유사도 및 추천 사유 계산
    recommendations = service.get_recommendations(user_vector, candidates)
    
    # 4. 정우님의 최종 응답 규격에 맞게 리턴
    return {
        "user_id": user_id,
        "recommendations": recommendations
    }