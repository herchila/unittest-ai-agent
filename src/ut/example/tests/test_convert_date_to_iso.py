from ut.example.converter import convert_date_to_iso


def test_convert_date_to_iso():
    # Arrange
    date_str = "18/07/2025"
    expected_result = "2025-07-18"

    # Act
    result = convert_date_to_iso(date_str)

    # Assert
    assert result == expected_result


def test_convert_date_to_iso_different_format():
    # Arrange
    date_str = "2025-07-18"
    format = "%Y-%m-%d"
    expected_result = "2025-07-18"

    # Act
    result = convert_date_to_iso(date_str, format)

    # Assert
    assert result == expected_result


def test_convert_date_to_iso_invalid_format():
    # Arrange
    date_str = "18-07-2025"
    format = "%d/%m/%Y"

    # Act
    result = convert_date_to_iso(date_str, format)

    # Assert
    assert result is None


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


def test_convert_date_to_iso_invalid_type_integer():
    # Arrange
    date_str = 123456

    # Act
    result = convert_date_to_iso(date_str)

    # Assert
    assert result is None


def test_convert_date_to_iso_invalid_type_list():
    # Arrange
    date_str = ["18/07/2025"]

    # Act
    result = convert_date_to_iso(date_str)

    # Assert
    assert result is None


def test_convert_date_to_iso_invalid_date():
    # Arrange
    date_str = "31/02/2025"

    # Act
    result = convert_date_to_iso(date_str)

    # Assert
    assert result is None


def test_convert_date_to_iso_leap_year():
    # Arrange
    date_str = "29/02/2024"
    expected_result = "2024-02-29"

    # Act
    result = convert_date_to_iso(date_str)

    # Assert
    assert result == expected_result
