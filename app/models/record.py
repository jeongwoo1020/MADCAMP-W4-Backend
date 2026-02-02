from sqlalchemy import Column, Integer, String, Float, Text, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class UserReview(Base):
    __tablename__ = "user_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    anime_id = Column(Integer, ForeignKey("animes.anime_id", ondelete="CASCADE"), nullable=False)
    
    status = Column(String(20), default="WATCHED") # WATCHED, REVIEWED
    
    watching_start = Column(Date)
    watching_end = Column(Date)
    
    score_story = Column(Integer)
    score_character = Column(Integer)
    score_art = Column(Integer)
    score_music = Column(Integer)
    score = Column(Float) # 가중치 평균
    comment = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 관계 설정
    user = relationship("User", back_populates="reviews")
    anime = relationship("Anime", back_populates="reviews")

    # 한 유저가 같은 애니를 중복 기록하지 않도록 설정
    __table_args__ = (UniqueConstraint('user_id', 'anime_id', name='unique_user_anime'),)