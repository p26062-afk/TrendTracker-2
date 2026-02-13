# 🗞️ 실시간 뉴스 트렌드 분석기 (Trend Tracker)

키워드로 최신 뉴스를 검색하고, AI(Gemini)를 통해 핵심 내용을 자동으로 요약해주는 사이드 프로젝트용 웹 애플리케이션입니다.

## 🚀 주요 기능

- **실시간 뉴스 검색**: Tavily API를 사용하여 전 세계 언론사의 고품질 뉴스 데이터를 검색합니다.
- **AI 멀티 뉴스 요약**: 여러 뉴스 기사들의 내용을 취합하여 핵심만 한국어로 요약해줍니다.
- **히스토리 관리**: 과거 검색했던 내역을 로컬 CSV 파일로 저장하고 언제든지 다시 조회할 수 있습니다.
- **데이터 익스포트**: 전체 검색 기록을 CSV 파일로 다운로드할 수 있습니다.

## 🛠️ 기술 스택

- **UI/Framework**: Streamlit
- **Search API**: Tavily API
- **AI Model**: Google Gemini 2.0 Flash
- **Data Management**: Pandas, CSV
- **Package Manager**: uv

## 📦 설치 및 실행 방법

### 1. 전제 조건 (uv 설치)

본 프로젝트는 초고속 파이썬 패키지 관리자인 `uv`를 사용합니다.

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 의존성 설치

프로젝트 루트 폴더에서 다음 명령어를 실행하여 가상환경 및 패키지를 설치합니다.

```bash
uv sync
```

### 3. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 본인의 API 키를 입력합니다.

```bash
cp .env.example .env
```

**`.env` 파일 필수 입력 항목:**
- `TAVILY_API_KEY`: [Tavily 공식 홈페이지](https://tavily.com/)에서 발급
- `GEMINI_API_KEY`: [Google AI Studio](https://aistudio.google.com/)에서 발급

### 4. 앱 실행

```bash
uv run streamlit run app.py
```

## 📁 폴더 구조

```text
initial_version/
├── app.py                      # 메인 Streamlit 어플리케이션
├── config/
│   └── settings.py             # 환경 설정 및 검증 로직
├── domain/
│   ├── news_article.py         # 뉴스 기사 데이터 모델
│   └── search_result.py        # 검색 결과 데이터 모델
├── services/
│   ├── search_service.py       # Tavily API 연동 서비스
│   ├── ai_service.py           # Gemini API 연동 서비스
│   └── search_orchestrator.py  # 전체 비즈니스 로직 연동
├── repositories/
│   └── search_repository.py    # CSV 데이터 영구 저장소
├── components/                 # UI 개별 컴포넌트 (사이드바, 결과창 등)
├── utils/                      # 공통 유틸리티 (에러 핸들러, 전처리 등)
└── data/                       # 검색 기록이 저장되는 폴더
```

## ⚠️ 주의 사항

- **API 한도**: Tavily와 Gemini 무료 플랜은 각각 월간/분당 호출 제한이 있습니다. 에러 발생 시 안내 메시지를 확인해주세요.
- **데이터 보안**: `data/search_history.csv` 파일은 로컬에 저장되므로, 파일을 삭제하면 과거 기록이 모두 삭제됩니다.

## 🚫 라이선스

본 프로젝트의 Git 및 GitHub 관련 작업은 일절 금지되어 있습니다. (내부 개발 규정)
