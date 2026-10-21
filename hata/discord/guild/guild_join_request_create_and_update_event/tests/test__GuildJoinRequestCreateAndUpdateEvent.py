import vampytest

from ...guild_join_request import (
    GuildJoinRequest, guild_join_request_convert_to_data, guild_join_request_create, GuildJoinRequestStatus
)

from ..guild_join_request_create_and_update_event import (
    GuildJoinRequestCreateAndUpdateEvent, guild_join_request_create_and_update_event_convert_to_data,
    guild_join_request_create_and_update_event_create, guild_join_request_create_and_update_event_create_from_data
)

def assert_guild_join_request_create_and_update_event_fields_set(guild_join_request_create_and_update_event):
    vampytest.assert_instance(guild_join_request_create_and_update_event, GuildJoinRequestCreateAndUpdateEvent)
    vampytest.assert_instance(guild_join_request_create_and_update_event.guild_id, int)
    vampytest.assert_instance(
        guild_join_request_create_and_update_event.guild_join_request, GuildJoinRequest, nullable = True
    )
    vampytest.assert_instance(guild_join_request_create_and_update_event.status, GuildJoinRequestStatus)


def test__guild_join_request_create_and_update_event_create__no_fields():
    guild_join_request_create_and_update_event = guild_join_request_create_and_update_event_create()
    assert_guild_join_request_create_and_update_event_fields_set(guild_join_request_create_and_update_event)


def test__guild_join_request_create_and_update_event_create__all_fields():
    guild_id = 202610100090
    guild_join_request = guild_join_request_create(
        guild_join_request_id = 202610100091
    )
    status = GuildJoinRequestStatus.rejected
    
    guild_join_request_create_and_update_event = guild_join_request_create_and_update_event_create(
        guild_id = guild_id,
        guild_join_request = guild_join_request,
        status = status,
    )
    assert_guild_join_request_create_and_update_event_fields_set(guild_join_request_create_and_update_event)
    
    vampytest.assert_eq(guild_join_request_create_and_update_event.guild_id, guild_id)
    vampytest.assert_eq(guild_join_request_create_and_update_event.guild_join_request, guild_join_request)
    vampytest.assert_eq(guild_join_request_create_and_update_event.status, status)


def test__guild_join_request_create_and_update_event_create_from_data():
    guild_id = 202610100092
    guild_join_request = guild_join_request_create(
        guild_join_request_id = 202610100093
    )
    status = GuildJoinRequestStatus.rejected
    
    data = {
        'guild_id': str(guild_id),
        'request': guild_join_request_convert_to_data(guild_join_request, defaults = True),
        'status': status.value,
    }
    
    guild_join_request_create_and_update_event = guild_join_request_create_and_update_event_create_from_data(data)
    assert_guild_join_request_create_and_update_event_fields_set(guild_join_request_create_and_update_event)
    
    vampytest.assert_eq(guild_join_request_create_and_update_event.guild_id, guild_id)
    vampytest.assert_eq(guild_join_request_create_and_update_event.guild_join_request, guild_join_request)
    vampytest.assert_eq(guild_join_request_create_and_update_event.status, status)


def test__guild_join_request_create_and_update_event_convert_to_data():
    guild_id = 202610100094
    guild_join_request = guild_join_request_create(
        guild_join_request_id = 202610100095
    )
    status = GuildJoinRequestStatus.rejected
    
    guild_join_request_create_and_update_event = guild_join_request_create_and_update_event_create(
        guild_id = guild_id,
        guild_join_request = guild_join_request,
        status = status,
    )
    
    expected_output = {
        'guild_id': str(guild_id),
        'request': guild_join_request_convert_to_data(guild_join_request, defaults = True),
        'status': status.value,
    }
    
    vampytest.assert_eq(
        guild_join_request_create_and_update_event_convert_to_data(
            guild_join_request_create_and_update_event, defaults = True
        ),
        expected_output,
    )
