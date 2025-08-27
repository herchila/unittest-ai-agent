# Automated Unit Test Generation CLI with AI

[![Tests](https://github.com/herchila/unittest-ai-agent/actions/workflows/test.yml/badge.svg)](https://github.com/herchila/unittest-ai-agent/actions/workflows/test.yml)
[![Coverage](https://github.com/herchila/unittest-ai-agent/actions/workflows/coverage.yml/badge.svg)](https://github.com/herchila/unittest-ai-agent/actions/workflows/coverage.yml)
[![gitleaks](https://github.com/herchila/unittest-ai-agent/actions/workflows/gitleaks.yml/badge.svg)](https://github.com/herchila/unittest-ai-agent/actions/workflows/gitleaks.yml)

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Poetry Version](https://img.shields.io/badge/poetry-2.1.3%2B-blue.svg)](https://python-poetry.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Unittest AI Agent is a Python tool that automatically generates comprehensive unit tests for your Python functions and classes using OpenAI's GPT models. It analyzes your source code, prepares context-rich prompts, and writes robust pytest-based test suites.

## Features

- **Automatic Source Analysis:** Extracts imports, functions, and class context from your Python files.
- **Prompt Engineering:** Uses customizable prompt templates for both standalone functions and class methods.
- **LLM Integration:** Sends code context to OpenAI GPT-4o to generate high-quality unit tests.
- **Test Postprocessing:** Cleans and adapts generated code for your project structure.
- **Test Writing:** Saves generated tests to the appropriate directory.

## Getting Started

0. **Requirements:**
   - Python 3.9 or higher
   - OpenAI API key
   - Poetry `curl -sSL https://install.python-poetry.org | python3`

1. **Install dependencies:**
   ```sh
   poetry install
   ```

2. **Set your OpenAI API key:**
   - Rename the `.env.example` to `.env`:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Run the test generator:**
   ```sh
   poetry run ut generate example/converter.py
   ```

   This will analyze `ut/example/converter.py` and generate tests in `ut/example/tests/`.

### Customization

- **Prompt Templates:** Edit files in `ut/prompts/` to change how prompts are constructed for the LLM.

### Example

Given a function like:

```python
def convert_date_to_iso(date_str: str, format: str = "%d/%m/%Y") -> str:
    ...
```

The agent will generate a suite of pytest tests covering various edge cases and save them to `ut_output/test_convert.py`.


## 🚀 Project Roadmap
This project is under active development. Below is a summary of our progress and a look at what's ahead.

Contributions are highly encouraged!

👉 Roadmap: https://focusmap.pro/roadmap/45a1b599-aead-4c11-b749-032e5ea168e1

## License

Apache 2.0
