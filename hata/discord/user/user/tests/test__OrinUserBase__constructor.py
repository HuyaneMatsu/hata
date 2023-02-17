import vampytest

from ....bases import Icon, IconType
from ....color import Color

from ..flags import UserFlag
from ..orin_user_base import OrinUserBase


def _assert_fields_set(user):
    """
    Asserts whether every fields of the given user are set.
    
    Parameters
    ----------
    user : ``OrinUserBase``
        The user to check.
    """
    vampytest.assert_instance(user, OrinUserBase)
    vampytest.assert_instance(user.avatar, Icon)
    vampytest.assert_instance(user.avatar_decoration, Icon)
    vampytest.assert_instance(user.banner, Icon)
    vampytest.assert_instance(user.banner_color, Color, nullable = True)
    vampytest.assert_instance(user.discriminator, int)
    vampytest.assert_instance(user.flags, UserFlag)
    vampytest.assert_instance(user.id, int)
    vampytest.assert_instance(user.name, str)


def test__OrinUserBase__new__0():
    """
    Tests whether ``OrinUserBase.__new__`` works as intended.
    
    Case: No fields given.
    """
    user = OrinUserBase()
    _assert_fields_set(user)


def test__OrinUserBase__new__1():
    """
    Tests whether ``OrinUserBase.__new__`` works as intended.
    
    Case: All fields given.
    """
    avatar = Icon(IconType.static, 32)
    avatar_decoration = Icon(IconType.animated_apng, 25)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    flags = UserFlag(1)
    name = 'voice in the dark'
    
    user = OrinUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        flags = flags,
        name = name,
    )
    _assert_fields_set(user)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.name, name)


def test__OrinUserBase__create_empty():
    """
    Tests whether ``OrinUserBase._create_empty`` works as intended.
    """
    user_id = 202302040014
    user = OrinUserBase._create_empty(user_id)
    _assert_fields_set(user)
    
    vampytest.assert_eq(user.id, user_id)
