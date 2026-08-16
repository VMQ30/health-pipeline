"""Pipeline utility functions for data extraction and DuckDB database ingestion."""

import logging
import duckdb
import pandas as pd
from datasets import load_dataset


def extract_data(data_path: str) -> pd.DataFrame:
    """Extracts dataset from Hugging Face datasets into a Pandas DataFrame.

    Args:
        data_path (str): Hugging Face dataset repository path or local dataset path.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the extracted 'train' split dataset.

    Raises:
        Exception: Re-raises any exception encountered during dataset extraction.
    """
    try:
        logging.info(f"Extracting data from {data_path}")
        ds = load_dataset(data_path)
        df = ds["train"].to_pandas()
        logging.debug(f"Extracted columns: {df.columns.tolist()}")
        return df
    except Exception as e:
        logging.error(f"Failed Extraction: {str(e)}")
        raise


def load_data(
    df: pd.DataFrame,
    db_path: str,
    table_name: str,
    schema_name: str,
) -> None:
    """Loads a pandas DataFrame into a DuckDB table.

    Creates the schema and table if they do not exist prior to loading data.

    Args:
        df (pd.DataFrame): The pandas DataFrame to persist in DuckDB.
        db_path (str): File system path to the DuckDB database file.
        table_name (str): Destination database table name.
        schema_name (str): Destination database schema name.

    Raises:
        Exception: Re-raises any exception encountered during database connection or table creation.
    """
    try:
        logging.info(f"Loading data into {schema_name}.{table_name}")
        with duckdb.connect(database=db_path, read_only=False) as con:
            con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
            con.execute(
                f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} AS SELECT * FROM df"
            )
        logging.info("Successfully loaded data into database")
    except Exception as e:
        logging.error(f"Failed Loading: {str(e)}")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extract_data("Nicolybgs/healthcare_data")
