from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType
from ....color import Color
from ....role import Role
from ....utils import is_url

from ...avatar_decoration import AvatarDecoration

from ..flags import GuildProfileFlag
from ..guild_profile import GuildProfile

from .test__GuildProfile__constructor import _check_is_all_fields_set


def test__GuildProfile__copy():
    """
    Tests whether ``GuildProfile.copy`` works as intended.
    """
    avatar = Icon(IconType.static, 12)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150013)
    banner = Icon(IconType.static, 15)
    boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = GuildProfileFlag(3)
    joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    nick = 'Ayumi'
    pending = False
    role_ids = [202211110023, 202211110024]
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
    copy = guild_profile.copy()
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(guild_profile, copy)
    vampytest.assert_eq(guild_profile, copy)


def test__GuildProfile__copy_with__no_fields():
    """
    Tests whether ``GuildProfile.copy_with`` works as intended.
    
    Case: No fields given.
    """
    avatar = Icon(IconType.static, 12)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150014)
    banner = Icon(IconType.static, 15)
    boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    flags = GuildProfileFlag(3)
    joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    nick = 'Ayumi'
    pending = False
    role_ids = [202211110023, 202211110024]
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
    copy = guild_profile.copy_with()
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(guild_profile, copy)
    vampytest.assert_eq(guild_profile, copy)


