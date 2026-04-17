import vampytest

from ...integration_account import IntegrationAccount

from ..fields import put_account


def test__put_account():
    """
    Tests whether ``put_account`` works as intended.
    """
    account = IntegrationAccount('hello', 'hell')
    
    for input_value, expected_output in (
        (account, {'account': account.to_data()}),
    ):
        data = put_account(input_value, {}, True)
        vampytest.assert_eq(data, expected_output)
