from datetime import datetime as DateTime

import vampytest

from ....bases import Icon, IconType

from ..flags import GuildProfileFlag
from ..guild_profile import GuildProfile


def _check_is_all_fields_set(guild_profile):
    """
    Asserts whether all fields of the given guild profiles are set.
    
    Parameters
    ----------
    guild_profile : ``GuildProfile``
    """
    vampytest.assert_instance(guild_profile, GuildProfile)
    vampytest.assert_instance(guild_profile.avatar, Icon)
    vampytest.assert_instance(guild_profile.boosts_since, DateTime, nullable = True)
    vampytest.assert_instance(guild_profile.flags, GuildProfileFlag)
    vampytest.assert_instance(guild_profile.joined_at, DateTime, nullable = True)
    vampytest.assert_instance(guild_profile.nick, str, nullable = True)
    vampytest.assert_instance(guild_profile.pending, bool)
    vampytest.assert_instance(guild_profile.role_ids, tuple, nullable = True)
    vampytest.assert_instance(guild_profile.timed_out_until, DateTime, nullable = True)


def test__GuildProfile__new__0():
    """
    Tests whether ``GuildProfile.__new__`` works as intended.
    
    Case: No parameters.
    """
    guild_profile = GuildProfile()
    _check_is_all_fields_set(guild_profile)



def test__GuildProfile__new__1():
    """
    Tests whether ``GuildProfile.__new__`` works as intended.
    
    Case: include internals & defaults.
    """
    avatar = Icon(IconType.static, 12)
    boosts_since = DateTime(2016, 5, 14)
    flags = GuildProfileFlag(3)
    joined_at = DateTime(2016, 5, 15)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100005, 2022100006]
    timed_out_until = DateTime(2016, 5, 20)
    
    
    guild_profile = GuildProfile(
        avatar = avatar,
        boosts_since = boosts_since,
        flags = flags,
        joined_at = joined_at,
        nick = nick,
        pending = pending,
        role_ids = role_ids,
        timed_out_until = timed_out_until,
    )
    _check_is_all_fields_set(guild_profile)
    
    vampytest.assert_eq(guild_profile.avatar, avatar)
    vampytest.assert_eq(guild_profile.boosts_since, boosts_since)
    vampytest.assert_eq(guild_profile.flags, flags)
    vampytest.assert_eq(guild_profile.joined_at, joined_at)
    vampytest.assert_eq(guild_profile.nick, nick)
    vampytest.assert_eq(guild_profile.pending, pending)
    vampytest.assert_eq(guild_profile.role_ids, tuple(role_ids))
    vampytest.assert_eq(guild_profile.timed_out_until, timed_out_until)


def test__GuildProfile__create_empty():
    """
    Tests whether ``GuildProfile._create_empty`` works as intended.
    
    Case: No parameters.
    """
    guild_profile = GuildProfile._create_empty()
    _check_is_all_fields_set(guild_profile)
