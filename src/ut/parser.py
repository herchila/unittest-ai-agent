"""Automated Unit Test Generation CLI with AI."""
import ast


def source_code_analysis(file_path: str) -> tuple[str, list[dict]]:
    """Analyze a Python source file and extract import statements \
    and detailed information about each function.

    Args:
        file_path: The path to the .py file to analyze.

    Returns:
        A tuple containing:
        - A string with all the import statements found.
        - A list of dictionaries, where each dictionary represents a function
        and contains its name, full source code,
        and the code of its parent class (if it exists).
    """

    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = ast.parse(source_code)

    # --- Step 1: Extract all imports ---
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # ast.unparse converts a node back to source code.
            # This is much more robust than handling line numbers.
            imports.append(ast.unparse(node))

    imports_code = "\n".join(imports)

    # --- Preparation for finding parent classes ---
    # ast does not keep references to parent nodes, so we create them ourselves
    # to be able to look up the tree from a function.
    parent_map = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }

    # --- Step 2 and 3: Extract functions, docstrings, type hints and parent classes ---
    functions_analysis = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # ast.unparse(node) gives us the COMPLETE code of the function,
            # including the `def` signature, the arguments with their type hints,
            # the return type hint, and the docstring.
            function_code = ast.unparse(node)

            parent_class_code = None
            parent = parent_map.get(node)
            if parent and isinstance(parent, ast.ClassDef):
                parent_class_code = ast.unparse(parent)

            analysis = {
                "function_name": node.name,
                "function_code": function_code,
                "parent_class_code": parent_class_code,
            }
            functions_analysis.append(analysis)

    return imports_code, functions_analysis
