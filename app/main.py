from fastapi import FastAPI
from app.api import records, analysis, anime, auth, recommend, chat

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Akiba.zip API",
    description="애니메이션 취향 분석 MVP",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin-allow-popups"
    return response

app.include_router(anime.router, prefix="/api/animes", tags=["Anime"])
app.include_router(records.router, prefix="/api/records", tags=["Records"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(recommend.router, prefix="/api/recommend", tags=["Recommend"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI backend!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
