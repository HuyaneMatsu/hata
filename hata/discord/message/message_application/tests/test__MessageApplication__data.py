import vampytest

from ....bases import Icon, ICON_TYPE_STATIC

from ..message_application import MessageApplication

from .test__MessageApplication__constructor import _assert_fields_set


def test__MessageApplication__from_data():
    """
    Tests whether ``MessageApplication.from_data`` works as intended.
    """
    message_application_id = 202304140003
    
    cover = Icon(ICON_TYPE_STATIC, 12)
    icon = Icon(ICON_TYPE_STATIC, 23)
    description = 'Afraid'
    name = 'Chata'
    
    data = {
        'id': str(message_application_id),
        'cover_image': cover.as_base_16_hash,
        'icon': icon.as_base_16_hash,
        'description': description,
        'name': name,
    }
    
    message_application = MessageApplication.from_data(data)
    
    _assert_fields_set(message_application)
    vampytest.assert_eq(message_application.id, message_application_id)
    
    vampytest.assert_eq(message_application.cover, cover)
    vampytest.assert_eq(message_application.description, description)
    vampytest.assert_eq(message_application.icon, icon)
    vampytest.assert_eq(message_application.name, name)


def test__MessageApplication__to_data():
    """
    Tests whether ``MessageApplication.to_data`` works as intended.
    
    Case: defaults & include internals.
    """
    message_application_id = 202304140004
    
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
    
    expected_data = {
        'id': str(message_application_id),
        'cover_image': cover.as_base_16_hash,
        'icon': icon.as_base_16_hash,
        'description': description,
        'name': name,
    }
    
    vampytest.assert_eq(
        message_application.to_data(
            defaults = True,
            include_internals = True,
        ),
        expected_data,
    )
