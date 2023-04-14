import vampytest

from ....bases import Icon, ICON_TYPE_STATIC
from ....user import User

from ..integration_application import IntegrationApplication

from .test__IntegrationApplication__constructor import _assert_fields_set


def test__IntegrationApplication__partial():
    """
    Tests whether ``IntegrationApplication.partial`` works as intended.
    """
    for integration_application, expected_value in (
        (IntegrationApplication.precreate(202210080012), False),
        (IntegrationApplication(), True),
    ):
        vampytest.assert_eq(integration_application.partial, expected_value)


def test__IntegrationApplication__copy():
    """
    Tests whether ``IntegrationApplication.copy`` works as intended.
    """
    bot = User.precreate(202212170048)
    icon = Icon(ICON_TYPE_STATIC, 23)
    description = 'Afraid'
    name = 'Chata'
    
    integration_application = IntegrationApplication(
        bot = bot,
        description = description,
        icon = icon,
        name = name,
    )
    
    copy = integration_application.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, integration_application)
    vampytest.assert_eq(copy, integration_application)


def test__IntegrationApplication__copy_with__0():
    """
    Tests whether ``IntegrationApplication.copy_with`` works as intended.
    
    Case: No fields given.
    """
    bot = User.precreate(202212170049)
    icon = Icon(ICON_TYPE_STATIC, 23)
    description = 'Afraid'
    name = 'Chata'
    
    integration_application = IntegrationApplication(
        bot = bot,
        description = description,
        icon = icon,
        name = name,
    )
    
    copy = integration_application.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, integration_application)
    vampytest.assert_eq(copy, integration_application)


def test__IntegrationApplication__copy_with__1():
    """
    Tests whether ``IntegrationApplication.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_bot = User.precreate(202212170050)
    old_icon = Icon(ICON_TYPE_STATIC, 23)
    old_description = 'Afraid'
    old_name = 'Chata'
    new_bot = User.precreate(202212170051)
    new_icon = Icon(ICON_TYPE_STATIC, 11)
    new_description = 'Rose'
    new_name = 'Slayer'
    
    integration_application = IntegrationApplication(
        bot = old_bot,
        description = old_description,
        icon = old_icon,
        name = old_name,
    )
    
    copy = integration_application.copy_with(
        bot = new_bot,
        description = new_description,
        icon = new_icon,
        name = new_name,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, integration_application)
    
    vampytest.assert_eq(copy.bot, new_bot)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.name, new_name)
