import vampytest

from ....user import User

from ...integration_application import IntegrationApplication

from ..discord import IntegrationMetadataDiscord


def _check_all_fields_set(integration_metadata):
    """
    Tests whether all attributes of an ``IntegrationMetadataDiscord`` are set.
    
    Parameters
    ----------
    integration_metadata : ``IntegrationMetadataDiscord``
        The integration detail to check out.
    """
    vampytest.assert_instance(integration_metadata, IntegrationMetadataDiscord)
    
    vampytest.assert_instance(integration_metadata.account, object)
    vampytest.assert_instance(integration_metadata.application, IntegrationApplication, nullable = True)


def test__IntegrationMetadataDiscord__new__0():
    """
    Tests whether ``IntegrationMetadataDiscord.__new__`` works as intended.
    
    Case: No fields given.
    """
    integration_metadata = IntegrationMetadataDiscord({})
    _check_all_fields_set(integration_metadata)


def test__IntegrationMetadataDiscord__new__1():
    """
    Tests whether ``IntegrationMetadataDiscord.__new__`` works as intended.
    
    Case: All fields given.
    """
    account = User.precreate(202210140013, name = 'Nekoishi')
    application = IntegrationApplication.precreate(202210140014, name = 'Koishi', bot = account)

    keyword_parameters = {
        'account': account,
        'application': application,
    }

    integration_metadata = IntegrationMetadataDiscord(keyword_parameters)
    _check_all_fields_set(integration_metadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_is(integration_metadata.account, account)
    vampytest.assert_eq(integration_metadata.application, application)


def test__IntegrationMetadataDiscord__create_empty():
    """
    Tests whether ``IntegrationMetadataDiscord._create_empty`` works as intended.
    """
    integration_metadata = IntegrationMetadataDiscord._create_empty()
    _check_all_fields_set(integration_metadata)
