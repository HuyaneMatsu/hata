import vampytest

from ....bases import Icon, ICON_TYPE_STATIC

from ..message_application import MessageApplication


def test__MessageApplication__repr():
    """
    tests whether ``MessageApplication.__repr__`` works as intended.
    """
    message_application_id = 202304140005
    
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
    
    vampytest.assert_instance(repr(message_application), str)


def test__MessageApplication__hash():
    """
    tests whether ``MessageApplication.__hash__`` works as intended.
    """
    message_application_id = 202304140006
    
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
    
    vampytest.assert_instance(hash(message_application), int)


def test__MessageApplication__eq():
    """
    Tests whether ``MessageApplication.__eq__`` works as intended.
    """
    message_application_id_1 = 202304140007
    message_application_id_2 = 202304140008
    
    cover = Icon(ICON_TYPE_STATIC, 12)
    icon = Icon(ICON_TYPE_STATIC, 23)
    description = 'Afraid'
    name = 'Chata'
    
    keyword_parameters = {
        'message_application_id': message_application_id_1,
        'cover': cover,
        'description': description,
        'icon': icon,
        'name': name,
    }
    
    message_application = MessageApplication.precreate(**keyword_parameters)
    vampytest.assert_eq(message_application, message_application)
    vampytest.assert_ne(message_application, object())
    
    for field_name, field_value in (
        ('message_application_id', message_application_id_2),
        ('cover', None),
        ('description', 'Rose'),
        ('icon', None),
        ('name', 'Slayer'),
    ):
        test_message_application = MessageApplication.precreate(
            **{**keyword_parameters, field_name: field_value},
        )
        vampytest.assert_ne(message_application, test_message_application)
