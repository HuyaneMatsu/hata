import vampytest

from ...oauth2 import Oauth2Scope
from ...user import ClientUserBase
from .. import Integration, IntegrationApplication, IntegrationType


def _get_discord_integration_data():
    return {
        'id': '202208280000',
        'type': 'discord',
        'name': 'Koishi',
        'account': {
            'id': '202208280001',
            'name': 'Koishi',
        },
        'application': {
            'id': '202208280002',
            'name': 'Koishi',
            'icon': None,
            'description': 'Shrimp fry.',
            'type': 1,
            'primary_sku_id': '202208280003',
            'bot':
                {
                    'id': '202208280001',
                    'username': 'Koishi',
                    'discriminator': '0001',
                    'bot': True
                }
        },
        'enabled': True,
        'scopes': ['applications.commands', 'bot'],
        'user': {
            'id': '202208280004',
            'username': 'Mama',
            'discriminator': '0001',
        }
    }


def test__Integration__new__0():
    """
    Tests whether ``Integration.__new__`` works as expected.
    
    Case: Discord integration.
    """
    data = _get_discord_integration_data()
    integration = Integration(data)
    
    vampytest.assert_eq(integration.id, int(data['id']))
    vampytest.assert_instance(integration.type, IntegrationType)
    vampytest.assert_instance(integration.name, str)
    vampytest.assert_instance(integration.account, ClientUserBase)
    vampytest.assert_instance(integration.application, IntegrationApplication)
    vampytest.assert_instance(integration.enabled, bool)
    vampytest.assert_eq(integration.scopes, (Oauth2Scope.applications_commands, Oauth2Scope.bot))
    vampytest.assert_instance(integration.user, ClientUserBase)
    vampytest.assert_is(integration.account, integration.application.bot)
