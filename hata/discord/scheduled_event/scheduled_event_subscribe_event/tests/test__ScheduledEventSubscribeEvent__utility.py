import vampytest

from ....guild import Guild
from ....user import ClientUserBase

from ..scheduled_event_subscribe_event import ScheduledEventSubscribeEvent

from .test__ScheduledEventSubscribeEvent__constructor import _assert_fields_set


def test__ScheduledEventSubscribeEvent__copy():
    """
    Tests whether ``ScheduledEventSubscribeEvent.copy`` works as intended.
    """
    guild_id = 202303120021
    scheduled_event_id = 202303120022
    user_id = 202303120023
    
    event = ScheduledEventSubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        user_id = user_id,
    )
    copy = event.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(event, copy)



def test__ScheduledEventSubscribeEvent__copy_with__0():
    """
    Tests whether ``ScheduledEventSubscribeEvent.copy_with`` works as intended.
    
    Case: no fields given.
    """
    guild_id = 202303120024
    scheduled_event_id = 202303120025
    user_id = 202303120026
    
    event = ScheduledEventSubscribeEvent(
        guild_id = guild_id,
        scheduled_event_id = scheduled_event_id,
        user_id = user_id,
    )
    copy = event.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(event, copy)



def test__ScheduledEventSubscribeEvent__copy_with__1():
    """
    Tests whether ``ScheduledEventSubscribeEvent.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_guild_id = 202303120027
    old_scheduled_event_id = 202303120028
    old_user_id = 202303120029
    
    new_guild_id = 202303120030
    new_scheduled_event_id = 202303120031
    new_user_id = 202303120032
    
    event = ScheduledEventSubscribeEvent(
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


def test__ScheduledEventSubscribeEvent__guild():
    """
    Tests whether ``ScheduledEventSubscribeEvent.guild`` works as intended.
    
    Case: no fields given.
    """
    guild_id_0 = 202303120033
    guild_id_1 = 202303120034
    
    for input_value, expected_output in (
        (0, None),
        (guild_id_0, None),
        (guild_id_1, Guild.precreate(guild_id_1)),
    ):
        event = ScheduledEventSubscribeEvent(
            guild_id = input_value,
        )
        
        vampytest.assert_is(event.guild, expected_output)


def test__ScheduledEventSubscribeEvent__user():
    """
    Tests whether ``ScheduledEventSubscribeEvent.user`` works as intended.
    
    Case: no fields given.
    """
    user_id = 202303120035
    
    event = ScheduledEventSubscribeEvent(
        user_id = user_id,
    )
    
    output = event.user
    vampytest.assert_instance(output, ClientUserBase)
    vampytest.assert_eq(output.id, user_id)
