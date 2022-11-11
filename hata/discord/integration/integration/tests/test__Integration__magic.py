import vampytest

from ....user import User

from ..integration import Integration
from ..preinstanced import IntegrationType


def test__Integration__repr():
    """
    Tests whether ``Integration.__repr__`` works as intended.
    """
    name = 'KEiNA'
    enabled = False
    integration_type = IntegrationType.twitch
    user = User.precreate(202210140034, name = 'Helix')
    integration_id = 202210140033
    
    integration = Integration.precreate(
        integration_id,
        name = name,
        enabled = enabled,
        integration_type = integration_type,
        user = user,
    )
    
    vampytest.assert_instance(repr(integration), str)


def test__Integration__hash():
    """
    Tests whether ``Integration.__hash__`` works as intended.
    """
    name = 'KEiNA'
    enabled = False
    integration_type = IntegrationType.twitch
    user = User.precreate(202210140035, name = 'Helix')
    integration_id = 202210140036
    
    integration = Integration.precreate(
        integration_id,
        name = name,
        enabled = enabled,
        integration_type = integration_type,
        user = user,
    )
    
    vampytest.assert_instance(repr(integration), str)


def test__Integration__eq():
    """
    Tests whether ``Integration.__eq__`` works as intended.
    """
    name = 'KEiNA'
    enabled = False
    integration_type = IntegrationType.twitch
    user = User.precreate(202210140037, name = 'Helix')
    integration_id = 202210140038
    
    keyword_parameters = {
        'name': name,
        'enabled': enabled,
        'integration_type': integration_type,
        'user': user,
    }
    
    integration = Integration.precreate(
        integration_id,
        **keyword_parameters
    )
    
    vampytest.assert_eq(integration, integration)
    vampytest.assert_ne(integration, object())
    
    test_integration = Integration(**keyword_parameters)
    vampytest.assert_eq(integration, test_integration)
    
    test_integration = Integration.precreate(202210140039, **keyword_parameters)
    vampytest.assert_ne(integration, test_integration)
    
    for field_name, field_value in (
        ('name', 'Purge'),
        ('enabled', True),
        ('integration_type', IntegrationType.discord),
    ):
        test_integration = Integration(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(integration, test_integration)
