import vampytest

from ..scheduled_event_unsubscribe_event import ScheduledEventUnsubscribeEvent


def test__ScheduledEventUnsubscribeEvent__repr():
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.__repr__`` works as intended.
    """
    guild_id = 202303120045
    scheduled_event_id = 202303120046
    user_id = 202303120047
    
    event = ScheduledEventUnsubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        user_id = user_id,
    )
    
    vampytest.assert_instance(repr(event), str)


def test__ScheduledEventUnsubscribeEvent__hash():
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.__hash__`` works as intended.
    """
    guild_id = 202303120048
    scheduled_event_id = 202303120049
    user_id = 202303120050
    
    event = ScheduledEventUnsubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        user_id = user_id,
    )
    
    vampytest.assert_instance(hash(event), int)


def _iter_options__eq():
    guild_id = 202303120051
    scheduled_event_id = 202303120052
    user_id = 202303120053
    
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
def test__ScheduledEventUnsubscribeEvent__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.__eq__`` works as intended.
    
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
    event_0 = ScheduledEventUnsubscribeEvent(**keyword_parameters_0)
    event_1 = ScheduledEventUnsubscribeEvent(**keyword_parameters_1)
    
    output = event_0 == event_1
    vampytest.assert_instance(output, bool)
    return output


def test__ScheduledEventUnsubscribeEvent__unpack():
    """
    Tests whether ``ScheduledEventUnsubscribeEvent`` unpacking works as intended.
    """
    guild_id = 202303120054
    scheduled_event_id = 202303120055
    user_id = 202303120056
    
    event = ScheduledEventUnsubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        user_id = user_id,
    )
    
    vampytest.assert_eq(len([*event]), len(event))
