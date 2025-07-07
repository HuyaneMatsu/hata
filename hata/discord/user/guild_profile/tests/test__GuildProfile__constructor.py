from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType

from ...avatar_decoration import AvatarDecoration

from ..flags import GuildProfileFlag
from ..guild_profile import GuildProfile


def _assert_fields_set(guild_profile):
    """
    Asserts whether all fields of the given guild profile are set.
    
    Parameters
    ----------
    guild_profile : ``GuildProfile``
    """
    vampytest.assert_instance(guild_profile, GuildProfile)
    vampytest.assert_instance(guild_profile.avatar, Icon)
    vampytest.assert_instance(guild_profile.avatar_decoration, AvatarDecoration, nullable = True)
    vampytest.assert_instance(guild_profile.banner, Icon)
    vampytest.assert_instance(guild_profile.boosts_since, DateTime, nullable = True)
    vampytest.assert_instance(guild_profile.flags, GuildProfileFlag)
    vampytest.assert_instance(guild_profile.joined_at, DateTime, nullable = True)
    vampytest.assert_instance(guild_profile.nick, str, nullable = True)
    vampytest.assert_instance(guild_profile.pending, bool)
    vampytest.assert_instance(guild_profile.role_ids, tuple, nullable = True)
    vampytest.assert_instance(guild_profile.timed_out_until, DateTime, nullable = True)


def test__GuildProfile__new__no_fields():
    """
    Tests whether ``GuildProfile.__new__`` works as intended.
    
    Case: No fields.
    """
    guild_profile = GuildProfile()
    _assert_fields_set(guild_profile)



def test__GuildProfile__new__all_fields():
    """
    Tests whether ``GuildProfile.__new__`` works as intended.
    
    Case: all fields.
    """
    avatar = Icon(IconType.static, 12)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150004)
    banner = Icon(IconType.static, 15)
    boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = GuildProfileFlag(3)
    joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100005, 2022100006]
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
    _assert_fields_set(guild_profile)
    
    vampytest.assert_eq(guild_profile.avatar, avatar)
    vampytest.assert_eq(guild_profile.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(guild_profile.banner, banner)
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
    """
    guild_profile = GuildProfile._create_empty()
    _assert_fields_set(guild_profile)
