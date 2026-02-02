from sqlalchemy.orm import Session
from app.models.user import User

def get_or_create_user(db: Session, email: str, nick_name: str, google_id: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, nick_name=nick_name, google_id=google_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user