import vampytest

from ....user import User

from ..integration_account import IntegrationAccount

from .test__IntegrationAccount__constructor import _assert_fields_set


def test__IntegrationAccount__from_data():
    """
    Tests whether ``IntegrationAccount.from_data`` works as intended.
    """
    integration_account_id = 202210100000
    name = 'sana'
    
    data = {
        'id': str(integration_account_id),
        'name': name
    }
    
    integration_account = IntegrationAccount.from_data(data)
    _assert_fields_set(integration_account)
    
    vampytest.assert_eq(integration_account.id, str(integration_account_id))
    vampytest.assert_eq(integration_account.name, name)


def test__IntegrationAccount__to_data():
    """
    Tests whether ``IntegrationAccount.to_data`` works as intended.
    """
    integration_account_id = 'forlane'
    name = 'sana'
    
    integration_account = IntegrationAccount(integration_account_id, name)
    
    expected_data = {
        'id': integration_account_id,
        'name': name,
    }
    
    vampytest.assert_eq(
        integration_account.to_data(),
        expected_data,
    )
