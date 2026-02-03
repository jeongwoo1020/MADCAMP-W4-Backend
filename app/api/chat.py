from fastapi import APIRouter, HTTPException
from app.schemas.recommend import QuoteAnalysisRequest, QuoteAnalysisResponse
from app.services import gemini_service as service

router = APIRouter()

@router.post("/chat", response_model=QuoteAnalysisResponse)
def analyze_user_quotes(request: QuoteAnalysisRequest):
    """
    명대사 리스트를 받아 즉석에서 성향 분석 문장을 리턴합니다. (DB 저장 없음)
    """
    # 1. 유효성 검사 (대사가 하나도 없는 경우)
    if not request.quotes:
        raise HTTPException(status_code=400, detail="분석할 대사를 최소 하나 이상 보내주세요.")
    
    # 2. Service 레이어 호출 (Gemini API 연동)
    result_text = service.generate_persona_analysis(request.quotes)
    
    # 3. 결과 바로 반환
    return QuoteAnalysisResponse(analysis=result_text)