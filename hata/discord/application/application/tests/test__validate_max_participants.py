import vampytest

from ..constants import MAX_PARTICIPANTS_DEFAULT
from ..fields import validate_max_participants


def test__validate_max_participants__0():
    """
    Validates whether ``validate_max_participants`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (MAX_PARTICIPANTS_DEFAULT, MAX_PARTICIPANTS_DEFAULT),
        (1, 1),
    ):
        output = validate_max_participants(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_max_participants__1():
    """
    Validates whether ``validate_max_participants`` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_max_participants(input_value)



def test__validate_max_participants__2():
    """
    Validates whether ``validate_max_participants`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        '',
    ):
        with vampytest.assert_raises(TypeError):
            validate_max_participants(input_value)
