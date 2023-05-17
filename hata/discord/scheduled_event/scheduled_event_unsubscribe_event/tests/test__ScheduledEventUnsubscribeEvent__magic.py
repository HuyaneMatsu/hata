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


def test__ScheduledEventUnsubscribeEvent__eq():
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.__repr__`` works as intended.
    """
    guild_id = 202303120051
    scheduled_event_id = 202303120052
    user_id = 202303120053
    
    keyword_parameters = {
        'guild_id': guild_id,
        'scheduled_event_id': scheduled_event_id,
        'user_id': user_id,
    }
    
    event = ScheduledEventUnsubscribeEvent(**keyword_parameters)
    
    vampytest.assert_eq(event, event)
    vampytest.assert_eq(event, object)
    
    for event_name, event_value in (
        ('guild_id', 0),
        ('scheduled_event_id', 0),
        ('user_id', 0),
    ):
        event_altered = ScheduledEventUnsubscribeEvent(**{**keyword_parameters, event_name: event_value})
        vampytest.assert_ne(event, event_altered)


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
