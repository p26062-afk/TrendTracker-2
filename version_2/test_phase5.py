from services.search_orchestrator import execute_news_search
from utils.exceptions import AppError
import os
from config.settings import Settings

def test_phase5():
    print("--- Phase 5 테스트 시작 ---")
    
    # 1. 빈 키워드 테스트
    print("빈 키워드 테스트...")
    try:
        execute_news_search("")
        print("실패: AppError가 발생해야 합니다.")
    except AppError as e:
        if e.error_type == "empty_input":
            print("성공: empty_input 에러가 정상적으로 발생했습니다.")
        else:
            print(f"실패: 예상치 못한 에러 타입: {e.error_type}")
    
    # 2. 임포트 확인 (이미 상단에서 확인됨)
    print("성공: search_orchestrator 상단 임포트 확인됨")

    print("--- Phase 5 테스트 종료 ---")

if __name__ == "__main__":
    test_phase5()
