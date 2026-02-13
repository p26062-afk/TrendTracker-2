from dataclasses import dataclass

@dataclass
class NewsArticle:
    title: str  # 기사 제목
    url: str    # 기사 URL
    snippet: str # 기사 스니펫
    pub_date: str = "" # 발행일
    raw_content: str = "" # 기사 원문 (AI 분석용)
    image: str = "" # 기사 대표 이미지 URL
