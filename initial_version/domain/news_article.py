from dataclasses import dataclass

@dataclass
class NewsArticle:
    title: str  # 기사 제목
    url: str    # 기사 URL
    snippet: str # 기사 스니펫
    pub_date: str = "" # 발행일
