from pathlib import Path

import pandas as pd
import typer
from loguru import logger
from tqdm import tqdm

from synch_de.config import PROCESSED_DATA_DIR

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
    input_path: Path = PROCESSED_DATA_DIR / "dataset.pkl",
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Generating features from dataset...")
    for i in tqdm(range(10), total=10):
        # Read the dataset
        processed_data = pd.read_pickle(input_path)
        
        # Initialize the features dataframe
        features = pd.DataFrame()
        
        # Generate exam_score
        features["exam_score"] = get_exam_score(processed_data)
        
        
        
        pass
    logger.success("Features generation complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
