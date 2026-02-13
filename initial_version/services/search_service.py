from typing import List
from tavily import TavilyClient
from domain.news_article import NewsArticle
from config.settings import Settings
from utils.exceptions import AppError

import time

def search_news(keyword: str, num_results: int = 5) -> List[NewsArticle]:
    """
    Tavily API를 사용하여 뉴스를 검색하고 최신순으로 정렬하여 반환합니다.
    최대 3회 재시도를 시도합니다.
    """
    if not Settings.TAVILY_API_KEY:
        raise AppError("api_key_invalid")
    
    max_retries = 3
    retry_delay = 2 # seconds
    
    for attempt in range(max_retries):
        try:
            client = TavilyClient(api_key=Settings.TAVILY_API_KEY)
            
            # SEARCH_DOMAINS 처리
            include_domains = []
            if Settings.SEARCH_DOMAINS:
                include_domains = [d.strip() for d in Settings.SEARCH_DOMAINS.split(",") if d.strip()]
            
            # 검색 결과 개수 설정
            max_results = max(num_results * 3, 20)
            
            # Tavily 검색 호출
            response = client.search(
                query=keyword,
                search_depth="advanced",
                include_domains=include_domains,
                max_results=max_results,
                topic="news"
            )
            
            results = response.get('results', [])
            if not results:
                return []
            
            # published_date 기준 내림차순 정렬
            sorted_results = sorted(
                results, 
                key=lambda x: x.get('published_date', ''), 
                reverse=True
            )
            
            articles = []
            for res in sorted_results[:num_results]:
                articles.append(NewsArticle(
                    title=res.get('title', ''),
                    url=res.get('url', ''),
                    snippet=res.get('content', ''),
                    pub_date=res.get('published_date', '')
                ))
                
            return articles

        except Exception as e:
            err_msg = str(e).lower()
            
            # 특정 에러 코드 처리
            if "401" in err_msg or "api key" in err_msg:
                raise AppError("api_key_invalid")
            elif "429" in err_msg or "rate limit" in err_msg:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise AppError("tavily_rate_limit")
            elif "400" in err_msg:
                raise AppError("tavily_bad_request")
            elif "500" in err_msg or "503" in err_msg:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise AppError("server_error")
            elif "timeout" in err_msg or "network" in err_msg or "connection" in err_msg:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise AppError("network_error")
            
            # 마지막 시도라면 에러 발생
            if attempt == max_retries - 1:
                raise AppError("network_error")
            time.sleep(retry_delay)
    
    return []
