import vampytest

from ....role import Role

from ..integration import Integration
from ..integration_type import IntegrationType


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
