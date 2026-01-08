from anthropic import Anthropic
from ut.llm.base_provider import LLMProvider


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-3-sonnet"):
        self.client = Anthropic(api_key=api_key)
        self.model = model
    
    def generate_test_code(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
