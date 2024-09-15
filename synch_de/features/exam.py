import pandas as pd


def extract_exam_responses(preprocessed_responses):
    exam_responses = preprocessed_responses[
        preprocessed_responses["key"].str.contains("step-9-test|step-10-test")
    ].copy()
    # drop duplicates of ["user_id", "key"] from exam_responses
    exam_responses = exam_responses.drop_duplicates(
        subset=["user_id", "key"], inplace=False, keep="first"
    )
    return exam_responses


def calculate_exam_features(exam_responses_from_one_user):

    exam_features = pd.DataFrame()
    
    # calclate exam points by summing correct column
    exam_points = exam_responses_from_one_user["correct"].sum()
    exam_features["exam_points"] = [exam_points]

    # calculate exam questions attempted by user
    exam_questions_attempted = exam_responses_from_one_user["key"].nunique()
    exam_features["exam_questions_attempted"] = [exam_questions_attempted]

    exam_features = exam_features.reset_index(drop=True)

    return exam_features
