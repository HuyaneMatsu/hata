import vampytest

from ....user import User

from ...integration_application import IntegrationApplication

from ..discord import IntegrationMetadataDiscord

from .test__IntegrationMetadataDiscord__constructor import _check_all_fields_set


def test__IntegrationMetadataDiscord__from_data__0():
    """
    Tests whether ``IntegrationMetadataDiscord.from_data`` works as intended.
    
    Case: non-discord integration.
    """
    account = User.precreate(202210140000, name = 'Nekoishi')
    application = IntegrationApplication.precreate(202210140001, name = 'Koishi', bot = account)
    
    data = {
        'account': {
            'id': str(account.id),
            'name': account.name,
        },
        'application': application.to_data(include_internals = True),
    }
    
    
    integration_metadata = IntegrationMetadataDiscord.from_data(data)
    
    _check_all_fields_set(integration_metadata)
    
    vampytest.assert_is(integration_metadata.account, account)
    vampytest.assert_eq(integration_metadata.application, application)


def test__IntegrationMetadataDiscord__to_data():
    """
    Tests whether ``IntegrationMetadataDiscord.to_data`` works as intended.
    
    Case: defaults.
    """
    account = User.precreate(202210140002, name = 'Nekoishi')
    application = IntegrationApplication.precreate(202210140003, name = 'Koishi', bot = account)
    
    integration_metadata = IntegrationMetadataDiscord({
        'account': account,
        'application': application,
    })
    
    expected_data = {
        'account': {
            'id': str(account.id),
            'name': account.name,
        },
        'application': application.to_data(
            defaults = True,
        ),
    }
    
    vampytest.assert_eq(
        integration_metadata.to_data(
            defaults = True,
        ),
        expected_data,
    )
