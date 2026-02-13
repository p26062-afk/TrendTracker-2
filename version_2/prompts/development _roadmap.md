# TrendTracker-2 Development Roadmap

## 🚀 현황 (Current Progress)
- **Phase 1~6 완료**: 기본 검색, AI 요약, 히스토리 관리, UI 통합 완료.
- **글로벌 상황 시각화 (Global Trend Visualization) 도입**:
    - 뉴스 데이터 기반 위치(Location) 자동 추출 및 지도(Map) 표시 기능 추가.
    - 트렌드 관련 상황을 직관적으로 이해할 수 있는 상황 사진(Situation Picture) 기능 추가.
    - 메인 결과 화면을 2단 구조(좌: 요약/뉴스, 우: 지도/상황)로 개편하여 정보 밀도 향상.

## 🛠 주요 업데이트 사항 (version_2.1)
1. **프리미엄 지리 시각화**: Pydeck을 도입하여 단순 지도를 넘어 **컬러풀한 하이라이트 레이어(Glowing Marker)**와 **입체적 각도(3D Pitch)**를 적용한 프리미엄 대시보드 맵 구현.
2. **상황 사진(Picture) 매칭**: 검색 결과 이미지 중 가장 적합한 사진을 상단 프리뷰로 노출하여 'Situation'에 대한 시각적 보조 강화.
3. **데이터 모델 확장**: `location_name`, `latitude`, `longitude`, `situation_image_url` 필드를 추가하여 과거 기록 조회 시에도 동일한 시각적 경험 제공.

## 📅 향후 계획 (Future Roadmap)
- **실시간 알림 기능**: 특정 키워드 트렌드 발생 시 알림 시스템 구축.
- **감성 분석 (Sentiment Analysis)**: 뉴스 트렌드에 대한 대중의 긍정/부정 평가 지표 추가.
- **멀티 모델 지원**: Gemini 외에 Claude, GPT-4 등 다양한 LLM 선택 옵션 제공.
- **모바일 최적화**: Streamlit 레이아웃 최적화를 통한 모바일 접근성 향상.
