# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Akiba Zip API"
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_HOST: str = "db" 
    DB_PORT: str = "5432"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"  # .env에 클래스 외 변수가 있어도 무시함
    )
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

settings = Settings()