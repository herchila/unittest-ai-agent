import os
import yaml

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any

@dataclass
class LLMConfig:
    provider: str
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.3
    max_tokens: int = 600


class Config:
    def __init__(self):
        self.config_paths = [
            Path.home() / ".config" / "ut" / "config.yaml",  # User global config
            Path.cwd() / ".ut.yaml",                         # Project config
            Path.cwd() / "ut.config.yaml",                   # Alternative project config
        ]
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load config from files in priority order."""
        # 1. Default config
        self._config = {
            "llm": {
                "provider": "openai",
                "model": "gpt-4o",
                "temperature": 0.3,
                "max_tokens": 600
            }
        }
        
        # 2. Load from config files (later files override earlier)
        for config_path in self.config_paths:
            if config_path.exists():
                with open(config_path) as f:
                    file_config = yaml.safe_load(f)
                    self._merge_config(file_config)
        
        # 3. Override with environment variables
        self._load_env_overrides()
    
    def _merge_config(self, new_config: Dict):
        """Deep merge configuration."""
        # Implementación simple, podrías usar bibliotecas como deepmerge
        if new_config:
            for key, value in new_config.items():
                if isinstance(value, dict) and key in self._config:
                    self._config[key].update(value)
                else:
                    self._config[key] = value
    
    def _load_env_overrides(self):
        """Override with environment variables."""
        if os.getenv("UT_PROVIDER"):
            self._config["llm"]["provider"] = os.getenv("UT_PROVIDER")
        if os.getenv("UT_MODEL"):
            self._config["llm"]["model"] = os.getenv("UT_MODEL")
        # API keys siempre desde env por seguridad
        if os.getenv("OPENAI_API_KEY"):
            self._config.setdefault("openai", {})["api_key"] = os.getenv("OPENAI_API_KEY")
        if os.getenv("ANTHROPIC_API_KEY"):
            self._config.setdefault("anthropic", {})["api_key"] = os.getenv("ANTHROPIC_API_KEY")
    
    def get_llm_config(self, provider_override: Optional[str] = None, 
                       model_override: Optional[str] = None) -> LLMConfig:
        """Get LLM configuration with optional overrides."""
        provider = provider_override or self._config["llm"]["provider"]
        model = model_override or self._config["llm"]["model"]
        
        # Get provider-specific config
        provider_config = self._config.get(provider, {})
        
        return LLMConfig(
            provider=provider,
            model=model,
            api_key=provider_config.get("api_key"),
            base_url=provider_config.get("base_url"),
            temperature=self._config["llm"].get("temperature", 0.3),
            max_tokens=self._config["llm"].get("max_tokens", 600)
        )
