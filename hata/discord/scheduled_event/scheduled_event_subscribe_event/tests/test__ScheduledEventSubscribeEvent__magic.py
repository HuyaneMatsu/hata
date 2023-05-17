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


def test__ScheduledEventSubscribeEvent__eq():
    """
    Tests whether ``ScheduledEventSubscribeEvent.__repr__`` works as intended.
    """
    guild_id = 202303120015
    scheduled_event_id = 202303120016
    user_id = 202303120017
    
    keyword_parameters = {
        'guild_id': guild_id,
        'scheduled_event_id': scheduled_event_id,
        'user_id': user_id,
    }
    
    event = ScheduledEventSubscribeEvent(**keyword_parameters)
    
    vampytest.assert_eq(event, event)
    vampytest.assert_ne(event, object())
    
    for event_name, event_value in (
        ('guild_id', 0),
        ('scheduled_event_id', 0),
        ('user_id', 0),
    ):
        event_altered = ScheduledEventSubscribeEvent(**{**keyword_parameters, event_name: event_value})
        vampytest.assert_ne(event, event_altered)


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
