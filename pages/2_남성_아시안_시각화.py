import pandas as pd
import streamlit as st

from student_data import GROUPS, SCORE_LABELS, get_students, select_group


st.set_page_config(page_title="남성·아시안 학생 시각화", page_icon="📊", layout="wide")
st.title("📊 남성·아시안 학생 시각화")
st.caption("CSV의 gender=male, race/ethnicity=Asian 값을 사용합니다.")
df = get_students()

group = st.radio("분석 대상", GROUPS, index=2, horizontal=True)
selected = select_group(df, group)
preparation = st.selectbox("시험 준비 과정", ["전체", "이수", "미이수"])
if preparation != "전체":
    selected = selected[selected["test preparation course"].eq(
        "completed" if preparation == "이수" else "none"
    )]

st.caption("남성 학생과 아시안 학생에는 아시안 남성 학생이 함께 포함됩니다.")
if selected.empty:
    st.warning("선택한 조건에 해당하는 학생이 없습니다. 필터를 변경해 주세요.")
    st.stop()

cols = st.columns(4)
cols[0].metric("선택한 학생 수", f"{len(selected):,}명")
for col, (score, label) in zip(cols[1:], SCORE_LABELS.items()):
    col.metric(f"{label} 평균", f"{selected[score].mean():.1f}점",
               delta=f"{selected[score].mean() - df[score].mean():+.1f}점", delta_color="off")
st.caption("평균 아래 차이는 필터를 적용하지 않은 전체 학생 평균과 비교한 값입니다.")

st.subheader("과목별 평균 비교")
comparison = pd.DataFrame({
    "과목": list(SCORE_LABELS.values()),
    "전체 학생": df[list(SCORE_LABELS)].mean().values,
    "선택한 학생": selected[list(SCORE_LABELS)].mean().values,
})
st.bar_chart(comparison, x="과목", y=["전체 학생", "선택한 학생"],
             stack=False, y_label="평균 점수")

st.subheader("점수 분포")
subject = st.selectbox("과목", list(SCORE_LABELS), format_func=SCORE_LABELS.get)
bins = list(range(0, 101, 10))
labels = ["0–10"] + [f"{start + 1}–{start + 10}" for start in range(10, 100, 10)]
counts = pd.cut(selected[subject], bins=bins, labels=labels, include_lowest=True)
distribution = counts.value_counts(sort=False).rename_axis("점수 구간").reset_index(name="학생 수")
st.bar_chart(distribution, x="점수 구간", y="학생 수", sort=False, y_label="학생 수")

st.subheader("읽기와 쓰기 점수의 관계")
st.scatter_chart(selected.rename(columns=SCORE_LABELS), x="읽기", y="쓰기")

with st.expander("선택한 학생의 원본 데이터"):
    st.dataframe(selected, hide_index=True, width="stretch")
    st.download_button("선택 데이터 CSV 다운로드",
                       selected.to_csv(index=False).encode("utf-8-sig"),
                       file_name="selected_students.csv", mime="text/csv")

st.caption("이 그래프는 해당 표본의 관측값을 보여줍니다. 성별이나 인종에 따른 인과관계를 설명하지 않습니다.")
