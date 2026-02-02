from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.record import UserReview
from app.schemas.records import ReviewCreate, OnboardingCreate
from sqlalchemy.dialects.postgresql import insert

# 1. 온보딩 대량 저장 (Bulk Insert)
def create_onboarding_records(db: Session, user_id: int, anime_ids: list):
    for a_id in anime_ids:
        stmt = insert(UserReview).values(
            user_id=user_id, 
            anime_id=a_id, 
            status="WATCHED"
        )
        db.execute(stmt.on_conflict_do_nothing(constraint='unique_user_anime'))
    db.commit()

# 2. 상세 리뷰 저장 및 업데이트 (Upsert)
def upsert_user_review(db: Session, user_id: str, review_in: ReviewCreate):
    # 가중치 평균 계산 로직 (예시: 산술 평균)
    avg_score = None
    scores = [review_in.score_story, review_in.score_character, review_in.score_art, review_in.score_music]
    valid_scores = [s for s in scores if s is not None]
    if valid_scores:
        avg_score = sum(valid_scores) / len(valid_scores)

    # PostgreSQL 전용 Upsert (ON CONFLICT) 문법
    stmt = insert(UserReview).values(
        user_id=user_id,
        anime_id=review_in.anime_id,
        status="REVIEWED",
        score_story=review_in.score_story,
        score_character=review_in.score_character,
        score_art=review_in.score_art,
        score_music=review_in.score_music,
        score=avg_score,
        comment=review_in.comment,
        watching_start=review_in.watching_start,
        watching_end=review_in.watching_end
    )
    
    # 충돌 발생 시(이미 WATCHED 데이터가 있을 시) 업데이트
    update_stmt = stmt.on_conflict_do_update(
        constraint='unique_user_anime',
        set_={
            "status": "REVIEWED",
            "score_story": stmt.excluded.score_story,
            "score_character": stmt.excluded.score_character,
            "score_art": stmt.excluded.score_art,
            "score_music": stmt.excluded.score_music,
            "score": stmt.excluded.score,
            "comment": stmt.excluded.comment,
            "watching_start": stmt.excluded.watching_start,
            "watching_end": stmt.excluded.watching_end,
            "updated_at": func.now()
        }
    )
    db.execute(update_stmt)
    db.commit()
    
    return db.query(UserReview).filter_by(user_id=user_id, anime_id=review_in.anime_id).first()

def get_user_records(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    return db.query(UserReview).filter(
            UserReview.user_id == user_id
        ).offset(skip).limit(limit).all()

def get_record_by_id(db: Session, record_id: int):
    return db.query(UserReview).filter(UserReview.id == record_id).first()

def get_summary_stats(db: Session, user_id: int):
    # SQL: SELECT COUNT(*), AVG(score), COUNT(score) FROM user_reviews WHERE user_id = :user_id
    stats = db.query(
        func.count(UserReview.id),
        func.avg(UserReview.score),
        func.count(UserReview.score)
    ).filter(UserReview.user_id == user_id).first()
    
    return stats # (total_count, avg_score, reviewed_count)

def delete_user_record(db: Session, user_id: int, anime_id: int):
    record = db.query(UserReview).filter_by(user_id=user_id, anime_id=anime_id).first()
    if record:
        db.delete(record)
        db.commit()
        return True
    return False