"""Shared student data analysis and optional OpenAI summary generation."""

import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

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


def dataset_summary(df: pd.DataFrame) -> dict:
    """Only aggregate statistics are included in the AI request."""
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "missing_values": df.isna().sum().to_dict(),
        "category_counts": {
            column: df[column].value_counts().to_dict()
            for column in df.columns if column not in SCORE_LABELS
        },
        "scores": df[list(SCORE_LABELS)].describe().round(2).to_dict(),
        "groups": {
            name: {
                "count": len(select_group(df, name)),
                "mean_scores": select_group(df, name)[list(SCORE_LABELS)]
                .mean().round(2).to_dict(),
            }
            for name in GROUPS
        },
    }


def generate_summary(summary: dict, api_key: str, model: str) -> str:
    payload = {
        "model": model,
        "store": False,
        "max_output_tokens": 700,
        "instructions": (
            "당신은 데이터 분석 도우미입니다. 제공된 집계 통계만 이용해 한국어로 "
            "StudentsPerformance.csv를 4~5문장으로 간략히 설명하세요. "
            "학생 수, 변수, 과목별 평균, 남성·Asian·Asian 남성 학생 수를 포함하세요. "
            "데이터 출처나 수집 시기, 인종 코드의 뜻을 추측하지 마세요. "
            "표본의 차이를 성별·인종의 타고난 능력이나 인과관계로 해석하지 마세요."
        ),
        "input": json.dumps(summary, ensure_ascii=False),
    }
    request = Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=45) as response:
            result = json.load(response)
    except HTTPError as exc:
        messages = {
            401: "API 키를 확인해 주세요.",
            403: "이 API 키의 모델 접근 권한을 확인해 주세요.",
            404: "모델 이름과 접근 권한을 확인해 주세요.",
            429: "요청 한도 또는 API 사용 잔액을 확인한 후 다시 시도해 주세요.",
        }
        raise RuntimeError(messages.get(exc.code, "AI 서비스 요청에 실패했습니다. 잠시 후 다시 시도해 주세요.")) from None
    except (URLError, TimeoutError):
        raise RuntimeError("AI 서비스에 연결할 수 없습니다. 네트워크를 확인하고 다시 시도해 주세요.") from None
    except (ValueError, UnicodeError):
        raise RuntimeError("AI 서비스 응답을 읽을 수 없습니다. 다시 시도해 주세요.") from None

    if result.get("status") != "completed":
        raise RuntimeError("AI 설명 생성이 완료되지 않았습니다. 다시 시도해 주세요.")
    text = "\n".join(
        part["text"]
        for item in result.get("output", []) if item.get("type") == "message"
        for part in item.get("content", []) if part.get("type") == "output_text"
    ).strip()
    if not text:
        raise RuntimeError("AI 설명이 비어 있습니다. 다시 시도해 주세요.")
    return text
