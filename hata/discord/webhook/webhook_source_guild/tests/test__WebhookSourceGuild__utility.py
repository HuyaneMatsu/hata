import vampytest

from ....bases import Icon, IconType
from ....guild import Guild

from ..guild import WebhookSourceGuild

from .test__WebhookSourceGuild__constructor import _assert_fields_set


def test__WebhookSourceGuild__copy():
    """
    Tests whether ``WebhookSourceGuild.copy`` works as intended.
    """
    guild_id = 202302010020
    icon = Icon(IconType.static, 12)
    name = 'senya'
    
    guild = WebhookSourceGuild(
        guild_id = guild_id,
        icon = icon,
        name = name,
    )
    copy = guild.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild)
    
    vampytest.assert_eq(copy, guild)


def test__WebhookSourceGuild__copy_with__0():
    """
    Tests whether ``WebhookSourceGuild.copy_with`` works as intended.
    
    Case: No fields given.
    """
    guild_id = 202302010021
    icon = Icon(IconType.static, 12)
    name = 'senya'
    
    guild = WebhookSourceGuild(
        guild_id = guild_id,
        icon = icon,
        name = name,
    )
    copy = guild.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild)
    
    vampytest.assert_eq(copy, guild)


def test__WebhookSourceGuild__copy_with__1():
    """
    Tests whether ``WebhookSourceGuild.copy_with`` works as intended.
    """
    old_guild_id = 202302010022
    old_icon = Icon(IconType.static, 12)
    old_name = 'senya'
    new_guild_id = 202302010023
    new_icon = Icon(IconType.animated, 13)
    new_name = 'yuuka'
    
    guild = WebhookSourceGuild(
        guild_id = old_guild_id,
        icon = old_icon,
        name = old_name,
    )
    copy = guild.copy_with(
        guild_id = new_guild_id,
        icon = new_icon,
        name = new_name,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild)

    vampytest.assert_eq(copy.id, new_guild_id)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.name, new_name)


def test__WebhookSourceGuild__guild():
    """
    Tests whether ``WebhookSourceGuild.guild`` works as intended.
    """
    guild_id = 202302010024
    icon = Icon(IconType.static, 12)
    name = 'senya'
    
    guild = WebhookSourceGuild(
        guild_id = guild_id,
        icon = icon,
        name = name,
    )
    
    source_guild = guild.guild
    vampytest.assert_instance(source_guild, Guild)
    vampytest.assert_eq(source_guild.id, guild_id)
    vampytest.assert_eq(source_guild.icon, icon)
    vampytest.assert_eq(source_guild.name, name)
