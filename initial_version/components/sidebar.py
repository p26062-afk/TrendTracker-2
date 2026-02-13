import streamlit as st
from typing import List, Optional
from datetime import datetime

def render_sidebar_header():
    """사이드바 상단 헤더를 렌더링합니다."""
    st.sidebar.title("🚀 initial_version")
    st.sidebar.markdown("키워드로 뉴스를 검색하고 AI가 요약해 드립니다.")
    st.sidebar.divider()

def render_settings() -> int:
    """설정 섹션을 렌더링하고 검색 건수를 반환합니다."""
    st.sidebar.subheader("⚙️ 설정")
    num_results = st.sidebar.slider(
        "검색 건수 설정", 
        min_value=1, 
        max_value=10, 
        value=5,
        help="가져올 뉴스 기사의 개수를 선택하세요."
    )
    return num_results

def render_info():
    """사용법 및 안내 정보를 렌더링합니다."""
    with st.sidebar.expander("ℹ️ 사용법"):
        st.markdown("""
        1. 메인 화면에 **검색어**를 입력합니다.
        2. **검색 버튼**을 클릭합니다.
        3. 최신 뉴스 5~10건을 검색하여 요약합니다.
        4. 과거 기록은 **검색 기록**에서 다시 볼 수 있습니다.
        """)
    
    st.sidebar.markdown("### 📊 API 한도")
    st.sidebar.info("Tavily 무료 플랜: 월 1,000건 검색 가능")
    
    with st.sidebar.expander("💾 데이터 저장 안내"):
        st.write("- 검색 기록은 `data/search_history.csv`에 저장됩니다.")
        st.write("- CSV 파일을 삭제하거나 경로를 변경하면 이전 기록이 사라집니다.")
        st.write("- 중요한 기록은 하단의 CSV 다운로드 기능을 통해 백업하세요.")

def render_history_list(search_keys: List[str], keywords_map: dict) -> Optional[str]:
    """과거 검색 기록 목록을 렌더링하고 선택된 키를 반환합니다."""
    st.sidebar.subheader("📜 검색 기록")
    
    if not search_keys:
        st.sidebar.info("저장된 검색 기록이 없습니다")
        return None
    
    # 표시용 형식: "키워드 (yyyy-mm-dd HH:MM)"
    # search_keys는 "키워드-yyyyMMddHHmm" 형식임
    options = []
    for sk in search_keys:
        display_name = keywords_map.get(sk, sk)
        options.append(display_name)
    
    selected_display = st.sidebar.selectbox(
        "이전 결과 불러오기",
        options=options,
        index=None,
        placeholder="기록을 선택하세요"
    )
    
    if selected_display:
        # display_name에서 search_key를 찾아야 함
        # keywords_map의 역방향 조회가 필요할 수 있음
        for sk, name in keywords_map.items():
            if name == selected_display:
                return sk
    return None

def render_download_button(csv_data: str, is_empty: bool):
    """CSV 다운로드 버튼을 렌더링합니다."""
    st.sidebar.divider()
    curr_date = datetime.now().strftime("%Y%m%d")
    filename = f"trendtracker_export_{curr_date}.csv"
    
    if is_empty:
        st.sidebar.button("📥 CSV 다운로드 (데이터 없음)", disabled=True)
    else:
        st.sidebar.download_button(
            label="📥 CSV 다운로드",
            data=csv_data,
            file_name=filename,
            mime="text/csv"
        )
