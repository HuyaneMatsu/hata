import vampytest

from ...integration_account import IntegrationAccount

from ..fields import validate_account


def test__validate_account__0():
    """
    Tests whether ``validate_account`` works as intended.
    
    Case: Passing.
    """
    account = IntegrationAccount('hello', 'hell')
    
    for input_value, expected_output in (
        (None, IntegrationAccount._create_empty()),
        (account, account),
    ):
        output = validate_account(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_account__1():
    """
    Tests whether ``validate_account`` works as intended.
    
    Case: `TypeError`
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_account(input_value)
