import os

import streamlit as st

from student_data import DATA_PATH, SCORE_LABELS, generate_summary, get_students, dataset_summary


st.set_page_config(page_title="학생 데이터 · AI 설명", page_icon="🎓", layout="wide")
st.title("🎓 학생 성적 데이터")
st.caption("StudentsPerformance.csv의 기본 통계와 AI 설명을 확인하세요.")
df = get_students()
summary = dataset_summary(df)

st.write(
    f"이 데이터에는 학생 {len(df):,}명의 성별, 인종/민족 분류, 부모의 교육 수준, "
    "급식 유형, 시험 준비 과정 이수 여부와 수학·읽기·쓰기 점수가 담겨 있습니다. "
    "점수는 0~100점 척도로 표시합니다."
)
cols = st.columns(4)
cols[0].metric("학생 수", f"{len(df):,}명")
for col, (score, label) in zip(cols[1:], SCORE_LABELS.items()):
    col.metric(f"{label} 평균", f"{df[score].mean():.1f}점")

st.subheader("AI로 간략한 설명 만들기")
st.caption("생성 버튼을 누르면 집계 통계를 OpenAI에 전송합니다. API 사용 요금이 발생할 수 있습니다.")

try:
    configured_key = st.secrets.get("OPENAI_API_KEY", "")
    configured_model = st.secrets.get("OPENAI_MODEL", "")
except st.errors.StreamlitSecretNotFoundError:
    configured_key = configured_model = ""
configured_key = configured_key or os.environ.get("OPENAI_API_KEY", "")
configured_model = configured_model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

with st.expander("AI 연결 설정", expanded=not bool(configured_key)):
    entered_key = st.text_input("OpenAI API 키", type="password", help="입력한 키는 현재 세션에서만 사용합니다.")
    model = st.text_input("모델", value=configured_model)
    st.caption("서버의 OPENAI_API_KEY 환경 변수 또는 Streamlit secrets로도 설정할 수 있습니다.")
api_key = (entered_key or configured_key).strip()
if not api_key:
    st.info("API 키를 설정하면 AI 설명을 생성할 수 있습니다. 기본 통계와 시각화는 키 없이 이용할 수 있습니다.")

data_version = DATA_PATH.stat().st_mtime_ns
if st.button("AI 설명 생성", type="primary", disabled=not api_key or not model.strip()):
    with st.spinner("데이터를 설명하고 있습니다…"):
        try:
            generated = generate_summary(summary, api_key, model.strip())
        except RuntimeError as exc:
            st.error(str(exc))
        else:
            st.session_state["student_ai_summary"] = (data_version, generated)

saved = st.session_state.get("student_ai_summary")
if saved and saved[0] == data_version:
    st.markdown(saved[1])
    st.caption("AI가 생성한 설명입니다. 수치는 아래 원본 데이터와 대조해 확인하세요.")

st.page_link("pages/2_남성_아시안_시각화.py", label="남성·아시안 학생 시각화 보기", icon="📊")
with st.expander("데이터 열과 원본 미리보기"):
    st.dataframe(df.head(20), hide_index=True, width="stretch")
    st.write(f"총 {len(df.columns)}개 열 · 결측값 {int(df.isna().sum().sum())}개")
