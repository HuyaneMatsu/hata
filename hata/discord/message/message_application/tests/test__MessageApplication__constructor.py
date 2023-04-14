import vampytest

from ....bases import Icon, ICON_TYPE_STATIC

from ..message_application import MessageApplication


def _assert_fields_set(message_application):
    """
    Checks whether every attributes are set of the message application.
    
    Parameters
    ----------
    message_application : ``MessageApplication``
        The message application to check.
    """
    vampytest.assert_instance(message_application, MessageApplication)
    
    vampytest.assert_instance(message_application.cover, Icon)
    vampytest.assert_instance(message_application.description, str, nullable = True)
    vampytest.assert_instance(message_application.icon, Icon)
    vampytest.assert_instance(message_application.name, str)


def test__MessageApplication__new__0():
    """
    Tests whether ``MessageApplication.__new__`` works as intended.
    
    Case: no parameters.
    """
    message_application = MessageApplication()
    _assert_fields_set(message_application)


def test__MessageApplication__new__1():
    """
    Tests whether ``MessageApplication.__new__`` works as intended.
    
    Case: all fields given.
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
    
    _assert_fields_set(message_application)
    
    vampytest.assert_eq(message_application.cover, cover)
    vampytest.assert_eq(message_application.description, description)
    vampytest.assert_eq(message_application.icon, icon)
    vampytest.assert_eq(message_application.name, name)


def test__MessageApplication__create_empty():
    """
    Tests whether ``MessageApplication._create_empty`` works as intended.
    """
    message_application_id = 202304140000
    
    message_application = MessageApplication._create_empty(message_application_id)
    
    _assert_fields_set(message_application)
    vampytest.assert_eq(message_application.id, message_application_id)


def test__MessageApplication__precreate__0():
    """
    Tests whether ``MessageApplication.precreate`` works as intended.
    
    Case: no fields given.
    """
    message_application_id = 202304140001
    
    message_application = MessageApplication.precreate(message_application_id)
    
    _assert_fields_set(message_application)
    vampytest.assert_eq(message_application.id, message_application_id)


def test__MessageApplication__precreate__1():
    """
    Tests whether ``MessageApplication.precreate`` works as intended.
    
    Case: all fields given.
    """
    message_application_id = 202304140002
    
    cover = Icon(ICON_TYPE_STATIC, 12)
    icon = Icon(ICON_TYPE_STATIC, 23)
    description = 'Afraid'
    name = 'Chata'
    
    message_application = MessageApplication.precreate(
        message_application_id,
        cover = cover,
        description = description,
        icon = icon,
        name = name,
    )
    _assert_fields_set(message_application)
    vampytest.assert_eq(message_application.id, message_application_id)
    
    vampytest.assert_eq(message_application.cover, cover)
    vampytest.assert_eq(message_application.description, description)
    vampytest.assert_eq(message_application.icon, icon)
    vampytest.assert_eq(message_application.name, name)
