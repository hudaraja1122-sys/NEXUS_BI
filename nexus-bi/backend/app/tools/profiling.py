import pandas as pd
import numpy as np
from typing import Dict, Any, List
from app.models.schemas import ColumnProfile, DataQualityScore

def infer_column_type(series: pd.Series) -> str:
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    
    # Check if object might be datetime
    if series.dtype == "object":
        sample = series.dropna().head(20)
        try:
            pd.to_datetime(sample, errors="raise")
            return "datetime"
        except (ValueError, TypeError):
            pass
        
        # Check cardinality for categorical vs text
        unique_ratio = series.nunique() / max(len(series), 1)
        if unique_ratio < 0.2:
            return "categorical"
        return "text"
    return "categorical"

def profile_dataframe(df: pd.DataFrame) -> tuple[List[ColumnProfile], DataQualityScore]:
    total_rows = len(df)
    columns_profile: List[ColumnProfile] = []
    
    total_cells = max(total_rows * len(df.columns), 1)
    total_nulls = int(df.isnull().sum().sum())
    
    duplicate_rows = int(df.duplicated().sum())
    duplicate_score = max(0.0, 1.0 - (duplicate_rows / max(total_rows, 1)))
    completeness_score = max(0.0, 1.0 - (total_nulls / total_cells))
    
    issues: List[str] = []
    if duplicate_rows > 0:
        issues.append(f"Found {duplicate_rows} duplicate rows ({round(duplicate_rows/total_rows*100, 1)}%).")
    if total_nulls > 0:
        issues.append(f"Dataset contains {total_nulls} missing cells across columns.")

    validity_checks = 0
    validity_passed = 0

    for col in df.columns:
        series = df[col]
        null_count = int(series.isnull().sum())
        unique_count = int(series.nunique())
        inferred = infer_column_type(series)
        
        stats: Dict[str, Any] = {}
        if inferred == "numeric":
            validity_checks += 1
            # Filter non-nulls for stats
            valid_nums = pd.to_numeric(series, errors="coerce").dropna()
            if len(valid_nums) > 0:
                stats = {
                    "min": float(valid_nums.min()),
                    "max": float(valid_nums.max()),
                    "mean": float(round(valid_nums.mean(), 2)),
                    "median": float(round(valid_nums.median(), 2)),
                }
                # Check for impossible negative numbers in typical metrics
                if col.lower() in ["revenue", "price", "quantity", "unit_price"] and stats["min"] < 0:
                    issues.append(f"Column '{col}' contains negative values.")
                else:
                    validity_passed += 1

        sample_vals = series.dropna().head(5).tolist()
        
        columns_profile.append(
            ColumnProfile(
                name=str(col),
                dtype=str(series.dtype),
                inferred_type=inferred,
                total_count=total_rows,
                null_count=null_count,
                null_percentage=round((null_count / max(total_rows, 1)) * 100, 2),
                unique_count=unique_count,
                sample_values=sample_vals,
                stats=stats or None,
            )
        )

    validity_score = (validity_passed / max(validity_checks, 1)) if validity_checks > 0 else 1.0
    consistency_score = 1.0  # Assumed high post-parsing for CSV/XLSX
    
    # Weighted composite score out of 100
    overall = int((completeness_score * 0.35 + validity_score * 0.35 + duplicate_score * 0.20 + consistency_score * 0.10) * 100)
    
    quality_score = DataQualityScore(
        overall_score=min(max(overall, 0), 100),
        completeness=round(completeness_score * 100, 1),
        validity=round(validity_score * 100, 1),
        consistency=round(consistency_score * 100, 1),
        duplicate_cleanliness=round(duplicate_score * 100, 1),
        issues_detected=issues,
    )
    
    return columns_profile, quality_score