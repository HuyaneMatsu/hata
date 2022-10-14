import vampytest

from ....user import ClientUserBase, User

from ..integration import Integration
from ..integration_type import IntegrationType
from ..metadata import IntegrationMetadataBase


def _check_is_attribute_set(integration):
    """
    Checks whether the given integration has all of it's attributes set.
    
    Parameters
    ----------
    integration : ``Integration``
        The integration to checkout.
    """
    vampytest.assert_instance(integration, Integration)
    
    vampytest.assert_instance(integration.id, int)
    vampytest.assert_instance(integration.enabled, bool)
    vampytest.assert_instance(integration.name, str)
    vampytest.assert_instance(integration.metadata, IntegrationMetadataBase)
    vampytest.assert_instance(integration.type, IntegrationType)
    vampytest.assert_instance(integration.user, ClientUserBase)


def test__Integration__new__0():
    """
    Tests whether ``Integration.__new__`` works as intended.
    
    Case: No parameters.
    """
    integration = Integration()
    _check_is_attribute_set(integration)


def test__Integration__new__1():
    """
    Tests whether ``Integration.__new__`` works as intended.
    
    Case: All parameters.
    """
    name = 'KEiNA'
    enabled = False
    integration_type = IntegrationType.twitch
    user = User.precreate(202210140025, name = 'Helix')
    integration_metadata = integration_type.metadata_type._create_empty()
    
    integration = Integration(
        name = name,
        enabled = enabled,
        integration_type = integration_type,
        user = user,
    )
    _check_is_attribute_set(integration)
    
    vampytest.assert_eq(integration.name, name)
    vampytest.assert_eq(integration.enabled, enabled)
    vampytest.assert_is(integration.type, integration_type)
    vampytest.assert_eq(integration.user, user)
    vampytest.assert_eq(integration.metadata, integration_metadata)


def test__Integration__precreate__0():
    """
    Tests whether ``Integration.precreate`` works as intended.
    
    Case: No parameters.
    """
    
    integration = Integration()
    _check_is_attribute_set(integration)


def test__Integration__precreate__1():
    """
    Tests whether ``Integration.precreate`` works as intended.
    
    Case: No parameters.
    """
    name = 'KEiNA'
    enabled = False
    integration_type = IntegrationType.twitch
    user = User.precreate(202210140026, name = 'Helix')
    integration_metadata = integration_type.metadata_type._create_empty()
    integration_id = 202210140027
    
    integration = Integration.precreate(
        integration_id,
        name = name,
        enabled = enabled,
        integration_type = integration_type,
        user = user,
    )
    _check_is_attribute_set(integration)
    vampytest.assert_eq(integration.id, integration_id)

    vampytest.assert_eq(integration.name, name)
    vampytest.assert_eq(integration.enabled, enabled)
    vampytest.assert_is(integration.type, integration_type)
    vampytest.assert_eq(integration.user, user)
    vampytest.assert_eq(integration.metadata, integration_metadata)

def test__Integration__precreate__2():
    """
    Tests whether ``Integration.precreate`` works as intended.
    
    Case: Check caching.
    """
    integration_id = 202210140031
    
    integration = Integration.precreate(
        integration_id,
    )
    
    test_integration = Integration.precreate(
        integration_id,
    )
    
    vampytest.assert_is(integration, test_integration)


def test__Integration__create_empty():
    """
    Tests whether ``Integration._create_empty`` works as intended.
    """
    integration_id = 202210140028
    
    integration = Integration._create_empty(integration_id)
    _check_is_attribute_set(integration)
    vampytest.assert_eq(integration.id, integration_id)


def test__Integration__create_with_role():
    """
    Tests whether ``Integration._create_empty`` works as intended.
    """
    integration_id = 202210140029
    role_id = 202210140030
    
    integration = Integration._create_with_role(integration_id, role_id)
    _check_is_attribute_set(integration)
    vampytest.assert_eq(integration.id, integration_id)
    vampytest.assert_eq(integration.role_id, role_id)
