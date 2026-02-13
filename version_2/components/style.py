import streamlit as st

def apply_custom_style():
    """앱 전반에 화이트 바탕, 블랙 글자의 프리미엄 라이트 테마를 적용합니다."""
    st.markdown("""
        <style>
        /* 메인 배경 및 기본 텍스트 스타일 */
        .stApp {
            background-color: #ffffff !important;
            color: #1e293b !important;
        }
        
        /* 텍스트 색상 강제 지정 */
        .stMarkdown, p, span, label {
            color: #1e293b !important;
        }
        
        /* 제목 스타일: 선명한 블랙 그라데이션 */
        h1, h2, h3 {
            background: linear-gradient(90deg, #0f172a, #334155);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
        }
        
        /* 카드 및 Expander 스타일: 깔끔한 화이트 카드 */
        .streamlit-expanderHeader {
            background-color: #f8fafc !important;
            border-radius: 12px !important;
            border: 1px solid #e2e8f0 !important;
            color: #2563eb !important; /* 액센트 블루 */
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
            margin-bottom: 10px !important;
        }
        
        .streamlit-expanderContent {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-top: none !important;
            border-radius: 0 0 12px 12px !important;
        }
        
        /* 버튼 스타일: 전문적인 블루 그라데이션 */
        .stButton>button {
            background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.6rem 2.4rem !important;
            font-weight: 700 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2) !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 12px rgba(37, 99, 235, 0.3) !important;
        }
        
        /* 사이드바 스타일: 차분한 그레이/화이트 */
        [data-testid="stSidebar"] {
            background-color: #f1f5f9 !important;
            border-right: 1px solid #e2e8f0 !important;
        }
        
        /* 입력창 스타일 */
        .stTextInput>div>div>input {
            background-color: #ffffff !important;
            color: #1e293b !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px !important;
        }
        
        /* 알림/정보 박스 스타일 */
        .stAlert {
            background-color: #f8fafc !important;
            border: 1px solid #3b82f6 !important;
            border-radius: 12px !important;
            color: #1e293b !important;
        }
        
        /* 구분선 */
        hr {
            border-top: 1px solid #e2e8f0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
