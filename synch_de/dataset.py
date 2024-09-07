"""Process the dataset."""

from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm
import pandas as pd
import dask as dd

from synch_de.config import PROCESSED_DATA_DIR, RAW_DATA_DIR


def greet():
    """Greet the user. This function is used for as an example during onboarding."""
    logger.info(
        "Hello, welcome to the dataset processing script!"
    )
    return "Hi!"

def drop_unnamed_columns(df: pd.DataFrame) -> pd.DataFrame:
    """drop any column that starts with 'Unnamed'

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    # Drop any column that starts with 'Unnamed'
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

def read_course_table() -> pd.DataFrame:
    """Read the course table."""
    df = pd.read_csv(
        RAW_DATA_DIR / "course.csv",
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
        index_col = "id",
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
    return df

def read_telecomsession_table() -> pd.DataFrame:
    """Read the telecomsession table."""
    df = pd.read_csv(
        RAW_DATA_DIR / "telecomsession.csv",
        parse_dates=[
            "created",
            "updated",
            "telecom_date"
        ],
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
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df


def return_int(value: int) -> int:
    """Returns the input value.
    This function is used for as an example during onboarding."""
    return value


############## Refactor main functions below ##############
app = typer.Typer()


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    # ----------------------------------------------
):
    #Read the tables
    task_table = read_task_table()
    telecomsession_table = read_telecomsession_table()
    telecomsession_table.head()


if __name__ == "__main__":
    app()
