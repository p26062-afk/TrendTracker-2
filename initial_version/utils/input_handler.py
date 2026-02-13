from typing import Optional

def preprocess_keyword(raw_input: str) -> Optional[str]:
    """
    검색어를 전처리합니다.
    1. 앞뒤 공백 제거
    2. 최대 100자 제한
    3. 빈 문자열이면 None 반환
    """
    if not raw_input:
        return None
    
    processed = raw_input.strip()
    if not processed:
        return None
    
    return processed[:100]
