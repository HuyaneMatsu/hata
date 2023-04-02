import vampytest

from ..fields import validate_icon_url


def test__validate_icon_url__0():
    """
    Tests whether `validate_icon_url` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('attachment://orin.png', 'attachment://orin.png'),
        ('https://orindance.party/', 'https://orindance.party/'),
    ):
        output = validate_icon_url(input_value)
        vampytest.assert_eq(output, expected_output)
