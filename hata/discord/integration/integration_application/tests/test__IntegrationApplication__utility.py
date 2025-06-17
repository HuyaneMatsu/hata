import vampytest

from ....bases import ICON_TYPE_STATIC, Icon, IconType
from ....user import User

from ..integration_application import IntegrationApplication

from .test__IntegrationApplication__constructor import _assert_fields_set


def test__IntegrationApplication__partial__with_id():
    """
    Tests whether ``IntegrationApplication.partial`` works as intended.
    
    Case: with id.
    """
    integration_application = IntegrationApplication.precreate(202210080012)
    
    output = integration_application.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__IntegrationApplication__partial__without_id():
    """
    Tests whether ``IntegrationApplication.partial`` works as intended.
    
    Case: without id.
    """
    integration_application = IntegrationApplication()
    
    output = integration_application.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


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


def test__IntegrationApplication__copy_with__no_fields():
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


def test__IntegrationApplication__copy_with__all_fields():
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


def _iter_options__icon_url():
    yield 202505310022, None, False
    yield 202505310023, Icon(IconType.animated, 5), True


@vampytest._(vampytest.call_from(_iter_options__icon_url()).returning_last())
def test__IntegrationApplication__icon_url(application_id, icon):
    """
    Tests whether ``IntegrationApplication.icon_url`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Identifier to create application with.
    
    icon : ``None | Icon``
        Icon to create the application with.
    
    Returns
    -------
    has_icon_url : `bool`
    """
    application = IntegrationApplication.precreate(
        application_id,
        icon = icon,
    )
    
    output = application.icon_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__icon_url_as():
    yield 202505310024, None, {'ext': 'webp', 'size': 128}, False
    yield 202505310025, Icon(IconType.animated, 5), {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__icon_url_as()).returning_last())
def test__IntegrationApplication__icon_url_as(application_id, icon, keyword_parameters):
    """
    Tests whether ``IntegrationApplication.icon_url_as`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Identifier to create application with.
    
    icon : ``None | Icon``
        Icon to create the application with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_icon_url : `bool`
    """
    application = IntegrationApplication.precreate(
        application_id,
        icon = icon,
    )
    
    output = application.icon_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
