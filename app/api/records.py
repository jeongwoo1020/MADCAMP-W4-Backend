from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from typing import List
from app.schemas.records import ReviewCreate, ReviewResponse, OnboardingCreate
from app.crud import record as crud_record

from app.api.deps import get_current_user 

router = APIRouter()

# 1. 입덕 애니 대량 선택 (Onboarding)
@router.post("/onboarding", status_code=201)
def create_onboarding(
    onboarding_in: OnboardingCreate, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user) # 토큰에서 ID 추출
):
    
    crud_record.create_onboarding_records(db, current_user_id, onboarding_in.anime_ids)
    return {"message": "Onboarding success"}

# 2. 상세 리뷰 작성 및 수정 (Upsert)
@router.post("/", response_model=ReviewResponse)
def create_or_update_record(
    review_in: ReviewCreate, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user) # 토큰에서 ID 추출
):
    # Pydantic 모델을 dict로 변환하여 CRUD에 전달
    return crud_record.upsert_user_review(db, current_user_id, review_in)

# 3. 내 모든 기록 조회 (선택 목록 + 리뷰)
@router.get("/", response_model=List[ReviewResponse])
def read_my_records(
    skip: int = 0, 
    limit: int = 20, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user) # 토큰에서 내 ID 추출
):
    # crud_record에 내 user_id만 필터링하는 함수가 있어야 합니다.
    records = crud_record.get_user_records(db, user_id=current_user_id, skip=skip, limit=limit)
    return records

# 4. 특정 기록 상세 조회
@router.get("/{record_id}", response_model=ReviewResponse)
def read_record_detail(
    record_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    # record_id로 조회하되, 반드시 내 user_id와 일치하는지 검증합니다.
    record = crud_record.get_record_by_id(db, record_id=record_id)
    
    if not record:
        raise HTTPException(status_code=404, detail="기록을 찾을 수 없습니다.")
    
    # [핵심] 소유권 확인: 남의 기록 id를 넣었을 경우 차단!
    if record.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="이 기록에 접근할 권한이 없습니다.")
        
    return record