"""Create features based on prior instruction (did-you-listen) survey data."""

import pandas as pd


def extract_prior_instruction_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts prior instruction data from a DataFrame.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing the data.

    Returns:
    - prior_instruction_data (pandas.DataFrame): The extracted prior instruction data.
    """

    prior_instruction_data: pd.DataFrame = df[
        df["key"].str.contains("did-you-listen")
    ]

    # Drop duplicates in prior_instruction_data
    prior_instruction_data = prior_instruction_data.drop_duplicates(
        subset=["user_id", "key"], inplace=False, keep="first"
    )

    return prior_instruction_data


def calculate_prior_instruction_features(
    prior_instruction_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate the prior instruction features based on the given prior_instruction_data.

    Parameters:
    prior_instruction_data (pandas.DataFrame): The data containing prior instruction information.

    Returns:
    pandas.DataFrame: The calculated prior instruction features.
    """

    features: pd.DataFrame = pd.DataFrame()

    # calculate the number of times each user answered the survey
    features["prior_insutruction_reporting_frequency"] = prior_instruction_data[
        "user_id"
    ].value_counts()

    features["proportion_of_prior_insutrction"] = (
        prior_instruction_data.groupby("user_id", observed=False).apply(
            get_proportion_of_prior_instruction
        )
    )

    # normalize the number of times each user answered the survey
    features = max_scale_prior_instruction_reporting_frequency(features)

    return features


def max_scale_prior_instruction_reporting_frequency(features):
    features["prior_insutruction_reporting_frequency_scaled_by_max"] = (
        features["prior_insutruction_reporting_frequency"]
        / features["prior_insutruction_reporting_frequency"].max()
    )
    return features


def get_proportion_of_prior_instruction(responses_from_one_user):
    """
    Calculate the proportion of prior instruction reported by a user.
    Parameters:
    responses_from_one_user (DataFrame): A DataFrame containing the responses
    to the did-you-listen survey questions from a single user.
    Returns:
    float: The proportion of prior instruction reported by the user.
    """

    responses_from_one_user.loc[:, "binary_listening_response"] = (
        responses_from_one_user["value"].map({"Yes": 1, "No": 0})
    )
    # Calculate the proportion of yes responses
    prior_insutrction_reported_proportion = responses_from_one_user[
        "binary_listening_response"
    ].mean()

    return prior_insutrction_reported_proportion
