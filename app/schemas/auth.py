from pydantic import BaseModel

class GoogleTokenRequest(BaseModel):
    id_token: str