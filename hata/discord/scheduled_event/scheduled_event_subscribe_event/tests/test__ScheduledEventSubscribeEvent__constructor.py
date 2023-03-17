import vampytest

from ..scheduled_event_subscribe_event import ScheduledEventSubscribeEvent


def _check_fields_set(event):
    """
    Checks whether every attribute is set of the given scheduled event subscribe event.
    
    Parameters
    ----------
    event : ``ScheduledEventSubscribeEvent``
        The event to check.
    """
    vampytest.assert_instance(event, ScheduledEventSubscribeEvent)
    vampytest.assert_instance(event.guild_id, int)
    vampytest.assert_instance(event.scheduled_event_id, int)
    vampytest.assert_instance(event.user_id, int)


def test__ScheduledEventSubscribeEvent__new__0():
    """
    Tests whether ``ScheduledEventSubscribeEvent.__new__`` works as intended.
    
    Case: No fields given.
    """
    event = ScheduledEventSubscribeEvent()
    _check_fields_set(event)


def test__ScheduledEventSubscribeEvent__new__1():
    """
    Tests whether ``ScheduledEventSubscribeEvent.__new__`` works as intended.
    
    Case: Fields given.
    """
    guild_id = 202303120000
    scheduled_event_id = 202303120001
    user_id = 202303120002
    
    event = ScheduledEventSubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        user_id = user_id,
    )
    _check_fields_set(event)
    
    vampytest.assert_eq(event.guild_id, guild_id)
    vampytest.assert_eq(event.scheduled_event_id, scheduled_event_id)
    vampytest.assert_eq(event.user_id, user_id)
