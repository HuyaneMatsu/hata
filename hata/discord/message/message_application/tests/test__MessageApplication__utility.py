import vampytest

from ....bases import ICON_TYPE_STATIC, Icon, IconType

from ..message_application import MessageApplication

from .test__MessageApplication__constructor import _assert_fields_set


def test__MessageApplication__partial():
    """
    Tests whether ``MessageApplication.partial`` works as intended.
    """
    for message_application, expected_value in (
        (MessageApplication.precreate(202304140009), False),
        (MessageApplication(), True),
    ):
        vampytest.assert_eq(message_application.partial, expected_value)


def test__MessageApplication__copy():
    """
    Tests whether ``MessageApplication.copy`` works as intended.
    """
    cover = Icon(ICON_TYPE_STATIC, 12)
    icon = Icon(ICON_TYPE_STATIC, 23)
    description = 'Afraid'
    name = 'Chata'
    
    message_application = MessageApplication(
        cover = cover,
        description = description,
        icon = icon,
        name = name,
    )
    
    copy = message_application.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_application)
    vampytest.assert_eq(copy, message_application)


def test__MessageApplication__copy_with__no_fields():
    """
    Tests whether ``MessageApplication.copy_with`` works as intended.
    
    Case: No fields given.
    """
    cover = Icon(ICON_TYPE_STATIC, 12)
    icon = Icon(ICON_TYPE_STATIC, 23)
    description = 'Afraid'
    name = 'Chata'
    
    message_application = MessageApplication(
        cover = cover,
        description = description,
        icon = icon,
        name = name,
    )
    
    copy = message_application.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_application)
    vampytest.assert_eq(copy, message_application)


def test__MessageApplication__copy_with__all_fields():
    """
    Tests whether ``MessageApplication.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_cover = Icon(ICON_TYPE_STATIC, 12)
    old_icon = Icon(ICON_TYPE_STATIC, 23)
    old_description = 'Afraid'
    old_name = 'Chata'
    
    new_cover = Icon(ICON_TYPE_STATIC, 22)
    new_icon = Icon(ICON_TYPE_STATIC, 11)
    new_description = 'Rose'
    new_name = 'Slayer'
    
    message_application = MessageApplication(
        cover = old_cover,
        description = old_description,
        icon = old_icon,
        name = old_name,
    )
    
    copy = message_application.copy_with(
        cover = new_cover,
        description = new_description,
        icon = new_icon,
        name = new_name,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, message_application)
    
    vampytest.assert_eq(copy.cover, new_cover)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.name, new_name)


def _iter_options__icon_url():
    yield 202505310014, None, False
    yield 202505310015, Icon(IconType.animated, 5), True


@vampytest._(vampytest.call_from(_iter_options__icon_url()).returning_last())
def test__MessageApplication__icon_url(application_id, icon):
    """
    Tests whether ``MessageApplication.icon_url`` works as intended.
    
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
    application = MessageApplication.precreate(
        application_id,
        icon = icon,
    )
    
    output = application.icon_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__icon_url_as():
    yield 202505310016, None, {'ext': 'webp', 'size': 128}, False
    yield 202505310017, Icon(IconType.animated, 5), {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__icon_url_as()).returning_last())
def test__MessageApplication__icon_url_as(application_id, icon, keyword_parameters):
    """
    Tests whether ``MessageApplication.icon_url_as`` works as intended.
    
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
    application = MessageApplication.precreate(
        application_id,
        icon = icon,
    )
    
    output = application.icon_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__cover_url():
    yield 202505310018, None, False
    yield 202505310019, Icon(IconType.animated, 5), True


@vampytest._(vampytest.call_from(_iter_options__cover_url()).returning_last())
def test__MessageApplication__cover_url(application_id, icon):
    """
    Tests whether ``MessageApplication.cover_url`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Identifier to create application with.
    
    icon : ``None | Icon``
        Icon to create the application with.
    
    Returns
    -------
    has_cover_url : `bool`
    """
    application = MessageApplication.precreate(
        application_id,
        cover = icon,
    )
    
    output = application.cover_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__cover_url_as():
    yield 202505310020, None, {'ext': 'webp', 'size': 128}, False
    yield 202505310021, Icon(IconType.animated, 5), {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__cover_url_as()).returning_last())
def test__MessageApplication__cover_url_as(application_id, icon, keyword_parameters):
    """
    Tests whether ``MessageApplication.cover_url_as`` works as intended.
    
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
    has_cover_url : `bool`
    """
    application = MessageApplication.precreate(
        application_id,
        cover = icon,
    )
    
    output = application.cover_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
