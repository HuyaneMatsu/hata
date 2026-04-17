import vampytest

from ....bases import Icon, IconType
from ....guild import Guild

from ..guild import WebhookSourceGuild


def _assert_fields_set(guild):
    """
    Asserts whether every fields are set of the given webhook source guild.
    
    Parameters
    ----------
    guild : ``WebhookSourceGuild``
        The webhook source guild to check.
    """
    vampytest.assert_instance(guild, WebhookSourceGuild)
    vampytest.assert_instance(guild.icon, Icon)
    vampytest.assert_instance(guild.id, int)
    vampytest.assert_instance(guild.name, str)


def test__WebhookSourceGuild__new__0():
    """
    Tests whether ``WebhookSourceGuild.__new__`` works as intended.
    
    Case: No fields given.
    """
    guild = WebhookSourceGuild()
    _assert_fields_set(guild)


def test__WebhookSourceGuild__new__1():
    """
    Tests whether ``WebhookSourceGuild.__new__`` works as intended.
    
    Case: All fields given.
    """
    guild_id = 202302010012
    icon = Icon(IconType.static, 12)
    name = 'senya'
    
    guild = WebhookSourceGuild(
        guild_id = guild_id,
        icon = icon,
        name = name,
    )
    _assert_fields_set(guild)
    
    vampytest.assert_eq(guild.id, guild_id)
    vampytest.assert_eq(guild.icon, icon)
    vampytest.assert_eq(guild.name, name)


def test__WebhookSourceGuild__from_guild():
    """
    Tests whether ``WebhookSourceGuild.from_guild`` works as intended.
    """
    guild_id = 202302010013
    icon = Icon(IconType.static, 12)
    name = 'senya'
    
    source_guild = Guild.precreate(
        guild_id,
        icon = icon,
        name = name,
    )
    
    guild = WebhookSourceGuild.from_guild(source_guild)
    _assert_fields_set(guild)
    
    vampytest.assert_eq(guild.id, guild_id)
    vampytest.assert_eq(guild.icon, icon)
    vampytest.assert_eq(guild.name, name)
