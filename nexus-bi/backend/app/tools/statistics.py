import duckdb
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from app.tools.sql import DuckDBTool

def group_by_metric(dataset_id: str, dimension: str, metric: str, agg: str = "SUM", limit: int = 10) -> List[Dict[str, Any]]:
    valid_aggs = {"SUM", "AVG", "COUNT", "MIN", "MAX", "MEDIAN"}
    agg_op = agg.upper() if agg.upper() in valid_aggs else "SUM"
    
    query = f"""
        SELECT 
            "{dimension}" AS dimension_value,
            {agg_op}("{metric}") AS aggregate_value
        FROM dataset
        WHERE "{dimension}" IS NOT NULL AND "{metric}" IS NOT NULL
        GROUP BY "{dimension}"
        ORDER BY aggregate_value DESC
        LIMIT {limit}
    """
    return DuckDBTool.execute_query(dataset_id, query)

def compare_periods(
    dataset_id: str, 
    date_column: str, 
    metric: str, 
    period_1_start: str, 
    period_1_end: str, 
    period_2_start: str, 
    period_2_end: str,
    agg: str = "SUM"
) -> Dict[str, Any]:
    query = f"""
        SELECT
            {agg}(CASE WHEN "{date_column}" >= ? AND "{date_column}" <= ? THEN "{metric}" ELSE 0 END) AS p1_val,
            {agg}(CASE WHEN "{date_column}" >= ? AND "{date_column}" <= ? THEN "{metric}" ELSE 0 END) AS p2_val
        FROM dataset
    """
    params = [period_1_start, period_1_end, period_2_start, period_2_end]
    rows = DuckDBTool.execute_query(dataset_id, query, params)
    
    p1 = float(rows[0]["p1_val"] or 0.0)
    p2 = float(rows[0]["p2_val"] or 0.0)
    abs_change = round(p2 - p1, 2)
    pct_change = round(((p2 - p1) / p1) * 100, 2) if p1 != 0 else 0.0
    
    return {
        "metric": metric,
        "period_1": {"start": period_1_start, "end": period_1_end, "value": p1},
        "period_2": {"start": period_2_start, "end": period_2_end, "value": p2},
        "absolute_change": abs_change,
        "percentage_change": pct_change
    }

def calculate_correlation(dataset_id: str, col1: str, col2: str) -> Dict[str, Any]:
    query = f"""
        SELECT CORR("{col1}", "{col2}") AS correlation_coefficient
        FROM dataset
        WHERE "{col1}" IS NOT NULL AND "{col2}" IS NOT NULL
    """
    result = DuckDBTool.execute_query(dataset_id, query)
    corr = result[0]["correlation_coefficient"]
    return {
        "column_1": col1,
        "column_2": col2,
        "correlation": round(float(corr), 4) if corr is not None else None
    }

def detect_outliers_iqr(dataset_id: str, metric: str, multiplier: float = 1.5) -> Dict[str, Any]:
    query = f"""
        SELECT 
            quantile_cont("{metric}", 0.25) AS q1,
            quantile_cont("{metric}", 0.75) AS q3
        FROM dataset
        WHERE "{metric}" IS NOT NULL
    """
    quantiles = DuckDBTool.execute_query(dataset_id, query)[0]
    q1 = float(quantiles["q1"])
    q3 = float(quantiles["q3"])
    iqr = q3 - q1
    lower_bound = q1 - (multiplier * iqr)
    upper_bound = q3 + (multiplier * iqr)
    
    count_query = f"""
        SELECT COUNT(*) as outlier_count
        FROM dataset
        WHERE "{metric}" < ? OR "{metric}" > ?
    """
    outliers = DuckDBTool.execute_query(dataset_id, count_query, [lower_bound, upper_bound])[0]
    
    return {
        "metric": metric,
        "q1": round(q1, 2),
        "q3": round(q3, 2),
        "iqr": round(iqr, 2),
        "lower_bound": round(lower_bound, 2),
        "upper_bound": round(upper_bound, 2),
        "outlier_count": int(outliers["outlier_count"])
    }