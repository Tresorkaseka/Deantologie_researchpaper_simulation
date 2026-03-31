from __future__ import annotations

import os
from types import SimpleNamespace

from litellm import completion


DEFAULT_MODEL_NAME = "provider/model-name"
COMMON_KEY_ENV_VARS = (
    "LLM_API_KEY",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
)
PROVIDER_KEY_ENV_VARS = {
    "openai": ("LLM_API_KEY", "OPENAI_API_KEY"),
    "anthropic": ("LLM_API_KEY", "ANTHROPIC_API_KEY"),
    "gemini": ("LLM_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"),
}


def get_llm_provider() -> str:
    return os.getenv("LLM_PROVIDER", "").strip().lower()


def get_llm_api_key() -> str | None:
    provider = get_llm_provider()
    env_names: list[str] = []
    for env_name in (*PROVIDER_KEY_ENV_VARS.get(provider, ()), *COMMON_KEY_ENV_VARS):
        if env_name not in env_names:
            env_names.append(env_name)

    for env_name in env_names:
        value = os.getenv(env_name)
        if value:
            return value
    return None


def get_llm_model_name() -> str:
    return os.getenv("LLM_MODEL_NAME", DEFAULT_MODEL_NAME).strip() or DEFAULT_MODEL_NAME


def get_llm_base_url() -> str | None:
    value = os.getenv("LLM_BASE_URL", "").strip()
    return value or None


def resolve_model_name(model_name: str, provider: str | None = None) -> str:
    cleaned_model_name = (model_name or "").strip()
    cleaned_provider = (provider or "").strip().lower()

    if not cleaned_model_name:
        return DEFAULT_MODEL_NAME
    if "/" in cleaned_model_name or not cleaned_provider:
        return cleaned_model_name
    return f"{cleaned_provider}/{cleaned_model_name}"


class _ChatCompletionsAdapter:
    def __init__(self, api_key: str, provider: str | None, base_url: str | None):
        self.api_key = api_key
        self.provider = provider
        self.base_url = base_url

    def create(self, model: str, messages: list[dict], max_tokens: int, temperature: float):
        kwargs = {
            "model": resolve_model_name(model, self.provider),
            "messages": messages,
            "api_key": self.api_key,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if self.base_url:
            kwargs["api_base"] = self.base_url
        return completion(**kwargs)


class LiteLLMClient:
    def __init__(self, api_key: str, provider: str | None = None, base_url: str | None = None):
        self.chat = SimpleNamespace(
            completions=_ChatCompletionsAdapter(
                api_key=api_key,
                provider=provider,
                base_url=base_url,
            )
        )


def create_llm_client(
    api_key: str,
    provider: str | None = None,
    base_url: str | None = None,
) -> LiteLLMClient:
    """
    Generic LLM adapter entry point.

    The repository can run with the provider and model preferred by the user as long
    as LiteLLM supports it, for example Anthropic, OpenAI, Gemini, or an
    OpenAI-compatible endpoint exposed through LLM_BASE_URL.
    """

    return LiteLLMClient(
        api_key=api_key,
        provider=provider or get_llm_provider(),
        base_url=base_url or get_llm_base_url(),
    )
