import vampytest

from ..integration_account import IntegrationAccount

from .test__IntegrationAccount__constructor import _check_is_every_attribute_set


def test__IntegrationAccount__copy():
    """
    Tests whether ``IntegrationAccount.copy`` works as intended.
    """
    integration_account_id = 'hana'
    name = 'cover'
    
    integration_account = IntegrationAccount(
        integration_account_id = integration_account_id,
        name = name,
    )
    copy = integration_account.copy()
    _check_is_every_attribute_set(copy)
    vampytest.assert_is_not(copy, integration_account)
    vampytest.assert_eq(copy, integration_account)


def test__IntegrationAccount__copy_with__0():
    """
    Tests whether ``IntegrationAccount.copy_with`` works as intended.
    
    Case: No fields given.
    """
    integration_account_id = 'hana'
    name = 'cover'
    
    integration_account = IntegrationAccount(
        integration_account_id = integration_account_id,
        name = name,
    )
    copy = integration_account.copy_with()
    _check_is_every_attribute_set(copy)
    vampytest.assert_is_not(copy, integration_account)
    vampytest.assert_eq(copy, integration_account)


def test__IntegrationAccount__copy_with__1():
    """
    Tests whether ``IntegrationAccount.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_integration_account_id = 'hana'
    old_name = 'cover'
    new_integration_account_id = 'flower'
    new_name = 'land'
    
    integration_account = IntegrationAccount(
        integration_account_id = old_integration_account_id,
        name = old_name,
    )
    copy = integration_account.copy_with(
        integration_account_id = new_integration_account_id,
        name = new_name,
    )
    _check_is_every_attribute_set(copy)
    vampytest.assert_is_not(copy, integration_account)
    
    vampytest.assert_eq(copy.id, new_integration_account_id)
    vampytest.assert_eq(copy.name, new_name)
