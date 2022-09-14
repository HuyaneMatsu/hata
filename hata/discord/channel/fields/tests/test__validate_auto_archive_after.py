import vampytest

from ...constants import AUTO_ARCHIVE_DEFAULT

from ..auto_archive_after import validate_auto_archive_after


def test__validate_auto_archive_after__0():
    """
    Tests whether ``validate_auto_archive_after`` works as intended.
    
    Case: passing.
    """
    for input_parameter, expected_output in (
        (AUTO_ARCHIVE_DEFAULT, AUTO_ARCHIVE_DEFAULT),
    ):
        output = validate_auto_archive_after(input_parameter)
        vampytest.assert_eq(output, expected_output)


def test__validate_auto_archive_after__1():
    """
    Tests whether ``validate_auto_archive_after`` works as intended.
    
    Case: value error.
    """
    for input_parameter in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_auto_archive_after(input_parameter)


def test__validate_auto_archive_after__2():
    """
    Tests whether ``validate_auto_archive_after`` works as intended.
    
    Case: type error.
    """
    for input_parameter in (
        '',
    ):
        with vampytest.assert_raises(TypeError):
            validate_auto_archive_after(input_parameter)
