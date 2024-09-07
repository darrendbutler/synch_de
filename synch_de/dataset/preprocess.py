"""File for preprocessing the data."""

from typing import Dict
import pandas as pd


def combine_tables(database: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    df = database["telecomsession"]
    return df
