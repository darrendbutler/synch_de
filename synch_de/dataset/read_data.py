"""Functions to read raw and external data before feature engineerings."""

from synch_de.config import RAW_DATA_DIR


import pandas as pd


def drop_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
    """drop any column that starts with 'Unnamed'

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    # Drop any column that starts with 'Unnamed'
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    return df


def read_course_table() -> pd.DataFrame:
    """Read the course table."""
    df = pd.read_csv(
        RAW_DATA_DIR / "course.csv",
        index_col="id",
        parse_dates=["start", "stop", "created", "updated"],
        dtype={
            "title": "category",
            "path": "category",
            "status": "category",
        },
    )
    df = drop_unnamed_columns(df)
    return df


def read_task_table() -> pd.DataFrame:
    """Read the task table."""
    df = pd.read_csv(
        RAW_DATA_DIR / "task.csv",
        index_col="id",
        parse_dates=[
            "created",
            "updated",
        ],
        dtype={
            "user_id": "category",
            "script": "category",
            "complete": "category",
        },
    )
    df = drop_unnamed_columns(df)
    return df


def read_telecomsession_table() -> pd.DataFrame:
    """Read the telecomsession table."""
    df = pd.read_csv(
        RAW_DATA_DIR / "telecomsession.csv",
        index_col="id",
        parse_dates=["created", "updated", "telecom_date"],
        dtype={
            "session_id": "category",
            "network_code": "category",
            "service_code": "category",
            "status_reason": "category",
            "cost_string": "category",
            "user_input": "category",
            "final_output": "category",
        },
    )
    # Drop any column that starts with 'Unnamed'
    df = drop_unnamed_columns(df)
    return df
