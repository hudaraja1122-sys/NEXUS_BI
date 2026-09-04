import re
import pandas as pd

def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    new_cols = []
    for col in cleaned.columns:
        # Lowercase, replace non-alphanumeric with underscores, strip trailing underscores
        c = re.sub(r"[^\w\s]", "", str(col).strip())
        c = re.sub(r"\s+", "_", c).lower()
        new_cols.append(c)
    cleaned.columns = new_cols
    return cleaned

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = normalize_column_names(df)
    # Attempt automatic date conversion on datetime-like columns
    for col in cleaned.columns:
        if "date" in col or "time" in col:
            try:
                cleaned[col] = pd.to_datetime(cleaned[col], errors="ignore")
            except Exception:
                pass
    return cleaned