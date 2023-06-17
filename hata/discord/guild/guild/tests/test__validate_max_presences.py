import vampytest

from ..constants import MAX_PRESENCES_DEFAULT
from ..fields import validate_max_presences


def test__validate_max_presences__0():
    """
    Tests whether `validate_max_presences` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, MAX_PRESENCES_DEFAULT),
        (0, 0),
        (1, 1),
    ):
        output = validate_max_presences(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_max_presences__1():
    """
    Tests whether `validate_max_presences` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_max_presences(input_value)


def test__validate_max_presences__2():
    """
    Tests whether `validate_max_presences` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_max_presences(input_value)
