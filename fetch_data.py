# AniList API에서 데이터를 수집하기 위한 script

import requests
import psycopg
import re
from datetime import date
import os
from dotenv import load_dotenv

# .env 파일을 읽어옵니다.
load_dotenv()

def get_connection():
    # os.getenv(변수명, 기본값)을 사용합니다.
    return psycopg.connect(
        host=os.getenv("DB_HOST"),          
        dbname=os.getenv("POSTGRES_DB"),    
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"), 
        port=os.getenv("DB_PORT")
    )

# 한글 제목 추출용 함수
def extract_korean_title(synonyms):
    hangul = re.compile('[ㄱ-ㅣ가-힣]+')
    for s in synonyms:
        if hangul.search(s):
            return s
    return None

# dsecription의 HTML 태그 제거 정규식 전처리 함수
def clean_description(raw_html):
    if not raw_html: return ""
    clean_re = re.compile('<.*?>')
    return re.sub(clean_re, '', raw_html)

# 날짜 형식 전처리 함수
def format_date(d_obj):
    if not d_obj or not d_obj.get('year'):
        return None
    try:
        # 월/일이 없는 경우 1월 1일로 기본값 설정
        return date(d_obj['year'], d_obj.get('month') or 1, d_obj.get('day') or 1)
    except ValueError:
        return None

# AniList GraphQL 쿼리 - 인기/평점 순 정렬하여 500개 추출
QUERY = '''
query ($page: Int, $perPage: Int) {
  Page (page: $page, perPage: $perPage) {
    media (type: ANIME,sort: [POPULARITY_DESC, SCORE_DESC]) {
      id
      title { romaji english native }
      synonyms
      coverImage { extraLarge }
      description
      startDate { year month day }
      endDate { year month day }
      genres
    }
  }
}
'''

def fetch_and_insert():
    conn = get_connection()
    cur = conn.cursor()
    
    print("🚀 데이터 수집 및 적재 시작...")
    
    # 500개를 위해 10페이지 수집 (페이지당 50개)
    for page in range(1, 11):
        response = requests.post('https://graphql.anilist.co', 
                                 json={'query': QUERY, 'variables': {'page': page, 'perPage': 50}})
        
        if response.status_code != 200:
            print(f"❌ API 에러 (Page {page}): {response.status_code}")
            continue
            
        data = response.json()['data']['Page']['media']

        for anime in data:
            # 0. API response 전처리 
            cleaned_desc = clean_description(anime['description'])
            start_date = format_date(anime['startDate']) # <-- 'start_date'로 만듦
            end_date = format_date(anime['endDate'])     # <-- 'end_date'로 만듦

            # 1. animes 테이블 저장 (Upsert)
            cur.execute("""
                INSERT INTO animes (anilist_id, title_en, image_url, description, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (anilist_id) DO UPDATE SET
                    title_en = EXCLUDED.title_en,
                    image_url = EXCLUDED.image_url,
                    description = EXCLUDED.description
                RETURNING anime_id;
            """, (
                anime['id'], 
                anime['title']['english'] or anime['title']['romaji'], 
                anime['coverImage']['extraLarge'], 
                cleaned_desc, 
                start_date,    
                end_date      
            ))
            
            anime_db_id = cur.fetchone()[0]

            # 2. 한국어 제목 저장
            ko_title = extract_korean_title(anime['synonyms']) or anime['title']['native']
            if ko_title:
                cur.execute("""
                    INSERT INTO anime_korean_titles (anime_id, title_kr) 
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING;
                """, (anime_db_id, ko_title))

            # 3. 장르 저장 및 매핑
            for g_name in anime['genres']:
                cur.execute("INSERT INTO genres (genre_name) VALUES (%s) ON CONFLICT (genre_name) DO NOTHING", (g_name,))
                cur.execute("SELECT genre_id FROM genres WHERE genre_name = %s", (g_name,))
                genre_id = cur.fetchone()[0]
                cur.execute("""
                    INSERT INTO anime_genre_mapping (anime_id, genre_id) 
                    VALUES (%s, %s) ON CONFLICT DO NOTHING
                """, (anime_db_id, genre_id))

        conn.commit()
        print(f"✅ Page {page} 완료 (현재 {page * 50}개 적재 중)")

    cur.close()
    conn.close()
    print("✨ 모든 데이터 수집 및 적재가 완료되었습니다!")

if __name__ == "__main__":
    fetch_and_insert()