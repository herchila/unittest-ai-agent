from parser import extract_functions_from_file, get_function_code
from llm_client import generate_test_code
from test_writer import clean_llm_output, write_test_file, postprocess_test_code


def load_prompt(path):
    with open(path, "r") as f:
        return f.read()


def main():
    file_path_to_test = "example/converter.py"
    prompt_template = load_prompt("prompts/unittest_prompt.txt")

    functions = extract_functions_from_file(file_path_to_test)
    for name, start, end in functions:
        print(f"\n📌 Function: {name}")
        func_code = get_function_code(file_path_to_test, start, end)
        raw_code = generate_test_code(func_code, prompt_template)
        clean_code = clean_llm_output(raw_code)
        test_code = postprocess_test_code(clean_code, name, "converter")
        print(test_code)
        write_test_file(name, test_code)


if __name__ == "__main__":
    main()
