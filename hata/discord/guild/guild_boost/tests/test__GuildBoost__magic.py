from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..guild_boost import GuildBoost


def test__GuildBoost__repr():
    """
    Tests whether ``GuildBoost.__repr__`` works as intended.
    """
    guild_boost_id = 202507060030
    
    ended = True
    ends_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    guild_id = 202507060031
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_id = 202507060032
    
    
    guild_boost = GuildBoost.precreate(
        guild_boost_id,
        
        ended = ended,
        ends_at = ends_at,
        guild_id = guild_id,
        paused_until = paused_until,
        user_id = user_id,
    )
    
    vampytest.assert_instance(repr(guild_boost), str)

    
    guild_boost = GuildBoost(
        paused_until = paused_until,
    )
    
    vampytest.assert_instance(repr(guild_boost), str)


def test__GuildBoost__hash():
    """
    Tests whether ``GuildBoost.__hash__`` works as intended.
    """
    guild_boost_id = 202507060033
    
    ended = True
    ends_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    guild_id = 202507060034
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_id = 202507060035
    
    
    guild_boost = GuildBoost.precreate(
        guild_boost_id,
        
        ended = ended,
        ends_at = ends_at,
        guild_id = guild_id,
        paused_until = paused_until,
        user_id = user_id,
    )
    
    vampytest.assert_instance(hash(guild_boost), int)

    
    guild_boost = GuildBoost(
        paused_until = paused_until,
    )
    
    vampytest.assert_instance(hash(guild_boost), int)


def _iter_options__eq():
    paused_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    keyword_parameters = {
        'paused_until': paused_until,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'paused_until': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__GuildBoost__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``GuildBoost.__eq__`` works as intended.
    
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
    guild_boost_0 = GuildBoost(**keyword_parameters_0)
    guild_boost_1 = GuildBoost(**keyword_parameters_1)
    
    output = guild_boost_0 == guild_boost_1
    vampytest.assert_instance(output, bool)
    return output
