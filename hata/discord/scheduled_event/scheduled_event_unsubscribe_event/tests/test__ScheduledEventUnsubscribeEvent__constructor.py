import vampytest

from ..scheduled_event_unsubscribe_event import ScheduledEventUnsubscribeEvent


def _assert_fields_set(event):
    """
    Checks whether every attribute is set of the given scheduled event unsubscribe event.
    
    Parameters
    ----------
    event : ``ScheduledEventUnsubscribeEvent``
        The event to check.
    """
    vampytest.assert_instance(event, ScheduledEventUnsubscribeEvent)
    vampytest.assert_instance(event.guild_id, int)
    vampytest.assert_instance(event.scheduled_event_id, int)
    vampytest.assert_instance(event.user_id, int)


def test__ScheduledEventUnsubscribeEvent__new__0():
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.__new__`` works as intended.
    
    Case: No fields given.
    """
    event = ScheduledEventUnsubscribeEvent()
    _assert_fields_set(event)


def test__ScheduledEventUnsubscribeEvent__new__1():
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.__new__`` works as intended.
    
    Case: Fields given.
    """
    guild_id = 202303120036
    scheduled_event_id = 202303120037
    user_id = 202303120038
    
    event = ScheduledEventUnsubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        user_id = user_id,
    )
    _assert_fields_set(event)
    
    vampytest.assert_eq(event.guild_id, guild_id)
    vampytest.assert_eq(event.scheduled_event_id, scheduled_event_id)
    vampytest.assert_eq(event.user_id, user_id)
