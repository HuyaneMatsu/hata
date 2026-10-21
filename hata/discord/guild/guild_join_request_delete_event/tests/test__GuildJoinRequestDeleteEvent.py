import vampytest

from ..guild_join_request_delete_event import (
    GuildJoinRequestDeleteEvent, guild_join_request_event_convert_to_data, guild_join_request_delete_event_create,
    guild_join_request_delete_event_create_from_data
)


def assert_guild_join_request_delete_event_fields_set(guild_join_request_delete_event):
    vampytest.assert_instance(guild_join_request_delete_event, GuildJoinRequestDeleteEvent)
    vampytest.assert_instance(guild_join_request_delete_event.guild_id, int)
    vampytest.assert_instance(guild_join_request_delete_event.guild_join_request_id, int)
    vampytest.assert_instance(guild_join_request_delete_event.user_id, int)


def test__guild_join_request_delete_event_create__no_fields():
    event = guild_join_request_delete_event_create()
    assert_guild_join_request_delete_event_fields_set(event)


def test__guild_join_request_delete_event_create__all_fields():
    guild_id = 202305160013
    guild_join_request_id = 202610100040
    user_id = 202305160014
    
    guild_join_request_delete_event = guild_join_request_delete_event_create(
        guild_id = guild_id,
        guild_join_request_id = guild_join_request_id,
        user_id = user_id,
    )
    assert_guild_join_request_delete_event_fields_set(guild_join_request_delete_event)
    
    vampytest.assert_eq(guild_join_request_delete_event.guild_id, guild_id)
    vampytest.assert_eq(guild_join_request_delete_event.guild_join_request_id, guild_join_request_id)
    vampytest.assert_eq(guild_join_request_delete_event.user_id, user_id)


def test__guild_join_request_delete_event_create_from_data():
    guild_id = 202305160015
    guild_join_request_id = 202610100030
    user_id = 202305160016
    
    data = {
        'guild_id': str(guild_id),
        'id': str(guild_join_request_id),
        'user_id': str(user_id),
    }
    
    guild_join_request_delete_event = guild_join_request_delete_event_create_from_data(data)
    assert_guild_join_request_delete_event_fields_set(guild_join_request_delete_event)
    
    vampytest.assert_eq(guild_join_request_delete_event.guild_id, guild_id)
    vampytest.assert_eq(guild_join_request_delete_event.guild_join_request_id, guild_join_request_id)
    vampytest.assert_eq(guild_join_request_delete_event.user_id, user_id)


def test__guild_join_request_event_convert_to_data():
    guild_id = 202305160017
    guild_join_request_id = 202610100031
    user_id = 202305160018
    
    guild_join_request_delete_event = guild_join_request_delete_event_create(
        guild_id = guild_id,
        guild_join_request_id = guild_join_request_id,
        user_id = user_id,
    )
    
    expected_output = {
        'guild_id': str(guild_id),
        'id': str(guild_join_request_id),
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        guild_join_request_event_convert_to_data(guild_join_request_delete_event, defaults = True),
        expected_output,
    )
