import vampytest

from ....bases import Icon, ICON_TYPE_STATIC
from ....user import ClientUserBase, User

from ..integration_application import IntegrationApplication


def _check_is_every_attribute_set(integration_application):
    """
    Checks whether every attributes are set of the integration application.
    
    Parameters
    ----------
    integration_application : ``IntegrationApplication``
        The integration application to check.
    """
    vampytest.assert_instance(integration_application, IntegrationApplication)
    
    vampytest.assert_instance(integration_application.bot, ClientUserBase)
    vampytest.assert_instance(integration_application.description, str, nullable = True)
    vampytest.assert_instance(integration_application.icon, Icon)
    vampytest.assert_instance(integration_application.name, str)


def test__IntegrationApplication__new__0():
    """
    Tests whether ``IntegrationApplication.__new__`` works as intended.
    
    Case: no parameters.
    """
    integration_application = IntegrationApplication()
    _check_is_every_attribute_set(integration_application)


def test__IntegrationApplication__new__1():
    """
    Tests whether ``IntegrationApplication.__new__`` works as intended.
    
    Case: all fields given.
    """
    bot = User.precreate(202210080013)
    icon = Icon(ICON_TYPE_STATIC, 23)
    description = 'Afraid'
    name = 'Chata'
    
    integration_application = IntegrationApplication(
        bot = bot,
        description = description,
        icon = icon,
        name = name,
    )
    
    _check_is_every_attribute_set(integration_application)
    
    vampytest.assert_is(integration_application.bot, bot)
    vampytest.assert_eq(integration_application.description, description)
    vampytest.assert_eq(integration_application.icon, icon)
    vampytest.assert_eq(integration_application.name, name)


def test__IntegrationApplication__create_empty():
    """
    Tests whether ``IntegrationApplication._create_empty`` works as intended.
    """
    integration_application_id = 202210080014
    
    integration_application = IntegrationApplication._create_empty(integration_application_id)
    
    _check_is_every_attribute_set(integration_application)
    vampytest.assert_eq(integration_application.id, integration_application_id)


def test__IntegrationApplication__precreate__0():
    """
    Tests whether ``IntegrationApplication.precreate`` works as intended.
    
    Case: no fields given.
    """
    integration_application_id = 202210080015
    
    integration_application = IntegrationApplication.precreate(integration_application_id)
    
    _check_is_every_attribute_set(integration_application)
    vampytest.assert_eq(integration_application.id, integration_application_id)


def test__IntegrationApplication__precreate__1():
    """
    Tests whether ``IntegrationApplication.precreate`` works as intended.
    
    Case: all fields given.
    """
    integration_application_id = 202210080016
    
    bot = User.precreate(202210080017)
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
    _check_is_every_attribute_set(integration_application)
    vampytest.assert_eq(integration_application.id, integration_application_id)
    
    vampytest.assert_is(integration_application.bot, bot)
    vampytest.assert_eq(integration_application.description, description)
    vampytest.assert_eq(integration_application.icon, icon)
    vampytest.assert_eq(integration_application.name, name)
