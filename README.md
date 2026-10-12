# 🎓 학생 성적 분석 대시보드

학생 성적 CSV의 기본 통계와 AI 설명, 남성·아시안 학생 데이터 시각화를 제공하는 Streamlit 앱입니다.

### Codespaces에서 실행하기

Codespaces에서 제공하는 Python 환경을 그대로 사용합니다. 가상환경을 생성하거나 활성화할 필요가 없습니다.

1. 필요한 패키지를 설치합니다. 이미 설치되어 있다면 생략할 수 있습니다.

   ```
   python -m pip install -r requirements.txt
   ```

2. 앱을 실행합니다.

   ```
   python -m streamlit run streamlit_app.py
   ```

3. Codespaces의 **포트(Ports)** 탭에서 `8501` 포트를 브라우저로 엽니다.

메인 코드는 `streamlit_app.py`에 작성합니다. 패키지를 추가할 때는 `python -m pip install 패키지명`으로 설치하고, 프로젝트에서 사용하는 패키지만 `requirements.txt`에 기록합니다.

### 학생 성적 분석 페이지

왼쪽 메뉴에서 **학생 데이터 AI 설명**과 **남성 아시안 시각화** 페이지를 열 수 있습니다.
`data/StudentsPerformance.csv`를 읽어 기본 통계를 표시하고, 남성 학생·아시안 학생·아시안 남성 학생을 선택해 과목별 평균, 점수 분포, 읽기/쓰기 관계를 확인합니다. 시험 준비 과정 이수 여부로 추가 필터링하고 선택 데이터를 다운로드할 수 있습니다.

AI 설명을 사용하려면 페이지에서 OpenAI API 키를 입력하거나 `OPENAI_API_KEY` 환경 변수 또는 `.streamlit/secrets.toml`에 설정하세요.

```toml
OPENAI_API_KEY = "여기에 API 키 입력"
OPENAI_MODEL = "gpt-4.1-mini"
```

`OPENAI_MODEL`은 선택 사항이며 페이지에서도 변경할 수 있습니다. 실제 키는 저장소에 커밋하지 마세요. 생성 버튼을 누를 때만 집계 통계를 전송하며, API 요금이 발생할 수 있습니다. 키가 없어도 기본 설명과 모든 시각화가 동작합니다.
AI 연결은 [OpenAI Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses)를 사용합니다.
