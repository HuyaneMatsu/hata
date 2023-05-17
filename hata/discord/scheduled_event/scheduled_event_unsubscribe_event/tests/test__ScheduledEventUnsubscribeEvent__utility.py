import vampytest

from ....guild import Guild
from ....user import ClientUserBase

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



def test__ScheduledEventUnsubscribeEvent__copy_with__0():
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



def test__ScheduledEventUnsubscribeEvent__copy_with__1():
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


def test__ScheduledEventUnsubscribeEvent__guild():
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.guild`` works as intended.
    
    Case: no fields given.
    """
    guild_id_0 = 202303120069
    guild_id_1 = 202303120070
    
    for input_value, expected_output in (
        (0, None),
        (guild_id_0, None),
        (guild_id_1, Guild.precreate(guild_id_1)),
    ):
        event = ScheduledEventUnsubscribeEvent(
            guild_id = input_value,
        )
        
        vampytest.assert_is(event.guild, expected_output)


def test__ScheduledEventUnsubscribeEvent__user():
    """
    Tests whether ``ScheduledEventUnsubscribeEvent.user`` works as intended.
    
    Case: no fields given.
    """
    user_id = 202303120071
    
    event = ScheduledEventUnsubscribeEvent(
        user_id = user_id,
    )
    
    output = event.user
    vampytest.assert_instance(output, ClientUserBase)
    vampytest.assert_eq(output.id, user_id)
