import vampytest

from ...integration_account import IntegrationAccount

from ..fields import put_account_into


def test__put_account_into():
    """
    Tests whether ``put_account_into`` works as intended.
    """
    account = IntegrationAccount('hello', 'hell')
    
    for input_value, expected_output in (
        (account, {'account': account.to_data()}),
    ):
        data = put_account_into(input_value, {}, True)
        vampytest.assert_eq(data, expected_output)
