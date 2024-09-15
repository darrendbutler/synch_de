import pandas as pd
from pathlib import Path
import pickle

def extract_edu_level_data(df: pd.DataFrame) -> pd.DataFrame:
    edu_level_data: pd.DataFrame = df[
        df["key"].str.contains("profile/schooling")
    ]

    edu_level_data = edu_level_data.drop_duplicates(
        subset=["user_id", "key"], inplace=False, keep="first"
    )
    return edu_level_data

def calc_edu_level_features(edu_level_data: pd.DataFrame) -> pd.DataFrame:
    features: pd.DataFrame = pd.DataFrame()

    features["education_level_freq"] = edu_level_data["user_id"].value_counts()
    return features

def max_scale_edu_level_freq(features):
    features["education_level_freq"] = (
        features["education_level_freq"]
        / features["education_level_freq"].max()
    )
    return features

def save_features(pivot_table: pd.DataFrame, output_path: Path):
    """Save the pivot table to a CSV file."""
    pivot_table.to_csv(output_path)
