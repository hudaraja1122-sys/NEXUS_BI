"""Provider-agnostic LLM interface.

Phase 1: interface + Gemini stub only (no agent logic yet — that's Phase 4/5).
Never let the model execute arbitrary code; it only returns structured
JSON/Pydantic outputs that deterministic tools then act on.
"""
from abc import ABC, abstractmethod
from typing import Any, Type

from pydantic import BaseModel

from app.core.config import get_settings


class LLMProvider(ABC):
    """Every provider (Gemini today; Groq/DeepSeek/etc. later) implements this."""

    @abstractmethod
    async def generate_structured(
        self, prompt: str, response_schema: Type[BaseModel]
    ) -> BaseModel:
        """Return a validated instance of response_schema. No free-form code execution."""
        raise NotImplementedError


class GeminiProvider(LLMProvider):
    """Thin wrapper around google-genai. Model name is config-driven — never hardcoded."""

    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.gemini_api_key
        self.model_name = settings.gemini_model
        # Client construction deferred to Phase 4 so Phase 1 has no external
        # network dependency at import time.
        self._client: Any = None

    def _ensure_client(self) -> None:
        if self._client is None:
            from google import genai  # imported lazily — Phase 4 dependency

            self._client = genai.Client(api_key=self.api_key)

    async def generate_structured(
        self, prompt: str, response_schema: Type[BaseModel]
    ) -> BaseModel:
        raise NotImplementedError(
            "Wired up in Phase 4 (Gemini integration) — see build order in the spec."
        )


def get_llm_provider() -> LLMProvider:
    """Factory so callers never import a concrete provider directly."""
    return GeminiProvider()
