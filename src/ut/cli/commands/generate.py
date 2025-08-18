"""Automated Unit Test Generation CLI with AI."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from ut.constants import FILE_PATH_PROMPT
from ut.llm_client import generate_test_code
from ut.parser import source_code_analysis

console = Console()


def generate(
    file_path: str = typer.Argument(
        ".", help="Path to source file or directory. Use '.' for current directory"
    ),
    output_dir: Optional[str] = typer.Option(
        "ut_output",
        "--output",
        "-o",
        help="Output directory for generated tests (default: ut_output/)",
    ),
    recursive: bool = typer.Option(
        True,
        "--recursive/--no-recursive",
        "-r/-R",
        help="Process files recursively in directories",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show what would be generated without creating files"
    ),
    mirror_structure: bool = typer.Option(
        True,
        "--mirror/--flat",
        help="Mirror source directory structure in output (default: mirror)",
    ),
) -> None:
    """
    Generate unit tests for Python files in any Python project.

    Works with Django, FastAPI, Flask, or any Python codebase.
    Tests are generated in 'ut_output/' directory by default, preserving \
        the source project structure for easy review and manual integration.

    Examples:
        ut generate  # Current directory -> ut_output/
        ut generate my_module.py  # Single file -> ut_output/test_my_module.py
        ut generate src/  # All files in src/ -> ut_output/src/...
        ut generate . --output tests/  # Custom output directory
        ut generate src/ --flat  # All tests in ut_output/ without subdirs

    After generation, review the tests in ut_output/ and move them to your
    project's test directory as needed.
    """

    # Clean up temporary files
    clean_temp_files(verbose=False)

    if not file_path:
        console.print("[bold red]Error: The file path cannot be empty.[/bold red]")
        raise typer.Exit(code=1)

    if not output_dir:
        console.print(
            "[bold red]Error: The output directory cannot be empty.[/bold red]"
        )
        raise typer.Exit(code=1)

    path = Path(file_path).resolve()
    output_base = Path(output_dir).resolve()

    if not dry_run:
        console.print(f"[bold cyan]📁 Output directory: {output_base}/[/bold cyan]")
        if output_base.exists() and any(output_base.iterdir()):
            console.print(
                "[yellow]⚠️  Output directory exists and contains files[/yellow]"
            )
            if not typer.confirm("Continue and potentially overwrite existing files?"):
                raise typer.Exit(0)

    if path.is_file():
        if not path.suffix == ".py":
            console.print(f"[bold red]Error: {path} is not a Python file[/bold red]")
            raise typer.Exit(1)

        console.print(f"[bold blue]Processing single file: {path.name}[/bold blue]")
        process_file(path, output_base, mirror_structure, verbose, dry_run)

    elif path.is_dir():
        console.print(
            "[bold red]Warning: Directory processing is not implemented yet.[/bold red]"
        )
        raise typer.Exit(1)

    else:
        msg_sufix = "is neither a file nor a directory"
        console.print(f"[bold red]Error: '{file_path}' {msg_sufix}[/bold red]")
        raise typer.Exit(1)

    # Clean up temporary files
    clean_temp_files()

    if not dry_run:
        console.print(
            f"\n✅ [bold green]Tests generated successfully in \
                {output_base}/[/bold green]"
        )
        console.print("\n[bold cyan]Next steps:[/bold cyan]")
        console.print("1. Review generated tests in the output directory")
        console.print("2. Copy relevant tests to your project's test directory")
        console.print("3. Adjust import paths if necessary")
        console.print(f"4. Run: [dim]pytest {output_dir}/[/dim] to test them")
    else:
        console.print("\n[yellow]Dry run completed. No files were created.[/yellow]")


def clean_temp_files(verbose: bool = True):
    """Remove temporary files and directories created during test generation."""
    import subprocess

    if verbose:
        console.print("\n[dim]Cleaning up temporary files...[/dim]")

    # Commands to clean up common Python temporary files and directories
    commands = [
        "find . -type f -name '*.pyc' -delete",
        "find . -type d -name '__pycache__' -exec rm -rf {} +",
        "find . -type d -name '*.egg-info' -exec rm -rf {} +",
        "find . -type f -name '.coverage' -delete",
        "find . -type d -name 'htmlcov' -exec rm -rf {} +",
        "find . -type d -name '.pytest_cache' -exec rm -rf {} +",
        "find . -type d -name '.mypy_cache' -exec rm -rf {} +",
        "find . -type d -name '.ruff_cache' -exec rm -rf {} +",
    ]

    for command in commands:
        try:
            subprocess.run(
                command, shell=True, check=True, capture_output=True, text=True
            )
        except subprocess.CalledProcessError:
            pass


def process_file(
    file_path: Path,
    output_base: Path,
    mirror_structure: bool,
    verbose: bool,
    dry_run: bool,
    base_path: Optional[Path] = None,
):
    """Process a single Python file to generate tests.

    Args:
        file_path (Path): The path to the Python file to process.
        output_base (Path): The base directory for output files.
        mirror_structure (bool): Whether to mirror the source directory structure.
        verbose (bool): Whether to print verbose output.
        dry_run (bool): Whether to perform a dry run (no file modifications).
        base_path (Optional[Path], optional): The base directory for the source files.
        Defaults to None.
    """
    if verbose:
        console.log(f"Extracting imports and functions from {file_path.name}")

    with console.status(
        f"[bold green]Generating tests for {file_path.name}...[/bold green]",
        spinner="dots",
    ):
        try:
            imports_code, functions_data = source_code_analysis(str(file_path))
        except Exception as e:
            console.print(f"[red]Failed to analyze {file_path.name}: {e}[/red]")
            return

        if not functions_data:
            if verbose:
                console.print(
                    f"[yellow]No functions found in {file_path.name}[/yellow]"
                )
            return

        # Determine output directory
        if mirror_structure and base_path:
            # Mirror the source structure in output
            rel_path = file_path.relative_to(base_path)
            test_dir = output_base / rel_path.parent
        else:
            # Flat structure - all tests in output_base
            test_dir = output_base

        if not dry_run:
            test_dir.mkdir(parents=True, exist_ok=True)

        if verbose:
            console.print(f"[dim]Test output directory: {test_dir}[/dim]")

        module_import_path = calculate_import_path_simple(file_path)

        all_test_functions = []
        all_imports = set()

        # Process each function in the file
        for i, func_data in enumerate(functions_data):
            function_name = func_data["function_name"]

            if verbose:
                console.log(
                    f"\n  → Processing function {i + 1}/{len(functions_data)}: \
                            [cyan]{function_name}[/cyan]"
                )

            # Generate prompt based on whether it's a class method
            # or standalone function
            if func_data["parent_class_code"]:
                if verbose:
                    console.log("    Class method detected")

                prompt = generate_class_method_prompt(
                    imports_code, function_name, func_data["parent_class_code"]
                )
            else:
                if verbose:
                    console.log("    Standalone function detected")

                prompt = generate_standalone_prompt(
                    imports_code, func_data["function_code"]
                )

            if verbose:
                console.log("    Sending to LLM...")

            if not dry_run:
                raw_response = generate_test_code(prompt)

                clean_code = postprocess_test_code_enhanced(
                    raw_response, function_name, module_import_path, file_path.stem
                )

                test_imports, test_functions = extract_imports_and_functions(clean_code)

                valid_functions = [
                    f for f in test_functions if f.strip() and "def test_" in f
                ]

                if valid_functions:
                    all_imports.update(test_imports)
                    all_test_functions.extend(valid_functions)
                    console.print(
                        f"    ✓ Generated {len(valid_functions)} \
                            test(s) for [green]{function_name}[/green]"
                    )
                else:
                    console.print(
                        f"    ⚠️ No valid tests generated for \
                                  [yellow]{function_name}[/yellow]"
                    )
            else:
                console.print(f"    [dim]Would generate test for {function_name}[/dim]")

        if not dry_run and all_test_functions:
            # Combine all tests into a single file
            combined_test_code = combine_test_code(
                all_imports, all_test_functions, file_path.stem, module_import_path
            )

            # Write the combined test file
            test_file_name = f"test_{file_path.stem}.py"
            test_file_path = test_dir / test_file_name

            with open(test_file_path, "w", encoding="utf-8") as f:
                f.write(combined_test_code)

            rel_test_path = test_file_path.relative_to(output_base)
            console.print(
                f"\n  📄 Test file created: [bold green]\
                {output_base}/{rel_test_path}[/bold green]"
            )
            console.print(f"     Contains {len(all_test_functions)} test functions")


def extract_imports_and_functions(test_code: str) -> tuple[set, list]:
    """
    Extract imports and test functions from generated test code.

    Args:
        test_code (str): The generated test code.

    Returns:
        tuple: (set of import statements, list of test function code blocks)
    """
    lines = test_code.strip().split("\n")
    imports = set()
    functions = []
    current_function: list[str] = []
    in_function = False
    decorator_lines = []

    for line in lines:
        # Skip malformed lines and comments
        if line.strip() == ")" or line.strip().startswith("#") and not in_function:
            continue

        # Check if it's an import statement
        if line.strip().startswith(("import ", "from ")) and not in_function:
            # Clean up malformed imports
            if "from test_" not in line and "TODO:" not in line:
                imports.add(line.strip())
        # Handle decorators
        elif line.strip().startswith("@"):
            if current_function:
                # Save the previous function
                functions.append("\n".join(current_function))
                current_function = []
            decorator_lines.append(line)
            in_function = False
        # Check if it's the start of a function
        elif line.startswith("def test_"):
            if current_function:
                # Save the previous function
                functions.append("\n".join(current_function))
                current_function = []
            # Add any decorators to this function
            if decorator_lines:
                current_function.extend(decorator_lines)
                decorator_lines = []
            in_function = True
            current_function.append(line)
        # If we're in a function, keep adding lines
        elif in_function:
            # Check if this line is not indented (end of function)
            if line and not line[0].isspace() and not line.startswith(("@", "#")):
                # End of function - check if it's complete
                if current_function and len("\n".join(current_function).strip()) > 0:
                    functions.append("\n".join(current_function))
                current_function = []
                in_function = False
                decorator_lines = []
                # Check if this line is an import
                if line.strip().startswith(("import ", "from ")):
                    if "from test_" not in line and "TODO:" not in line:
                        imports.add(line.strip())
            else:
                current_function.append(line)

    # Don't forget the last function if it's complete
    if current_function and len("\n".join(current_function).strip()) > 0:
        # Check if function is complete (has at least assert or pass)
        func_content = "\n".join(current_function)
        if (
            "assert" in func_content
            or "pass" in func_content
            or "raise" in func_content
        ):
            functions.append(func_content)

    # Remove duplicate functions (same name)
    seen_names = set()
    unique_functions = []
    for func in functions:
        # Extract function name
        for line in func.split("\n"):
            if line.startswith("def test_"):
                func_name = line.split("(")[0].replace("def ", "")
                if func_name not in seen_names:
                    seen_names.add(func_name)
                    unique_functions.append(func)
                break

    return imports, unique_functions


def combine_test_code(
    imports: set, test_functions: list, module_name: str, module_import_path: str
) -> str:
    """
    Combine imports and test functions into a single, well-formatted test file.

    Args:
        imports: Set of import statements
        test_functions: List of test function code blocks
        module_name: Name of the module being tested
        module_import_path: Import path for the module

    Returns:
        str: Complete test file content
    """
    # Organize imports
    stdlib_imports = []
    third_party_imports = []
    local_imports = []

    # Common standard library modules
    stdlib_modules = [
        "unittest",
        "datetime",
        "os",
        "sys",
        "json",
        "typing",
        "collections",
        "itertools",
        "functools",
        "pathlib",
        "re",
    ]

    # Common third-party test modules
    third_party_modules = [
        "pytest",
        "mock",
        "unittest.mock",
        "numpy",
        "pandas",
        "requests",
        "flask",
        "django",
        "fastapi",
    ]

    for imp in sorted(imports):
        # Skip malformed imports
        if not imp.startswith(("import ", "from ")):
            continue

        # Determine import type
        is_stdlib = any(module in imp for module in stdlib_modules)
        is_third_party = any(module in imp for module in third_party_modules)

        if is_stdlib:
            stdlib_imports.append(imp)
        elif is_third_party:
            third_party_imports.append(imp)
        elif module_import_path in imp or imp.startswith(f"from {module_import_path}"):
            local_imports.append(imp)
        else:
            # Default to third-party for unknown imports
            third_party_imports.append(imp)

    # Build the file content
    content_parts = []

    # Add file docstring
    content_parts.append(f'"""Tests for {module_name} module."""')
    content_parts.append("")

    # Add imports (PEP 8: standard library, blank line, third-party, blank line, local)
    if stdlib_imports:
        content_parts.extend(stdlib_imports)
        content_parts.append("")

    # Always include pytest if not already present
    if not any("pytest" in imp for imp in third_party_imports):
        third_party_imports.insert(0, "import pytest")

    if third_party_imports:
        content_parts.extend(third_party_imports)
        content_parts.append("")

    if local_imports:
        # Deduplicate and refine local imports
        refined_imports = refine_local_imports(
            local_imports, module_import_path, module_name
        )
        content_parts.extend(refined_imports)
        content_parts.append("")

    # Add two blank lines before test functions (PEP 8)
    content_parts.append("")

    # Add test functions with proper spacing
    for i, func in enumerate(test_functions):
        if i > 0:
            content_parts.append("")  # Two blank lines between functions
            content_parts.append("")
        content_parts.append(func)

    # Add final newline
    content_parts.append("")

    return "\n".join(content_parts)


def refine_local_imports(
    imports: list, module_import_path: str, file_stem: str
) -> list:
    """
    Refine local imports to avoid duplicates and ensure correctness.

    Args:
        imports: List of import statements
        module_import_path: The correct import path for the module
        file_stem: The name of the file without extension

    Returns:
        list: Refined import statements
    """
    refined = set()
    imported_items = set()

    # Common placeholder modules that LLMs use
    placeholder_modules = [
        "some_module",
        "your_module",
        "module_name",
        "my_module",
        "sample_module",
        "<module_name>",
        "path.to.module",
        "test_" + file_stem,  # Avoid self-imports
        file_stem if file_stem.startswith("test_") else None,
    ]

    for imp in imports:
        # Skip malformed imports
        if ")" in imp and "import" not in imp:
            continue

        # Skip TODO comments
        if "TODO:" in imp or "#" in imp:
            continue

        # Replace placeholder modules with actual module path
        for placeholder in placeholder_modules:
            if placeholder and placeholder in imp:
                imp = imp.replace(placeholder, module_import_path)

        # Parse the import statement
        if "from " in imp and " import " in imp:
            parts = imp.split(" import ")
            if len(parts) == 2:
                from_part = parts[0].replace("from ", "").strip()
                import_part = parts[1].strip()

                # Skip if it's trying to import from the test file itself
                if "test_" in from_part:
                    continue

                # Use the correct module path for local imports
                if from_part in placeholder_modules or from_part == module_import_path:
                    from_part = module_import_path

                # Handle multiple imports
                items = [item.strip() for item in import_part.split(",")]
                for item in items:
                    if item and item != "*":
                        import_key = f"{from_part}.{item}"
                        if import_key not in imported_items:
                            imported_items.add(import_key)
                            refined.add(f"from {from_part} import {item}")
        elif imp.startswith("import "):
            # Handle simple imports
            module = imp.replace("import ", "").strip()
            if module not in placeholder_modules and "test_" not in module:
                refined.add(imp)

    # If no specific imports were found, add a generic one
    if not any(module_import_path in imp for imp in refined):
        # Try to import the specific function being tested
        refined.add(f"from {module_import_path} import *")

    return sorted(list(refined))


def append_test_to_file(test_file_path: Path, test_code: str, function_name: str):
    """Append a test function to an existing test file or create a new one.

    Args:
        test_file_path (Path): The path to the test file.
        test_code (str): The code of the test function.
        function_name (str): The name of the function being tested.
    """

    if test_file_path.exists():
        with open(test_file_path, "r", encoding="utf-8") as f:
            existing_content = f.read()

        new_imports, new_functions = extract_imports_and_functions(test_code)
        existing_imports, existing_functions = extract_imports_and_functions(
            existing_content
        )

        all_imports = existing_imports.union(new_imports)
        all_functions = existing_functions + new_functions

        # Get module info from the existing imports
        module_import_path = None
        for imp in existing_imports:
            if "from " in imp and " import " in imp and "pytest" not in imp:
                module_import_path = (
                    imp.split(" import ")[0].replace("from ", "").strip()
                )
                break

        if not module_import_path:
            module_import_path = "your_module"  # Fallback

        combined_code = combine_test_code(
            all_imports,
            all_functions,
            test_file_path.stem.replace("test_", ""),
            module_import_path,
        )

        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(combined_code)
    else:
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(test_code)


def calculate_import_path_simple(file_path: Path) -> str:
    """Generate a reasonable import path for the module.

    Users will need to adjust this in their actual test files.

    Args:
        file_path (Path): The path to the file for which to generate the import path.

    Returns:
        str: The calculated import path.
    """

    # Try to make a reasonable guess at the import path
    parts: list[str] = []
    current = file_path.parent

    # Walk up until we find a reasonable root (has __init__.py or is a common root)
    while current.name and (current / "__init__.py").exists():
        parts.insert(0, current.name)
        current = current.parent

    # Add the module name
    parts.append(file_path.stem)

    # If we found no package structure, just use the module name
    if len(parts) == 1:
        return file_path.stem

    return ".".join(parts)


def postprocess_test_code_enhanced(
    test_code: str,
    function_name: str,
    module_import_path: str,
    module_name: str,
) -> str:
    """Enhanced post-processing that handles import paths correctly \
    for any project structure.

    Args:
        test_code (str): The test code to process.
        function_name (str): The name of the function being tested.
        module_import_path (str): The import path of the module being tested.
        module_name (str): The name of the module being tested.

    Returns:
        str: The processed test code.
    """

    import re

    # Remove markdown code blocks if present
    test_code = re.sub(r"```(?:python)?", "", test_code)
    test_code = test_code.strip("```").strip()

    placeholders = [
        "your_module",
        "module_name",
        "my_module",
        "sample_module",
        "<module_name>",
        "path.to.module",
    ]

    for placeholder in placeholders:
        test_code = test_code.replace(
            f"from {placeholder}", f"from {module_import_path}"
        )
        test_code = test_code.replace(
            f"import {placeholder}", f"import {module_import_path}"
        )

    if "from ." in test_code:
        # Convert relative imports to absolute based on test location
        test_code = re.sub(
            r"from \.([\w\.]*) import",
            f"from {module_import_path}\\1 import",
            test_code,
        )

    # Ensure the import statement exists if not present
    if module_import_path not in test_code and function_name in test_code:
        import_line = f"from {module_import_path} import {function_name}\n\n"
        if not test_code.startswith("import") and not test_code.startswith("from"):
            test_code = import_line + test_code

    # Clean up any double imports or malformed imports
    lines = test_code.split("\n")
    seen_imports = set()
    cleaned_lines = []

    for line in lines:
        if line.strip().startswith(("import ", "from ")):
            if line not in seen_imports:
                seen_imports.add(line)
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


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
    prompt = prompt_template.replace("{{function_code}}", function_code)
    return prompt
