import streamlit as st

from student_data import SCORE_LABELS, get_students
from student_summary import describe_students


st.set_page_config(page_title="학생 데이터 · 자동 분석", page_icon="🎓", layout="wide")
st.title("🎓 학생 성적 데이터")
st.caption("StudentsPerformance.csv를 직접 분석한 통계와 설명을 확인하세요.")
df = get_students()

st.write(
    f"이 데이터에는 학생 {len(df):,}명의 성별, 인종/민족 분류, 부모의 교육 수준, "
    "급식 유형, 시험 준비 과정 이수 여부와 수학·읽기·쓰기 점수가 담겨 있습니다. "
    "점수는 0~100점 척도로 표시합니다."
)
cols = st.columns(4)
cols[0].metric("학생 수", f"{len(df):,}명")
for col, (score, label) in zip(cols[1:], SCORE_LABELS.items()):
    col.metric(f"{label} 평균", f"{df[score].mean():.1f}점")

st.subheader("데이터 자동 분석 설명")
st.markdown(describe_students(df))
st.caption("CSV 통계를 계산해 자동으로 작성한 설명입니다. 데이터가 바뀌면 설명도 갱신됩니다.")

st.page_link("pages/2_남성_아시안_시각화.py", label="남성·아시안 학생 시각화 보기", icon="📊")
with st.expander("데이터 열과 원본 미리보기"):
    st.dataframe(df.head(20), hide_index=True, width="stretch")
    st.write(f"총 {len(df.columns)}개 열 · 결측값 {int(df.isna().sum().sum())}개")
