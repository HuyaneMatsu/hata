from datetime import datetime as DateTime

import vampytest

from ....bases import Icon, IconType
from ....role import Role

from ..guild_profile import GuildProfile

from .test__GuildProfile__constructor import _check_is_all_fields_set


def test__GuildProfile__copy():
    """
    Tests whether ``GuildProfile.copy`` works as intended.
    """
    avatar = Icon(IconType.static, 12)
    boosts_since = DateTime(2016, 5, 14)
    joined_at = DateTime(2016, 5, 15)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100023, 2022100024]
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
    copy = guild_profile.copy()
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(guild_profile, copy)
    vampytest.assert_eq(guild_profile, copy)


def test__GuildProfile__copy_with__0():
    """
    Tests whether ``GuildProfile.copy_with`` works as intended.
    
    Case: No fields given.
    """
    avatar = Icon(IconType.static, 12)
    boosts_since = DateTime(2016, 5, 14)
    joined_at = DateTime(2016, 5, 15)
    nick = 'Ayumi'
    pending = False
    role_ids = [2022100023, 2022100024]
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
    copy = guild_profile.copy_with()
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(guild_profile, copy)
    vampytest.assert_eq(guild_profile, copy)


def test__GuildProfile__copy_with__1():
    """
    Tests whether ``GuildProfile.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_avatar = Icon(IconType.static, 12)
    new_avatar = Icon(IconType.animated, 13)
    old_boosts_since = DateTime(2016, 5, 14)
    new_boosts_since = DateTime(2017, 5, 14)
    old_joined_at = DateTime(2016, 5, 15)
    new_joined_at = DateTime(2017, 5, 15)
    old_nick = 'Ayumi'
    new_nick = 'Necrophantasia'
    old_pending = False
    new_pending = True
    old_role_ids = [2022100025, 2022100026]
    new_role_ids = [2022100027, 2022100028]
    old_timed_out_until = DateTime(2016, 5, 20)
    new_timed_out_until = DateTime(2017, 5, 20)
    
    
    guild_profile = GuildProfile(
        avatar = old_avatar,
        boosts_since = old_boosts_since,
        joined_at = old_joined_at,
        nick = old_nick,
        pending = old_pending,
        role_ids = old_role_ids,
        timed_out_until = old_timed_out_until,
    )
    copy = guild_profile.copy_with(
        avatar = new_avatar,
        boosts_since = new_boosts_since,
        joined_at = new_joined_at,
        nick = new_nick,
        pending = new_pending,
        role_ids = new_role_ids,
        timed_out_until = new_timed_out_until,
    )
    
    _check_is_all_fields_set(copy)
    vampytest.assert_not_is(guild_profile, copy)

    vampytest.assert_eq(copy.avatar, new_avatar)
    vampytest.assert_eq(copy.joined_at, new_joined_at)
    vampytest.assert_eq(copy.boosts_since, new_boosts_since)
    vampytest.assert_eq(copy.nick, new_nick)
    vampytest.assert_eq(copy.pending, new_pending)
    vampytest.assert_eq(copy.role_ids, tuple(new_role_ids))
    vampytest.assert_eq(copy.timed_out_until, new_timed_out_until)


def test__GuildProfile__get_top_role__0():
    """
    Tests whether ``GuildProfile.get_top_role`` works as intended.
    
    Case: default.
    """
    default = object()
    
    guild_profile = GuildProfile()
    
    top_role = guild_profile.get_top_role(default)
    vampytest.assert_is(default, top_role)



def test__GuildProfile__get_top_role__1():
    """
    Tests whether ``GuildProfile.get_top_role`` works as intended.
    
    Case: actually has top role.
    """
    role_id_1 = 2022100028
    role_id_2 = 2022100029
    
    role_1 = Role.precreate(role_id_1, position = 10)
    role_2 = Role.precreate(role_id_2, position = 8)
    
    role_ids = [role_id_1, role_id_2]
    
    guild_profile = GuildProfile(role_ids = role_ids)
    
    top_role = guild_profile.get_top_role()
    vampytest.assert_is(top_role, role_1)


def test__GuildProfile__get_top_role__2():
    """
    Tests whether ``GuildProfile.get_top_role`` works as intended.
    
    Case: no roles cached.
    """
    role_id_1 = 2022100030
    role_id_2 = 2022100031
    
    role_ids = [role_id_1, role_id_2]
    
    guild_profile = GuildProfile(role_ids = role_ids)
    
    top_role = guild_profile.get_top_role()
    vampytest.assert_eq(top_role.id, role_id_2)


def test__GuildProfile__iter_role_ids():
    """
    Tests whether ``GuildProfile.get_top_role`` works as intended.
    """
    for input_role_ids, expected_output in (
        (None, []),
        ([2022100032, 2022100033], [2022100032, 2022100033]),
    ):
        guild_profile = GuildProfile(role_ids = input_role_ids)
        output_role_ids = [*guild_profile.iter_role_ids()]
        vampytest.assert_eq(output_role_ids, expected_output)


def test__GuildProfile__iter_roles():
    """
    Tests whether ``GuildProfile.get_top_role`` works as intended.
    """
    for input_role_ids, expected_output in (
        (None, []),
        ([2022100034, 2022100035], [Role.precreate(2022100034), Role.precreate(2022100035)]),
    ):
        guild_profile = GuildProfile(role_ids = input_role_ids)
        output_roles = [*guild_profile.iter_roles()]
        vampytest.assert_eq(output_roles, expected_output)


def test__GuildProfile__roles():
    """
    Tests whether ``GuildProfile.get_top_role`` works as intended.
    """
    for input_role_ids, expected_output in (
        (None, None),
        ([2022100036, 2022100037], [Role.precreate(2022100036), Role.precreate(2022100037)]),
        (
            [2022100038, 2022100039],
            [Role.precreate(2022100039, position = 0), Role.precreate(2022100038, position = 1)]
        ),
    ):
        guild_profile = GuildProfile(role_ids = input_role_ids)
        output_roles = guild_profile.roles
        vampytest.assert_eq(output_roles, expected_output)


def test__GuildProfile__color():
    """
    Tests whether ``GuildProfile.color`` works as intended.
    """
    role_1 = Role.precreate(2022100040, position = 0, color = 12345)
    role_2 = Role.precreate(2022100041, position = 2, color = 23456)
    
    for input_role_ids, expected_output in (
        (None, 0),
        ([role_1, role_2], role_2.color),
        ([role_1], role_1.color),
    ):
        guild_profile = GuildProfile(role_ids = input_role_ids)
        vampytest.assert_eq(guild_profile.color, expected_output)


def test__GuildProfile__created_at():
    """
    Tests whether ``GuildProfile.created_at`` works as intended.
    
    Case: no roles cached.
    """
    joined_at = DateTime(2020, 5, 14)
    guild_profile = GuildProfile(joined_at = joined_at)
    vampytest.assert_eq(guild_profile.created_at, joined_at)
