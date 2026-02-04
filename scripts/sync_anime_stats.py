# -*- coding: utf-8 -*-
import psycopg2
from psycopg2.extras import execute_values
import sys
import os

# 인코딩 문제 방지를 위해 표준 출력 설정 강제 (윈도우용)
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

GENRE_WEIGHTS = {
    "Action": {"story": 3, "art": 9, "char": 4, "music": 6},
    "Drama": {"story": 8, "art": 4, "char": 9, "music": 6},
    "Fantasy": {"story": 6, "art": 8, "char": 5, "music": 6},
    "Mystery": {"story": 10, "art": 4, "char": 6, "music": 5},
    "Adventure": {"story": 6, "art": 7, "char": 6, "music": 6},
    "Supernatural": {"story": 7, "art": 7, "char": 5, "music": 8},
    "Psychological": {"story": 10, "art": 4, "char": 9, "music": 4},
    "Thriller": {"story": 9, "art": 5, "char": 6, "music": 9},
    "Comedy": {"story": 4, "art": 5, "char": 9, "music": 4},
    "Sci-Fi": {"story": 7, "art": 9, "char": 4, "music": 7},
    "Horror": {"story": 6, "art": 6, "char": 4, "music": 10},
    "Romance": {"story": 6, "art": 4, "char": 10, "music": 6},
    "Slice of Life": {"story": 5, "art": 5, "char": 10, "music": 4},
    "Music": {"story": 4, "art": 6, "char": 6, "music": 10},
    "Sports": {"story": 5, "art": 8, "char": 10, "music": 6},
    "Ecchi": {"story": 2, "art": 10, "char": 4, "music": 4},
    "Mecha": {"story": 6, "art": 10, "char": 4, "music": 7},
    "Mahou Shoujo": {"story": 6, "art": 8, "char": 7, "music": 8}
}

def run():
    conn = None
    try:
        # [수정] 연결 옵션에 client_encoding을 아예 포함
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),          
            dbname=os.getenv("POSTGRES_DB"),    
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"), 
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()

        cur.execute("""
            SELECT a.anime_id, a.anilist_id, string_agg(g.genre_name, '|')
            FROM animes a
            LEFT JOIN anime_genre_mapping agm ON a.anime_id = agm.anime_id
            LEFT JOIN genres g ON agm.genre_id = g.genre_id
            GROUP BY a.anime_id, a.anilist_id;
        """)
        rows = cur.fetchall()

        stats_data = []
        for anime_id, anilist_id, genre_str in rows:
            temp_vec = {"story": 0, "art": 0, "char": 0, "music": 0}
            genres = genre_str.split('|') if genre_str else []
            for g in genres:
                if g in GENRE_WEIGHTS:
                    for k in temp_vec: temp_vec[k] += GENRE_WEIGHTS[g][k]
            
            total = sum(temp_vec.values())
            v = {k: round(v/total, 3) if total > 0 else 0.25 for k, v in temp_vec.items()}
            stats_data.append((anilist_id, anime_id, v['story'], v['art'], v['char'], v['music']))

        upsert_sql = """
            INSERT INTO anime_stats (anilist_id, anime_id, avg_story, avg_art, avg_character, avg_music)
            VALUES %s
            ON CONFLICT (anilist_id) DO UPDATE SET
                avg_story = EXCLUDED.avg_story,
                avg_art = EXCLUDED.avg_art,
                avg_character = EXCLUDED.avg_character,
                avg_music = EXCLUDED.avg_music;
        """
        execute_values(cur, upsert_sql, stats_data)
        conn.commit()
        print("✨ 성공! 데이터가 anime_stats에 저장되었습니다.")

    except Exception as e:
        # [수정] 에러 출력 시 인코딩 문제 방지를 위해 repr 사용
        print(f"❌ 에러 상세 정보: {repr(e)}")
    finally:
        if conn is not None: conn.close()

if __name__ == "__main__":
    run()