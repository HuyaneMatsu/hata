from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....user import ClientUserBase, User, ZEROUSER

from ...guild import Guild

from ..guild_boost import GuildBoost

from .test__GuildBoost__constructor import _assert_fields_set


def test__GuildBoost__copy():
    """
    Tests whether ``GuildBoost.copy`` works as intended.
    """
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    guild_boost = GuildBoost(
        paused_until = paused_until,
    )
    copy = guild_boost.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(guild_boost, copy)

    vampytest.assert_eq(guild_boost, copy)



def test__GuildBoost__copy_with__no_fields():
    """
    Tests whether ``GuildBoost.copy_with`` works as intended.
    
    Case: no fields given.
    """
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    guild_boost = GuildBoost(
        paused_until = paused_until,
    )
    copy = guild_boost.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(guild_boost, copy)

    vampytest.assert_eq(guild_boost, copy)



def test__GuildBoost__copy_with__all_fields():
    """
    Tests whether ``GuildBoost.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    new_paused_until = DateTime(2016, 6, 14, tzinfo = TimeZone.utc)
    
    guild_boost = GuildBoost(
        paused_until = old_paused_until,
    )
    copy = guild_boost.copy_with(
        paused_until = new_paused_until,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(guild_boost, copy)

    vampytest.assert_eq(copy.paused_until, new_paused_until)


def _iter_options__guild():
    guild_id_0 = 202507060040
    guild_id_1 = 202507060041
    
    yield 202507060043, 0, None
    yield 202507060044, guild_id_0, None
    yield 202507060045, guild_id_1, Guild.precreate(guild_id_1)


@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__GuildBoost__guild(guild_boost_id, guild_id):
    """
    Tests whether ``GuildBoost.guild`` works as intended.
    
    Parameters
    ----------
    guild_boost_id : `int`
        Guild boost identifier.
    
    guild_id : `int`
        Guild identifier to create the guild_boost with.
    
    Returns
    -------
    guild : ``None | Guild``
    """
    guild_boost = GuildBoost.precreate(
        guild_boost_id,
        guild_id = guild_id,
    )
    
    output = guild_boost.guild
    vampytest.assert_instance(output, Guild, nullable = True)
    return output


def _iter_options__user():
    user_id_0 = 202507060046
    
    yield 202507060047, 0, ZEROUSER
    yield 202507060048, user_id_0, User.precreate(user_id_0)


@vampytest._(vampytest.call_from(_iter_options__user()).returning_last())
def test__GuildBoost__user(guild_boost_id, user_id):
    """
    Tests whether ``GuildBoost.user`` works as intended.
    
    Parameters
    ----------
    guild_boost_id : `int`
        Guild boost identifier.
    
    user_id : `int`
        User identifier to create the guild_boost with.
    
    Returns
    -------
    user : ``ClientUserBase``
    """
    guild_boost = GuildBoost.precreate(
        guild_boost_id,
        user_id = user_id,
    )
    
    output = guild_boost.user
    vampytest.assert_instance(output, ClientUserBase)
    return output


def test__GuildBoost__partial__true():
    """
    Tests whether ``GuildBoost.partial`` works as intended.
    
    Case: true.
    """
    guild_boost = GuildBoost()
    
    output = guild_boost.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__GuildBoost__partial__false():
    """
    Tests whether ``GuildBoost.partial`` works as intended.
    
    Case: false.
    """
    guild_boost_id = 202507060049
    
    guild_boost = GuildBoost.precreate(
        guild_boost_id,
    )
    
    output = guild_boost.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
