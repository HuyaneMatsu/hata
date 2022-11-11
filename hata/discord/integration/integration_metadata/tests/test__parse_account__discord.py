import vampytest

from ....user import User

from ...integration_account import IntegrationAccount

from ..fields import parse_account__discord


def test__parse_account__discord():
    """
    Tests whether ``parse_account__discord`` works as intended.
    """
    account_id = 202210140015
    name = 'hell'
    
    account = IntegrationAccount(str(account_id), name)
    user = User.precreate(account_id, name = name, bot = True)
    
    for data, expected_output in (
        ({}, IntegrationAccount._create_empty()),
        ({'account': None}, IntegrationAccount._create_empty()),
        ({'account': account.to_data()}, user),
    ):
        output = parse_account__discord(data)
        vampytest.assert_eq(output, expected_output)
