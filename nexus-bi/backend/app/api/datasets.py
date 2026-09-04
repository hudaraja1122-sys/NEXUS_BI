from __future__ import annotations

import os
import uuid
import json
from datetime import datetime
from typing import List, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, status
import pandas as pd

from app.core.config import settings
from app.models.schemas import (
    DatasetUploadResponse,
    DatasetSummary,
    DatasetProfileOut,
    ColumnProfileOut,
    DataQualityIssueOut,
    DatasetListResponse,
)
from app.tools.profiling import profile_dataframe
from app.tools.cleaning import clean_dataset

router = APIRouter(prefix="/datasets", tags=["datasets"])

METADATA_DIR = os.path.join(settings.DATA_DIR, "metadata")
UPLOADS_DIR = os.path.join(settings.DATA_DIR, "uploads")
os.makedirs(METADATA_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)


@router.post("/upload", response_model=DatasetUploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    filename = file.filename or "uploaded_file.csv"
    if not (filename.endswith(".csv") or filename.endswith(".xlsx")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported format. Only .csv and .xlsx files are permitted."
        )

    ext = ".csv" if filename.endswith(".csv") else ".xlsx"
    file_type = "csv" if ext == ".csv" else "xlsx"

    contents = await file.read()
    file_size = len(contents)

    max_bytes = getattr(settings, "MAX_FILE_SIZE_MB", 50) * 1024 * 1024
    if file_size > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum size of {getattr(settings, 'MAX_FILE_SIZE_MB', 50)}MB."
        )

    dataset_id = str(uuid.uuid4())
    saved_raw_filename = f"{dataset_id}_raw{ext}"
    saved_clean_filename = f"{dataset_id}_clean.parquet"
    
    raw_path = os.path.join(UPLOADS_DIR, saved_raw_filename)
    clean_path = os.path.join(UPLOADS_DIR, saved_clean_filename)

    with open(raw_path, "wb") as f:
        f.write(contents)

    try:
        if ext == ".csv":
            df = pd.read_csv(raw_path)
        else:
            df = pd.read_excel(raw_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse dataset file: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="The uploaded file contains no data rows.")

    # 1. Profiling
    columns_profile, quality_score = profile_dataframe(df)

    # 2. Cleaning & Parquet export (with fallback)
    try:
        cleaned_df = clean_dataset(df)
        cleaned_df.to_parquet(clean_path, index=False)
    except Exception as e:
        print(f"[Warning] Parquet export skipped or failed: {e}")

    # 3. Safe attribute extraction for schema output
    valid_types = {"numeric", "categorical", "datetime", "boolean", "text"}
    col_out_list = []

    for col in columns_profile:
        col_dict = col if isinstance(col, dict) else getattr(col, "__dict__", {})
        stats = col_dict.get("stats") or {}
        
        inferred = str(col_dict.get("inferred_type", "text")).lower()
        if inferred not in valid_types:
            inferred = "text"

        raw_samples = col_dict.get("sample_values") or []
        cleaned_samples = [str(x) if pd.notna(x) else "" for x in raw_samples[:5]]

        def clean_val(val: Any) -> float | None:
            if val is not None and pd.notna(val):
                try:
                    return float(val)
                except (ValueError, TypeError):
                    return None
            return None

        col_out_list.append(
            ColumnProfileOut(
                name=str(col_dict.get("name", "")),
                inferred_type=inferred,
                null_count=int(col_dict.get("null_count") or 0),
                null_pct=float(col_dict.get("null_percentage") or 0.0),
                unique_count=int(col_dict.get("unique_count") or 0),
                sample_values=cleaned_samples,
                min_value=clean_val(stats.get("min")),
                max_value=clean_val(stats.get("max")),
                mean_value=clean_val(stats.get("mean")),
                median_value=clean_val(stats.get("median")),
                std_value=clean_val(stats.get("std")),
            )
        )

    # 4. Safe Quality Score & Issues
    issues_list = []
    if isinstance(quality_score, dict):
        score_val = float(quality_score.get("overall_score", 100.0))
        for iss in quality_score.get("issues_detected", []):
            issues_list.append(
                DataQualityIssueOut(
                    column="general",
                    issue_type="missing_values",
                    severity="medium",
                    detail=str(iss),
                )
            )
    else:
        score_val = float(getattr(quality_score, "overall_score", 100.0))

    profile_out = DatasetProfileOut(
        row_count=len(df),
        column_count=len(df.columns),
        duplicate_row_count=int(df.duplicated().sum()),
        quality_score=score_val,
        columns=col_out_list,
        issues=issues_list,
    )

    summary_out = DatasetSummary(
        id=dataset_id,
        filename=filename,
        file_type=file_type,
        uploaded_at=datetime.utcnow(),
        file_size_bytes=file_size,
        row_count=len(df),
        column_count=len(df.columns),
        quality_score=score_val,
    )

    response_payload = DatasetUploadResponse(
        dataset=summary_out,
        profile=profile_out,
    )

    # 5. Persist JSON metadata record
    meta_path = os.path.join(METADATA_DIR, f"{dataset_id}.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(response_payload.model_dump_json(indent=2))

    return response_payload


@router.get("", response_model=DatasetListResponse)
async def list_datasets():
    datasets: List[DatasetSummary] = []
    for fname in os.listdir(METADATA_DIR):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(METADATA_DIR, fname), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "dataset" in data:
                        datasets.append(DatasetSummary(**data["dataset"]))
            except Exception:
                continue
    datasets.sort(key=lambda x: x.uploaded_at, reverse=True)
    return DatasetListResponse(datasets=datasets)


@router.get("/{dataset_id}", response_model=DatasetUploadResponse)
async def get_dataset(dataset_id: str):
    meta_path = os.path.join(METADATA_DIR, f"{dataset_id}.json")
    if not os.path.exists(meta_path):
        raise HTTPException(status_code=404, detail="Dataset not found.")
    with open(meta_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return DatasetUploadResponse(**data)