import vampytest

from ....user import User

from ...integration_account import IntegrationAccount

from ..fields import put_account__discord


def test__put_account__discord():
    """
    Tests whether ``put_account__discord`` works as intended.
    """
    account_id = 202210140016
    name = 'hell'
    
    account = IntegrationAccount(str(account_id), name)
    user = User.precreate(account_id, name = name, bot = True)
    
    for input_value, expected_output in (
        (user, {'account': account.to_data()}),
    ):
        data = put_account__discord(input_value, {}, True)
        vampytest.assert_eq(data, expected_output)
