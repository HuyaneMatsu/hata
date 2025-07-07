import vampytest

from ....guild import Guild
from ....user import ClientUserBase

from ...scheduled_event import ScheduledEvent

from ..scheduled_event_unsubscribe_event import ScheduledEventUnsubscribeEvent

from .test__ScheduledEventUnsubscribeEvent__constructor import _assert_fields_set


def test__ScheduledEventUnsubscribeEvent__copy():
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.copy`` works as intended.
    """
    guild_id = 202303120057
    scheduled_event_id = 202303120058
    user_id = 202303120059
    
    event = ScheduledEventUnsubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        user_id = user_id,
    )
    copy = event.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(event, copy)



def test__ScheduledEventUnsubscribeEvent__copy_with__no_fields():
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.copy_with`` works as intended.
    
    Case: no fields given.
    """
    guild_id = 202303120060
    scheduled_event_id = 202303120061
    user_id = 202303120062
    
    event = ScheduledEventUnsubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        user_id = user_id,
    )
    copy = event.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(event, copy)



def test__ScheduledEventUnsubscribeEvent__copy_with__all_fields():
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_guild_id = 202303120063
    old_scheduled_event_id = 202303120064
    old_user_id = 202303120065
    
    new_guild_id = 202303120066
    new_scheduled_event_id = 202303120067
    new_user_id = 202303120068
    
    event = ScheduledEventUnsubscribeEvent(
        guild_id = old_guild_id,
        scheduled_event_id = old_scheduled_event_id,
        user_id = old_user_id,
    )
    copy = event.copy_with(
        guild_id = new_guild_id,
        scheduled_event_id = new_scheduled_event_id,
        user_id = new_user_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.scheduled_event_id, new_scheduled_event_id)
    vampytest.assert_eq(copy.user_id, new_user_id)


def _iter_options__guild():
    guild_id_0 = 202303120069
    guild_id_1 = 202303120070
    
    yield 0, None
    yield guild_id_0, None
    yield guild_id_1, Guild.precreate(guild_id_1)


@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__ScheduledEventUnsubscribeEvent__guild(guild_id):
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.guild`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier to create event with.
    
    Returns
    -------
    guild : ``None | Guild``
    """
    event = ScheduledEventUnsubscribeEvent(
        guild_id = guild_id,
    )
    
    output = event.guild
    vampytest.assert_instance(output, Guild, nullable = True)
    return output


def test__ScheduledEventUnsubscribeEvent__user():
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.user`` works as intended.
    """
    user_id = 202303120071
    
    event = ScheduledEventUnsubscribeEvent(
        user_id = user_id,
    )
    
    output = event.user
    vampytest.assert_instance(output, ClientUserBase)
    vampytest.assert_eq(output.id, user_id)


def _iter_options__scheduled_event():
    scheduled_event_id_0 = 202506220002
    scheduled_event_id_1 = 202506220003
    
    yield 0, None
    yield scheduled_event_id_0, None
    yield scheduled_event_id_1, ScheduledEvent.precreate(scheduled_event_id_1)
    

@vampytest._(vampytest.call_from(_iter_options__scheduled_event()).returning_last())
def test__ScheduledEventUnsubscribeEvent__scheduled_event(scheduled_event_id):
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.scheduled_event`` works as intended.
    
    Parameters
    ----------
    scheduled_event_id : `int`
        ScheduledEvent identifier to create event with.
    
    Returns
    -------
    scheduled_event : ``None | ScheduledEvent``
    """
    event = ScheduledEventUnsubscribeEvent(
        scheduled_event_id = scheduled_event_id,
    )
    
    output = event.scheduled_event
    vampytest.assert_instance(output, ScheduledEvent, nullable = True)
    return output
