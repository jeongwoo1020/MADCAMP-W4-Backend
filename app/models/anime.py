from sqlalchemy import Column, Integer, String, Text, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

# 중간 테이블: 애니-장르 매핑
anime_genre_mapping = Table(
    "anime_genre_mapping",
    Base.metadata,
    Column("anime_id", Integer, ForeignKey("animes.anime_id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.genre_id", ondelete="CASCADE"), primary_key=True),
)

class Anime(Base):
    __tablename__ = "animes"

    anime_id = Column(Integer, primary_key=True, index=True)
    anilist_id = Column(Integer, unique=True, index=True)
    title_en = Column(String(255))
    image_url = Column(Text)
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)

    # 관계 설정
    korean_titles = relationship("AnimeKoreanTitle", back_populates="anime", cascade="all, delete-orphan")
    genres = relationship("Genre", secondary=anime_genre_mapping, back_populates="animes")
    reviews = relationship("UserReview", back_populates="anime")

class AnimeKoreanTitle(Base):
    __tablename__ = "anime_korean_titles"

    id = Column(Integer, primary_key=True, index=True)
    anime_id = Column(Integer, ForeignKey("animes.anime_id", ondelete="CASCADE"))
    title_kr = Column(String(255))
    
    anime = relationship("Anime", back_populates="korean_titles")

class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, index=True)
    genre_name = Column(String(50), unique=True)
    
    animes = relationship("Anime", secondary=anime_genre_mapping, back_populates="genres")