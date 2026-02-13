from typing import List
from google import genai
from domain.news_article import NewsArticle
from config.settings import Settings
from utils.exceptions import AppError

import time

def summarize_news(articles: List[NewsArticle]) -> dict:
    """
    Gemini API를 사용하여 뉴스 기사들의 리스트를 요약하고, 관련 위치 정보와 특이사항을 추출합니다.
    """
    if not articles:
        return {
            "summary": "요약할 기사가 없습니다.",
            "location_name": "알 수 없음",
            "lat": 0.0,
            "lon": 0.0
        }
    
    if not Settings.GEMINI_API_KEY:
        raise AppError("api_key_invalid")
    
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            client = genai.Client(api_key=Settings.GEMINI_API_KEY)
            
            news_list_str = ""
            for i, article in enumerate(articles, 1):
                content_to_analyze = article.raw_content[:2000] if article.raw_content else article.snippet
                news_list_str += f"[{i}] 제목: {article.title}\n    발행일: {article.pub_date}\n    내용: {content_to_analyze}\n\n"
            
            prompt = f"""당신은 전 세계 뉴스를 분석하고 통찰력을 제공하는 전문 뉴스 분석가입니다. 
제공된 {len(articles)}개의 뉴스 데이터를 바탕으로 다음 형식을 엄격히 지켜서 한국어로 응답해주세요.

[SUMMARY]
### 1. 🌐 글로벌 핵심 뉴스 요약
- 각 기사의 핵심 내용을 종합하여 요약하세요.
- 불릿 포인트 형식으로 구성하세요.

### 2. 🗺️ 뉴스 관계 지도 및 연결 고리
- 검색된 결과들 사이의 상관관계나 공통 트렌드를 분석하세요.

### 3. 🛡️ 사고/재난 대응 및 미래 전망
- 문제 해결 방안이나 미래 전망을 제시하세요.

[LOCATIONS]
위 뉴스들이 다루는 사건의 주요 지점들을 모두 식별하여 리스트 형식으로 작성하세요. 
각 지점은 '장소명: 위도, 경도' 형식으로 작성해야 합니다. 
(예: "테헤란: 35.6892, 51.3890 | 이스파한: 32.6546, 51.6680")
실제 사건이 벌어지는 장소나 직접적인 영향권인 대상 지역을 우선적으로 식별하세요.

[IMAGE_QUERY]
위 상황과 위치를 가장 잘 설명할 수 있는 시각적 검색어(영문)를 한 줄로 작성하세요. (예: "Tehran Iran military", "Venezuela economic crisis city view")

[분석할 뉴스 데이터]
{news_list_str}
"""
            
            model_id = Settings.GEMINI_MODEL or "gemini-2.0-flash"
            
            response = client.models.generate_content(
                model=model_id,
                contents=prompt
            )
            
            if not response or not response.text:
                raise AppError("ai_error")
            
            text = response.text.strip()
            
            # 파싱 로직
            summary = ""
            locations = [] # [{name, lat, lon}]
            image_query = ""
            
            if "[SUMMARY]" in text and "[LOCATIONS]" in text:
                parts = text.split("[LOCATIONS]")
                summary = parts[0].replace("[SUMMARY]", "").strip()
                
                rest = parts[1]
                loc_section = rest.split("[IMAGE_QUERY]")[0].strip()
                if "[IMAGE_QUERY]" in rest:
                    image_query = rest.split("[IMAGE_QUERY]")[1].strip()
                
                # 장소 리스트 파싱 (예: "테헤란: 35.6, 51.3 | 이스파한: 32.6, 51.6")
                import re
                loc_entries = loc_section.split("|")
                for entry in loc_entries:
                    try:
                        name_part, coord_part = entry.split(":")
                        name = name_part.strip()
                        nums = re.findall(r"[-+]?\d*\.\d+|\d+", coord_part)
                        if len(nums) >= 2:
                            locations.append({
                                "name": name,
                                "lat": float(nums[0]),
                                "lon": float(nums[1])
                            })
                    except:
                        continue
            else:
                summary = text
                
            return {
                "summary": summary,
                "locations": locations,
                "image_query": image_query
            }

        except Exception as e:
            # ... (error handling remains the same or similar)
            err_msg = str(e).lower()
            if "api key" in err_msg or "invalid" in err_msg:
                raise AppError("gemini_api_key_invalid")
            elif "429" in err_msg or "rate limit" in err_msg:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise AppError("gemini_rate_limit")
            
            if attempt == max_retries - 1:
                raise AppError("ai_error")
            time.sleep(retry_delay)
            
    return {
        "summary": "요약 생성에 실패했습니다.",
        "location_name": "에러",
        "lat": 0.0,
        "lon": 0.0
    }
