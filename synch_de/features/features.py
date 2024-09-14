from pathlib import Path

import pandas as pd
import typer
from loguru import logger

from synch_de.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR
from synch_de.features.prior_insutrction import (
    calculate_prior_instruction_features,
    extract_prior_instruction_data,
)
from synch_de.plots import create_data_profile

app = typer.Typer()


def get_exam_score(processed_data: pd.DataFrame) -> pd.Series:
    """Calculate the exam score for each user."""
    # Group processed_data by user_id
    user_group = processed_data.groupby("user_id")

    # Initialize the features dataframe
    features = pd.DataFrame()

    # Generate exam_score
    features["exam_score"] = user_group["exam_score"].mean()

    return features["exam_score"]


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
    # -----------------------------------------
):
    logger.info("Generating features from dataset...")

    input_path = INTERIM_DATA_DIR / "processed_responses.pkl"
    df = pd.read_pickle(input_path)

    features = pd.DataFrame()

    prior_instruction_data = extract_prior_instruction_data(df)
    prior_insutrction_features = calculate_prior_instruction_features(
        prior_instruction_data
    )

    # Get a subset of the data for user 42930 for testing purposes
    responses_from_one_user = prior_instruction_data[
        prior_instruction_data["user_id"] == "42930"
    ].copy()

    # Concatenate the features to the features dataframe
    features = pd.concat([features, prior_insutrction_features], axis=1)

    prior_instruction_data["user_id"].value_counts()

    logger.success("Features generation complete.")

    # Create a data profile for the prior_instruction data
    create_data_profile(prior_instruction_data, "prior_insutrction_data.pkl")
    # Save the prior_instruction_data to INTERIM_DATA_DIR
    prior_instruction_data.to_pickle(
        INTERIM_DATA_DIR / "prior_instruction_data.pkl"
    )

    # -----------------------------------------


if __name__ == "__main__":
    app()
