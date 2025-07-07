from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....core import GUILD_BOOSTS

from ..guild_boost import GuildBoost


def _assert_fields_set(guild_boost):
    """
    Checks whether every attribute is set of the given guild boost.
    
    Parameters
    ----------
    guild_boost : ``GuildBoost``
        The guild boost to check.
    """
    vampytest.assert_instance(guild_boost, GuildBoost)
    vampytest.assert_instance(guild_boost.ended, int)
    vampytest.assert_instance(guild_boost.ends_at, DateTime, nullable = True)
    vampytest.assert_instance(guild_boost.guild_id, int)
    vampytest.assert_instance(guild_boost.id, int)
    vampytest.assert_instance(guild_boost.paused_until, DateTime, nullable = True)
    vampytest.assert_instance(guild_boost.user_id, int)


def test__GuildBoost__new__no_fields():
    """
    Tests whether ``GuildBoost.__new__`` works as intended.
    
    Case: No fields given.
    """
    guild_boost = GuildBoost()
    _assert_fields_set(guild_boost)


def test__GuildBoost__new__all_fields():
    """
    Tests whether ``GuildBoost.__new__`` works as intended.
    
    Case: Fields given.
    """
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    guild_boost = GuildBoost(
        paused_until = paused_until,
    )
    _assert_fields_set(guild_boost)
    
    vampytest.assert_eq(guild_boost.paused_until, paused_until)


def test__GuildBoost__create_empty():
    """
    Tests whether ``GuildBoost._create_empty`` works as intended.
    
    Case: No fields given.
    """
    guild_boost_id = 202507060010
    
    guild_boost = GuildBoost._create_empty(guild_boost_id)
    _assert_fields_set(guild_boost)
    
    vampytest.assert_eq(guild_boost.id, guild_boost_id)


def test__GuildBoost_precreate():
    """
    Tests whether ``GuildBoost.precreate`` works as intended.
    
    Case: No fields given.
    """
    guild_boost_id = 202507060011
    
    ended = True
    ends_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    guild_id = 202507060012
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_id = 202507060013
    
    guild_boost = GuildBoost.precreate(
        guild_boost_id,
        
        ended = ended,
        ends_at = ends_at,
        guild_id = guild_id,
        paused_until = paused_until,
        user_id = user_id,
    )
    _assert_fields_set(guild_boost)
    
    vampytest.assert_eq(guild_boost.ended, ended)
    vampytest.assert_eq(guild_boost.ends_at, ends_at)
    vampytest.assert_eq(guild_boost.guild_id, guild_id)
    vampytest.assert_eq(guild_boost.id, guild_boost_id)
    vampytest.assert_eq(guild_boost.paused_until, paused_until)
    vampytest.assert_eq(guild_boost.user_id, user_id)
    
    vampytest.assert_is(GUILD_BOOSTS.get(guild_boost_id, None), guild_boost)
