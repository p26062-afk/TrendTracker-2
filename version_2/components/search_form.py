import streamlit as st
from typing import Optional
from utils.input_handler import preprocess_keyword

def render_search_form() -> Optional[str]:
    """
    키워드 입력을 위한 검색 폼을 렌더링합니다.
    사용자가 검색 버튼을 누르면 전처리된 키워드를 반환합니다.
    """
    with st.container():
        keyword = st.text_input("검색어 입력", placeholder="관심 있는 뉴스 키워드를 입력하세요 (예: AI 트렌드, 삼성전자)")
        col1, col2 = st.columns([1, 4])
        with col1:
            search_button = st.button("🔍 검색", use_container_width=True)
            
        if search_button:
            if not keyword:
                st.warning("검색어를 입력해주세요")
                return None
            
            clean_keyword = preprocess_keyword(keyword)
            if clean_keyword is None:
                st.warning("유효한 검색어를 입력해주세요")
                return None
            
            return clean_keyword
    return None
