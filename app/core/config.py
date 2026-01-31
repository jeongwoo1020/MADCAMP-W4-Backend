# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Akiba Zip API"
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str = "db"  # 도커 서비스 이름이 'db'라면 이렇게 씁니다.
    DB_PORT: str = "5432" 
    
    @property
    def DATABASE_URL(self) -> str:
        # 가져온 변수들로 접속 URL을 조합합니다.
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    # .env 파일을 찾아서 읽어오라는 설정
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()