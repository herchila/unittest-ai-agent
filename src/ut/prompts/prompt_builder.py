"""Automated Unit Test Generation CLI with AI."""
from ut.constants import FILE_PATH_PROMPT


def _load_prompt(prompt_file):
    try:
        full_path = f"{FILE_PATH_PROMPT}/{prompt_file}"
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        exit(1)


def generate_class_method_prompt(
    imports_code: str,
    function_name: str,
    parent_class_code: str,
) -> str:
    """Generate prompt for class method testing."""

    prompt_template = _load_prompt("generate_unittest_class.txt")
    prompt = prompt_template.replace("{{imports_code}}", imports_code)
    prompt = prompt.replace("{{function_name}}", function_name)
    prompt = prompt.replace("{{parent_class_code}}", parent_class_code)
    return prompt


def generate_standalone_prompt(imports_code: str, function_code: str) -> str:
    """Generate prompt for standalone function testing."""

    prompt_template = _load_prompt("generate_unittest_standalone.txt")
    prompt = prompt_template.replace("{{imports_code}}", imports_code)
    prompt = prompt.replace("{{function_code}}", function_code)
    return prompt
