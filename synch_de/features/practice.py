import pandas as pd


PRACTICE_STEPS = [
    "intro-step",
    "1",
    "2",
    "4",
    "5",
    "3",
    "6",
    "7",
    "8",
]

EXAM_STEPS = ["9", "10"]


def expand_question_keys(df):
    # Label step, lesson, and question
    df["step_num"] = get_step(df["key"])
    df["lesson_num"] = get_lesson_number(df["key"])
    df["question_num"] = get_question_number(df["key"])
    return df


def get_step(keys):
    """Takes lesson keys from response table and
        returns series of corresponding steps.

    Args:
        keys (series): keys from response table

    Returns:
        series: series of lessons steps
    """
    # step questions follow this regex pattern
    step_pattern = r"((?<=step-)\d{1,2}|baseline|intro-step|endline|course-menu|exam-questions)"
    step_column = keys.str.extract(step_pattern)
    return step_column


def get_lesson_number(keys):
    lesson_pattern = r"(?<=lesson-)([\d{1,2}])"
    lesson_column = keys.str.extract(lesson_pattern)
    return lesson_column


def get_question_number(keys):
    question_pattern = r"(?<=q)([\d{1,2}])"
    question_column = keys.str.extract(question_pattern)
    return question_column


def extract_practice_responses(preprocessed_responses):
    is_course_3_lesson_question = preprocessed_responses["key"].str.contains(
        "airscience-2022a/course/.*/go-to-question"
    )
    practice_responses = preprocessed_responses[is_course_3_lesson_question]
    return practice_responses


def calculate_unique_practice_questions_answered(user_practice_attempts):
    return user_practice_attempts["key"].nunique()


def calculate_practice_features(practice_responses):
    practice_features = pd.DataFrame()
    unique_practice_questions_answered = practice_responses.groupby(
        "user_id", observed=True
    ).apply(calculate_unique_practice_questions_answered, include_groups=False)
    practice_features["unique_practice_questions_answered"] = (
        unique_practice_questions_answered
    )

    practice_features["unique_practice_questions_answered_scaled_by_max"] = (
        practice_features["unique_practice_questions_answered"]
        / practice_features["unique_practice_questions_answered"].max()
    )
    return practice_features
