import vampytest

from ....bases import Icon, IconType

from ..user_base import UserBase

from .test__UserBase__constructor import _assert_fields_set


def test__UserBase__copy():
    """
    Tests whether ``UserBase.copy`` works as intended.
    """
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    
    user = UserBase(
        avatar = avatar,
        name = name,
    )
    
    copy = user.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(user, copy)


def test__UserBase__copy_with__0():
    """
    Tests whether ``UserBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    avatar = Icon(IconType.static, 14)
    name = 'orin'
    
    user = UserBase(
        avatar = avatar,
        name = name,
    )
    
    copy = user.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(user, copy)


def test__UserBase__copy_with__1():
    """
    Tests whether ``UserBase.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_avatar = Icon(IconType.static, 14)
    old_name = 'orin'
    new_avatar = Icon(IconType.animated, 23)
    new_name = 'okuu'
    
    user = UserBase(
        avatar = old_avatar,
        name = old_name,
    )
    
    copy = user.copy_with(
        avatar = new_avatar,
        name = new_name,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(user, copy)
    
    vampytest.assert_eq(copy.avatar, new_avatar)
    vampytest.assert_eq(copy.name, new_name)
