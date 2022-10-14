import vampytest

from ..integration_account import IntegrationAccount


def test__IntegrationAccount__repr():
    """
    Tests whether ``IntegrationAccount.__repr__`` works as intended.
    """
    integration_account_id = 'hana'
    name = 'cover'
    
    integration_account = IntegrationAccount(integration_account_id, name)
    
    vampytest.assert_instance(repr(integration_account), str)


def test__IntegrationAccount__hash():
    """
    Tests whether ``IntegrationAccount.__hash__`` works as intended.
    """
    integration_account_id = 'hana'
    name = 'cover'
    
    integration_account = IntegrationAccount(integration_account_id, name)
    
    vampytest.assert_instance(hash(integration_account), int)


def test__IntegrationAccount__eq():
    """
    Tests whether ``IntegrationAccount.__eq__`` works as intended.
    """
    integration_account_id = 'hana'
    name = 'cover'
    
    keyword_parameters = {
        'integration_account_id': integration_account_id,
        'name': name,
    }
    
    integration_account = IntegrationAccount(**keyword_parameters)
    
    vampytest.assert_eq(integration_account, integration_account)
    vampytest.assert_ne(integration_account, object())
    
    for field_name, field_value in (
        ('integration_account_id', 'forlane'),
        ('name', 'sana'),
    ):
        test_integration_account = IntegrationAccount(**{**keyword_parameters, field_name: field_value})
        
        vampytest.assert_ne(integration_account, test_integration_account)
