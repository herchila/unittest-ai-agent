import os

from enum import Enum

from ut.llm.base_provider import LLMProvider
from ut.llm.openai_provider import OpenAIProvider
from ut.llm.anthropic_provider import AnthropicProvider
from ut.llm.ollama_provider import OllamaProvider


class LLMType(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


def _openai_provider(model: str, **kwargs) -> OpenAIProvider:
    api_key = kwargs.get("api_key") or os.getenv("OPENAI_API_KEY")
    model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
    return OpenAIProvider(api_key, model)


def _anthropic_provider(model: str, **kwargs) -> AnthropicProvider:
    api_key = kwargs.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
    model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet")
    return AnthropicProvider(api_key, model)


def _ollama_provider(model: str, **kwargs) -> OllamaProvider:
    base_url = kwargs.get("base_url") or os.getenv("OLLAMA_URL", "http://localhost:11434")
    model = model or os.getenv("OLLAMA_MODEL", "llama2")
    return OllamaProvider(base_url, model)


def create_llm_provider(
    provider_type: str = None,
    model: str = None,
    **kwargs
) -> LLMProvider:
    """Factory to create LLM providers."""
    
    # Default from environment
    if not provider_type:
        provider_type = os.getenv("LLM_PROVIDER", "openai")
    
    provider_type = LLMType(provider_type.lower())

    provider_strategy = {
        LLMType.OPENAI: _openai_provider,
        LLMType.ANTHROPIC: _anthropic_provider,
        LLMType.OLLAMA: _ollama_provider,
    }

    provider = provider_strategy.get(provider_type)
    if not provider:
        raise ValueError(f"Unsupported provider: {provider_type}")

    return provider(model, **kwargs)
