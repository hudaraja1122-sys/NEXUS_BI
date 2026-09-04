"""Centralized, typed configuration.

Everything environment-specific (API keys, model names, limits) lives here —
never hardcoded inside agents, routes, or services. This is the single
source of truth the spec calls for in sections 3 and 4.
"""
from functools import lru_cache
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = Field(default="development")
    DATA_DIR: str = "data"
    MAX_FILE_SIZE_MB: int = 50

    # --- AI provider (Gemini primary; see services/llm_provider.py for abstraction) ---
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.5-flash", alias="GEMINI_MODEL")

    # --- Cost-safety / agent limits (spec section 4) ---
    max_investigation_steps: int = Field(default=8, alias="MAX_INVESTIGATION_STEPS")
    max_llm_calls_per_question: int = Field(default=10, alias="MAX_LLM_CALLS_PER_QUESTION")

    # --- CORS ---
    cors_origins_raw: str = Field(default="http://localhost:3000", alias="CORS_ORIGINS")

    # --- Storage (local filesystem for MVP; see spec section 2 for future migration) ---
    upload_dir: str = Field(default="./data/uploads", alias="UPLOAD_DIR")
    reports_dir: str = Field(default="./data/reports", alias="REPORTS_DIR")
    duckdb_path: str = Field(default="./data/nexus.duckdb", alias="DUCKDB_PATH")

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
settings = get_settings()

