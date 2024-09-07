"""Process the dataset."""

from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm

from synch_de.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from synch_de.dataset.read_data import (
    read_course_table,
    read_task_table,
    read_telecomsession_table,
)

def greet():
    """Greet the user. This function is used for as an example during onboarding."""
    logger.info(
        "Hello, welcome to the dataset processing script!"
    )
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
    course_table = read_course_table()
    task_table = read_task_table()
    telecomsession_table = read_telecomsession_table()


if __name__ == "__main__":
    app()
