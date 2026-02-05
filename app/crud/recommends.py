from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func, not_
from app.models.record import UserReview
from app.models.user import UserInsight
from app.models.anime import Anime, AnimeKoreanTitle
from app.models.recommed import AnimeStats

# 1. 유저의 취향 벡터 가져오기
def get_user_preference_vector(db: Session, user_id: int):
    """
    user_insights 테이블에서 정우님이 저장한 preference_vector(JSONB)를 가져옵니다.
    """
    insight = db.query(UserInsight).filter(UserInsight.user_id == user_id).first()
    return insight.preference_vector if insight else None

# 2. 추천 후보군 추출 (안 본 애니 + 스탯 데이터 JOIN)
def get_anime_stats_candidates(db: Session, user_id: int, limit: int = 500):
    """
    유저가 안 본 애니메이션들 중, anime_stats(벡터)가 존재하는 데이터만 JOIN해서 가져옵니다.
    """
    # 유저가 이미 본(또는 리뷰한) 애니 ID 리스트
    watched_ids_query = db.query(UserReview.anime_id).filter(UserReview.user_id == user_id)
    
    # Anime + AnimeStats를 JOIN하여 한꺼번에 가져오기
    return db.query(
        Anime.anime_id,
        Anime.title_en,
        Anime.image_url,
        AnimeStats.avg_story,
        AnimeStats.avg_art,
        AnimeStats.avg_character,
        AnimeStats.avg_music,
        AnimeKoreanTitle.title_kr
    ).join(AnimeStats, Anime.anime_id == AnimeStats.anime_id) \
     .outerjoin(AnimeKoreanTitle, Anime.anime_id == AnimeKoreanTitle.anime_id) \
     .filter(not_(Anime.anime_id.in_(watched_ids_query))) \
     .limit(limit) \
     .all()
