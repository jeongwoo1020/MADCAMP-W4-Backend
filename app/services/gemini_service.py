from google import genai
import os
from typing import List

# 1. 클라이언트 초기화 (애플리케이션 시작 시 한 번만 실행되도록 전역에 둡니다)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_persona_analysis(quotes: List[str]) -> str:
    """
    클라이언트에서 받은 명대사 리스트를 기반으로 즉석 분석을 수행합니다.
    """
    if not quotes:
        return "분석하고 싶은 명대사를 입력해주세요"
    
    input_quotes = "\n".join([f"- {q}" for q in quotes])

    # [프롬프트 설정]
    prompt = f"""
    You are an expert Anime Quote Analyst. Your task is to provide a soulful analysis of the user's personality based on their favorite anime quotes.

    [Task Rules]
    1. Generate exactly 2-3 sentences in Korean.
    2. Follow this specific 2-step structure:
    - Step 1 (Quote Review): Provide a warm and insightful appreciation of the specific quotes provided. Acknowledge the core values (e.g., effort, talent, solitude) within the text.
    - Step 2 (Preference Link): Connect those values to the user's personal taste. Start with phrases like "평소 ~한 취향을 가지고 계신 것 같네요" or "~한 서사에 깊이 공감하시는 것 같습니다."

    [Tone & Manner]
    - Friendly, polished, and empathetic.
    - Do not use overly robotic or repetitive phrases.

    [Expression Bank for Step 2]
    • If Passion/Effort: 열정 넘치는 애니메이션과 인물의 성장 서사
    • If Solitude/Philosophy: 깊은 사색과 철학적인 메시지가 담긴 묵직한 작품
    • If Sacrifice/Friendship: 뜨거운 동료애와 숭고한 희생이 돋보이는 감동적인 서사
    • If Wit/Reality: 냉철한 현실 풍자와 위트 있는 통찰이 담긴 감각적인 스토리

    [Variety Rule]
    Be creative and fashion-forward in your language. Ensure the output feels like a personalized letter.

    —
    Example Output:
    정말 열정이 넘치는 대사네요. 재능뿐만 아니라 노력과 갈고 닦은 센스를 강조하는 점이 인상 깊습니다. 평소 열정 넘치는 애니메이션과 대사에 깊이 감동하는 취향을 가지고 계신 것 같네요.
    
    [User's Input Quotes]
    {input_quotes}
    """
    
    try:
        # [핵심 수정] model 변수 대신 client.models.generate_content를 직접 사용합니다.
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        # 에러의 구체적인 메시지를 반환하도록 수정
        print(f"Full Error: {e}")
        return f"Gemini API Error: {str(e)}"
    
def check_models():
    for m in client.models.list():
        print(f"사용 가능 모델: {m.name}")