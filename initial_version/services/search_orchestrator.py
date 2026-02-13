from datetime import datetime
from domain.search_result import SearchResult
from services.search_service import search_news
from services.ai_service import summarize_news
from repositories.search_repository import save_result
from utils.key_generator import generate_search_key
from utils.input_handler import preprocess_keyword
from utils.exceptions import AppError

def execute_news_search(keyword: str, num_results: int = 5) -> SearchResult:
    """
    뉴스 검색, AI 요약, 데이터 저장을 아우르는 전체 프로세스를 실행합니다.
    """
    # 1. 입력값 전처리
    clean_keyword = preprocess_keyword(keyword)
    if clean_keyword is None:
        raise AppError("empty_input")
    
    # 2. 검색 키 생성
    search_key = generate_search_key(clean_keyword)
    search_time = datetime.now()
    
    # 3. 뉴스 검색
    articles = search_news(clean_keyword, num_results=num_results)
    
    # 4. AI 요약
    if articles:
        ai_summary = summarize_news(articles)
    else:
        ai_summary = "뉴스 검색 결과가 없어 요약을 생성할 수 없습니다."
        
    # 5. 결과 객체 생성
    result = SearchResult(
        search_key=search_key,
        search_time=search_time,
        keyword=clean_keyword,
        articles=articles,
        ai_summary=ai_summary
    )
    
    # 6. 데이터 저장
    save_result(result)
    
    # 7. 결과 반환
    return result
