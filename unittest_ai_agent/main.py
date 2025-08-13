import os

from parser import source_code_analysis
from llm_client import generate_test_code
from test_writer import clean_llm_output, write_test_file, postprocess_test_code


def load_prompt(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: file not found in '{path}'")
        exit(1)


def main():
    file_path_to_test = "example/converter.py"
    print(f"🚀 Initializing test generation for: {file_path_to_test}")
    
    imports_code, functions_data = source_code_analysis(file_path_to_test)
    if not functions_data:
        print("No functions found in the source file.")
        return
    
    for func_data in functions_data:
        function_name = func_data["function_name"]
        print(f"\nProcessing: `def {function_name}(...)`...")

        if func_data["parent_class_code"]:
            print(f" Parent class found: {func_data['parent_class_code'].splitlines()[0]}")
            prompt_template = load_prompt("prompts/generate_unittest_class.txt")
            prompt = prompt_template.replace("{{imports_code}}", imports_code)
            prompt = prompt.replace("{{function_name}}", function_name)
            prompt = prompt.replace("{{parent_class_code}}", func_data['parent_class_code'])
        else:
            print(f"Standalone function found: {function_name}")
            prompt_template = load_prompt("prompts/generate_unittest_standalone.txt")
            prompt = prompt_template.replace("{{imports_code}}", imports_code)
            prompt = prompt.replace("{{function_code}}", func_data['function_code'])

        print("Sending prompt to LLM...")
        raw_response = generate_test_code(prompt, prompt_template)
        clean_code = clean_llm_output(raw_response)

        module_name = os.path.splitext(os.path.basename(file_path_to_test))[0]
        clean_code = postprocess_test_code(clean_code, function_name, module_name)

        write_test_file(function_name, clean_code)
        print(f"✅ Test code for `{function_name}` generated successfully!\n")

    print(f"🚀 All tests generated successfully!")

if __name__ == "__main__":
    main()
