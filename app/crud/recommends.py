from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func, not_
from app.models.record import UserReview
from app.models.user import UserInsight
from app.models.anime import Anime

# 1. 추천 엔진용 유저 점수 데이터 추출 (벡터 생성용)
def get_user_ratings_for_vector(db: Session, user_id: int):
    """
    유저가 매긴 점수들을 가져와서 추천 엔진(Service)이 
    유저의 취향 벡터를 계산할 수 있게 합니다.
    """
    return db.query(UserReview.anime_id, UserReview.score) \
             .filter(UserReview.user_id == user_id, UserReview.score.isnot(None)) \
             .all()

# 2. 추천 후보군 애니메이션 추출 (안 본 것만)
def get_recommendation_candidates(db: Session, user_id: int, limit: int = 500):
    """
    유저가 이미 시청한(WATCHED, REVIEWED) 애니를 제외하고 
    추천 후보가 될 만한 데이터를 가져옵니다.
    """
    # 유저가 이미 본 애니 ID 리스트
    watched_ids = db.query(UserReview.anime_id) \
                    .filter(UserReview.user_id == user_id) \
                    .all()
    watched_ids = [r[0] for r in watched_ids]

    return db.query(Anime) \
             .filter(not_(Anime.anime_id.in_(watched_ids))) \
             .limit(limit) \
             .all()

# 3. 분석 결과 및 벡터 저장 (Upsert into user_insights)
def upsert_user_insight(db: Session, user_id: int, top_genres: list, vector: list, persona: str):
    """
    LLM 분석 결과와 추천용 벡터를 JSONB 형태로 저장합니다.
    정우님이 설계하신 user_insights 테이블을 활용합니다.
    """
    stmt = insert(UserInsight).values(
        user_id=user_id,
        top_genres=top_genres, # JSONB
        preference_vector=vector, # JSONB
        persona_text=persona,
        updated_at=func.now()
    )

    # 이미 데이터가 있으면 최신 분석 결과로 덮어쓰기
    update_stmt = stmt.on_conflict_do_update(
        index_elements=['user_id'],
        set_={
            "top_genres": stmt.excluded.top_genres,
            "preference_vector": stmt.excluded.preference_vector,
            "persona_text": stmt.excluded.persona_text,
            "updated_at": func.now()
        }
    )
    db.execute(update_stmt)
    db.commit()
    return True