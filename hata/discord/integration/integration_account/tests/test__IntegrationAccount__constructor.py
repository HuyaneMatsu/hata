import vampytest

from ..integration_account import IntegrationAccount


def _check_is_every_attribute_set(integration_account):
    """
    Checks whether every attribute of the given integration account is set.
    
    Parameters
    ----------
    integration_account : ``IntegrationAccount``
        The integration account to check.
    """
    vampytest.assert_instance(integration_account, IntegrationAccount)
    
    vampytest.assert_instance(integration_account.id, str)
    vampytest.assert_instance(integration_account.name, str)


def test__IntegrationAccount__new__0():
    """
    Tests whether ``IntegrationAccount.__new__`` works as intended.
    
    Case: no fields given.
    """
    integration_account = IntegrationAccount()
    _check_is_every_attribute_set(integration_account)


def test__IntegrationAccount__new__1():
    """
    Tests whether ``IntegrationAccount.__new__`` works as intended.
    
    Case: all fields given.
    """
    integration_account_id = 'forlane'
    name = 'sana'
    
    integration_account = IntegrationAccount(integration_account_id, name)
    _check_is_every_attribute_set(integration_account)
    
    vampytest.assert_eq(integration_account.id, integration_account_id)
    vampytest.assert_eq(integration_account.name, name)


def test__IntegrationAccount__create_empty():
    """
    Tests whether ``IntegrationAccount._create_empty`` works as intended.
    """
    integration_account = IntegrationAccount._create_empty()
    _check_is_every_attribute_set(integration_account)
