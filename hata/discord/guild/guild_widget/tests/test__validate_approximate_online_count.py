import vampytest

from ..fields import validate_approximate_online_count


def test__validate_approximate_online_count__0():
    """
    Tests whether `validate_approximate_online_count` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (1, 1),
    ):
        output = validate_approximate_online_count(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_approximate_online_count__1():
    """
    Tests whether `validate_approximate_online_count` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        -1,
    ):
        with vampytest.assert_raises(ValueError):
            validate_approximate_online_count(input_value)


def test__validate_approximate_online_count__2():
    """
    Tests whether `validate_approximate_online_count` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_approximate_online_count(input_value)
