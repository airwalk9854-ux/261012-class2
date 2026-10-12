import streamlit as st


st.set_page_config(page_title="학생 성적 분석", page_icon="🎓", layout="wide")

navigation = st.navigation([
    st.Page("pages/1_학생_데이터_AI_설명.py", title="학생 데이터 AI 설명", icon="🎓", default=True),
    st.Page("pages/2_남성_아시안_시각화.py", title="남성·아시안 시각화", icon="📊"),
])
navigation.run()
