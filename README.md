# Akiba.zip Backend

**Akiba.zip**의 백엔드 서버 저장소입니다.  
FastAPI를 기반으로 구축되었으며, 사용자의 취향을 분석하여 애니메이션을 추천하고 다양한 커뮤니티 기능을 제공합니다.

## ✨ 주요 기능

### 1. 인증 (Authentication)
사용자 계정 관리 및 보안을 담당합니다.
- **Google OAuth2**: 구글 계정을 연동하여 간편하고 안전하게 로그인할 수 있습니다.
- **JWT (JSON Web Token)**: 로그인 성공 시 Access Token을 발급하여 세션 상태를 관리합니다.

### 2. 애니 기록 (Anime Recording)
사용자가 애니메이션에 대한 경험을 기록하는 기능입니다.
- **온보딩 (Onboarding)**: 서비스 가입 직후, 감명 깊게 본 '인생 애니'를 선택하여 초기 취향 데이터를 수집합니다.
- **별점 및 리뷰**: 애니메이션에 별점(5점 만점)을 부여하고, 상세한 감상평을 남길 수 있습니다.
<img width="1182" height="866" alt="maindashboard" src="https://github.com/user-attachments/assets/4ed93557-a588-419c-bbc1-8ea94f777332" />

### 3. 취향 분석과 추천시스템 (Analysis & Recommendation) 
사용자의 활동 데이터를 기반으로 정교한 추천을 제공합니다. 이는 **컨텐츠 기반 필터링(Content-based Filtering)** 방식을 사용합니다.

- **장르 벡터 (Genre Vector)**: 사용자가 선호하는 장르(액션, 로맨스 등)의 분포를 분석한 벡터입니다.
- **선호 벡터 (Preference Vector)**: 사용자가 스토리, 작화, 캐릭터, 음악 중 어떤 요소를 중요하게 생각하는지(가중치)를 분석한 결과입니다. (L1 정규화 적용)
- **코사인 유사도 (Cosine Similarity)**: 사용자 선호 벡터와 애니메이션의 속성 벡터(Story, Art, Char, Music) 간의 유사도를 계산하여 추천합니다.
<img width="825" height="730" alt="analysis" src="https://github.com/user-attachments/assets/f2521f6e-53ec-4854-a281-6b3f0145829d" />


### 4. 명대사 분석 (Famous Lines Analysis) 
Google의 최신 AI 모델을 활용한 감성 분석 기능입니다.
- **Gemini Pro 연동**: Google **Gemini-2.0-flash** 모델을 사용합니다.
- **페르소나 분석**: 사용자가 저장한 애니메이션 명대사들을 분석하여, 사용자의 성격과 내면의 가치관(예: 열정, 고독, 희생 등)을 파악하고 따뜻한 코멘트를 제공합니다.
<img width="1277" height="862" alt="quote" src="https://github.com/user-attachments/assets/c884e416-a639-4683-8898-0b872334a521" />

---

## 🏗️ 아키텍처 (Architecture)

유지보수와 확장성을 고려하여 **계층형 아키텍처(Layered Architecture)**를 채택했습니다.

- **API Layer** (`app/api/`):  
  엔드포인트 정의 및 요청/응답 검증
- **Service Layer** (`app/services/`):  
  비즈니스 로직(추천, AI 분석 등) 수행
- **CRUD Layer** (`app/crud/`):  
  DB 데이터 조작
- **Models** (`app/models/`):  
  DB 스키마 정의

## 🛠️ 기술 스택 (Tech Stack)

| Category | Technology | Description |
| --- | --- | --- |
| **Framework** | **FastAPI** | 고성능 비동기 Python 웹 프레임워크 |
| **Language** | **Python** | 3.x 버전 사용 |
| **Database** | **PostgreSQL** | ACID 호환 관계형 데이터베이스 |
| **ORM** | **SQLAlchemy** | Python 객체와 DB 테이블 매핑 |
| **AI Model** | **Google Gemini** | 명대사 분석 및 페르소나 생성 |
| **Math** | **NumPy** | 벡터 연산 및 추천 알고리즘 계산 |
