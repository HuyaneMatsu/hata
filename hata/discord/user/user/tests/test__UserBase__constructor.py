import vampytest

from ....bases import Icon, IconType

from ..user_base import UserBase


def _assert_fields_set(user):
    """
    Asserts whether every fields of the given user are set.
    
    Parameters
    ----------
    user : ``UserBase``
        The user to check.
    """
    vampytest.assert_instance(user, UserBase)
    vampytest.assert_instance(user.avatar, Icon)
    vampytest.assert_instance(user.id, int)
    vampytest.assert_instance(user.name, str)


def test__UserBase__new__0():
    """
    Tests whether ``UserBase.__new__`` works as intended.
    
    Case: No fields given.
    """
    user = UserBase()
    _assert_fields_set(user)


def test__UserBase__new__1():
    """
    Tests whether ``UserBase.__new__`` works as intended.
    
    Case: All fields given.
    """
    avatar = Icon(IconType.static, 32)
    name = 'voice in the dark'
    
    user = UserBase(
        avatar = avatar,
        name = name,
    )
    _assert_fields_set(user)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.name, name)


def test__UserBase__create_empty():
    """
    Tests whether ``UserBase._create_empty`` works as intended.
    """
    user_id = 202302030001
    user = UserBase._create_empty(user_id)
    _assert_fields_set(user)
    
    vampytest.assert_eq(user.id, user_id)
