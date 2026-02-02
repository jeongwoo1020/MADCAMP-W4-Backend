from sqlalchemy.orm import Session
from app.models.record import UserReview
from app.schemas.record import ReviewCreate
from sqlalchemy.dialects.postgresql import insert

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