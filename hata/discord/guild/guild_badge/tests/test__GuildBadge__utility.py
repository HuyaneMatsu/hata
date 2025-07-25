import vampytest

from ....bases import Icon, IconType
from ....guild import Guild

from ..guild_badge import GuildBadge

from .test__GuildBadge__constructor import _assert_fields_set


def test__GuildBadge__copy():
    """
    Tests whether ``GuildBadge.copy`` works as intended.
    """
    enabled = False
    guild_id = 202405170010
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    guild = GuildBadge(
        enabled = enabled,
        guild_id = guild_id,
        icon = icon,
        tag = tag,
    )
    copy = guild.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild)
    
    vampytest.assert_eq(copy, guild)


def test__GuildBadge__copy_with__no_fields():
    """
    Tests whether ``GuildBadge.copy_with`` works as intended.
    
    Case: No fields given.
    """
    enabled = False
    guild_id = 202405170011
    icon = Icon(IconType.static, 12)
    tag = 'ORIN'
    
    guild = GuildBadge(
        enabled = enabled,
        guild_id = guild_id,
        icon = icon,
        tag = tag,
    )
    copy = guild.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild)
    
    vampytest.assert_eq(copy, guild)


def test__GuildBadge__copy_with__all_fields():
    """
    Tests whether ``GuildBadge.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_enabled = False
    old_guild_id = 202405170012
    old_icon = Icon(IconType.static, 12)
    old_tag = 'ORIN'
    
    new_enabled = True
    new_guild_id = 202405170013
    new_icon = Icon(IconType.animated, 13)
    new_tag = 'OKUU'
    
    guild_badge = GuildBadge(
        enabled = old_enabled,
        guild_id = old_guild_id,
        icon = old_icon,
        tag = old_tag,
    )
    copy = guild_badge.copy_with(
        enabled = new_enabled,
        guild_id = new_guild_id,
        icon = new_icon,
        tag = new_tag,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_badge)

    vampytest.assert_eq(copy.enabled, new_enabled)
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.tag, new_tag)


def _iter_options__guild():
    guild_id_0 = 202405170014
    guild_id_1 = 202405170015
    
    yield 0, None
    yield guild_id_0, None
    yield guild_id_1, Guild.precreate(guild_id_1)


@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__GuildBadge__guild(guild_id):
    """
    Tests whether ``GuildBadge.guild`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to test with.
    
    Returns
    -------
    guild : ``None | Guild``
    """
    guild_badge = GuildBadge(
        guild_id = guild_id,
    )
    
    output = guild_badge.guild
    vampytest.assert_instance(output, Guild, nullable = True)
    return output


def _iter_options__icon_url():
    yield 202505310026, None, False
    yield 202505310027, Icon(IconType.animated, 5), True


@vampytest._(vampytest.call_from(_iter_options__icon_url()).returning_last())
def test__GuildBadge__icon_url(guild_id, icon):
    """
    Tests whether ``GuildBadge.icon_url`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Identifier to create guild badge with.
    
    icon : ``None | Icon``
        Icon to create the guild badge with.
    
    Returns
    -------
    has_icon_url : `bool`
    """
    guild_badge = GuildBadge(
        guild_id = guild_id,
        icon = icon,
    )
    
    output = guild_badge.icon_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__icon_url_as():
    yield 202505310028, None, {'ext': 'webp', 'size': 128}, False
    yield 202505310029, Icon(IconType.animated, 5), {'ext': 'webp', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__icon_url_as()).returning_last())
def test__GuildBadge__icon_url_as(guild_id, icon, keyword_parameters):
    """
    Tests whether ``GuildBadge.icon_url_as`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Identifier to create guild badge with.
    
    icon : ``None | Icon``
        Icon to create the guild badge with.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass.
    
    Returns
    -------
    has_icon_url : `bool`
    """
    guild_badge = GuildBadge(
        guild_id = guild_id,
        icon = icon,
    )
    
    output = guild_badge.icon_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
