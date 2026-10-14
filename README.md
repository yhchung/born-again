# 다시 태어난다면 · Born Again

2005년 세계 출생아 중 한 명으로 태어나는 한국어 확률 시뮬레이션.

- 공개 URL: https://yhchung.github.io/born-again/
- 서버·계정·API 키 없이 실행하는 정적 HTML/CSS/JS.
- `data.json`: 217개 국가·지역의 WDI 공개 통계. 국가별 2005년 인구 × 조출생률로 출생 가중치 계산.
- 다른 지표는 2000~2010년 범위에서 2005년 최근접 연도. 결측을 임의 국가 평균으로 채우지 않음.
- 소득 5분위 균등 추첨, 도시인구 비율 대리 사용, 생활 항목 독립 추첨. 실제 결합분포나 개인 미래 예측이 아님. 도시별 통계가 없으므로 도시명은 생성하지 않음.
- 소득 점유율/20은 해당 소득집단 평균의 국가 평균 대비 배수. GDP를 개인 소득으로 쓰지 않음.
- 초등 순취학률은 당시 아동의 여건을 보여주는 대리지표이며 2005년생의 실제 학령기 결과가 아님.
- URL hash의 32비트 seed로 동일 결과 재현. 데이터셋/모형 변경 시 결과가 달라질 수 있음.

## 실행과 검증

```sh
/usr/bin/python3 -m http.server 8765 --bind 127.0.0.1
node scripts/test.mjs
/usr/bin/python3 scripts/fetch_data.py
```

`fetch_data.py`는 World Bank API에 접속하고 원자료를 비추적 `data/`에 저장한 뒤 `data.json`을 갱신한다. 사이트 통계 설명 모달에 지표별 원자료 링크와 연도를 표시한다. WDI 데이터는 CC BY 4.0, 원제공기관의 별도 조건 확인.

## 배포

별도 공개 저장소 `yhchung/born-again`의 main 브랜치 루트를 GitHub Pages로 제공한다. 이 폴더 밖의 상위 업무 저장소를 공개하지 않는다. `.nojekyll`로 빌드 없이 제공한다.
