"""Automated Unit Test Generation CLI with AI."""

from typing import Optional

import typer
from typing_extensions import Annotated

from ut.cli.commands.generate import generate

app = typer.Typer(help="Automated Unit Test Generation CLI")

__version__ = "0.1.0"

app.command("generate")(generate)


def _version_cb(v: bool):
    if v:
        typer.echo(f"ut {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            help="Show version and exit.",
            callback=_version_cb,
            is_eager=True,
        ),
    ] = None,
    verbose: Annotated[
        bool, typer.Option("--verbose", help="Enable verbose output.")
    ] = False,
):
    """Entry point for the CLI.

    Args:
        ctx (typer.Context): The context object for the CLI.
        version (Annotated[ Optional[bool], typer.Option, optional): Show version.
        verbose (Annotated[ bool, typer.Option, optional): Enable verbose output.
    """

    ctx.obj = {"verbose": verbose}


if __name__ == "__main__":
    app()
