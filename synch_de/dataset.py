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
    return df


def read_task_table() -> pd.DataFrame:
    """Read the task table."""
    df = pd.read_csv(
        RAW_DATA_DIR / "task.csv",
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
    read_course_table().info()
    task_table = read_task_table()
    filtered_task_table = task_table[
        (task_table["script"].str.contains("2022"))
        & (task_table["script"].str.contains("lesson"))
        & (task_table["created"] >= pd.Timestamp("2022-08-01"))
        & (task_table["created"] <= pd.Timestamp("2022-12-31"))
    ]
    # Print a list of the unique values in the "script" column
    filtered_task_table["script"].unique()
    
    unique_values_count = filtered_task_table[
        "script"
    ].nunique()
    print(f"Number of unique values: {unique_values_count}")
    task_table["script"].nunique()


if __name__ == "__main__":
    app()
