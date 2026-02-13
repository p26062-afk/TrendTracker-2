import streamlit as st
from contextlib import contextmanager

@contextmanager
def show_loading(message: str = "뉴스를 검색하고 있습니다..."):
    """
    로딩 상태(spinner)를 표시하는 context manager입니다.
    
    사용 예시:
    with show_loading("데이터를 분석 중입니다..."):
        perform_task()
    """
    with st.spinner(message):
        yield
