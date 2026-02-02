from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.records import ReviewCreate, ReviewResponse, OnboardingCreate
from app.crud import record as crud_record

router = APIRouter()

# 입덕 애니 대량 선택 (Onboarding)
@router.post("/onboarding", status_code=201)
def create_onboarding(onboarding_in: OnboardingCreate, db: Session = Depends(get_db)):
    current_user_id = 1
    crud_record.create_onboarding_records(db, current_user_id, onboarding_in.anime_ids)
    return {"message": "Onboarding success"}

# 상세 리뷰 작성 및 수정 (Upsert)
@router.post("/", response_model=ReviewResponse)
def create_or_update_record(review_in: ReviewCreate, db: Session = Depends(get_db)):
    current_user_id = 1
    # Pydantic 모델을 dict로 변환하여 CRUD에 전달
    return crud_record.upsert_user_review(db, current_user_id, review_in.dict())