"""Student data analysis and local statistical descriptions."""

from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).parent / "data" / "StudentsPerformance.csv"
SCORE_LABELS = {
    "math score": "수학",
    "reading score": "읽기",
    "writing score": "쓰기",
}
GROUPS = ("남성 학생", "아시안 학생", "아시안 남성 학생")


@st.cache_data
def load_students(modified_at: int) -> pd.DataFrame:
    """Invalidate the cache when the CSV changes."""
    return pd.read_csv(DATA_PATH)


def get_students() -> pd.DataFrame:
    return load_students(DATA_PATH.stat().st_mtime_ns)


def select_group(df: pd.DataFrame, group: str) -> pd.DataFrame:
    male = df["gender"].eq("male")
    asian = df["race/ethnicity"].eq("Asian")
    masks = {
        "남성 학생": male,
        "아시안 학생": asian,
        "아시안 남성 학생": male & asian,
    }
    return df.loc[masks[group]].copy()
