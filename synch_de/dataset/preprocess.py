"""File for preprocessing the data."""

from typing import Dict
import pandas as pd


def combine_tables(database: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    df = database["telecomsession"]
    return df


def merge_course_registration(course_table, registration_table):
    df = course_table.merge(
        registration_table,
        left_on="id",
        right_on="course_id",
        suffixes=("_course", "_regist"),
        how="inner",
    )

    return df


def merge_user_table(user_table, df):
    """
    Merge the given user_table with the given dataframe (df) based on the 'user_id' column.
    Parameters:
    - user_table (pandas.DataFrame): The user table to be merged.
    - df (pandas.DataFrame): The dataframe to be merged with the user table.
    Returns:
    - df (pandas.DataFrame): The merged dataframe.
    """
    df = df.merge(
        user_table,
        left_on="user_id",
        right_on="id",
        suffixes=("_course", "_user"),
        how="inner",
    )

    return df


def merge_task_table(task_table, df):
    """
    Merge the given task_table DataFrame with the df DataFrame based on the 'user_id' column.
    Parameters:
    - task_table (DataFrame): The DataFrame containing the task table.
    - df (DataFrame): The DataFrame to be merged with the task_table.
    Returns:
    - df (DataFrame): The merged DataFrame.
    """
    df = df.merge(
        task_table,
        left_on="user_id",
        right_on="user_id",
        suffixes=("_user", "_task"),
        how="inner",
    )

    return df


def merge_response_table(response_table, df):
    """
    Merge the response table with the given DataFrame.
    Parameters:
    response_table (pandas.DataFrame): The response table to be merged.
    df (pandas.DataFrame): The DataFrame to merge with the response table.
    Returns:
    pandas.DataFrame: The merged DataFrame.
    """
    df = df.merge(
        response_table.rename(columns={"created": "created_resp"}),
        left_on="user_id",
        right_on="user_id",
        suffixes=("_task", "_response"),
        how="inner",
    )

    return df


def merge_tables(
    course_table, registration_table, user_table, task_table, response_table
):
    """
    Merge multiple tables to create a consolidated dataset.

    Parameters:
    course_table (pandas.DataFrame): The table containing course information.
    registration_table (pandas.DataFrame): The table containing registration information.
    user_table (pandas.DataFrame): The table containing user information.
    task_table (pandas.DataFrame): The table containing task information.
    response_table (pandas.DataFrame): The table containing response information.

    Returns:
    pandas.DataFrame: The merged dataset.
    """
    # merge course with registration
    df = merge_course_registration(course_table, registration_table)

    # merge registration with user_table
    df = merge_user_table(user_table, df)

    # merge the task table
    df = merge_task_table(task_table, df)

    # merge with response table
    df = merge_response_table(response_table, df)

    return df


def mark_rows_for_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Marks rows in the DataFrame for analysis based on specific conditions.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The modified DataFrame with rows marked for analysis.

    """


    # keep path = "airscience-2022b" and "airscience-2022a"
    df["for_analysis"] = df["path"].isin(
        ["airscience-2022b", "airscience-2022a"]
    )
    # is active
    df["for_analysis"] = df["for_analysis"] & (df["status"] == "active")
    # tester == 0
    df["for_analysis"] = df["for_analysis"] & (df["tester"] == 0)

    # create a boolean mask for whether the value in df["created_resp"] is between 2022-08-11 and 2022-12-31
    df["for_analysis"] = df["for_analysis"] & (
        df["created_resp"].between("2022-08-11", "2022-12-31")
    )

    return df


def get_analysis_subset(df, selected_columns):
    df = df[df["for_analysis"] == 1][selected_columns]
    return df
