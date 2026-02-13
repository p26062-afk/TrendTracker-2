import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Settings:
    """
    프로젝트 설정을 관리하는 클래스입니다.
    환경변수에서 설정을 읽어오며, 필수 설정이 누락된 경우 명확한 에러 메시지를 출력합니다.
    """
    
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    CSV_PATH = os.getenv("CSV_PATH", "data/search_history.csv")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    SEARCH_DOMAINS = os.getenv("SEARCH_DOMAINS", "")

    @classmethod
    def validate_config(cls):
        """필수 환경변수가 설정되어 있는지 확인합니다."""
        missing_vars = []
        if not cls.TAVILY_API_KEY:
            missing_vars.append("TAVILY_API_KEY")
        if not cls.GEMINI_API_KEY:
            missing_vars.append("GEMINI_API_KEY")
        if not cls.CSV_PATH:
            missing_vars.append("CSV_PATH")
            
        if missing_vars:
            error_msg = "\n" + "="*60 + "\n"
            error_msg += "❌ 필수 환경변수가 누락되었습니다!\n\n"
            error_msg += f"누락된 변수: {', '.join(missing_vars)}\n\n"
            error_msg += "설정 방법:\n"
            error_msg += "1. .env.example 파일을 .env로 복사하세요.\n"
            error_msg += "2. .env 파일에 각 API 키를 입력하세요.\n\n"
            error_msg += "API 키 발급 안내:\n"
            error_msg += "- Tavily API (검색): https://tavily.com/\n"
            error_msg += "- Google Gemini API (요약): https://aistudio.google.com/\n"
            error_msg += "="*60 + "\n"
            raise ValueError(error_msg)

# 초기화 시 검증을 하려면 클래스 메서드를 호출하거나 인스턴스화할 때 체크할 수 있습니다.
# 여기서는 가져다 쓰는 곳에서 validate_config()를 호출하거나, 
# 혹은 파일 로드시 바로 체크할 수 있도록 구성할 수 있습니다.
# prompt에서는 'Settings import 성공'을 확인하므로, import 시점에 에러가 나면 테스트가 실패할 수 있습니다.
# 따라서 필요한 시점에 validate_config를 호출하는 것이 좋습니다.
