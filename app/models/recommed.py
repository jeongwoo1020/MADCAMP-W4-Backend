from sqlalchemy import Column, Integer, Float, ForeignKey
from app.db.session import Base

class AnimeStats(Base):
    __tablename__ = "anime_stats"

    anilist_id = Column(Integer, primary_key=True)
    anime_id = Column(Integer, ForeignKey("animes.anime_id", ondelete="CASCADE"))
    avg_story = Column(Float, default=0.0)
    avg_art = Column(Float, default=0.0)
    avg_character = Column(Float, default=0.0)
    avg_music = Column(Float, default=0.0)