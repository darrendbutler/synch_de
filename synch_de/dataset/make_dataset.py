"""Process the dataset."""

from pathlib import Path

import typer
from loguru import logger
from ydata_profiling import ProfileReport

# from tqdm.auto import tqdm # included in case you want to use tqdm

from synch_de.config import (
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    INTERIM_DATA_DIR,
    REPORTS_DIR,
)
from synch_de.dataset.read_data import (
    read_course_table,
    read_registration_table,
    read_response_table,
    read_task_table,
    read_user_table,
)
from synch_de.dataset.preprocess import (
    get_analysis_subset,
    mark_rows_for_analysis,
    merge_tables,
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
    logger.info("Preprocessing dataset.")

    # Read the tables into their own dataframes
    logger.info("Reading raw data data.")
    course_table = read_course_table()
    task_table = read_task_table()
    user_table = read_user_table()
    response_table = read_response_table()
    registration_table = read_registration_table()

    # Combine tables into one flat table
    logger.info("Merging Tables.")
    df = merge_tables(
        course_table,
        registration_table,
        user_table,
        task_table,
        response_table,
    )

    # Flag rows of interest
    df = mark_rows_for_analysis(df)

    # Keep flagged rows and needed columns
    selected_columns = [
        "created_resp",
        "user_id",
        "script",
        "key",
        "value",
        "correct",
        "complete",
    ]

    # Keep only rows that are flagged for analysis
    # TODO: Extract this to a function
    df = get_analysis_subset(df, selected_columns)

    # change the data type of the user_id column to category
    df["user_id"] = df["user_id"].astype("category")

    # Save processed data as pickle file
    logger.info("Saving processed data.")
    file_name = "processed_responses.pkl"
    output_path = INTERIM_DATA_DIR / file_name
    df.to_pickle(output_path)

    logger.success("Preprocessing complete.")

    # Generate a preprocessing report
    report_title = f"Preprocessing Report for {file_name}"
    logger.success("Creating Preporeccesing Report...")
    profile = ProfileReport(df, title=report_title, explorative=True, sortby="created_resp")
    profile.to_file(REPORTS_DIR / f"{report_title}.html")


if __name__ == "__main__":
    app()
