"""Process the dataset."""

from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm

from synch_de.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from synch_de.dataset.read_data import (
    read_content_table,
    read_course_table,
    read_inbound_table,
    read_outbound_table,
    read_registration_table,
    read_response_table,
    read_task_table,
    read_telecomsession_table,
    read_user_table,
    read_channel_table,
)
from synch_de.dataset.preprocess import (
    combine_tables,
    merge_course_registration,
    merge_response_table,
    merge_task_table,
    merge_user_table,
)


def greet():
    """Greet the user. This function is used for as an example during onboarding."""
    logger.info("Hello, welcome to the dataset processing script!")
    return "Hi!"


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

    # Read the tables into their own dataframes
    course_table = read_course_table()
    task_table = read_task_table()
    user_table = read_user_table()
    response_table = read_response_table()
    registration_table = read_registration_table()

    # Combine tables into flat table
    # merge course with registration
    df = merge_course_registration(course_table, registration_table)

    # merge registration with user_table
    df = merge_user_table(user_table, df)

    # merge the task table
    df = merge_task_table(task_table, df)

    # merge with response table
    df = merge_response_table(response_table, df)

    # Save the processed data
    df.to_pickle(output_path)


if __name__ == "__main__":
    app()
