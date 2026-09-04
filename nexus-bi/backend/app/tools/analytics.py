from __future__ import annotations

import os
import duckdb
from typing import Any, Dict, List
from app.core.config import settings

UPLOADS_DIR = os.path.join(settings.DATA_DIR, "uploads")


def get_dataset_view(con: duckdb.DuckDBPyConnection, dataset_id: str):
    parquet_path = os.path.join(UPLOADS_DIR, f"{dataset_id}_clean.parquet").replace(os.sep, "/")
    csv_path = os.path.join(UPLOADS_DIR, f"{dataset_id}_raw.csv").replace(os.sep, "/")

    if os.path.exists(parquet_path):
        source = f"read_parquet('{parquet_path}')"
    elif os.path.exists(csv_path):
        source = f"read_csv_auto('{csv_path}')"
    else:
        raise FileNotFoundError(f"Dataset files missing for {dataset_id}")

    con.execute(f"CREATE OR REPLACE VIEW dataset AS SELECT * FROM {source}")


def tool_get_kpis(dataset_id: str) -> Dict[str, Any]:
    """Calculates top-level baseline business metrics."""
    con = duckdb.connect(database=":memory:")
    try:
        get_dataset_view(con, dataset_id)
        return con.execute("""
            SELECT 
                ROUND(COALESCE(SUM(Revenue), 0), 2) AS total_revenue,
                ROUND(COALESCE(SUM(Profit), 0), 2) AS total_profit,
                COUNT(*) AS total_orders,
                ROUND(COALESCE(AVG(Discount), 0) * 100, 1) AS avg_discount_pct
            FROM dataset
        """).df().to_dict(orient="records")[0]
    finally:
        con.close()


def tool_temporal_performance(dataset_id: str) -> List[Dict[str, Any]]:
    """Compares metrics over quarters to identify period-over-period collapses."""
    con = duckdb.connect(database=":memory:")
    try:
        get_dataset_view(con, dataset_id)
        query = """
            SELECT 
                CONCAT(CAST(YEAR(TRY_CAST(Order_Date AS DATE)) AS VARCHAR), '-Q', CAST(QUARTER(TRY_CAST(Order_Date AS DATE)) AS VARCHAR)) AS quarter,
                ROUND(SUM(Revenue), 2) AS revenue,
                ROUND(SUM(Profit), 2) AS profit,
                ROUND(AVG(Discount) * 100, 1) AS avg_discount,
                COUNT(*) AS order_count
            FROM dataset
            WHERE TRY_CAST(Order_Date AS DATE) IS NOT NULL
            GROUP BY quarter
            ORDER BY quarter ASC
        """
        return con.execute(query).df().to_dict(orient="records")
    finally:
        con.close()


def tool_category_drilldown(dataset_id: str) -> List[Dict[str, Any]]:
    """Identifies which category is contributing to net losses."""
    con = duckdb.connect(database=":memory:")
    try:
        get_dataset_view(con, dataset_id)
        query = """
            SELECT 
                Category AS name,
                ROUND(SUM(Revenue), 2) AS revenue,
                ROUND(SUM(Profit), 2) AS profit,
                ROUND(AVG(Discount) * 100, 1) AS avg_discount
            FROM dataset
            GROUP BY Category
            ORDER BY profit ASC
        """
        return con.execute(query).df().to_dict(orient="records")
    finally:
        con.close()


def tool_sub_entity_investigation(dataset_id: str, culprit_category: str = "Electronics") -> List[Dict[str, Any]]:
    """Autonomous recursive step: drills down into specific products within the distressed category."""
    con = duckdb.connect(database=":memory:")
    try:
        get_dataset_view(con, dataset_id)
        query = f"""
            SELECT 
                Product AS product_name,
                ROUND(SUM(Revenue), 2) AS revenue,
                ROUND(SUM(Profit), 2) AS profit,
                ROUND(AVG(Discount) * 100, 1) AS avg_discount,
                SUM(Quantity) AS units_sold
            FROM dataset
            WHERE LOWER(Category) = LOWER('{culprit_category}')
            GROUP BY Product
            ORDER BY profit ASC
        """
        return con.execute(query).df().to_dict(orient="records")
    finally:
        con.close()


def tool_discount_impact_audit(dataset_id: str) -> List[Dict[str, Any]]:
    """Audits the relationship between heavy discounting and margin erosion."""
    con = duckdb.connect(database=":memory:")
    try:
        get_dataset_view(con, dataset_id)
        query = """
            SELECT 
                CASE 
                    WHEN Discount = 0 THEN '0% Full Price'
                    WHEN Discount <= 0.15 THEN '1%-15% Moderate'
                    WHEN Discount <= 0.30 THEN '16%-30% High'
                    ELSE '>30% Severe Discount'
                END AS discount_tier,
                ROUND(SUM(Profit), 2) AS total_profit,
                COUNT(*) AS order_volume,
                ROUND(AVG(Profit / NULLIF(Revenue, 0)) * 100, 1) AS margin_pct
            FROM dataset
            GROUP BY discount_tier
            ORDER BY MIN(Discount) ASC
        """
        return con.execute(query).df().to_dict(orient="records")
    finally:
        con.close()