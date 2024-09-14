from pathlib import Path

import pandas as pd
import typer
from loguru import logger
from tqdm import tqdm
from ydata_profiling import ProfileReport


from synch_de.config import FIGURES_DIR, PROCESSED_DATA_DIR, REPORTS_DIR
import time

app = typer.Typer()


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = FIGURES_DIR / "plot.png",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Generating plot from data...")
    for i in tqdm(range(1), total=1):
        time.sleep(5)
        logger.info("Something happened")
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Plot generation complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()


def create_data_profile(df: pd.DataFrame, file_name: str) -> None:
    """
    Create a data profile for the given DataFrame.
    Parameters:
    - df: pandas.DataFrame
        The DataFrame to create the data profile for.
    - file_name: str
        The name of the file to include in the data profile report title.
    Returns:
    None
    """

    report_title = f"Data Profile {file_name}"
    logger.info("Creating data profile...")
    profile = ProfileReport(
        df, title=report_title, explorative=True, sortby="created_resp"
    )
    profile.to_file(REPORTS_DIR / f"{report_title}.html")
    logger.success("Data profile created...")
