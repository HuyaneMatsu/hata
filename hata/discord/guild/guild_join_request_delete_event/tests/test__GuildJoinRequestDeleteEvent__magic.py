import vampytest

from ..guild_join_request_delete_event import GuildJoinRequestDeleteEvent


def test__GuildJoinRequestDeleteEvent__repr():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.__repr__`` works as intended.
    """
    guild_id = 202305160019
    user_id = 202305160020
    
    event = GuildJoinRequestDeleteEvent(
        guild_id = guild_id,
        user_id = user_id,
    )
    
    vampytest.assert_instance(repr(event), str)


def test__GuildJoinRequestDeleteEvent__hash():
    """
    Tests whether ``GuildJoinRequestDeleteEvent.__hash__`` works as intended.
    """
    guild_id = 202305160021
    user_id = 202305160022
    
    event = GuildJoinRequestDeleteEvent(
        guild_id = guild_id,
        user_id = user_id,
    )
    
    vampytest.assert_instance(hash(event), int)


def _iter_options__eq():
    guild_id = 202305160023
    user_id = 202305160024
    
    keyword_parameters = {
        'guild_id': guild_id,
        'user_id': user_id,
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
            'guild_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user_id': 0,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__GuildJoinRequestDeleteEvent__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``GuildJoinRequestDeleteEvent.__eq__`` works as intended.
    
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
    event_0 = GuildJoinRequestDeleteEvent(**keyword_parameters_0)
    event_1 = GuildJoinRequestDeleteEvent(**keyword_parameters_1)
    
    output = event_0 == event_1
    vampytest.assert_instance(output, bool)
    return output


def test__GuildJoinRequestDeleteEvent__unpack():
    """
    Tests whether ``GuildJoinRequestDeleteEvent`` unpacking works as intended.
    """
    guild_id = 202305160025
    user_id = 202305160026
    
    event = GuildJoinRequestDeleteEvent(
        guild_id = guild_id,
        user_id = user_id,
    )
    
    vampytest.assert_eq(len([*event]), len(event))
