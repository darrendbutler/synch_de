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
from synch_de.dataset.preprocess import combine_tables


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
    # Read the tables
    database = {
        "telecomsession": read_telecomsession_table(),
        "channel": read_channel_table(),
        "course": read_course_table(),
        "task": read_task_table(),
        "user": read_user_table(),
        "content": read_content_table(),
        "outbound": read_outbound_table(),
        "inbound": read_inbound_table(),
        "response": read_response_table(),
        "registration": read_registration_table(),
    }

    # TODO: Combine tables into flat table
    df = combine_tables(database)


if __name__ == "__main__":
    app()
