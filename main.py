import os

from unittest_ai_agent.parser import source_code_analysis
from unittest_ai_agent.llm_client import generate_test_code
from unittest_ai_agent.test_writer import write_test_file, postprocess_test_code


BASE_DIR = os.path.dirname(__file__)
FILE_PATH_SAMPLE_FUNCTION = os.path.join(BASE_DIR, "unittest_ai_agent", "example", "converter.py")
FILE_PATH_PROMPT = os.path.join(BASE_DIR, "unittest_ai_agent", "prompts")


def load_prompt(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: file not found in '{path}'")
        exit(1)


def main():
    print(f"🚀 Initializing test generation for: {FILE_PATH_SAMPLE_FUNCTION}")

    imports_code, functions_data = source_code_analysis(FILE_PATH_SAMPLE_FUNCTION)

    if not functions_data:
        print("No functions found in the source file.")
        return
    
    for func_data in functions_data:
        function_name = func_data["function_name"]
        print(f"\nProcessing: `def {function_name}(...)`...")

        if func_data["parent_class_code"]:
            print(f" Parent class found: {func_data['parent_class_code'].splitlines()[0]}")
            prompt_template = load_prompt(f"{FILE_PATH_PROMPT}/generate_unittest_class.txt")
            prompt = prompt_template.replace("{{imports_code}}", imports_code)
            prompt = prompt.replace("{{function_name}}", function_name)
            prompt = prompt.replace("{{parent_class_code}}", func_data['parent_class_code'])
        else:
            print(f"Standalone function found: {function_name}")
            prompt_template = load_prompt(f"{FILE_PATH_PROMPT}/generate_unittest_standalone.txt")
            prompt = prompt_template.replace("{{imports_code}}", imports_code)
            prompt = prompt.replace("{{function_code}}", func_data['function_code'])

        print("Sending prompt to LLM...")
        raw_response = generate_test_code(prompt)

        module_name = os.path.splitext(os.path.basename(FILE_PATH_SAMPLE_FUNCTION))[0]
        clean_code = postprocess_test_code(raw_response, function_name, module_name)

        write_test_file(function_name, clean_code)
        print(f"✅ Test code for `{function_name}` generated successfully!\n")

    print(f"🚀 All tests generated successfully!")

if __name__ == "__main__":
    main()