def test__GuildProfile__copy_with__all_fields():
    """
    Tests whether ``GuildProfile.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_avatar = Icon(IconType.static, 12)
    old_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150015)
    old_banner = Icon(IconType.static, 15)
    old_boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_joined_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    old_nick = 'Ayumi'
    old_pending = False
    old_role_ids = [202211110025, 202211110026]
    old_timed_out_until = DateTime(2016, 5, 20, tzinfo = TimeZone.utc)
    old_flags = GuildProfileFlag(3)
    
    new_avatar = Icon(IconType.animated, 13)
    new_avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 3), sku_id = 202407150016)
    new_banner = Icon(IconType.static, 15)
    new_boosts_since = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    new_joined_at = DateTime(2017, 5, 15, tzinfo = TimeZone.utc)
    new_nick = 'Necrophantasia'
    new_pending = True
    new_role_ids = [202211110027, 202211110028]
    new_timed_out_until = DateTime(2017, 5, 20, tzinfo = TimeZone.utc)
    new_flags = GuildProfileFlag(4)
    
    
    guild_profile = GuildProfile(
        avatar = old_avatar,
        avatar_decoration = old_avatar_decoration,
        banner = old_banner,
        boosts_since = old_boosts_since,
        flags = old_flags,
        joined_at = old_joined_at,
        nick = old_nick,
        pending = old_pending,
        role_ids = old_role_ids,
        timed_out_until = old_timed_out_until,
    )
    copy = guild_profile.copy_with(
        avatar = new_avatar,
        avatar_decoration = new_avatar_decoration,
        banner = new_banner,
        boosts_since = new_boosts_since,
        flags = new_flags,
        joined_at = new_joined_at,
        nick = new_nick,
        pending = new_pending,
        role_ids = new_role_ids,
        timed_out_until = new_timed_out_until,
    )
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(guild_profile, copy)

    vampytest.assert_eq(copy.avatar, new_avatar)
    vampytest.assert_eq(copy.avatar_decoration, new_avatar_decoration)
    vampytest.assert_eq(copy.banner, new_banner)
    vampytest.assert_eq(copy.boosts_since, new_boosts_since)
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.joined_at, new_joined_at)
    vampytest.assert_eq(copy.nick, new_nick)
    vampytest.assert_eq(copy.pending, new_pending)
    vampytest.assert_eq(copy.role_ids, tuple(new_role_ids))
    vampytest.assert_eq(copy.timed_out_until, new_timed_out_until)


def test__GuildProfile__get_top_role__default():
    """
    Tests whether ``GuildProfile.get_top_role`` works as intended.
    
    Case: default.
    """
    default = object()
    
    guild_profile = GuildProfile()
    
    top_role = guild_profile.get_top_role(default)
    vampytest.assert_is(default, top_role)


def test__GuildProfile__get_top_role__has_top_role():
    """
    Tests whether ``GuildProfile.get_top_role`` works as intended.
    
    Case: actually has top role.
    """
    role_id_0 = 202211110028
    role_id_1 = 202211110029
    
    role_0 = Role.precreate(role_id_0, position = 10)
    role_1 = Role.precreate(role_id_1, position = 8)
    
    role_ids = [role_id_0, role_id_1]
    
    guild_profile = GuildProfile(role_ids = role_ids)
    
    top_role = guild_profile.get_top_role()
    vampytest.assert_is(top_role, role_0)


def test__GuildProfile__get_top_role__no_roles_in_cache():
    """
    Tests whether ``GuildProfile.get_top_role`` works as intended.
    
    Case: no roles cached.
    """
    role_id_0 = 202211110030
    role_id_1 = 202211110031
    
    role_ids = [role_id_0, role_id_1]
    
    guild_profile = GuildProfile(role_ids = role_ids)
    
    top_role = guild_profile.get_top_role()
    vampytest.assert_eq(top_role.id, role_id_1)


def _iter_options__iter_role_ids():
    role_id_0 = 202211110032
    role_id_1 = 202211110033
    
    yield None, []
    yield [role_id_0], [role_id_0]
    yield [role_id_0, role_id_1], [role_id_0, role_id_1]


@vampytest._(vampytest.call_from(_iter_options__iter_role_ids()).returning_last())
def test__GuildProfile__iter_role_ids(input_role_ids):
    """
    Tests whether ``GuildProfile.iter_role_ids`` works as intended.
    
    Parameters
    ----------
    input_role_ids : `None | list<int>`
        Role identifiers to create the guild profile with.
    
    Returns
    -------
    output : `list<int>`
    """
    guild_profile = GuildProfile(role_ids = input_role_ids)
    return [*guild_profile.iter_role_ids()]


def _iter_options__iter_roles():
    role_id_0 = 202211110034
    role_id_1 = 202211110035
    
    role_0 = Role.precreate(role_id_0)
    role_1 = Role.precreate(role_id_1)
    
    yield None, []
    yield [role_id_0], [role_0]
    yield [role_id_0, role_id_1], [role_0, role_1]


@vampytest._(vampytest.call_from(_iter_options__iter_roles()).returning_last())
def test__GuildProfile__iter_roles(input_role_ids):
    """
    Tests whether ``GuildProfile.iter_roles`` works as intended.
    
    Parameters
    ----------
    input_role_ids : `None | list<int>`
        Role identifiers to create the guild profile with.
    
    Returns
    -------
    output : `list<Role>`
    """
    guild_profile = GuildProfile(role_ids = input_role_ids)
    return [*guild_profile.iter_roles()]


def _iter_options__roles():
    role_id_0 = 202211110036
    role_id_1 = 202211110037
    role_id_2 = 202211110038
    role_id_3 = 202211110039
    
    role_0 = Role.precreate(role_id_0)
    role_1 = Role.precreate(role_id_1)
    role_2 = Role.precreate(role_id_2, position = 1)
    role_3 = Role.precreate(role_id_3, position = 0)
    
    yield None, None
    yield [role_id_0, role_id_1], [role_0, role_1]
    yield [role_id_2, role_id_3], [role_3, role_2]


@vampytest._(vampytest.call_from(_iter_options__roles()).returning_last())
def test__GuildProfile__roles(input_role_ids):
    """
    Tests whether ``GuildProfile.roles`` works as intended.
    
    Parameters
    ----------
    input_role_ids : `None | list<int>`
        Role identifiers to create the guild profile with.
    
    Returns
    -------
    output : `None | list<Role>`
    """
    guild_profile = GuildProfile(role_ids = input_role_ids)
    output = guild_profile.roles
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Role)
    
    return output


def _iter_options__color():
    role_id_0 = 202211110040
    role_id_1 = 202211110041
    
    color_0 = Color(12345)
    color_1 = Color(23456)
    
    role_0 = Role.precreate(role_id_0, position = 0, color = color_0)
    role_1 = Role.precreate(role_id_1, position = 2, color = color_1)
    
    yield None, [role_0, role_1], Color(0)
    yield [role_id_0, role_id_1], [role_0, role_1], role_1.color
    yield [role_id_0], [role_0, role_1], role_0.color


@vampytest._(vampytest.call_from(_iter_options__color()).returning_last())
def test__GuildProfile__color(input_role_ids, extra):
    """
    Tests whether ``GuildProfile.color`` works as intended.
    
    Parameters
    ----------
    input_role_ids : `None | list<int>`
        Role identifiers to create the guild profile with.
    extra : `list<object>`
        Additional entities to keep in the cache.
    
    Returns
    -------
    output : ``Color``
    """
    guild_profile = GuildProfile(role_ids = input_role_ids)
    output = guild_profile.color
    vampytest.assert_instance(output, Color)
    return output


def test__GuildProfile__created_at():
    """
    Tests whether ``GuildProfile.created_at`` works as intended.
    
    Case: no roles cached.
    """
    joined_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    guild_profile = GuildProfile(joined_at = joined_at)
    vampytest.assert_eq(guild_profile.created_at, joined_at)


def _iter_options__avatar_decoration_url():
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150017)
    
    yield None, False
    yield avatar_decoration, True


@vampytest._(vampytest.call_from(_iter_options__avatar_decoration_url()).returning_last())
def test__GuildProfile__avatar_decoration_url(avatar_decoration):
    """
    Tests whether ``GuildProfile.avatar_decoration_url`` work as intended.
    
    Parameters
    ----------
    avatar_decoration : ``None | AvatarDecoration``
        Avatar decoration to create the guild profile with.
    
    Returns
    -------
    has_avatar_decoration_url : `bool`
    """
    guild_profile = GuildProfile(avatar_decoration = avatar_decoration)
    output = guild_profile.avatar_decoration_url
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)


def _iter_options__avatar_decoration_url_as():
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202407150018)
    
    yield None, {'ext': 'jpg', 'size': 128}, False
    yield avatar_decoration, {'ext': 'jpg', 'size': 128}, True


@vampytest._(vampytest.call_from(_iter_options__avatar_decoration_url_as()).returning_last())
def test__GuildProfile__avatar_decoration_url_as(avatar_decoration, keyword_parameters):
    """
    Tests whether ``GuildProfile.avatar_decoration_url_as`` work as intended.
    
    Parameters
    ----------
    avatar_decoration : ``None | AvatarDecoration``
        Avatar decoration to create the guild profile with.
    
    keyword_parameters : `dict<str, object>`
        Keyword parameters to use.
    
    Returns
    -------
    has_avatar_decoration_url : `bool`
    """
    guild_profile = GuildProfile(avatar_decoration = avatar_decoration)
    output = guild_profile.avatar_decoration_url_as(**keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    return (output is not None)
