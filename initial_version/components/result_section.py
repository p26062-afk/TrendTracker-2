import streamlit as st
from typing import List
from domain.news_article import NewsArticle

def render_summary(title: str, summary: str):
    """AI 요약 결과를 렌더링합니다."""
    st.subheader(f"✨ {title}")
    st.info(summary)

def render_news_list(articles: List[NewsArticle]):
    """검색된 뉴스 기사 목록을 렌더링합니다."""
    st.markdown("### 📰 관련 뉴스 기사")
    
    if not articles:
        st.warning("검색된 기사가 없습니다.")
        return

    for article in articles:
        # expander 제목: 제목 + (발행일)
        expander_title = article.title
        if article.pub_date:
            expander_title += f" ({article.pub_date})"
            
        with st.expander(expander_title):
            if article.pub_date:
                st.write(f"📅 **발행일:** {article.pub_date}")
            
            st.write(article.snippet)
            st.markdown(f"[🔗 기사 보기]({article.url})")
