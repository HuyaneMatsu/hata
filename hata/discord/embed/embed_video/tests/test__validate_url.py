import vampytest

from ..fields import validate_url


def test__validate_url__0():
    """
    Tests whether `validate_url` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        ('https://orindance.party/', 'https://orindance.party/'),
        ('attachment://koishi.png', 'attachment://koishi.png'),
    ):
        output = validate_url(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_url__1():
    """
    Tests whether `validate_url` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_url(input_value)
