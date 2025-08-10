import ast


def extract_functions_from_file(file_path: str) -> list:
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start_line = node.lineno - 1
            end_line = node.body[-1].lineno
            functions.append((node.name, start_line, end_line))
    return functions


def get_function_code(file_path: str, start: int, end: int) -> str:
    with open(file_path, "r") as f:
        lines = f.readlines()
    return "".join(lines[start:end])
