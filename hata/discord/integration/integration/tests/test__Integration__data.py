import vampytest

from ....user import User

from ..integration import Integration
from ..preinstanced import IntegrationType

from .test__Integration__constructor import _check_is_attribute_set


def test__Integration__from_data__0():
    """
    Tests whether ``Integration.from_data`` works as expected.
    """
    name = 'KEiNA'
    enabled = False
    integration_type = IntegrationType.twitch
    user = User.precreate(202210140021, name = 'Helix')
    integration_id = 202210140022
    
    data = {
        'id': str(integration_id),
        'name': name,
        'enabled': enabled,
        'type': integration_type.value,
        'user': user.to_data(),
    }
    
    integration = Integration.from_data(data)
    _check_is_attribute_set(integration)
    
    vampytest.assert_eq(integration.id, integration_id)
    vampytest.assert_eq(integration.enabled, enabled)
    vampytest.assert_is(integration.type, integration_type)
    vampytest.assert_eq(integration.user, user)


def test__Integration__from_data__1():
    """
    Tests whether ``Integration.from_data`` works as expected.
    
    Case: Check caching,
    """
    integration_id = 202210140032
    
    data = {
        'id': str(integration_id),
    }
    
    integration = Integration.from_data(data)
    test_integration = Integration.from_data(data)
    vampytest.assert_is(integration, test_integration)


def test__Integration__to_data():
    """
    Tests whether ``Integration.to_data`` works as intended.
    
    Case: defaults & include internals.
    """
    name = 'KEiNA'
    enabled = False
    integration_type = IntegrationType.twitch
    user = User.precreate(202210140023, name = 'Helix')
    integration_id = 202210140024
    integration_metadata = integration_type.metadata_type._create_empty()
    
    integration = Integration.precreate(
        integration_id,
        name = name,
        enabled = enabled,
        user = user,
        integration_type = integration_type,
    )
    
    expected_data = {
        'id': str(integration_id),
        'name': name,
        'enabled': enabled,
        'type': integration_type.value,
        'user': user.to_data(),
        **integration_metadata.to_data(defaults = True),
    }
    
    vampytest.assert_eq(
        integration.to_data(
            defaults = True,
            include_internals = True,
        ),
        expected_data,
    )
