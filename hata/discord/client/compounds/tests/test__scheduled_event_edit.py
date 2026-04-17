from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType
from ....scheduled_event import PrivacyLevel, Schedule, ScheduledEvent, ScheduledEventEntityType, ScheduledEventStatus
from ....utils import datetime_to_timestamp, image_to_base64

from ...client import Client

from .helpers import IMAGE_DATA, TestDiscordApiClient


async def test__Client__scheduled_event_edit__stuffed():
    """
    Tests whether ``Client.scheduled_event_edit`` works as intended.
    
    Case: stuffed scheduled_event.
    
    This function is a coroutine.
    """
    client_id = 202602070003
    guild_id = 202602070004
    scheduled_event_id = 202602070005
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        guild_id = guild_id,
    )
    
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
    status = ScheduledEventStatus.cancelled
    location = 'hell'
    
    mock_api_scheduled_event_edit_called = False
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    client = Client(token, api = api, client_id = client_id)
    
    
    expected_scheduled_event_data = {
        'scheduled_start_time': datetime_to_timestamp(start),
        'recurrence_rule': schedule.to_data(defaults = True, start = start),
        'privacy_level': privacy_level.value,
        'name': name,
        'entity_type': entity_type.value,
        'entity_metadata': entity_type.metadata_type(location = location).to_data(defaults = True),
        'scheduled_end_time': datetime_to_timestamp(end),
        'image': image_to_base64(image_data),
        'description': description,
        'status': status.cancelled,
        'channel_id': None, # <- this one is coming from the target serialiser to remove the old one.
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
        'status': status.cancelled,
        'entity_metadata': entity_type.metadata_type(location = location).to_data(defaults = False),
        'guild_id': str(guild_id),
    }
    
    
    async def mock_api_scheduled_event_edit(input_guild_id, input_scheduled_event_id, input_scheduled_event_data, input_reason):
        nonlocal mock_api_scheduled_event_edit_called
        nonlocal guild_id
        nonlocal scheduled_event_id
        nonlocal expected_scheduled_event_data
        nonlocal output_scheduled_event_data
        nonlocal reason
        mock_api_scheduled_event_edit_called = True
        vampytest.assert_eq(guild_id, input_guild_id)
        vampytest.assert_eq(scheduled_event_id, input_scheduled_event_id)
        vampytest.assert_eq(expected_scheduled_event_data, input_scheduled_event_data)
        vampytest.assert_eq(reason, input_reason)
        return output_scheduled_event_data
    
    api.scheduled_event_edit = mock_api_scheduled_event_edit
        
    try:
        # location & stage  & voice are mutually exclusive
        output = await client.scheduled_event_edit(
            scheduled_event,
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
            status = status,
            reason = reason,
        )
        vampytest.assert_true(mock_api_scheduled_event_edit_called)
        
        vampytest.assert_is(output, None)
    finally:
        client._delete()
        client = None
