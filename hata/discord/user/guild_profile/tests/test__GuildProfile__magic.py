from datetime import datetime as DateTime

import vampytest

from ....bases import Icon, IconType

from ..guild_profile import GuildProfile


def test__GuildProfile__repr():
    """
    Tests whether ``GuildProfile.__repr__`` works as intended.
    """
    avatar = Icon(IconType.static, 12)
    boosts_since = DateTime(2016, 5, 14)
    joined_at = DateTime(2016, 5, 15)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100007, 2022100008]
    timed_out_until = DateTime(2016, 5, 20)
    
    
    guild_profile = GuildProfile(
        avatar = avatar,
        boosts_since = boosts_since,
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
    boosts_since = DateTime(2016, 5, 14)
    joined_at = DateTime(2016, 5, 15)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100009, 2022100010]
    timed_out_until = DateTime(2016, 5, 20)
    
    
    guild_profile = GuildProfile(
        avatar = avatar,
        boosts_since = boosts_since,
        joined_at = joined_at,
        nick = nick,
        pending = pending,
        role_ids = role_ids,
        timed_out_until = timed_out_until,
    )
    
    vampytest.assert_instance(hash(guild_profile), int)


def test__GuildProfile__eq():
    """
    Tests whether ``GuildProfile.__eq__`` works as intended.
    """
    avatar = Icon(IconType.static, 12)
    boosts_since = DateTime(2016, 5, 14)
    joined_at = DateTime(2016, 5, 15)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100011, 2022100012]
    timed_out_until = DateTime(2016, 5, 20)
    
    keyword_parameters = {
        'avatar': avatar,
        'boosts_since': boosts_since,
        'joined_at': joined_at,
        'nick': nick,
        'pending': pending,
        'role_ids': role_ids,
        'timed_out_until': timed_out_until,
    }
    
    guild_profile = GuildProfile(**keyword_parameters)
    
    vampytest.assert_eq(guild_profile, guild_profile)
    vampytest.assert_ne(guild_profile, object())
    
    for field_name, field_value in (
        ('avatar', None),
        ('boosts_since', None),
        ('nick', None),
        ('pending', True),
        ('role_ids', None),
        ('timed_out_until', None),
    ):
        test_guild_profile = GuildProfile(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(guild_profile, test_guild_profile)
