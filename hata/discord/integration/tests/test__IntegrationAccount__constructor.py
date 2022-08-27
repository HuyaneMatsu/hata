import vampytest

from ...user import ClientUserBase
from .. import IntegrationAccount, IntegrationType


def test__IntegrationAccount__new_0():
    """
    Tests whether Discord integration account users are created correctly.
    """
    data = {'id': '202208270005', 'name': 'Satori'}
    
    user = IntegrationAccount(data, IntegrationType.discord)
    
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.bot, True)
    vampytest.assert_eq(user.id, int(data['id']))
    vampytest.assert_eq(user.name, data['name'])
