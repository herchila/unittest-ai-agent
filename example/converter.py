from datetime import datetime


def convert_date_to_iso(date_str, format="%d/%m/%Y"):
    """
    Converts a date in string format to ISO 8601 format.

    Args:
        date_str (str): The date as a string, for example "18/07/2025".
        format (str): The format of the date.

    Returns:
        str: The date in ISO format, for example "2025-07-18".
    """
    try:
        date = datetime.strptime(date_str, format)
        return date.date().isoformat()
    except ValueError:
        return None
