from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType

from ...avatar_decoration import AvatarDecoration

from ..flags import GuildProfileFlag
from ..guild_profile import GuildProfile


def test__GuildProfile__repr():
    """
    Tests whether ``GuildProfile.__repr__`` works as intended.
    """
    avatar = Icon(IconType.static, 12)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150010)
    banner = Icon(IconType.static, 15)
    boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = GuildProfileFlag(3)
    joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100007, 2022100008]
    timed_out_until = DateTime(2016, 5, 20, tzinfo = TimeZone.utc)
    
    
    guild_profile = GuildProfile(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        boosts_since = boosts_since,
        flags = flags,
        joined_at = joined_at,
        nick = nick,
        pending = pending,
        role_ids = role_ids,
        timed_out_until = timed_out_until,
    )
    
    vampytest.assert_instance(repr(guild_profile), str)


def test__GuildProfile__hash():
    """
    Tests whether ``GuildProfile.__hash__`` works as intended.
    """
    avatar = Icon(IconType.static, 12)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150011)
    banner = Icon(IconType.static, 15)
    boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = GuildProfileFlag(3)
    joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100009, 2022100010]
    timed_out_until = DateTime(2016, 5, 20, tzinfo = TimeZone.utc)
    
    
    guild_profile = GuildProfile(
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        boosts_since = boosts_since,
        flags = flags,
        joined_at = joined_at,
        nick = nick,
        pending = pending,
        role_ids = role_ids,
        timed_out_until = timed_out_until,
    )
    
    vampytest.assert_instance(hash(guild_profile), int)


def _iter_options__eq():
    avatar = Icon(IconType.static, 12)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150012)
    banner = Icon(IconType.static, 15)
    boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = GuildProfileFlag(3)
    joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100011, 2022100012]
    timed_out_until = DateTime(2016, 5, 20, tzinfo = TimeZone.utc)
    
    keyword_parameters = {
        'avatar': avatar,
        'avatar_decoration': avatar_decoration,
        'banner': banner,
        'boosts_since': boosts_since,
        'flags': flags,
        'joined_at': joined_at,
        'nick': nick,
        'pending': pending,
        'role_ids': role_ids,
        'timed_out_until': timed_out_until,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'avatar': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'avatar_decoration': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'banner': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'boosts_since': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flags': GuildProfileFlag(0),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'joined_at': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'pending': True,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'role_ids': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'timed_out_until': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__GuildProfile__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``GuildProfile.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    guild_profile_0 = GuildProfile(**keyword_parameters_0)
    guild_profile_1 = GuildProfile(**keyword_parameters_1)
    
    output = guild_profile_0 == guild_profile_1
    vampytest.assert_instance(output, bool)
    return output
