import streamlit as st
import pandas as pd
from typing import List
from domain.news_article import NewsArticle

def render_summary(title: str, summary: str):
    """AI 요약 결과를 렌더링합니다."""
    st.subheader(f"✨ {title}")
    st.markdown(summary)
    st.divider()

def render_news_list(articles: List[NewsArticle]):
    """검색된 뉴스 기사 목록을 쾌적한 카드 레이아웃으로 바로 렌더링합니다."""
    st.markdown("### 📰 관련 뉴스 피드")
    
    if not articles:
        st.warning("검색된 기사가 없습니다.")
        return

    for article in articles:
        # 카드 컨테이너 스타일 시뮬레이션
        with st.container():
            st.markdown(f"#### {article.title}")
            
            # 사진을 바로 노출 (링크 형태가 아닌 시각적 요소로)
            if article.image:
                st.image(article.image, use_container_width=True)
                
            if article.pub_date:
                st.caption(f"📅 **발행일:** {article.pub_date}")
            
            st.write(article.snippet)
            st.markdown(f"[🔗 기사 원문 보기]({article.url})")
            st.write("---")

import pydeck as pdk

def render_location_map(locations: List[dict]):
    """여러 위치 정보를 하이라이트된 프리미엄 지도로 표시합니다."""
    if not locations or len(locations) == 0:
        st.info("💡 정확한 위치 좌표를 분석 중이거나 찾을 수 없습니다.")
        return

    # 데이터프레임 생성
    df_list = []
    for loc in locations:
        df_list.append({
            'name': loc['name'],
            'lat': loc['lat'],
            'lon': loc['lon']
        })
    map_data = pd.DataFrame(df_list)
    
    # 지도 제목 (장소 나열)
    names = ", ".join([loc['name'] for loc in locations])
    st.markdown(f"### 📍 주요 지역: {names}")
    
    # 평균 좌표로 초기 중심점 설정
    avg_lat = map_data['lat'].mean()
    avg_lon = map_data['lon'].mean()
    
    # Pydeck 설정
    view_state = pdk.ViewState(
        latitude=avg_lat,
        longitude=avg_lon,
        zoom=3,
        pitch=45,
    )
    
    # 멀티 마커 레이어 (그린)
    center_layer = pdk.Layer(
        "ScatterplotLayer",
        map_data,
        get_position='[lon, lat]',
        get_color='[34, 197, 94, 200]',
        get_radius=80000,
        radius_min_pixels=8,
        radius_max_pixels=15,
        pickable=True,
    )
    
    # 파동 효과 레이어
    pulse_layer = pdk.Layer(
        "ScatterplotLayer",
        map_data,
        get_position='[lon, lat]',
        get_color='[74, 222, 128, 100]',
        get_radius=200000,
        radius_min_pixels=15,
        radius_max_pixels=40,
    )

    r = pdk.Deck(
        map_style='light',
        initial_view_state=view_state,
        layers=[pulse_layer, center_layer],
        tooltip={"text": "{name}"}
    )
    
    st.pydeck_chart(r)

def render_situation_picture(image_url: str, keyword: str, location_name: str = ""):
    """상황을 설명하는 사진(Picture)을 클릭 과정 없이 바로 표시합니다."""
    st.markdown("### 📸 상황 사진 (Picture)")
    
    # 1. 고해상도 기본 뉴스 사진 배경 (최후의 보루)
    final_fallback = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1600&q=80"
    
    # 2. 이미지 URL 결정
    display_url = image_url if image_url and image_url.startswith("http") else final_fallback
    
    # 3. 사진 렌더링
    try:
        st.image(display_url, caption=f"'{keyword}' 관련 상황 분석 사진", use_container_width=True)
    except Exception:
        # 렌더링 실패 시 최후의 보루 이미지로 재시도
        st.image(final_fallback, caption="상황 관련 시각 정보 (기본)", use_container_width=True)
    
    # 4. 부가 정보 (위치 정보와 이미지의 연결성 강조)
    if location_name and location_name != "알 수 없음":
        st.caption(f"📍 위치 기반 시각화: {location_name}")
