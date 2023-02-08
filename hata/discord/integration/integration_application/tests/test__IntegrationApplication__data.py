import vampytest

from ....bases import Icon, ICON_TYPE_STATIC
from ....user import User

from ..integration_application import IntegrationApplication

from .test__IntegrationApplication__constructor import _check_is_every_attribute_set


def test__IntegrationApplication__from_data():
    """
    Tests whether ``IntegrationApplication.from_data`` works as intended.
    """
    integration_application_id = 202210080019
    
    bot = User.precreate(202210080018)
    icon = Icon(ICON_TYPE_STATIC, 23)
    description = 'Afraid'
    name = 'Chata'
    
    data = {
        'id': str(integration_application_id),
        'bot': bot.to_data(defaults = True, include_internals = True),
        'icon': icon.as_base_16_hash,
        'description': description,
        'name': name,
    }
    
    integration_application = IntegrationApplication.from_data(data)
    
    _check_is_every_attribute_set(integration_application)
    vampytest.assert_eq(integration_application.id, integration_application_id)
    
    vampytest.assert_is(integration_application.bot, bot)
    vampytest.assert_eq(integration_application.description, description)
    vampytest.assert_eq(integration_application.icon, icon)
    vampytest.assert_eq(integration_application.name, name)


def test__IntegrationApplication__to_data():
    """
    Tests whether ``IntegrationApplication.to_data`` works as intended.
    
    Case: defaults & include internals.
    """
    integration_application_id = 202210080020
    
    bot = User.precreate(202210080021)
    icon = Icon(ICON_TYPE_STATIC, 23)
    description = 'Afraid'
    name = 'Chata'
    
    integration_application = IntegrationApplication.precreate(
        integration_application_id,
        bot = bot,
        description = description,
        icon = icon,
        name = name,
    )
    
    expected_data = {
        'id': str(integration_application_id),
        'bot': bot.to_data(defaults = True, include_internals = True),
        'icon': icon.as_base_16_hash,
        'description': description,
        'name': name,
    }
    
    vampytest.assert_eq(
        integration_application.to_data(
            defaults = True,
            include_internals = True,
        ),
        expected_data,
    )
