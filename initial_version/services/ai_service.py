from typing import List
from google import genai
from domain.news_article import NewsArticle
from config.settings import Settings
from utils.exceptions import AppError

import time

def summarize_news(articles: List[NewsArticle]) -> str:
    """
    Gemini API를 사용하여 뉴스 기사들의 리스트를 요약합니다.
    최대 3회 재시도를 시도합니다.
    """
    if not articles:
        return "요약할 기사가 없습니다."
    
    if not Settings.GEMINI_API_KEY:
        raise AppError("api_key_invalid")
    
    max_retries = 3
    retry_delay = 5 # Gemini rate limit is more sensitive, wait longer
    
    for attempt in range(max_retries):
        try:
            client = genai.Client(api_key=Settings.GEMINI_API_KEY)
            
            # 뉴스 목록 구성
            news_list_str = ""
            for i, article in enumerate(articles, 1):
                news_list_str += f"{i}. 제목: {article.title}\n   내용: {article.snippet}\n\n"
            
            # 프롬프트 구성
            prompt = f"""다음 뉴스 기사들의 핵심 내용을 한국어로 요약해주세요:
- 불릿 포인트 형식으로 최대 5개 항목
- 각 항목은 1~2문장

[뉴스 목록]
{news_list_str}
"""
            
            # 모델명 설정
            model_id = Settings.GEMINI_MODEL or "gemini-2.5-flash"
            
            # Gemini 호출
            response = client.models.generate_content(
                model=model_id,
                contents=prompt
            )
            
            if not response or not response.text:
                raise AppError("ai_error")
                
            return response.text.strip()

        except Exception as e:
            err_msg = str(e).lower()
            if "api key" in err_msg or "invalid" in err_msg:
                raise AppError("gemini_api_key_invalid")
            elif "429" in err_msg or "rate limit" in err_msg:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                raise AppError("gemini_rate_limit")
            elif "400" in err_msg:
                raise AppError("gemini_bad_request")
            
            if attempt == max_retries - 1:
                raise AppError("ai_error")
            time.sleep(retry_delay)
            
    return "요약 생성에 실패했습니다."
