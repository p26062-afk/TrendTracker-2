from datetime import datetime

def generate_search_key(keyword: str) -> str:
    """
    "키워드-yyyymmddhhmm" 형식의 검색 키워드를 생성합니다.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M")
    return f"{keyword}-{timestamp}"
