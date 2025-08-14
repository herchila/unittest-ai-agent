# Unittest AI Agent

Unittest AI Agent is a Python tool that automatically generates comprehensive unit tests for your Python functions and classes using OpenAI's GPT models. It analyzes your source code, prepares context-rich prompts, and writes robust pytest-based test suites.

## Features

- **Automatic Source Analysis:** Extracts imports, functions, and class context from your Python files.
- **Prompt Engineering:** Uses customizable prompt templates for both standalone functions and class methods.
- **LLM Integration:** Sends code context to OpenAI GPT-4o to generate high-quality unit tests.
- **Test Postprocessing:** Cleans and adapts generated code for your project structure.
- **Test Writing:** Saves generated tests to the appropriate directory.

## Project Structure

- `main.py` — Entry point for test generation.
- `unittest_ai_agent/`
  - `parser.py` — Source code analysis utilities.
  - `llm_client.py` — OpenAI API integration.
  - `test_writer.py` — Test file writing and postprocessing.
  - `prompts/` — Prompt templates for LLM.
  - `example/` — Example source and generated tests.
- `requirements.txt` — Python dependencies.

## Getting Started

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Set your OpenAI API key:**
   - Create a `.env` file in the project root:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Run the test generator:**
   ```sh
   python main.py
   ```

   This will analyze `unittest_ai_agent/example/converter.py` and generate tests in `unittest_ai_agent/example/tests/`.

## Customization

- **Prompt Templates:** Edit files in `unittest_ai_agent/prompts/` to change how prompts are constructed for the LLM.
- **Source File:** Change `FILE_PATH_SAMPLE_FUNCTION` in `main.py` to target a different Python file.

## Example

Given a function like:

```python
def convert_date_to_iso(date_str: str, format: str = "%d/%m/%Y") -> str:
    ...
```

The agent will generate a suite of pytest tests covering various edge cases and save them to `unittest_ai_agent/example/tests/test_convert_date_to_iso.py`.

## 🚀 Project Roadmap
This project is under active development. Below is a summary of our progress and a look at what's ahead. Contributions are highly encouraged!

### ✅ Phase 1: Core Test Generation Engine (MVP)
[ x ] Develop "Dev Engineer" Agent: A core agent capable of generating unit tests from a single Python source file.

[ x ] LLM Integration: Connect the agent to a foundational LLM (e.g., GPT-4o, Llama 3) to power code generation.

[ x ] Basic CLI: A simple command-line interface to input a file and receive the generated test file.

---

### 🎯 Phase 2: Multi-Agent Collaboration & Feedback Loop
[ ] Introduce "QA Engineer" Agent: Develop a second agent responsible for reviewing, validating, and executing the generated tests.

[ ] Implement Test Execution Tool: Create a secure tool for the QA Agent to programmatically run pytest, capture results, and parse code coverage reports.

[ ] Establish Collaborative Framework (CrewAI): Refactor the agent logic into a Crew to manage the feedback loop, allowing the Dev Agent to fix tests based on the QA Agent's feedback until a target coverage is achieved.

---

### 🏗️ Phase 3: API-First Architecture & State Management
[ ] Expose via API: Wrap the agent crew in a FastAPI application to make it accessible as a service.

[ ] Job State Management: Integrate Redis or a database to manage the state of long-running jobs, allowing for asynchronous operation.

[ ] Containerization: Create a Dockerfile and docker-compose.yml to ensure a consistent and reproducible environment for the entire application stack.

---

### ✨ Future
[ ] LLMOps & Observability: Integrate with tools like LangSmith to trace, debug, and evaluate the performance of the agent interactions.

[ ] IDE Integration: Develop a VSCode extension for a seamless developer experience right within the editor.

[ ] Multi-Language Support: Expand capabilities beyond Python to include other languages like JavaScript/TypeScript and Go.

[ ] Automated Code Refactoring: Empower the Dev Agent to suggest fixes in the source code itself, not just the tests.

---

## License

MIT License