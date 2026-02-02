from fastapi import FastAPI
from app.api import records, analysis, anime

app = FastAPI(
    title="Akiba.zip API",
    description="애니메이션 취향 분석 MVP",
    version="1.0.0"
)

app.include_router(anime.router, prefix="/api/animes", tags=["Anime"])
app.include_router(records.router, prefix="/api/records", tags=["Records"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI backend!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
