from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func
from app.models.user import UserInsight

# 1. 저장된 인사이트(벡터, 페르소나 등) 가져오기
def get_user_insight(db: Session, user_id: int):
    return db.query(UserInsight).filter(UserInsight.user_id == user_id).first()

# 2. 분석 결과 저장/업데이트
def upsert_user_insight(db: Session, user_id: int, insight_data: dict):
    stmt = insert(UserInsight).values(user_id=user_id, **insight_data)
    update_stmt = stmt.on_conflict_do_update(
        index_elements=['user_id'],
        set_={**insight_data, "updated_at": func.now()}
    )
    db.execute(update_stmt)
    db.commit()