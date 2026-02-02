from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.records import ReviewCreate, ReviewResponse
from app.crud.record import upsert_user_review

router = APIRouter()

@router.post("/", response_model=ReviewResponse)
def create_or_update_record(review_in: ReviewCreate, db: Session = Depends(get_db)):
    # 지금은 테스트용으로 user_id를 고정하지만, 나중에 구글 로그인 연동 후에는 토큰에서 가져옵니다
    current_user_id = "test_google_user_123"
    return upsert_user_review(db, current_user_id, review_in)