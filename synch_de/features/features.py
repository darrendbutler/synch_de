from pathlib import Path

import pandas as pd
import typer
from loguru import logger

from synch_de.config import PROCESSED_DATA_DIR, INTERIM_DATA_DIR
from synch_de.features.education_level import extract_edu_level_data
from synch_de.features.exam import (
    calculate_exam_features,
    extract_exam_responses,
)
from synch_de.features.practice import (
    calculate_practice_features,
    extract_practice_responses,
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

    ##### Education Level #####
    # Extract education level responses
    education_level_responses = extract_edu_level_data(preprocessed_responses)
    # Exract education level features
    education_level_features = (
        education_level_responses[["user_id", "value"]]
        .copy()
        .rename(columns={"value": "education_level"})
    )
    create_data_profile(education_level_features, "education_level_responses.pkl")
    education_level_features.to_pickle(INTERIM_DATA_DIR / "education_level_responses.pkl")

    ##### Practice Features #####

    # Extract practice responses
    practice_responses = extract_practice_responses(preprocessed_responses)
    create_data_profile(practice_responses, "practice_responses.pkl")
    practice_responses.to_pickle(INTERIM_DATA_DIR / "practice_responses.pkl")

    # Calculate Practice Features
    practice_features = calculate_practice_features(practice_responses.copy())

    ##### Exam Features #####

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

    ##### Prior Insutrction Features #####

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

    # Combine all features
    features = (
        pd.merge(
            prior_insutrction_features.reset_index(),
            exam_features.reset_index(),
            on="user_id",
            how="outer",
        )
        .merge(
            practice_features.reset_index(),
            on="user_id",
            how="outer",
        )
        .merge(
            education_level_features.reset_index(),
            on="user_id",
            how="outer",
        )
    )

    # create a data profile for the features
    create_data_profile(features, "features_outer.pkl")
    # Save the features to output_path
    features.to_csv(PROCESSED_DATA_DIR / "features_outer.csv")

    # note: in cleaning, drop user_id 44758 because they
    # took both exams, may be staff
    # Consider how you'd like to deal with scaling and outliers

    logger.success("Features generation complete.")

    # -----------------------------------------


if __name__ == "__main__":
    app()
