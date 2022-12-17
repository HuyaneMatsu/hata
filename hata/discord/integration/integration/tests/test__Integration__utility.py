import vampytest

from ....role import Role
from ....user import User

from ..integration import Integration
from ..preinstanced import IntegrationType

from .test__Integration__constructor import _check_is_attribute_set


def test__Integration__role__0():
    """
    Tests whether ``Integration.role`` works as intended.
    
    Case: not cached.
    """
    role_id = 202210090008
    integration_type = IntegrationType.twitch
    
    integration_metadata = Integration(integration_type = integration_type, role_id = role_id)
    
    role = integration_metadata.role
    vampytest.assert_instance(role, Role)
    vampytest.assert_eq(role.id, role_id)


def test__Integration__role__1():
    """
    Tests whether ``Integration.role`` works as intended.
    
    Case: cached.
    """
    role_id = 202210090009
    integration_type = IntegrationType.twitch
    expected_role = Role.precreate(role_id)
    
    integration_metadata = Integration(integration_type = integration_type, role_id = role_id)
    
    role = integration_metadata.role
    vampytest.assert_instance(role, Role)
    vampytest.assert_is(role, expected_role)


def test__Integration__role__2():
    """
    Tests whether ``Integration.role`` works as intended.
    
    Case: no role.
    """
    role_id = 0
    integration_type = IntegrationType.twitch
    
    integration_metadata = Integration(integration_type = integration_type, role_id = role_id)
    
    role = integration_metadata.role
    vampytest.assert_is(role, None)


def test__Integration__role__3():
    """
    Tests whether ``Integration.role`` works as intended.
    
    Case: integration type without role.
    """
    integration_type = IntegrationType.discord
    
    integration_metadata = Integration(integration_type = integration_type)
    
    role = integration_metadata.role
    vampytest.assert_is(role, None)


def test__Integration__partial():
    """
    Tests whether ``Integration.partial`` works as intended.
    """
    for (integration, expected_output) in (
        (Integration(), True),
        (Integration(integration_type = IntegrationType.discord), True),
        (Integration.precreate(202210140045), True),
        (Integration.precreate(202210140046, integration_type = IntegrationType.discord), False),
    ):
        partial = integration.partial
        vampytest.assert_instance(partial, bool)
        vampytest.assert_eq(partial, expected_output)


def test__Integration__copy():
    """
    Tests whether ``Integration.copy`` works as intended.
    """
    name = 'KEiNA'
    enabled = False
    integration_type = IntegrationType.twitch
    user = User.precreate(202212170029, name = 'Helix')
    subscriber_count = 12
    
    integration = Integration(
        name = name,
        enabled = enabled,
        integration_type = integration_type,
        user = user,
        subscriber_count = subscriber_count,
    )
    
    copy = integration.copy()
    _check_is_attribute_set(copy)
    vampytest.assert_is_not(copy, integration)
    vampytest.assert_eq(copy, integration)


def test__Integration__copy_with__0():
    """
    Tests whether ``Integration.copy_with`` works as intended.
    """
    name = 'KEiNA'
    enabled = False
    integration_type = IntegrationType.twitch
    user = User.precreate(202212170030, name = 'Helix')
    subscriber_count = 12
    
    integration = Integration(
        name = name,
        enabled = enabled,
        integration_type = integration_type,
        user = user,
        subscriber_count = subscriber_count,
    )
    
    copy = integration.copy_with()
    _check_is_attribute_set(copy)
    vampytest.assert_is_not(copy, integration)
    vampytest.assert_eq(copy, integration)


def test__Integration__copy_with__1():
    """
    Tests whether ``Integration.copy_with`` works as intended.
    """
    old_name = 'KEiNA'
    new_name = 'Empty'
    old_enabled = False
    new_enabled = True
    old_integration_type = IntegrationType.twitch
    new_integration_type = IntegrationType.youtube
    old_user = User.precreate(202212170031, name = 'Helix')
    new_user = User.precreate(202212170032, name = 'Wither')
    old_subscriber_count = 12
    new_subscriber_count = 11
    
    integration = Integration(
        name = old_name,
        enabled = old_enabled,
        integration_type = old_integration_type,
        user = old_user,
        subscriber_count = old_subscriber_count,
    )
    
    copy = integration.copy_with(
        name = new_name,
        enabled = new_enabled,
        integration_type = new_integration_type,
        user = new_user,
        subscriber_count = new_subscriber_count,
    )
    _check_is_attribute_set(copy)
    vampytest.assert_is_not(copy, integration)

    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_is(copy.type, new_integration_type)
    vampytest.assert_eq(copy.user, new_user)
    vampytest.assert_eq(copy.metadata, new_integration_type.metadata_type({'subscriber_count': new_subscriber_count}))
