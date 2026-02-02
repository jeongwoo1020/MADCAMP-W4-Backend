from sqlalchemy.orm import Session
from app.models.anime import Anime, AnimeKoreanTitle, Genre, anime_genre_mapping

# 1. 애니메이션 목록 및 검색
def get_animes(db: Session, skip: int = 0, limit: int = 100):
    # 한국어 제목과 장르를 함께 가져옵니다.
    return db.query(Anime).offset(skip).limit(limit).all()

# 2. 특정 애니 상세 정보
def get_anime_by_id(db: Session, anime_id: int):
    return db.query(Anime).filter(Anime.anime_id == anime_id).first()

# 3. 애니 ID 리스트에 해당하는 모든 장르 이름 가져오기
def get_genres_by_anime_ids(db: Session, anime_ids: list):
    return db.query(Genre.genre_name) \
             .join(anime_genre_mapping) \
             .filter(anime_genre_mapping.c.anime_id.in_(anime_ids)) \
             .all()