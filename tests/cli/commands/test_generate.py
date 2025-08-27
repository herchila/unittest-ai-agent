"""Tests for generate module."""
from unittest.mock import patch

from ut.cli.commands.generate import generate


def test_generate_happy_path_file(tmp_path):
    """Test the generate function with a single file input."""

    # Arrange
    source_file = tmp_path / "my_test_module.py"
    source_file.write_text("def hello(): pass")

    # Act
    with patch("ut.cli.commands.generate.typer.confirm", return_value=True), patch(
        "ut.cli.commands.generate.generate_test_code"
    ), patch("ut.cli.commands.generate.process_file") as mock_process, patch(
        "ut.cli.commands.generate.console"
    ), patch(
        "ut.cli.commands.generate.clean_temp_files"
    ) as mock_clean:
        generate(
            file_path=source_file,
            output_dir=str(tmp_path),
            recursive=True,
            verbose=True,
            dry_run=False,
            mirror_structure=True,
        )

    # Assert
    mock_process.assert_called_once()
    mock_clean.assert_called()
