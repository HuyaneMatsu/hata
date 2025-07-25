import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....guild import GuildBadge

from ...avatar_decoration import AvatarDecoration
from ...name_plate import NamePlate

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
    vampytest.assert_instance(user.avatar_decoration, AvatarDecoration, nullable = True)
    vampytest.assert_instance(user.banner, Icon)
    vampytest.assert_instance(user.banner_color, Color, nullable = True)
    vampytest.assert_instance(user.discriminator, int)
    vampytest.assert_instance(user.display_name, str, nullable = True)
    vampytest.assert_instance(user.flags, UserFlag)
    vampytest.assert_instance(user.id, int)
    vampytest.assert_instance(user.name, str)
    vampytest.assert_instance(user.name_plate, NamePlate, nullable = True)
    vampytest.assert_instance(user.primary_guild_badge, GuildBadge, nullable = True)


def test__OrinUserBase__new__no_fields():
    """
    Tests whether ``OrinUserBase.__new__`` works as intended.
    
    Case: No fields given.
    """
    user = OrinUserBase()
    _assert_fields_set(user)


def test__OrinUserBase__new__all_fields():
    """
    Tests whether ``OrinUserBase.__new__`` works as intended.
    
    Case: All fields given.
    """
    avatar = Icon(IconType.static, 32)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160066)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    discriminator = 2222
    display_name = 'Far'
    flags = UserFlag(1)
    name = 'voice in the dark'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030003,
    )
    primary_guild_badge = GuildBadge(guild_id = 202405180006, tag = 'miau')
    
    user = OrinUserBase(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        display_name = display_name,
        flags = flags,
        name = name,
        name_plate = name_plate,
        primary_guild_badge = primary_guild_badge,
    )
    _assert_fields_set(user)
    
    vampytest.assert_eq(user.avatar, avatar)
    vampytest.assert_eq(user.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(user.banner, banner)
    vampytest.assert_eq(user.banner_color, banner_color)
    vampytest.assert_eq(user.discriminator, discriminator)
    vampytest.assert_eq(user.display_name, display_name)
    vampytest.assert_eq(user.flags, flags)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.name_plate, name_plate)
    vampytest.assert_eq(user.primary_guild_badge, primary_guild_badge)


def test__OrinUserBase__create_empty():
    """
    Tests whether ``OrinUserBase._create_empty`` works as intended.
    """
    user_id = 202302040014
    user = OrinUserBase._create_empty(user_id)
    _assert_fields_set(user)
    
    vampytest.assert_eq(user.id, user_id)
