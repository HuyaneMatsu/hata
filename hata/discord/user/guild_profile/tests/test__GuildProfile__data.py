from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType
from ....utils import datetime_to_timestamp

from ...avatar_decoration import AvatarDecoration

from ..flags import GuildProfileFlag
from ..guild_profile import GuildProfile

from .test__GuildProfile__constructor import _assert_fields_set


def test__GuildProfile__from_data():
    """
    Tests whether ``GuildProfile.from_data`` works as intended.
    """
    avatar = Icon(IconType.static, 12)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150005)
    banner = Icon(IconType.static, 15)
    boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = GuildProfileFlag(3)
    joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100013, 2022100014]
    timed_out_until = DateTime(2016, 5, 20, tzinfo = TimeZone.utc)
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'banner': banner.as_base_16_hash,
        'premium_since': datetime_to_timestamp(boosts_since),
        'joined_at': datetime_to_timestamp(joined_at),
        'nick': nick,
        'pending': pending,
        'roles': [str(role_id) for role_id in role_ids],
        'communication_disabled_until': datetime_to_timestamp(timed_out_until),
        'flags': int(flags),
    }
    
    guild_profile = GuildProfile.from_data(data)
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


def test__GuildProfile__to_data():
    """
    Tests whether ``GuildProfile.to_data`` works as intended.
    """
    avatar = Icon(IconType.static, 12)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150006)
    banner = Icon(IconType.static, 15)
    boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = GuildProfileFlag(3)
    joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100015, 2022100016]
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
    
    vampytest.assert_eq(
        guild_profile.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'avatar': avatar.as_base_16_hash,
            'avatar_decoration_data': avatar_decoration.to_data(defaults = True),
            'banner': banner.as_base_16_hash,
            'premium_since': datetime_to_timestamp(boosts_since),
            'joined_at': datetime_to_timestamp(joined_at),
            'nick': nick,
            'pending': pending,
            'roles': [str(role_id) for role_id in role_ids],
            'communication_disabled_until': datetime_to_timestamp(timed_out_until),
            'flags': int(flags),
        },
    )


def test__Guild_profile__set_joined__already_set():
    """
    Tests whether ``GuildProfile._set_joined`` works as intended.
    
    Case: already set.
    """
    joined_at_0 = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    joined_at_1 = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    guild_profile = GuildProfile(joined_at = joined_at_0)
    guild_profile._set_joined({'joined_at': datetime_to_timestamp(joined_at_1)})
    vampytest.assert_eq(guild_profile.joined_at, joined_at_0)


def test__Guild_profile__set_joined__1not_yet_set():
    """
    Tests whether ``GuildProfile._set_joined`` works as intended.
    
    Case: not yet set.
    """
    joined_at_0 = None
    joined_at_1 = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    guild_profile = GuildProfile(joined_at = joined_at_0)
    guild_profile._set_joined({'joined_at': datetime_to_timestamp(joined_at_1)})
    vampytest.assert_eq(guild_profile.joined_at, joined_at_1)


def test__GuildProfile__update_attributes():
    """
    Tests whether ``GuildProfile._update_attributes`` works as intended.
    """
    avatar = Icon(IconType.static, 12)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150007)
    banner = Icon(IconType.static, 15)
    boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = GuildProfileFlag(3)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100017, 2022100018]
    timed_out_until = DateTime(2016, 5, 20, tzinfo = TimeZone.utc)
    
    data = {
        'avatar': avatar.as_base_16_hash,
        'avatar_decoration_data': avatar_decoration.to_data(),
        'banner': banner.as_base_16_hash,
        'premium_since': datetime_to_timestamp(boosts_since),
        'nick': nick,
        'pending': pending,
        'roles': [str(role_id) for role_id in role_ids],
        'communication_disabled_until': datetime_to_timestamp(timed_out_until),
        'flags': int(flags),
    }
    
    guild_profile = GuildProfile()
    guild_profile._update_attributes(data)
    
    vampytest.assert_eq(guild_profile.avatar, avatar)
    vampytest.assert_eq(guild_profile.avatar_decoration, avatar_decoration)
    vampytest.assert_eq(guild_profile.banner, banner)
    vampytest.assert_eq(guild_profile.boosts_since, boosts_since)
    vampytest.assert_eq(guild_profile.flags, flags)
    vampytest.assert_eq(guild_profile.nick, nick)
    vampytest.assert_eq(guild_profile.pending, pending)
    vampytest.assert_eq(guild_profile.role_ids, tuple(role_ids))
    vampytest.assert_eq(guild_profile.timed_out_until, timed_out_until)


def test__GuildProfile__difference_update_attributes():
    """
    Tests whether ``GuildProfile._difference_update_attributes`` works as intended.
    """
    old_avatar = Icon(IconType.static, 12)
    old_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150008)
    old_banner = Icon(IconType.static, 15)
    old_boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_nick = 'Ayumi'
    old_pending = False
    old_role_ids = [2022100019, 2022100020]
    old_timed_out_until = DateTime(2016, 5, 20, tzinfo = TimeZone.utc)
    old_flags = GuildProfileFlag(3)
    
    new_avatar = Icon(IconType.animated, 13)
    new_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 3), sku_id = 202407150009)
    new_banner = Icon(IconType.static, 16)
    new_boosts_since = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    new_nick = 'Necrophantasia'
    new_pending = True
    new_role_ids = [2022100021, 2022100022]
    new_timed_out_until = DateTime(2017, 5, 20, tzinfo = TimeZone.utc)
    new_flags = GuildProfileFlag(4)
    
    data = {
        'avatar': new_avatar.as_base_16_hash,
        'avatar_decoration_data': new_avatar_decoration.to_data(),
        'banner': new_banner.as_base_16_hash,
        'premium_since': datetime_to_timestamp(new_boosts_since),
        'nick': new_nick,
        'pending': new_pending,
        'roles': [str(role_id) for role_id in new_role_ids],
        'communication_disabled_until': datetime_to_timestamp(new_timed_out_until),
        'flags': int(new_flags),
    }
    
    guild_profile = GuildProfile(
        avatar = old_avatar,
        avatar_decoration = old_avatar_decoration,
        banner = old_banner,
        boosts_since = old_boosts_since,
        flags = old_flags,
        nick = old_nick,
        pending = old_pending,
        role_ids = old_role_ids,
        timed_out_until = old_timed_out_until,
    )
    
    old_attributes = guild_profile._difference_update_attributes(data)
    
    vampytest.assert_eq(guild_profile.avatar, new_avatar)
    vampytest.assert_eq(guild_profile.avatar_decoration, new_avatar_decoration)
    vampytest.assert_eq(guild_profile.banner, new_banner)
    vampytest.assert_eq(guild_profile.boosts_since, new_boosts_since)
    vampytest.assert_eq(guild_profile.flags, new_flags)
    vampytest.assert_eq(guild_profile.nick, new_nick)
    vampytest.assert_eq(guild_profile.pending, new_pending)
    vampytest.assert_eq(guild_profile.role_ids, tuple(new_role_ids))
    vampytest.assert_eq(guild_profile.timed_out_until, new_timed_out_until)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'avatar': old_avatar,
            'avatar_decoration': old_avatar_decoration,
            'banner': old_banner,
            'boosts_since': old_boosts_since,
            'flags': old_flags,
            'nick': old_nick,
            'pending': old_pending,
            'role_ids': tuple(old_role_ids),
            'timed_out_until': old_timed_out_until,
        },
    )
