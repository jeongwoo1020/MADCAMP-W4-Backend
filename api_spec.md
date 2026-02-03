# Akiba.zip API Specification


## 1. Authentication (인증)

### 1-1. Google Login
구글 로그인 토큰을 검증하고, 백엔드 전용 액세스 토큰을 발급합니다.
* **Method**: `POST`
* **Path**: `/auth/google`
* **Request Body**:
    ```json
    {
      "id_token": "string" // 구글에서 받은 id_token
    }
    ```
* **Response Body**:
    ```json
    {
      "access_token": "string", // 백엔드 API 호출 시 Header에 Bearer로 사용
      "user_id": 1,
      "nick_name": "string"
    }
    ```

---

## 2. Anime (애니메이션 정보)

### 2-1. Read Animes (애니 목록 조회)
애니메이션 목록을 조회합니다 (페이징 지원).
* **Method**: `GET`
* **Path**: `/animes/`
* **Query Parameters**:
    * `skip` (int, default: 0): 건너뛸 개수
    * `limit` (int, default: 20): 가져올 개수
* **Response Body**:
    ```json
    [
      {
        "anime_id": 1,
        "anilist_id": 12345,
        "title_en": "string",
        "image_url": "string",
        "description": "string",
        "start_date": "2023-01-01",
        "end_date": "2023-03-30",
        "genres": [
          {
            "genre_id": 1,
            "genre_name": "Action"
          }
        ],
        "korean_titles": [
          {
            "title_kr": "string"
          }
        ]
      }
    ]
    ```

### 2-2. Get Anime Detail (애니 상세 조회)
특정 애니메이션의 상세 정보를 조회합니다.
* **Method**: `GET`
* **Path**: `/animes/{anime_id}`
* **Path Variables**:
    * `anime_id` (int): 애니메이션 ID
* **Response Body**:
    ```json
    {
      "anime_id": 1,
      "anilist_id": 12345,
      "title_en": "string",
      "image_url": "string",
      "description": "string",
      "start_date": "2023-01-01",
      "end_date": "2023-03-30",
      "genres": [
        {
          "genre_id": 1,
          "genre_name": "Action"
        }
      ],
      "korean_titles": [
        {
          "title_kr": "string"
        }
      ]
    }
    ```

---

## 3. Records (기록 및 리뷰)
**Header**: `Authorization: Bearer <access_token>` 필요

### 3-1. Onboarding (입덕 애니 대량 선택)
회원가입 직후, 여러 애니메이션을 '봤어요' 처리할 때 사용합니다.
* **Method**: `POST`
* **Path**: `/records/onboarding`
* **Request Body**:
    ```json
    {
      "anime_ids": [1, 2, 3] // 본 애니메이션 ID 리스트
    }
    ```
* **Response Body**:
    ```json
    {
      "message": "Onboarding success"
    }
    ```

### 3-2. Create or Update Review (리뷰 작성/수정)
애니메이션에 대한 상세 리뷰(평점, 코멘트, 시청 기간)를 작성하거나 수정합니다.
* **Method**: `POST`
* **Path**: `/records/`
* **Request Body**:
    ```json
    {
      "anime_id": 1,
      "watching_start": "2023-01-01", // Optional (이하 동일), YYYY-MM-DD
      "watching_end": "2023-01-02",
      "score_story": 5,     // 1~5 정수
      "score_character": 4, // 1~5 정수
      "score_art": 3,       // 1~5 정수
      "score_music": 5,     // 1~5 정수
      "comment": "재밌었습니다."
    }
    ```
* **Response Body**:
    ```json
    {
      "id": 1,
      "anime_id": 1,
      "status": "REVIEWED", // WATCHED -> REVIEWED 
      "watching_start": "2023-01-01",
      "watching_end": "2023-01-02",
      "score_story": 5,
      "score_character": 4,
      "score_art": 3,
      "score_music": 5,
      "score": 4.25, // 평균 평점 (서버 계산)
      "comment": "재밌었습니다.",
      "updated_at": "2023-10-27T10:00:00"
    }
    ```

### 3-3. Read My Records (내 기록 전체 조회)
내가 기록한 모든 애니메이션 리뷰와 상태를 조회합니다.
* **Method**: `GET`
* **Path**: `/records/`
* **Query Parameters**:
    * `skip` (int, default: 0)
    * `limit` (int, default: 20)
