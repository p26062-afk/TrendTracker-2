from services.search_service import search_news
from utils.exceptions import AppError
import os
from config.settings import Settings

# API 키가 없는 상태에서 테스트
Settings.TAVILY_API_KEY = ""
try:
    search_news("test")
except AppError as e:
    print(f"Caught expected AppError: {e.error_type}")
except Exception as e:
    print(f"Caught unexpected error: {type(e).__name__}: {e}")
