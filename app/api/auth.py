from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from app.db.session import get_db
from app.schemas.auth import GoogleTokenRequest
from app.crud import user as crud_user
from app.core.config import settings
from app.core.security import create_access_token

router = APIRouter()

@router.post("/google")
def google_login(token_in: GoogleTokenRequest, db: Session = Depends(get_db)):
    try:
        # 1. 구글 토큰 검증
        idinfo = id_token.verify_oauth2_token(
            token_in.id_token, 
            requests.Request(), 
            settings.GOOGLE_CLIENT_ID
        )

        # 2. 유저 정보 추출
        email = idinfo.get('email')
        name = idinfo.get('name')
        google_id = idinfo.get('sub') # 구글 고유 유저 ID

        # 3. DB 확인 및 회원가입
        user = crud_user.get_or_create_user(db, email, name, google_id)
        
        access_token = create_access_token(data={"sub": str(user.user_id)})

        # 4. 결과 반환 (실무에선 여기서 JWT를 발행합니다)
        return {
            "access_token": access_token,
            "user_id": user.user_id,
            "nick_name": user.nick_name
        }

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google Token")