from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType
from ....scheduled_event import PrivacyLevel, Schedule, ScheduledEvent, ScheduledEventEntityType, ScheduledEventStatus
from ....guild import Guild
from ....utils import datetime_to_timestamp, image_to_base64

from ...client import Client

from .helpers import IMAGE_DATA, TestDiscordApiClient


async def test__Client__scheduled_event_create__stuffed():
    """
    Tests whether ``Client.scheduled_event_create`` works as intended.
    
    Case: stuffed scheduled_event.
    
    This function is a coroutine.
    """
    client_id = 202602070000
    guild_id = 202602070001
    scheduled_event_id = 202602070002
    reason = 'howling moon'
    
    description = 'koishi'
    end = DateTime(2016, 3, 10, tzinfo = TimeZone.utc)
    entity_type = ScheduledEventEntityType.location
    image = Icon(IconType.static, 45555)
    image_data = IMAGE_DATA
    name = 'komeiji'
    privacy_level = PrivacyLevel.public
    schedule = Schedule(occurrence_spacing = 2)
    start = DateTime(2017, 4, 6, tzinfo = TimeZone.utc)
    status = ScheduledEventStatus.active
    location = 'hell'
    
    mock_api_scheduled_event_create_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    guild = Guild.precreate(guild_id)
    
    
    expected_scheduled_event_data = {
        'scheduled_start_time': datetime_to_timestamp(start),
        'recurrence_rule': schedule.to_data(defaults = False, start = start),
        'privacy_level': privacy_level.value,
        'name': name,
        'entity_type': entity_type.value,
        'entity_metadata': entity_type.metadata_type(location = location).to_data(defaults = False),
        'scheduled_end_time': datetime_to_timestamp(end),
        'image': image_to_base64(image_data),
        'description': description,
    }
    
    output_scheduled_event_data = {
        'id': str(scheduled_event_id),
        'description': description,
        'scheduled_end_time': datetime_to_timestamp(end),
        'entity_type': entity_type.value,
        'image': image.as_base_16_hash,
        'name': name,
        'privacy_level': privacy_level.value,
        'recurrence_rule': schedule.to_data(defaults = False, start = start),
        'scheduled_start_time': datetime_to_timestamp(start),
        'status': status.value,
        'entity_metadata': entity_type.metadata_type(location = location).to_data(defaults = False),
        'guild_id': str(guild_id),
    }
    
    
    async def mock_api_scheduled_event_create(input_guild_id, input_scheduled_event_data, input_reason):
        nonlocal mock_api_scheduled_event_create_called
        nonlocal guild_id
        nonlocal expected_scheduled_event_data
        nonlocal output_scheduled_event_data
        nonlocal reason
        mock_api_scheduled_event_create_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(expected_scheduled_event_data, input_scheduled_event_data)
        vampytest.assert_eq(reason, input_reason)
        return output_scheduled_event_data
    
    api.scheduled_event_create = mock_api_scheduled_event_create
        
    try:
        # location & stage  & voice are mutually exclusive
        output = await client.scheduled_event_create(
            guild,
            description = description,
            end = end,
            image = image_data,
            location = location,
            name = name,
            privacy_level = privacy_level,
            schedule = schedule,
            # stage = stage,
            start = start,
            # voice = voice,
            reason = reason,
        )
        vampytest.assert_true(mock_api_scheduled_event_create_called)
        
        vampytest.assert_instance(output, ScheduledEvent)
        vampytest.assert_eq(output.id, scheduled_event_id)
        vampytest.assert_eq(output.guild_id, guild_id)
        vampytest.assert_eq(output.description, description)
        vampytest.assert_eq(output.end, end)
        vampytest.assert_eq(output.image, image)
        vampytest.assert_is(output.entity_type, entity_type)
        vampytest.assert_eq(output.entity_metadata, entity_type.metadata_type(location = location))
        vampytest.assert_eq(output.name, name)
        vampytest.assert_is(output.privacy_level, privacy_level)
        vampytest.assert_eq(output.schedule, schedule.copy_with(start = start))
        vampytest.assert_eq(output.start, start)
        vampytest.assert_is(output.status, status)
        
        # It should not be registered, just returned
        vampytest.assert_is(guild.scheduled_events.get(scheduled_event_id, None), output)
    finally:
        client._delete()
        client = None
