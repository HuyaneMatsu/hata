import vampytest

from ..fields import validate_version


def test__validate_version__0():
    """
    Tests whether `validate_version` works as intended.
    
    Case: passing.
    """
    version = 202302260011
    
    for input_value, expected_output in (
        (version, version),
        (str(version), version),
    ):
        output = validate_version(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_version__1():
    """
    Tests whether `validate_version` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '-1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_version(input_value)


def test__validate_version__2():
    """
    Tests whether `validate_version` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_version(input_value)
