import pandas as pd
import os
from domain.search_result import SearchResult
from config.settings import Settings
from utils.exceptions import AppError

def save_result(result: SearchResult) -> bool:
    """
    검색 결과를 CSV 파일에 저장합니다. 
    파일이 존재하지 않으면 헤더를 포함하여 생성하고, 존재하면 데이터를 추가합니다.
    """
    try:
        df = result.to_dataframe()
        
        # 디렉토리가 없으면 생성
        directory = os.path.dirname(Settings.CSV_PATH)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # 파일 존재 여부에 따라 헤더 포함 여부 결정
        file_exists = os.path.isfile(Settings.CSV_PATH)
        
        df.to_csv(
            Settings.CSV_PATH,
            mode='a',
            header=not file_exists,
            index=False,
            encoding='utf-8-sig'
        )
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        raise AppError("file_error")

def load_results() -> pd.DataFrame:
    """
    CSV 파일에서 이전 검색 기록을 불러옵니다.
    """
    # 명세된 컬럼 구조
    columns = [
        "search_key", "search_time", "keyword", "article_index",
        "title", "url", "snippet", "ai_summary",
        "location_name", "latitude", "longitude", "situation_image_url"
    ]
    
    if not os.path.exists(Settings.CSV_PATH):
        return pd.DataFrame(columns=columns)
    
    try:
        df = pd.read_csv(Settings.CSV_PATH, encoding='utf-8-sig')
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        raise AppError("file_error")

def get_all_keys() -> list[str]:
    """저장된 모든 고유 검색 키(search_key)를 반환합니다."""
    df = load_results()
    if df.empty:
        return []
    # 최신순으로 반환하기 위해 역순 정렬 (보통 아래에 추가되므로)
    return df['search_key'].unique().tolist()[::-1]

def get_all_as_csv() -> str:
    """전체 데이터를 CSV 문자열로 반환합니다."""
    if not os.path.exists(Settings.CSV_PATH):
        return ""
    with open(Settings.CSV_PATH, "r", encoding="utf-8-sig") as f:
        return f.read()

def find_by_key(search_key: str) -> SearchResult:
    """특정 키에 해당하는 검색 결과를 찾아 SearchResult 객체로 반환합니다."""
    from domain.news_article import NewsArticle
    
    df = load_results()
    rows = df[df['search_key'] == search_key]
    
    if rows.empty:
        raise AppError("file_error")
    
    first_row = rows.iloc[0]
    articles = []
    
    for _, row in rows.iterrows():
        articles.append(NewsArticle(
            title=row.get('title', ''),
            url=row.get('url', ''),
            snippet=row.get('snippet', ''),
            pub_date=row.get('pub_date', ''),
            image=row.get('article_image', '')
        ))
        
    import json
    return SearchResult(
        search_key=first_row['search_key'],
        search_time=pd.to_datetime(first_row['search_time']),
        keyword=first_row['keyword'],
        articles=articles,
        ai_summary=first_row.get('ai_summary', ''),
        location_name=first_row.get('location_name', '알 수 없음'),
        latitude=float(first_row.get('latitude', 0.0)),
        longitude=float(first_row.get('longitude', 0.0)),
        locations=json.loads(first_row.get('locations', '[]')),
        situation_image_url=first_row.get('situation_image_url', '')
    )
