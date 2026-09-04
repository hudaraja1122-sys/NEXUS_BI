from __future__ import annotations

import os
import duckdb
from typing import Any, Dict, List
from app.core.config import settings

UPLOADS_DIR = os.path.join(settings.DATA_DIR, "uploads")


def execute_sql_on_dataset(dataset_id: str, sql: str) -> List[Dict[str, Any]]:
    """Executes a validated read-only SQL query on the stored dataset using an in-memory DuckDB instance."""
    clean_parquet_path = os.path.join(UPLOADS_DIR, f"{dataset_id}_clean.parquet")
    raw_csv_path = os.path.join(UPLOADS_DIR, f"{dataset_id}_raw.csv")
    raw_xlsx_path = os.path.join(UPLOADS_DIR, f"{dataset_id}_raw.xlsx")

    # Determine available data file
    if os.path.exists(clean_parquet_path):
        target_path = clean_parquet_path.replace(os.sep, "/")
        source_query = f"read_parquet('{target_path}')"
    elif os.path.exists(raw_csv_path):
        target_path = raw_csv_path.replace(os.sep, "/")
        source_query = f"read_csv_auto('{target_path}')"
    elif os.path.exists(raw_xlsx_path):
        target_path = raw_xlsx_path.replace(os.sep, "/")
        source_query = f"st_read('{target_path}')"
    else:
        raise FileNotFoundError(f"No valid data file found for dataset ID: {dataset_id}")

    # Guard against mutating statements
    sanitized_sql = sql.strip().rstrip(";")
    lowered = sanitized_sql.lower()
    forbidden_tokens = ["drop", "delete", "insert", "update", "alter", "create", "truncate", "copy"]
    if any(token in lowered.split() for token in forbidden_tokens):
        raise ValueError("Mutating operations are disabled. Only SELECT queries are permitted.")

    con = duckdb.connect(database=":memory:")
    try:
        # Create virtual view named 'dataset' so standard generated SQL queries execute directly
        con.execute(f"CREATE VIEW dataset AS SELECT * FROM {source_query}")
        result_df = con.execute(sanitized_sql).df()

        # Handle NaNs and non-serializable pandas nulls
        result_df = result_df.where(result_df.notnull(), None)
        return result_df.to_dict(orient="records")
    finally:
        con.close()