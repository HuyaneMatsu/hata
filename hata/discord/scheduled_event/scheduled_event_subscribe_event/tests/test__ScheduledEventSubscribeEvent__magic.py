import vampytest

from ..scheduled_event_subscribe_event import ScheduledEventSubscribeEvent


def test__ScheduledEventSubscribeEvent__repr():
    """
    Tests whether ``ScheduledEventSubscribeEvent.__repr__`` works as intended.
    """
    guild_id = 202303120009
    scheduled_event_id = 202303120010
    user_id = 202303120011
    
    event = ScheduledEventSubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        user_id = user_id,
    )
    
    vampytest.assert_instance(repr(event), str)


def test__ScheduledEventSubscribeEvent__hash():
    """
    Tests whether ``ScheduledEventSubscribeEvent.__hash__`` works as intended.
    """
    guild_id = 202303120012
    scheduled_event_id = 202303120013
    user_id = 202303120014
    
    event = ScheduledEventSubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        user_id = user_id,
    )
    
    vampytest.assert_instance(hash(event), int)


def _iter_options__eq():
    guild_id = 202303120015
    scheduled_event_id = 202303120016
    user_id = 202303120017
    
    keyword_parameters = {
        'guild_id': guild_id,
        'scheduled_event_id': scheduled_event_id,
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
            'scheduled_event_id': 0,
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
def test__ScheduledEventSubscribeEvent__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ScheduledEventSubscribeEvent.__eq__`` works as intended.
    
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
    event_0 = ScheduledEventSubscribeEvent(**keyword_parameters_0)
    event_1 = ScheduledEventSubscribeEvent(**keyword_parameters_1)
    
    output = event_0 == event_1
    vampytest.assert_instance(output, bool)
    return output


def test__ScheduledEventSubscribeEvent__unpack():
    """
    Tests whether ``ScheduledEventSubscribeEvent`` unpacking works as intended.
    """
    guild_id = 202303120018
    scheduled_event_id = 202303120019
    user_id = 202303120020
    
    event = ScheduledEventSubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        user_id = user_id,
    )
    
    vampytest.assert_eq(len([*event]), len(event))
