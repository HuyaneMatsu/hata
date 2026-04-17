import vampytest

from ....bases import Icon, ICON_TYPE_STATIC
from ....user import User

from ..integration_application import IntegrationApplication


def test__IntegrationApplication__repr():
    """
    tests whether ``IntegrationApplication.__repr__`` works as intended.
    """
    integration_application_id = 202210080022
    
    bot = User.precreate(202210080023)
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
    
    vampytest.assert_instance(repr(integration_application), str)


def test__IntegrationApplication__eq():
    """
    Tests whether ``IntegrationApplication.__eq__`` works as intended.
    """
    integration_application_id_1 = 202210080023
    integration_application_id_2 = 202210080024
    
    bot = User.precreate(202210080025)
    icon = Icon(ICON_TYPE_STATIC, 23)
    description = 'Afraid'
    name = 'Chata'
    
    keyword_parameters = {
        'integration_application_id': integration_application_id_1,
        'bot': bot,
        'description': description,
        'icon': icon,
        'name': name,
    }
    
    integration_application = IntegrationApplication.precreate(**keyword_parameters)
    vampytest.assert_eq(integration_application, integration_application)
    vampytest.assert_ne(integration_application, object())
    
    for field_name, field_value in (
        ('integration_application_id', integration_application_id_2),
        ('bot', None),
        ('description', 'Rose'),
        ('icon', None),
        ('name', 'Slayer'),
    ):
        test_integration_application = IntegrationApplication.precreate(
            **{**keyword_parameters, field_name: field_value},
        )
        vampytest.assert_ne(integration_application, test_integration_application)


def test__IntegrationApplication__hash():
    """
    tests whether ``IntegrationApplication.__hash__`` works as intended.
    """
    integration_application_id = 202210110001
    
    bot = User.precreate(202210110002)
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
    
    vampytest.assert_instance(hash(integration_application), int)
