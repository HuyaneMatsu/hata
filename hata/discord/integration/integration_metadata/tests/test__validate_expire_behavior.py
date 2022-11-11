import vampytest

from ..fields import validate_expire_behavior
from ..preinstanced import IntegrationExpireBehavior


def test__validate_expire_behavior__0():
    """
    Tests whether `validate_expire_behavior` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (IntegrationExpireBehavior.kick, IntegrationExpireBehavior.kick),
        (IntegrationExpireBehavior.kick.value, IntegrationExpireBehavior.kick)
    ):
        output = validate_expire_behavior(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_expire_behavior__1():
    """
    Tests whether `validate_expire_behavior` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_expire_behavior(input_value)
