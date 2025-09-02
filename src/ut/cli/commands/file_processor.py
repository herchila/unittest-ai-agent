"""Automated Unit Test Generation CLI with AI."""
from pathlib import Path
from typing import Optional

from rich.console import Console

from ut.cli.commands.constants import DEF_TEST_STRING
from ut.cli.commands.helper import verbose_log, verbose_print
from ut.llm_client import generate_test_code
from ut.parser import calculate_import_path_simple, source_code_analysis
from ut.prompts.prompt_builder import (
    generate_class_method_prompt,
    generate_standalone_prompt,
)
from ut.test_writer import (
    combine_test_code,
    extract_imports_and_functions,
    postprocess_test_code_enhanced,
)

console = Console()


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
    verbose_log(f"Extracting imports and functions from {file_path.name}", verbose)

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

        verbose_print(f"[dim]Test output directory: {test_dir}[/dim]", verbose)

        module_import_path = calculate_import_path_simple(file_path)

        all_test_functions = []
        all_imports = set()

        # Process each function in the file
        for i, func_data in enumerate(functions_data):
            function_name = func_data["function_name"]

            verbose_log(
                f"\n  → Processing function {i + 1}/{len(functions_data)}: \
                            [cyan]{function_name}[/cyan]",
                verbose,
            )

            # Generate prompt based on whether it's a class method
            # or standalone function
            if func_data["parent_class_code"]:
                verbose_log("    Class method detected", verbose)

                prompt = generate_class_method_prompt(
                    imports_code, function_name, func_data["parent_class_code"]
                )
            else:
                verbose_log("    Standalone function detected", verbose)

                prompt = generate_standalone_prompt(
                    imports_code, func_data["function_code"]
                )

            verbose_log("    Sending to LLM...", verbose)

            if not dry_run:
                raw_response = generate_test_code(prompt)

                clean_code = postprocess_test_code_enhanced(
                    raw_response, function_name, module_import_path, file_path.stem
                )

                test_imports, test_functions = extract_imports_and_functions(clean_code)

                valid_functions = [
                    f for f in test_functions if f.strip() and DEF_TEST_STRING in f
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
