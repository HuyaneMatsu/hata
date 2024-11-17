import vampytest

from ....user import User

from ...integration_application import IntegrationApplication

from ..discord import IntegrationMetadataDiscord

from .test__IntegrationMetadataDiscord__constructor import _assert_fields_set


def test__IntegrationMetadataDiscord__copy():
    """
    Tests whether ``IntegrationMetadataDiscord.copy`` works as intended.
    """
    account = User.precreate(202212170033, name = 'Nekoishi')
    application = IntegrationApplication.precreate(202212170034, name = 'Koishi', bot = account)
    
    integration_metadata = IntegrationMetadataDiscord(
        account = account,
        application = application,
    )
    
    copy = integration_metadata.copy()
    _assert_fields_set(integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)
    vampytest.assert_eq(copy, integration_metadata)


def test__IntegrationMetadataDiscord__copy_with__no_fields():
    """
    Tests whether ``IntegrationMetadataDiscord.copy_with`` works as intended.
    
    Case: No fields given.
    """
    account = User.precreate(202212170035, name = 'Nekoishi')
    application = IntegrationApplication.precreate(202212170036, name = 'Koishi', bot = account)

    integration_metadata = IntegrationMetadataDiscord(
        account = account,
        application = application,
    )
    
    copy = integration_metadata.copy_with()
    _assert_fields_set(integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)
    vampytest.assert_eq(copy, integration_metadata)


def test__IntegrationMetadataDiscord__copy_with__all_fields():
    """
    Tests whether ``IntegrationMetadataDiscord.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_account = User.precreate(202212170037, name = 'Nekoishi')
    old_application = IntegrationApplication.precreate(202212170038, name = 'Koishi', bot = old_account)
    new_account = User.precreate(202212170039, name = 'Nyandre')
    new_application = IntegrationApplication.precreate(202212170040, name = 'Flandre', bot = old_account)

    integration_metadata = IntegrationMetadataDiscord(
        account = old_account,
        application = old_application,
    )
    
    copy = integration_metadata.copy_with(
        account = new_account,
        application = new_application,
    )
    
    _assert_fields_set(integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)
    
    vampytest.assert_eq(copy.account, new_account)
    vampytest.assert_eq(copy.application, new_application)


def test__IntegrationMetadataDiscord__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``IntegrationMetadataDiscord.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    account = User.precreate(202304080002, name = 'Nekoishi')
    application = IntegrationApplication.precreate(202304080003, name = 'Koishi', bot = account)

    integration_metadata = IntegrationMetadataDiscord(
        account = account,
        application = application,
    )
    
    copy = integration_metadata.copy_with_keyword_parameters({})
    _assert_fields_set(integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)
    vampytest.assert_eq(copy, integration_metadata)


def test__IntegrationMetadataDiscord__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``IntegrationMetadataDiscord.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    old_account = User.precreate(202304080004, name = 'Nekoishi')
    old_application = IntegrationApplication.precreate(202304080005, name = 'Koishi', bot = old_account)
    new_account = User.precreate(202304080006, name = 'Nyandre')
    new_application = IntegrationApplication.precreate(202304080007, name = 'Flandre', bot = old_account)

    integration_metadata = IntegrationMetadataDiscord(
        account = old_account,
        application = old_application,
    )
    
    copy = integration_metadata.copy_with_keyword_parameters({
        'account': new_account,
        'application': new_application,
    })
    
    _assert_fields_set(integration_metadata)
    vampytest.assert_is_not(copy, integration_metadata)
    
    vampytest.assert_eq(copy.account, new_account)
    vampytest.assert_eq(copy.application, new_application)
