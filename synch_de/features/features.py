from pathlib import Path

import pandas as pd
import typer
from loguru import logger

from synch_de.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR
from synch_de.features.exam import (
    calculate_exam_features,
    extract_exam_responses,
)
from synch_de.features.prior_insutrction import (
    calculate_prior_instruction_features,
    extract_prior_instruction_data,
)
from synch_de.plots import create_data_profile

app = typer.Typer()


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
    # -----------------------------------------
):
    logger.info("Generating features from dataset...")

    # Read preprocessed responses
    input_path = INTERIM_DATA_DIR / "processed_responses.pkl"
    preprocessed_responses = pd.read_pickle(input_path)

    # Initialize the features dataframe
    features = pd.DataFrame()

    # Extract responses to exam questions and calculate exam features
    exam_responses = extract_exam_responses(preprocessed_responses)
    create_data_profile(exam_responses, "exam_responses.pkl")
    exam_responses.to_pickle(INTERIM_DATA_DIR / "exam_responses.pkl")

    # Calculate exam features
    exam_features = (
        (
            exam_responses.groupby(by="user_id", observed=True).apply(
                calculate_exam_features, include_groups=False
            )
        )
        .reset_index(drop=False)
        .drop(columns="level_1")
        .set_index("user_id")
    )

    # Create Prior Instruction Features
    prior_instruction_data = extract_prior_instruction_data(
        preprocessed_responses
    )
    prior_insutrction_features = calculate_prior_instruction_features(
        prior_instruction_data
    )
    # Create a data profile for the prior_instruction data
    create_data_profile(prior_instruction_data, "prior_insutrction_data.pkl")
    # Save the prior_instruction_data to INTERIM_DATA_DIR
    prior_instruction_data.to_pickle(
        INTERIM_DATA_DIR / "prior_instruction_data.pkl"
    )

    features = pd.merge(
        prior_insutrction_features.reset_index(),
        exam_features.reset_index(),
        on="user_id",
        how="inner",
    )

    # note: in cleaning, drop user_id 44758 because they
    # took both exams, may be staff
    # Consider how you'd like to deal with scaling and outliers

    logger.success("Features generation complete.")

    # -----------------------------------------


if __name__ == "__main__":
    app()
