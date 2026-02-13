from domain.news_article import NewsArticle
from domain.search_result import SearchResult
from repositories.search_repository import save_result, load_results
from datetime import datetime
import os
from config.settings import Settings

# 테스트용 CSV 경로 설정
test_csv = "data/test_history.csv"
Settings.CSV_PATH = test_csv

# 기존 테스트 파일 삭제
if os.path.exists(test_csv):
    os.remove(test_csv)

def test_phase4():
    print("--- Phase 4 테스트 시작 ---")
    
    # 1. 샘플 데이터 생성
    articles = [
        NewsArticle("제목1", "https://news1.com", "내용1"),
        NewsArticle("제목2", "https://news2.com", "내용2")
    ]
    res = SearchResult("테스트-20260211", datetime.now(), "테스트", articles, "AI 요약입니다.")

    # 2. 저장 테스트
    print("데이터 저장 시도...")
    save_result(res)
    if os.path.exists(test_csv):
        print(f"성공: {test_csv} 파일이 생성되었습니다.")
    else:
        print("실패: 파일이 생성되지 않았습니다.")

    # 3. 로드 테스트
    print("데이터 로드 시도...")
    df = load_results()
    print(f"로드된 행 수: {len(df)}")
    print("컬럼 리스트:", df.columns.tolist())
    
    if len(df) == 2 and "article_index" in df.columns:
        print("성공: 데이터가 정상적으로 로드되었습니다.")
    else:
        print("실패: 데이터 로드가 올바르지 않습니다.")

    # 4. 추가 저장 테스트 (Append)
    print("추가 데이터 저장 시도...")
    save_result(res)
    df_new = load_results()
    print(f"추가 후 전체 행 수: {len(df_new)}")
    
    if len(df_new) == 4:
        print("성공: 데이터가 정상적으로 추가(Append)되었습니다.")
    else:
        print("실패: 데이터 추가가 올바르지 않습니다.")

    print("--- Phase 4 테스트 종료 ---")

if __name__ == "__main__":
    test_phase4()
