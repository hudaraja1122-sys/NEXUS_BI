import os
import duckdb
from typing import List, Dict, Any, Optional
from app.core.config import settings

class DuckDBTool:
    @staticmethod
    def _get_clean_parquet_path(dataset_id: str) -> str:
        path = os.path.join(settings.DATA_DIR, "uploads", f"{dataset_id}_clean.parquet")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Cleaned dataset storage for ID '{dataset_id}' not found.")
        return path

    @classmethod
    def execute_query(cls, dataset_id: str, query: str, params: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        """Executes a validated read-only SQL query over the dataset."""
        parquet_file = cls._get_clean_parquet_path(dataset_id)
        
        # Enforce read-only guards
        forbidden = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE", "EXEC", "TRUNCATE"]
        normalized_q = query.strip().upper()
        if any(keyword in normalized_q.split() for keyword in forbidden):
            raise PermissionError("Unpermitted SQL command: only read-only aggregation queries are allowed.")
            
        con = duckdb.connect(database=":memory:")
        try:
            # Register parquet as the analytical table 'dataset'
            con.execute(f"CREATE VIEW dataset AS SELECT * FROM read_parquet('{parquet_file}')")
            res = con.execute(query, params or []).fetchdf()
            return res.to_dict(orient="records")
        finally:
            con.close()