from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # 여기 변경
import jwt
from app.core.config import settings

reusable_oauth2 = HTTPBearer()

def get_current_user(res: HTTPAuthorizationCredentials = Depends(reusable_oauth2)):
    # res.credentials 안에 우리가 넣은 JWT 문자열이 들어옵니다.
    token = res.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
        return int(user_id)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="인증에 실패했습니다.")