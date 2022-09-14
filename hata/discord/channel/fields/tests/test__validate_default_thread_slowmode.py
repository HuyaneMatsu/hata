import vampytest

from ..default_thread_slowmode import validate_default_thread_slowmode


def test__validate_default_thread_slowmode__0():
    """
    Validates whether ``validate_default_thread_slowmode`` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (0, 0),
    ):
        output = validate_default_thread_slowmode(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_default_thread_slowmode__1():
    """
    Validates whether ``validate_default_thread_slowmode`` works as intended.
    
    Case: value error.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_default_thread_slowmode(input_value)



def test__validate_default_thread_slowmode__2():
    """
    Validates whether ``validate_default_thread_slowmode`` works as intended.
    
    Case: type error.
    """
    for input_value in (
        '',
    ):
        with vampytest.assert_raises(TypeError):
            validate_default_thread_slowmode(input_value)
