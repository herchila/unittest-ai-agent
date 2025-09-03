"""Helper functions for CLI commands."""
from rich.console import Console


def verbose_message(message: str, verbose: bool, print_func: Console) -> None:
    """Print a message if verbose is enabled.

    Args:
        message (str): The message to print.
        verbose (bool): Flag indicating if verbose mode is enabled.
        print_func (Console): The print function to use
            (e.g., console.print or console.log).
    """
    if verbose:
        print_func(message)


def verbose_print(message: str, verbose: bool):
    """Print a message if verbose is enabled.

    Args:
        message (str): The message to print.
        verbose (bool): Flag indicating if verbose mode is enabled.
    """
    verbose_message(message, verbose, Console().print)


def verbose_log(message: str, verbose: bool):
    """Print a log message if verbose is enabled.

    Args:
        message (str): The message to log.
        verbose (bool): Flag indicating if verbose mode is enabled.
    """
    verbose_message(message, verbose, Console().log)


def clean_temp_files(verbose: bool = True):
    """Remove temporary files and directories created during test generation.

    Args:
        verbose (bool, optional): Flag indicating if verbose mode is enabled.
            Defaults to True.
    """
    import subprocess

    verbose_print("\n[dim]Cleaning up temporary files...[/dim]", verbose)

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