* **Response Body**:
    `List[ReviewResponse]` (3-2와 동일한 객체 리스트)

### 3-4. Read Record Detail (특정 기록 조회)
특정 기록의 상세 내용을 조회합니다. (본인 기록만 조회 가능)
* **Method**: `GET`
* **Path**: `/records/{record_id}`
* **Path Variables**:
    * `record_id` (int): 기록 ID
* **Response Body**:
    `ReviewResponse` (3-2와 동일한 객체)

---

## 4. Analysis (취향 분석)
**Header**: `Authorization: Bearer <access_token>` 필요

### 4-1. Summary (요약 정보)
사용자의 시청 수, 평균 평점, 선호 장르 등을 요약해서 보여줍니다.
* **Method**: `GET`
* **Path**: `/analysis/summary`
* **Response Body**:
    ```json
    {
      "total_watched_count": 10,
      "total_reviewed_count": 5,
      "avg_score": 4.5,
      "recent_genres": ["Action", "Romance", "Fantasy"]
    }
    ```

### 4-2. Genre Analysis (장르 분포)
사용자가 본 애니메이션의 장르 분포를 반환합니다. 파이 차트 등에 사용 가능합니다.
* **Method**: `GET`
* **Path**: `/analysis/genre`
* **Response Body**:
    ```json
    {
      "genre_distribution": [
        {
          "label": "이세계물",
          "value": 70.5
        },
        {
          "label": "일상",
          "value": 29.5
        }
      ],
      "analysis_text": "당신은 '이세계물'에 70% 편향되어 있습니다..."
    }
    ```

### 4-3. Preference Analysis (취향 벡터)
사용자의 취향 분석 벡터 데이터를 반환합니다. (JSON 형태)
* **Method**: `GET`
* **Path**: `/analysis/preference`
* **Response Body**:
    ```json
    // 내부 로직에 따라 구조가 달라질 수 있음 (Raw JSON)
    {
      "score_art": 0.24,
      "score_music": 0.24,
      "score_story": 0.24,
      "score_character": 0.29
    }
    ```

### 4-4. Time Analysis (시계열 분석)
월별 시청 기록 수, 누적 시청 시간, 활동 패턴 등을 분석합니다.
* **Method**: `GET`
* **Path**: `/analysis/time`
* **Response Body**:
    ```json
    {
      "timeline_data": [
        {
          "date": "2025-01",
          "count": 5
        }
      ],
      "most_active_month": "2025-01",
      "weekly_avg_records": 2.5,
      "total_watching_time": 1200, // 분 단위
      "consecutive_days": 3
    }
    ```

---

## 5. Recommend (추천 시스템)
**Header**: `Authorization: Bearer <access_token>` 필요

### 5-1. Get Recommendations (맞춤 애니 추천)
사용자의 취향 벡터(Insight)와 유사한 애니메이션을 추천합니다.
* **Method**: `GET`
* **Path**: `/recommend/{user_id}`
* **Path Variables**:
    * `user_id` (int): 추천받을 사용자 ID (본인 ID)
* **Response Body**:
    ```json
    {
      "user_id": 1,
      "recommendations": [
        {
          "anime_id": 10,
          "title_en": "Frieren: Beyond Journey's End",
          "image_url": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx154587-gJHx8zP659q6.jpg",
          "similarity_score": 0.98,
          "reason": "정우님이 좋아하시는 '판타지' 장르라 추천해요!"
        },
        {
          "anime_id": 45,
          "title_en": "Spy x Family",
          "image_url": "...",
          "similarity_score": 0.85,
          "reason": "최근 평점이 높은 작품입니다."
        }
      ]
    }
    ```

---

## 6. Chat (AI 명대사 분석)

### 6-1. Analyze Quotes (명대사 성향 분석)
사용자가 입력한 명대사 리스트를 바탕으로 AI가 성향을 즉석에서 분석해줍니다. (DB 저장 X)
* **Method**: `POST`
* **Path**: `/chat/chat`
* **Request Body**:
    ```json
    {
      "quotes": [
        "포기하면 그 시합은 종료야",
        "왼손은 거들 뿐",
        "도망치면 하나, 전진하면 둘"
      ]
    }
    ```
* **Response Body**:
    ```json
    {
      "analysis": "당신은 끈기 있고 열정적인 사람이며, 어려움 앞에서도 물러서지 않는 도전 정신을 가지고 있습니다."
    }
    ```
