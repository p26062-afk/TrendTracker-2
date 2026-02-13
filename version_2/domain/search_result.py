from dataclasses import dataclass
from datetime import datetime
from typing import List
import pandas as pd
from .news_article import NewsArticle

@dataclass
class SearchResult:
    search_key: str  # PK, "키워드-yyyymmddhhmm" 형식
    search_time: datetime  # 검색 실행 시간
    keyword: str  # 검색 키워드
    articles: List[NewsArticle]  # 뉴스 기사 리스트
    ai_summary: str  # AI 요약 결과
    location_name: str = "" # 대표 위치 명칭
    latitude: float = 0.0 # 대표 위도
    longitude: float = 0.0 # 대표 경도
    locations: List[dict] = None # [{'name': str, 'lat': float, 'lon': float}] 리스트
    situation_image_url: str = "" # 상황 설명 사진 URL

    def to_dataframe(self) -> pd.DataFrame:
        """
        검색 결과를 CSV 저장을 위해 Long format(기사 1건=1행)으로 변환합니다.
        """
        data = []
        for i, article in enumerate(self.articles, 1):
            import json
            data.append({
                "search_key": self.search_key,
                "search_time": self.search_time,
                "keyword": self.keyword,
                "article_index": i,
                "title": article.title,
                "url": article.url,
                "snippet": article.snippet,
                "article_image": article.image,
                "ai_summary": self.ai_summary,
                "location_name": self.location_name,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "locations": json.dumps(self.locations if self.locations else []),
                "situation_image_url": self.situation_image_url
            })
        return pd.DataFrame(data)
