import numpy as np
from typing import List, Union

def generate_reason(user_vec: list, anime_stats: list) -> str:
    """
    유저 취향과 애니 스탯을 비교해 가장 비중이 높은 요소를 기반으로 추천 사유를 만듭니다.
    순서: 0:Story, 1:Art, 2:Char, 3:Music
    """
    labels = ["탄탄한 스토리", "화려한 작화", "매력적인 캐릭터", "몰입감 넘치는 음악"]
    
    # 유저가 중요하게 생각하고, 애니메이션도 점수가 높은 항목 찾기 (단순 곱 연산)
    scores = [u * a for u, a in zip(user_vec, anime_stats)]
    best_idx = scores.index(max(scores))
    
    return f"선호하시는 {labels[best_idx]} 요소가 돋보이는 작품이라 추천해 드려요!"

def get_recommendations(user_vector: Union[list, dict], candidates: List) -> List[dict]:
    # dict -> numpy 
    if isinstance(user_vector, dict):
        user_vector = [
            user_vector.get('score_story', 0.25),
            user_vector.get('score_art', 0.25),
            user_vector.get('score_character', 0.25),
            user_vector.get('score_music', 0.25)
        ]
    
    v_u = np.array(user_vector, dtype=float)
    scored_results = []

    for anime in candidates:
        v_a = np.array([
            anime.avg_story or 0.0, 
            anime.avg_art or 0.0, 
            anime.avg_character or 0.0, 
            anime.avg_music or 0.0
        ])
        
        # 코사인 유사도 계산
        norm_u = np.linalg.norm(v_u)
        norm_a = np.linalg.norm(v_a)
        
        if norm_u == 0 or norm_a == 0:
            score = 0.0
        else:
            score = np.dot(v_u, v_a) / (norm_u * norm_a)
        
        scored_results.append({
            "anime_id": anime.anime_id,
            "title_en": anime.title_en, # DB 필드명에 맞춰 매핑
            "title_kr": anime.title_kr, # 한국어 제목 추가
            "image_url": anime.image_url, # Anime 모델의 이미지 필드
            "similarity_score": round(float(score), 4),
            "reason": generate_reason(user_vector, v_a.tolist())
        })
    
    scored_results.sort(key=lambda x: x['similarity_score'], reverse=True)
    return scored_results[:5]