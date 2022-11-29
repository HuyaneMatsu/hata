import vampytest

from ..fields import validate_custom_install_url


def test__validate_custom_install_url__0():
    """
    Tests whether `validate_custom_install_url` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('https://orindance.party/', 'https://orindance.party/'),
    ):
        output = validate_custom_install_url(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_custom_install_url__1():
    """
    Tests whether `validate_custom_install_url` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(ValueError):
            validate_custom_install_url(input_value)


def test__validate_custom_install_url__2():
    """
    Tests whether `validate_custom_install_url` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_custom_install_url(input_value)
