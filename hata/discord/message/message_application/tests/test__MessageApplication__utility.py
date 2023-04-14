import vampytest

from ....bases import Icon, ICON_TYPE_STATIC

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


def test__MessageApplication__copy_with__0():
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


def test__MessageApplication__copy_with__1():
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
