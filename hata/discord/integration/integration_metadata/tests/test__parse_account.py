import vampytest

from ...integration_account import IntegrationAccount

from ..fields import parse_account


def test__parse_account():
    """
    Tests whether ``parse_account`` works as intended.
    """
    account = IntegrationAccount('hello', 'hell')
    
    for data, expected_output in (
        ({}, IntegrationAccount._create_empty()),
        ({'account': None}, IntegrationAccount._create_empty()),
        ({'account': account.to_data()}, account),
    ):
        output = parse_account(data)
        vampytest.assert_eq(output, expected_output)
