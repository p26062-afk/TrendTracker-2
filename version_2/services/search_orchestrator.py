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
    
    # 4. AI 요약 및 위치 추출
    locations = []
    ai_summary = ""
    location_name = "알 수 없음"
    lat, lon = 0.0, 0.0
    situation_image_url = ""
    
    if articles:
        ai_data = summarize_news(articles)
        ai_summary = ai_data.get("summary", "")
        locations = ai_data.get("locations", [])
        image_query = ai_data.get("image_query", "")
        
        # 하위 호환성을 위한 대표 위치 설정 (첫 번째 장소)
        if locations:
            location_name = locations[0]["name"]
            lat = locations[0]["lat"]
            lon = locations[0]["lon"]
        
        # 기사 중 이미지가 있는 것들 중 위치 명칭이 포함된 기사의 이미지를 우선 선택
        best_image = ""
        for article in articles:
            if article.image and article.image.startswith("http"):
                # 식별된 장소들 중 하나라도 기사에 언급되어 있는지 확인
                found_loc = False
                for loc in locations:
                    loc_lower = loc["name"].lower()
                    if loc_lower in article.title.lower() or loc_lower in article.snippet.lower():
                        best_image = article.image
                        found_loc = True
                        break
                if found_loc:
                    break
                if not best_image:
                    best_image = article.image
        
        # 만약 기사 자체에 이미지가 하나도 없다면, AI 쿼리를 바탕으로 한 사진 시도
        if not best_image:
            best_image = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1600&q=80"
            if locations:
                best_image = f"https://source.unsplash.com/1600x900/?{locations[0]['name'].replace(' ', ',')},city"
        
        situation_image_url = best_image
    else:
        ai_summary = "뉴스 검색 결과가 없어 요약을 생성할 수 없습니다."
        
    # 5. 결과 객체 생성
    result = SearchResult(
        search_key=search_key,
        search_time=search_time,
        keyword=clean_keyword,
        articles=articles,
        ai_summary=ai_summary,
        location_name=location_name,
        latitude=lat,
        longitude=lon,
        locations=locations,
        situation_image_url=situation_image_url
    )
    
    # 6. 데이터 저장
    save_result(result)
    
    # 7. 결과 반환
    return result
