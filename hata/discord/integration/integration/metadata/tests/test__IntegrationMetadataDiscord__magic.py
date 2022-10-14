import vampytest

from .....user import User

from ....integration_application import IntegrationApplication

from ..discord import IntegrationMetadataDiscord


def test__IntegrationMetadataDiscord__repr():
    """
    Tests whether ``IntegrationMetadataDiscord.__new__`` works as intended.
    
    Case: All fields given.
    """
    account = User.precreate(202210140004, name = 'Nekoishi')
    application = IntegrationApplication.precreate(202210140005, name = 'Koishi', bot = account)
    

    integration_metadata = IntegrationMetadataDiscord({
        'account': account,
        'application': application,
    })
    
    vampytest.assert_instance(repr(integration_metadata), str)


def test__IntegrationMetadataDiscord__eq():
    """
    Tests whether ``IntegrationMetadataDiscord.__eq__`` works as intended.
    """
    account = User.precreate(202210140006, name = 'Nekoishi')
    application = IntegrationApplication.precreate(202210140007, name = 'Koishi', bot = account)
    
    
    keyword_parameters = {
        'account': account,
        'application': application,
    }
    
    integration_metadata = IntegrationMetadataDiscord(keyword_parameters)
    
    vampytest.assert_eq(integration_metadata, integration_metadata)
    vampytest.assert_ne(integration_metadata, object())
    
    for field_name, field_value in (
        (
            'account',
            User.precreate(
                202210140008,
                name = 'Hecate',
            )
        ), (
            'application',
            IntegrationApplication.precreate(
                202210140009,
                name = 'Koishi',
                bot = User.precreate(
                    202210140010,
                ),
            )
        ),
    ):
        integration_metadata_test = IntegrationMetadataDiscord({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(integration_metadata, integration_metadata_test)


def test__IntegrationMetadataDiscord__hash():
    """
    Tests whether ``IntegrationMetadataDiscord.__hash__`` works as intended.
    
    Case: All fields given.
    """
    account = User.precreate(202210140011, name = 'Nekoishi')
    application = IntegrationApplication.precreate(202210140012, name = 'Koishi', bot = account)
    

    integration_metadata = IntegrationMetadataDiscord({
        'account': account,
        'application': application,
    })
    
    vampytest.assert_instance(hash(integration_metadata), int)
