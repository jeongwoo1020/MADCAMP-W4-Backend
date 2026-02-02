from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from collections import Counter
from datetime import date, timedelta

from app.models.record import UserReview
from app.crud import record as crud_record
from app.crud import animes as crud_anime
from app.crud import analysis as crud_analysis

class AnalysisService:
    # --- [Private: 집계 전용 로직] ---
    
    @staticmethod
    def _calculate_preference_vector(records):
        """별점 가중치 계산 (Story, Art 등)"""
        fields = ["score_story", "score_character", "score_art", "score_music"]
        avg_scores = {f: 0.0 for f in fields}
        count = 0
        for r in records:
            if any(getattr(r, f) is not None for f in fields):
                for f in fields:
                    avg_scores[f] += (getattr(r, f) or 0)
                count += 1
        if count > 0:
            for f in fields: avg_scores[f] /= count
            total = sum(avg_scores.values())
            return {k: round(v / total, 2) for k, v in avg_scores.items()} if total > 0 else {k: 0.25 for k in fields}
        return {k: 0.25 for k in fields}

    @staticmethod
    def _calculate_genre_data(genres):
        """전체 장르 분포 및 페르소나 계산"""
        counts = Counter([g.genre_name for g in genres])
        total = sum(counts.values())
        dist = [{"label": n, "value": round((c/total)*100, 1)} for n, c in counts.most_common(5)] if total > 0 else []
        top_2 = [g[0] for g in counts.most_common(2)]
        persona = f"{' / '.join(top_2)} 중심의 덕후" if top_2 else "취향 분석 중"
        return dist, persona

    @staticmethod
    def _calculate_time_metrics(records):
        """시계열 지표 계산"""
        if not records:
            return {
                "timeline_data": [],
                "most_active_month": "기록 없음",
                "weekly_avg_records": 0.0,
                "total_watching_time": 0,
                "consecutive_days": 0
            }
        
        monthly = Counter([r.updated_at.strftime("%Y-%m") for r in records])
        most_active = monthly.most_common(1)[0][0] if monthly else "정보 없음"
        week_keys = {r.updated_at.strftime("%Y-%U") for r in records}
        weekly_avg = round(len(records) / len(week_keys), 1) if week_keys else 0.0
        
        active_dates = sorted({r.updated_at.date() for r in records}, reverse=True)
        streak, curr = 0, date.today()
        for d in active_dates:
            if d == curr: streak += 1; curr -= timedelta(days=1)
            elif d > curr: continue
            else: break
        return {
            "timeline_data": [{"date": m, "count": c} for m, c in sorted(monthly.items())],
            "most_active_month": most_active,
            "weekly_avg_records": weekly_avg,
            "total_watching_time": len(records) * 24,
            "consecutive_days": streak
        }

    # --- [Public: API 엔드포인트 로직] ---

    @staticmethod
    def sync_user_insight(db: Session, user_id: int):
        """리뷰 작성 시 무거운 분석 데이터를 DB에 보관 (Write Path)"""
        records = crud_record.get_user_records(db, user_id=user_id, limit=1000)
        if not records: return None
        
        genres = crud_anime.get_genres_by_anime_ids(db, [r.anime_id for r in records])
        
        pref_vector = AnalysisService._calculate_preference_vector(records)
        genre_dist, persona = AnalysisService._calculate_genre_data(genres)
        time_data = AnalysisService._calculate_time_metrics(records)
        
        insight_data = {
            "top_genres": genre_dist,
            "preference_vector": pref_vector, # 장르 분석에서 쓸 예정
            "persona_text": persona,
            "time_metrics": time_data
        }
        crud_analysis.upsert_user_insight(db, user_id, insight_data)

    @staticmethod    
    def get_summary(db: Session, user_id: int):
        """[Summary API] 실시간 가벼운 통계 정보만 반환"""
        stats = crud_record.get_summary_stats(db, user_id)
        
        # 최근 10개 기록에서 장르 3개 추출 (실시간성 반영)
        recent_records = db.query(UserReview.anime_id)\
            .filter(UserReview.user_id == user_id)\
            .order_by(desc(UserReview.updated_at))\
            .limit(10).all()
        
        recent_genres = []
        if recent_records:
            recent_ids = [r[0] for r in recent_records]
            genre_objs = crud_anime.get_genres_by_anime_ids(db, recent_ids)
            recent_genres = [g[0] for g in Counter([g.genre_name for g in genre_objs]).most_common(3)]
        
        return {
            "total_watched_count": stats[0] or 0,
            "total_reviewed_count": stats[2] or 0,
            "avg_score": round(float(stats[1]), 2) if stats[1] else 0.0,
            "recent_genres": recent_genres
        }
        
    @staticmethod
    def get_genre_analysis(db: Session, user_id: int):
        """[Genre API] 저장된 분포 + 페르소나 + 취향 가중치 벡터 합쳐서 반환"""
        insight = crud_analysis.get_user_insight(db, user_id)
        return {
            "genre_distribution": insight.top_genres if insight else [], 
            "analysis_text": insight.persona_text if insight else ""
        }
        
    @staticmethod
    def get_preference_analysis(db: Session, user_id: int):
        """[취향 API] 저장된 별점 가중치 벡터"""
        insight = crud_analysis.get_user_insight(db, user_id)
        return insight.preference_vector if (insight and insight.preference_vector) else {}

    @staticmethod
    def get_time_analysis(db: Session, user_id: int):
        """[Time API] 저장된 시계열 데이터 반환"""
        insight = crud_analysis.get_user_insight(db, user_id)
        if not insight or not insight.time_metrics:
            return {
                "timeline_data": [],
                "most_active_month": "기록 없음",
                "weekly_avg_records": 0.0,
                "total_watching_time": 0,
                "consecutive_days": 0
            }
        
        return insight.time_metrics