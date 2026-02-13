import streamlit as st
import pandas as pd
from datetime import datetime

from config.settings import Settings
from services.search_orchestrator import execute_news_search
from repositories import search_repository as repo
from components.search_form import render_search_form
from components.sidebar import (
    render_sidebar_header, render_settings, render_info, 
    render_history_list, render_download_button
)
from components.result_section import render_summary, render_news_list
from components.loading import show_loading
from utils.error_handler import handle_error
from utils.exceptions import AppError

# 0. 환경 변수 검증
try:
    Settings.validate_config()
except ValueError as e:
    st.error(str(e))
    st.stop()

# 페이지 설정
st.set_page_config(page_title="initial_version", layout="wide", page_icon="🚀")

# 1. 초기화 및 세션 상태 관리
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "new_search" # "new_search" | "history"

if "last_result" not in st.session_state:
    st.session_state.last_result = None

def main():
    """
    Streamlit 앱의 메인 엔트리 포인트입니다.
    사이드바와 메인 영역을 렌더링하고 사용자 입력을 처리합니다.
    """
    # 시각적 피드백: 사이드바 렌더링
    render_sidebar_header()
    num_results = render_settings()
    render_info()
    
    # 저장된 기록 가져오기
    try:
        search_keys = repo.get_all_keys()
    except Exception:
        search_keys = []
    
    # keywords_map 생성
    keywords_map = {}
    for sk in search_keys:
        try:
            parts = sk.rsplit("-", 1)
            keyword = parts[0]
            ts = parts[1]
            dt = datetime.strptime(ts, "%Y%m%d%H%M")
            display_name = f"{keyword} ({dt.strftime('%Y-%m-%d %H:%M')})"
            keywords_map[sk] = display_name
        except Exception:
            keywords_map[sk] = sk

    # 기록 리스트 렌더링
    selected_key = render_history_list(search_keys, keywords_map)
    
    # CSV 다운로드 버튼
    csv_data = repo.get_all_as_csv()
    render_download_button(csv_data, len(search_keys) == 0)

    # 2. 메인 영역 처리
    st.title("🗞️ 실시간 뉴스 트렌드 분석기")
    
    # 기록이 선택되면 모드 전환
    if selected_key:
        st.session_state.current_mode = "history"
        try:
            st.session_state.last_result = repo.find_by_key(selected_key)
        except AppError as e:
            handle_error(e.error_type)
    
    # 새 검색 폼
    keyword_input = render_search_form()
    
    if keyword_input:
        st.session_state.current_mode = "new_search"
        try:
            with show_loading("🔍 뉴스를 검색하고 있습니다..."):
                result = execute_news_search(keyword_input, num_results=num_results)
                st.session_state.last_result = result
            
            if result.articles:
                st.success(f"🎉 '{keyword_input}' 검색 완료! {len(result.articles)}건의 뉴스를 찾았습니다.")
            else:
                st.info(f"💡 '{keyword_input}'에 대한 검색 결과가 없습니다.")
            
        except AppError as e:
            handle_error(e.error_type)
        except Exception as e:
            st.error(f"알 수 없는 오류가 발생했습니다: {str(e)}")

    # 3. 결과 표시 영역
    if st.session_state.last_result:
        res = st.session_state.last_result
        
        if st.session_state.current_mode == "new_search":
            title_prefix = f"'{res.keyword}' 키워드 분석 결과"
        else:
            title_prefix = f"과거 기록: {res.keyword}"
            
        render_summary(title_prefix, res.ai_summary)
        render_news_list(res.articles)
    else:
        # 초기 화면 안내
        st.write("---")
        if not search_keys:
            st.info("👋 환영합니다! 아직 검색 기록이 없습니다. 키워드를 입력해 첫 검색을 시작해보세요!")
        else:
            st.info("💡 왼쪽 검색창에 키워드를 입력하여 최신 뉴스를 확인하거나, 사이드바에서 과거 기록을 선택하세요.")
        
        st.markdown("""
        ### 🚀 주요 기능
        - **최신 뉴스 검색**: Tavily API를 사용하여 신뢰할 수 있는 언론사의 최신 뉴스를 가져옵니다.
        - **AI 핵심 요약**: Google Gemini (Llama 등 지원 가능)를 통해 복잡한 내용을 간결하게 요약해드립니다.
        - **히스토리 관리**: 모든 검색 결과는 로컬 CSV 파일에 안전하게 저장되며 언제든 다시 볼 수 있습니다.
        """)
        st.image("https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=2070&auto=format&fit=crop", caption="Trends via Unsplash")

if __name__ == "__main__":
    main()
