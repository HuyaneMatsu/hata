from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....core import GUILD_BOOSTS
from ....utils import datetime_to_timestamp

from ..guild_boost import GuildBoost

from .test__GuildBoost__constructor import _assert_fields_set


def test__GuildBoost__from_data():
    """
    Tests whether ``GuildBoost.from_data`` works as intended.
    """
    guild_boost_id = 202507060014
    
    ended = True
    ends_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    guild_id = 202507060015
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_id = 202507060016
    
    data = {
        'id': str(guild_boost_id),
        
        'ended': ended,
        'ends_at': datetime_to_timestamp(ends_at),
        'guild_id': str(guild_id),
        'pause_ends_at': datetime_to_timestamp(paused_until),
        'user_id': str(user_id),
    }
    
    guild_boost = GuildBoost.from_data(data)
    _assert_fields_set(guild_boost)
    
    vampytest.assert_eq(guild_boost.ended, ended)
    vampytest.assert_eq(guild_boost.ends_at,ends_at)
    vampytest.assert_eq(guild_boost.guild_id, guild_id)
    vampytest.assert_eq(guild_boost.id, guild_boost_id)
    vampytest.assert_eq(guild_boost.paused_until, paused_until)
    vampytest.assert_eq(guild_boost.user_id, user_id)
    
    vampytest.assert_is(GUILD_BOOSTS.get(guild_boost_id, None), guild_boost)


def test__GuildBoost__set_attributes():
    """
    Tests whether ``GuildBoost._set_attributes`` works as intended.
    """
    guild_boost_id = 202507060020
    
    ended = True
    ends_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    guild_id = 202507060021
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_id = 202507060022
    
    data = {
        'ended': ended,
        'ends_at': datetime_to_timestamp(ends_at),
        'guild_id': str(guild_id),
        'pause_ends_at': datetime_to_timestamp(paused_until),
        'user_id': str(user_id),
    }
    
    guild_boost = GuildBoost.precreate(
        guild_boost_id,
    )
    guild_boost._set_attributes(data)
    _assert_fields_set(guild_boost)
    
    vampytest.assert_eq(guild_boost.ended, ended)
    vampytest.assert_eq(guild_boost.ends_at,ends_at)
    vampytest.assert_eq(guild_boost.guild_id, guild_id)
    vampytest.assert_eq(guild_boost.paused_until, paused_until)
    vampytest.assert_eq(guild_boost.user_id, user_id)


def test__GuildBoost__update_attributes():
    """
    Tests whether ``GuildBoost._update_attributes`` works as intended.
    """
    guild_boost_id = 202507060023
    
    ended = True
    ends_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    data = {
        'ended': ended,
        'ends_at': datetime_to_timestamp(ends_at),
        'pause_ends_at': datetime_to_timestamp(paused_until),
    }
    
    guild_boost = GuildBoost.precreate(
        guild_boost_id,
    )
    guild_boost._update_attributes(data)
    _assert_fields_set(guild_boost)
    
    vampytest.assert_eq(guild_boost.ended, ended)
    vampytest.assert_eq(guild_boost.ends_at, ends_at)
    vampytest.assert_eq(guild_boost.paused_until, paused_until)


def test__GuildBoost__difference_update_attributes():
    """
    Tests whether ``GuildBoost._difference_update_attributes`` works as intended.
    """
    guild_boost_id = 202507060023
    
    old_ended = True
    old_ends_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    old_paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    new_ended = False
    new_ends_at = DateTime(2016, 6, 15, tzinfo = TimeZone.utc)
    new_paused_until = DateTime(2016, 6, 14, tzinfo = TimeZone.utc)
    
    data = {
        'ended': new_ended,
        'ends_at': datetime_to_timestamp(new_ends_at),
        'pause_ends_at': datetime_to_timestamp(new_paused_until),
    }
    
    guild_boost = GuildBoost.precreate(
        guild_boost_id,
        ended = old_ended,
        ends_at = old_ends_at,
        paused_until = old_paused_until,
    )
    output = guild_boost._difference_update_attributes(data)
    _assert_fields_set(guild_boost)
    
    vampytest.assert_eq(guild_boost.ended, new_ended)
    vampytest.assert_eq(guild_boost.ends_at, new_ends_at)
    vampytest.assert_eq(guild_boost.paused_until, new_paused_until)
    
    vampytest.assert_instance(output, dict)
    
    vampytest.assert_eq(
        output,
        {
            'ended': old_ended,
            'ends_at': old_ends_at,
            'paused_until': old_paused_until,
        },
    )


def test__GuildBoost__to_data():
    """
    Tests whether ``GuildBoost.to_data`` works as intended.
    
    Case: Include defaults and internals.
    """
    guild_boost_id = 202507060017
    
    ended = True
    ends_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    guild_id = 202507060018
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_id = 202507060019
    
    guild_boost = GuildBoost.precreate(
        guild_boost_id,
        
        ended = ended,
        ends_at = ends_at,
        guild_id = guild_id,
        paused_until = paused_until,
        user_id = user_id,
    )
    
    expected_output = {
        'id': str(guild_boost_id),
        
        'ended': ended,
        'ends_at': datetime_to_timestamp(ends_at),
        'guild_id': str(guild_id),
        'pause_ends_at': datetime_to_timestamp(paused_until),
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        guild_boost.to_data(defaults = True, include_internals = True),
        expected_output,
    )
