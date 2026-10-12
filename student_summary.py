"""Local descriptions calculated from student statistics."""

import pandas as pd

from student_data import GROUPS, SCORE_LABELS, select_group


def describe_students(df: pd.DataFrame) -> str:
    """Generate a Korean description from current CSV statistics, without an API."""
    if df.empty:
        return "분석할 학생 데이터가 없습니다."

    means = df[list(SCORE_LABELS)].mean().dropna()
    scores = ", ".join(
        f"{SCORE_LABELS[score]} {mean:.1f}점" for score, mean in means.items()
    )
    groups = ", ".join(
        f"{group} {len(select_group(df, group)):,}명"
        for group in GROUPS
    )
    missing = int(df.isna().sum().sum())
    sentences = [
        f"이 데이터는 학생 {len(df):,}명의 성별, 인종/민족 분류, 부모 교육 수준, "
        "급식 유형, 시험 준비 과정 이수 여부와 수학·읽기·쓰기 점수를 담고 있습니다.",
        f"과목별 평균은 {scores}입니다." if scores else "계산 가능한 과목 점수가 없습니다.",
        f"분석 대상에는 {groups}이 포함됩니다. 아시안 남성 학생은 앞의 두 집단에도 포함됩니다.",
        f"전체 {len(df.columns)}개 열에 결측값은 {missing:,}개입니다.",
    ]
    if len(means) > 1:
        highest = means[means.eq(means.max())]
        lowest = means[means.eq(means.min())]
        if means.max() == means.min():
            sentences.append("모든 과목의 평균 점수가 같습니다.")
        else:
            high_labels = "·".join(SCORE_LABELS[score] for score in highest.index)
            low_labels = "·".join(SCORE_LABELS[score] for score in lowest.index)
            sentences.append(
                f"평균이 가장 높은 과목은 {high_labels}, 가장 낮은 과목은 {low_labels}이며 "
                f"평균 차이는 {means.max() - means.min():.1f}점입니다."
            )
    return "\n\n".join(sentences)
