import vampytest

from ....bases import IconType, Icon

from ..user_base import UserBase


def test__UserBase__from_data():
    """
    Tests whether ``UserBase.from_data`` works as intended.
    """
    data = {}
    
    with vampytest.assert_raises(NotImplementedError):
        UserBase.from_data(data)


def test__UserBase__to_data():
    """
    Tests whether ``UserBase.to_data`` works as intended.
    
    Case: Include internals and defaults.
    """
    user_id = 202302030000
    name = 'suika'
    avatar = Icon(IconType.static, 24)
    
    user = UserBase(
        name = name,
        avatar = avatar,
    )
    user.id = user_id
    
    expected_output = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': None,
        'accent_color': None,
        'discriminator': '0000',
        'global_name': None,
        'username': name,
        'banner': None,
        'id': str(user_id),
        'public_flags': 0,
        'bot': False,
    }
    
    vampytest.assert_eq(
        user.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__UserBase__update_attributes():
    """
    Tests whether ``UserBase._update_attributes` works as intended.
    """
    name = 'suika'
    avatar = Icon(IconType.static, 24)
    
    user = UserBase()
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'username': name,
    }
    
    user._update_attributes(data)
    
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.avatar, avatar)


def test__UserBase__difference_update_attributes():
    """
    Tests whether ``UserBase._difference_update_attributes` works as intended.
    """
    old_name = 'suika'
    old_avatar = Icon(IconType.static, 24)
    new_name = 'ibuki'
    new_avatar = Icon(IconType.animated, 13)
    
    user = UserBase(
        avatar = old_avatar,
        name = old_name,
    )
    
    data = {
        'avatar': new_avatar.as_base_16_hash,
        'username': new_name,
    }
    
    old_attributes = user._difference_update_attributes(data)
    
    vampytest.assert_eq(user.name, new_name)
    vampytest.assert_eq(user.avatar, new_avatar)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'name': old_name,
            'avatar': old_avatar,
        },
    )
