"""Pydantic request/response models for the dataset API.

These mirror app.services.profiling's dataclasses but add HTTP-facing
concerns (validation, JSON schema, examples). Keeping the dataclasses
framework-free means profiling logic stays unit-testable without spinning
up FastAPI.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal, Dict, List, Optional

from pydantic import BaseModel, Field


class ColumnProfileOut(BaseModel):
    name: str
    inferred_type: Literal["numeric", "categorical", "datetime", "boolean", "text"]
    null_count: int
    null_pct: float
    unique_count: int
    sample_values: list[Any]
    min_value: float | None = None
    max_value: float | None = None
    mean_value: float | None = None
    median_value: float | None = None
    std_value: float | None = None


class DataQualityIssueOut(BaseModel):
    column: str
    issue_type: Literal[
        "missing_values", "duplicate_rows", "constant_column", "high_cardinality", "mixed_types"
    ]
    severity: Literal["low", "medium", "high"]
    detail: str


class DatasetProfileOut(BaseModel):
    row_count: int
    column_count: int
    duplicate_row_count: int
    quality_score: float = Field(ge=0, le=100)
    columns: list[ColumnProfileOut]
    issues: list[DataQualityIssueOut]


class DatasetSummary(BaseModel):
    """Metadata record — what's stored/listed without re-profiling."""

    id: str
    filename: str
    file_type: Literal["csv", "xlsx"]
    uploaded_at: datetime
    file_size_bytes: int
    row_count: int
    column_count: int
    quality_score: float


class DatasetUploadResponse(BaseModel):
    dataset: DatasetSummary
    profile: DatasetProfileOut


class DatasetListResponse(BaseModel):
    datasets: list[DatasetSummary]


class ErrorResponse(BaseModel):
    detail: str


# =====================================================================
# Backward-compatibility models for app.tools.profiling and older code
# =====================================================================
class ColumnProfile(BaseModel):
    name: str
    dtype: str
    inferred_type: str
    total_count: int = 0
    null_count: int = 0
    null_percentage: float = 0.0
    unique_count: int = 0
    sample_values: Optional[List[Any]] = None
    stats: Optional[Dict[str, Any]] = None


class DataQualityScore(BaseModel):
    overall_score: int = 100
    completeness: float = 100.0
    validity: float = 100.0
    consistency: float = 100.0
    duplicate_cleanliness: float = 100.0
    issues_detected: List[str] = []


# Alias in case any tool imports QualityScore
QualityScore = DataQualityScore

class ChartSpec(BaseModel):
    chart_type: Literal["bar", "line", "pie", "scatter", "table"]
    title: str
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    series: Optional[str] = None


class QueryRequest(BaseModel):
    dataset_id: str
    prompt: str


class QueryResponse(BaseModel):
    sql_query: str
    summary_text: str
    chart: ChartSpec
    data: List[Dict[str, Any]]