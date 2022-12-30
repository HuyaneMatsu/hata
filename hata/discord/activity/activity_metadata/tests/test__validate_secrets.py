import vampytest

from ...activity_secrets import ActivitySecrets

from ..fields import validate_secrets


def test__validate_secrets__0():
    """
    Tests whether `validate_secrets` works as intended.
    
    Case: passing.
    """
    secrets = ActivitySecrets(join = 'hell')
    
    for input_value, expected_output in (
        (None, None),
        (secrets, secrets),
    ):
        output = validate_secrets(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_secrets__1():
    """
    Tests whether `validate_secrets` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_secrets(input_value)
