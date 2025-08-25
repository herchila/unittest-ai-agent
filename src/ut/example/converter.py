"""Automated Unit Test Generation CLI with AI."""

from datetime import datetime


def convert_date_to_iso(date_str: str, format: str = "%d/%m/%Y") -> str | None:
    """Convert a date in string format to ISO 8601 format.

    Args:
        date_str (str): The date as a string, for example "18/07/2025".
        format (str): The format of the date.

    Returns:
        str: The date in ISO format, for example "2025-07-18".
    """
    if not date_str or not isinstance(date_str, str):
        return None

    try:
        format = str(format).strip()
    except Exception:
        format = "%d/%m/%Y"

    try:
        date = datetime.strptime(date_str, format)
        return date.date().isoformat()
    except ValueError:
        return None
