from example.converter import convert_date_to_iso


def test_convert_date_to_iso():
    # Arrange
    date_str = "18/07/2025"
    expected = "2025-07-18"

    # Act
    result = convert_date_to_iso(date_str)

    # Assert
    assert result == expected


def test_convert_date_to_iso_valid_date_custom_format():
    # Arrange
    date_str = "07-18-2025"
    format = "%m-%d-%Y"
    expected = "2025-07-18"

    # Act
    result = convert_date_to_iso(date_str, format)

    # Assert
    assert result == expected


def test_convert_date_to_iso_empty_string():
    # Arrange
    date_str = ""

    # Act
    result = convert_date_to_iso(date_str)

    # Assert
    assert result is None


def test_convert_date_to_iso_none_input():
    # Arrange
    date_str = None

    # Act
    result = convert_date_to_iso(date_str)

    # Assert
    assert result is None


def test_convert_date_to_iso_invalid_format():
    # Arrange
    date_str = "18/07/2025"
    format = "%Y-%d-%m"

    # Act
    result = convert_date_to_iso(date_str, format)

    # Assert
    assert result is None


def test_convert_date_to_iso_invalid_date_string():
    # Arrange
    date_str = "invalid_date"

    # Act
    result = convert_date_to_iso(date_str)

    # Assert
    assert result is None


def test_convert_date_to_iso_invalid_type():
    # Arrange
    date_str = 12345
    # Act
    result = convert_date_to_iso(date_str)

    # Assert
    assert result is None


def test_convert_date_to_iso_invalid_format_type():
    # Arrange
    date_str = "18/07/2025"
    format = 12345

    # Act
    result = convert_date_to_iso(date_str, format)

    # Assert
    assert result == "2025-07-18"  # Default format should be used


def test_convert_date_to_iso_whitespace_format():
    # Arrange
    date_str = "18/07/2025"
    format = "   "

    # Act
    result = convert_date_to_iso(date_str, format)

    # Assert
    assert result == "2025-07-18"  # Default format should be used


def test_convert_date_to_iso_leap_year():
    # Arrange
    date_str = "29/02/2024"
    expected = "2024-02-29"

    # Act
    result = convert_date_to_iso(date_str, format)

    # Assert
    assert result == expected
