from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class User(Base):
    __tablename__ = "users" # SQL의 Users 테이블과 매칭

    user_id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String(255), unique=True)
    email = Column(String(255))
    nick_name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 관계 설정
    reviews = relationship("UserReview", back_populates="user", cascade="all, delete-orphan")
    insight = relationship("UserInsight", back_populates="user", uselist=False, cascade="all, delete-orphan")

class UserInsight(Base):
    __tablename__ = "user_insights"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    top_genres = Column(JSON) # PostgreSQL의 JSONB로 동작
    preference_vector = Column(JSON)
    persona_text = Column(Text)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="insight")