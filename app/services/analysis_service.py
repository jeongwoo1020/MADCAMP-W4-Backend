from sqlalchemy.orm import Session
from collections import Counter
from datetime import date, datetime, timedelta
from app.crud import record as crud_record
from app.crud import animes as crud_anime

class AnalysisService:
    
    # 1. 요약 정보 API (/api/analysis/summary)
    @staticmethod
    def get_summary(db: Session, user_id: int):
        records = crud_record.get_user_record_data(db, user_id)
        if not records: return {"total_watched_count": 0, "total_reviewed_count": 0, "avg_score": 0, "recent_genres": []}

        scores = [r.score for r in records if r.score is not None]
        
        # 최근 장르 상위 3개 추출 로직
        anime_ids = [r.anime_id for r in records]
        genres = crud_anime.get_genres_by_anime_ids(db, anime_ids)
        top_3_genres = [g[0] for g in Counter([g.genre_name for g in genres]).most_common(3)]

        return {
            "total_watched_count": len(records),
            "total_reviewed_count": len(scores),
            "avg_score": round(sum(scores) / len(scores), 2) if scores else 0.0,
            "recent_genres": top_3_genres
        }

    # 2. 장르 분석 API (/api/analysis/genre) - 상위 4개 + 기타 전략
    @staticmethod
    def get_genre_analysis(db: Session, user_id: int):
        records = crud_record.get_user_record_data(db, user_id)
        anime_ids = [r.anime_id for r in records]
        genres = crud_anime.get_genres_by_anime_ids(db, anime_ids)
        
        genre_counts = Counter([g.genre_name for g in genres])
        total = sum(genre_counts.values())
        
        sorted_genres = genre_counts.most_common()
        top_4 = sorted_genres[:4]
        others_count = sum(count for name, count in sorted_genres[4:])

        distribution = [{"label": name, "value": round((count/total)*100, 1)} for name, count in top_4]
        if others_count > 0:
            distribution.append({"label": "기타", "value": round((others_count/total)*100, 1)})

        # 분석 텍스트 생성 (예시)
        top_names = " / ".join([g[0] for g in top_4[:2]])
        top_percent = round((sum(g[1] for g in top_4[:2]) / total) * 100) if total > 0 else 0
        
        return {
            "genre_distribution": distribution,
            "analysis_text": f"당신은 '{top_names}' 장르에 {top_percent}% 편향되어 있습니다."
        }

    # 3. 시계열 분석 API (/api/analysis/time)
    @staticmethod
    def get_time_metrics(db: Session, user_id: int):
        records = crud_record.get_user_record_data(db, user_id)
        if not records: return None

        # 월별 그룹화 (YYYY-MM)
        monthly_counts = Counter([r.updated_at.strftime("%Y-%m") for r in records])
        timeline = [{"date": m, "count": c} for m, c in sorted(monthly_counts.items())]

        # 가장 활발했던 달
        most_active_month = max(monthly_counts, key=monthly_counts.get)

        # 주간 평균 기록 수 (첫 기록일부터 현재까지의 주차 계산)
        first_date = min(r.updated_at for r in records).date()
        total_weeks = max((date.today() - first_date).days / 7, 1)
        weekly_avg = round(len(records) / total_weeks, 1)

        # 누적 시청 시간 (TVA 평균 24분 가정)
        total_watching_time = len(records) * 24

        # 연속 기록 일수 (Streak)
        active_dates = sorted({r.updated_at.date() for r in records}, reverse=True)
        streak = 0
        curr = date.today()
        if active_dates and active_dates[0] >= curr - timedelta(days=1):
            if active_dates[0] == curr - timedelta(days=1): curr -= timedelta(days=1)
            for d in active_dates:
                if d == curr: streak += 1; curr -= timedelta(days=1)
                else: break

        return {
            "timeline_data": timeline,
            "most_active_month": most_active_month,
            "weekly_avg_records": weekly_avg,
            "total_watching_time": total_watching_time,
            "consecutive_days": streak
        }