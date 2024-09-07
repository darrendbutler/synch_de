"""Functions to read raw and external data before feature engineerings."""

import pandas as pd

from synch_de.config import RAW_DATA_DIR

# TODO: Select columns in the read functions with usecols parameter
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
            "id": "category",
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
            "id": "category",
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
            "id": "category",
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

def read_channel_table() -> pd.DataFrame:
    """Read the channel table."""
    df = pd.read_csv(
        RAW_DATA_DIR / "channel.csv",
        index_col="id",
        parse_dates=["created", "updated",],
        dtype={
            "id": "category",
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

def read_user_table() -> pd.DataFrame:
    """read the user table from the raw data directory

    Returns:
        pd.DataFrame: _description_
    """
    df = pd.read_csv(
        RAW_DATA_DIR / "user.csv",
        index_col="id",
        parse_dates=["created", "updated", "opt_out"],
        dtype={
            "id": "category",
            "phone": "category",
            "tester": "category",
            "active": "category",
        },
    )
    # Drop any column that starts with 'Unnamed'
    df = drop_unnamed_columns(df)
    return df

def read_registration_table() -> pd.DataFrame:
    """read the registration table from the raw data directory

    Returns:
        pd.DataFrame: _description_
    """
    df = pd.read_csv(
        RAW_DATA_DIR / "registration.csv",
        index_col="id",
        parse_dates=["created", "updated",],
        dtype={
            "id": "category",
            "user_id": "category",
            "course_id": "category",
        },
    )
    # Drop any column that starts with 'Unnamed'
    df = drop_unnamed_columns(df)
    return df

def read_response_table() -> pd.DataFrame:
    """read the response table from the raw data directory

    Returns:
        pd.DataFrame: _description_
    """
    df = pd.read_csv(
        RAW_DATA_DIR / "response.csv",
        index_col="id",
        parse_dates=["created", "updated",],
        dtype={
            "id": "category",
            "source_id": "category",
            "user_id": "category",
            "key": "category",
            "value": "category",
            "correct": 'Int64',
        },
    )
    # Drop any column that starts with 'Unnamed'
    df = drop_unnamed_columns(df)
    return df

def read_inbound_table() -> pd.DataFrame:
    """read the inbound table from the raw data directory

    Returns:
        pd.DataFrame: _description_
    """
    df = pd.read_csv(
        RAW_DATA_DIR / "inbound.csv",
        index_col="id",
        parse_dates=["created", "updated",],
        dtype={
            "id": "category",
            "propmt_id": "category",
            "channel_id": "category",
            "text": "category",
        },
    )
    # Drop any column that starts with 'Unnamed'
    df = drop_unnamed_columns(df)
    return df

def read_outbound_table() -> pd.DataFrame:
    """read the outbound table from the raw data directory

    Returns:
        pd.DataFrame: _description_
    """
    df = pd.read_csv(
        RAW_DATA_DIR / "outbound.csv",
        index_col="id",
        parse_dates=["created", "updated",],
        dtype={
            "id": "category",
            "channel_id": "category",
            "status_id": "category",
            "header": "category",
        },
    )
    # Drop any column that starts with 'Unnamed'
    df = drop_unnamed_columns(df)
    return df

def read_content_table() -> pd.DataFrame:
    """read the content table from the raw data directory

    Returns:
        pd.DataFrame: _description_
    """
    df = pd.read_csv(
        RAW_DATA_DIR / "content.csv",
        index_col="id",
        parse_dates=["created", "updated",],
        dtype={
            "id": "category",
            "script": "category",
            "section": "category",
            "version": "category",
            "kind": "category",
            "content": "category",
            "correct_value": "category",
        },
    )
    # Drop any column that starts with 'Unnamed'
    df = drop_unnamed_columns(df)
    return df


