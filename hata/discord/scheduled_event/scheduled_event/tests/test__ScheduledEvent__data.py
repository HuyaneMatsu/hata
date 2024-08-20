from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType
from ....client import Client
from ....guild import Guild
from ....user import User
from ....utils import datetime_to_timestamp

from ...schedule import Schedule

from ..preinstanced import PrivacyLevel, ScheduledEventEntityType, ScheduledEventStatus
from ..scheduled_event import ScheduledEvent

from .test__ScheduledEvent__constructor import _assert_fields_set


def test__ScheduledEvent__from_data__default():
    """
    Tests whether ``ScheduledEvent.from_data`` works as intended.
    
    Case: default.
    """
    scheduled_event_id = 202303160011
    
    channel_id = 202303160012
    description = 'koishi'
    end = DateTime(2016, 3, 10, tzinfo = TimeZone.utc)
    entity_type = ScheduledEventEntityType.location
    image = Icon(IconType.static, 45)
    name = 'komeiji'
    privacy_level = PrivacyLevel.public
    schedule = Schedule(occurrence_spacing = 2)
    start = DateTime(2017, 4, 6, tzinfo = TimeZone.utc)
    status = ScheduledEventStatus.active
    location = 'hell'
    
    creator = User.precreate(202303160013, name = 'Orin')
    entity_id = 202303160014
    guild_id = 202303160015
    sku_ids = [202303160016, 202303160017]
    user_count = 66
    
    data = {
        'id': str(scheduled_event_id),
        'channel_id': str(channel_id),
        'description': description,
        'scheduled_end_time': datetime_to_timestamp(end),
        'entity_type': entity_type.value,
        'image': image.as_base_16_hash,
        'name': name,
        'privacy_level': privacy_level.value,
        'recurrence_rule': schedule.to_data(defaults = True, start = start),
        'scheduled_start_time': datetime_to_timestamp(start),
        'status': status.value,
        'entity_metadata': entity_type.metadata_type(location = location).to_data(defaults = True),
        'creator': creator.to_data(defaults = True, include_internals = True),
        'entity_id': str(entity_id),
        'guild_id': str(guild_id),
        'sku_ids': [str(sku_id) for sku_id in sku_ids],
        'user_count': user_count,
    }
    
    scheduled_event = ScheduledEvent.from_data(data)
    _assert_fields_set(scheduled_event)
    
    vampytest.assert_eq(scheduled_event.id, scheduled_event_id)
    
    vampytest.assert_eq(scheduled_event.channel_id, channel_id)
    vampytest.assert_eq(scheduled_event.description, description)
    vampytest.assert_eq(scheduled_event.end, end)
    vampytest.assert_eq(scheduled_event.entity_metadata, entity_type.metadata_type(location = location))
    vampytest.assert_is(scheduled_event.entity_type, entity_type)
    vampytest.assert_eq(scheduled_event.image, image)
    vampytest.assert_eq(scheduled_event.name, name)
    vampytest.assert_is(scheduled_event.privacy_level, privacy_level)
    vampytest.assert_eq(scheduled_event.schedule, schedule.copy_with(start = start))
    vampytest.assert_eq(scheduled_event.start, start)
    vampytest.assert_is(scheduled_event.status, status)
        
    vampytest.assert_is(scheduled_event.creator, creator)
    vampytest.assert_eq(scheduled_event.entity_id, entity_id)
    vampytest.assert_eq(scheduled_event.guild_id, guild_id)
    vampytest.assert_eq(scheduled_event.sku_ids, tuple(sku_ids))
    vampytest.assert_eq(scheduled_event.user_count, user_count)


def test__ScheduledEvent__from_data__global_caching():
    """
    Tests whether ``ScheduledEvent.from_data`` works as intended.
    
    Case: global caching.
    """
    scheduled_event_id = 202303160018
    
    data = {
        'id': str(scheduled_event_id),
    }
    
    scheduled_event = ScheduledEvent.from_data(data)
    test_scheduled_event = ScheduledEvent.from_data(data)
    
    vampytest.assert_is(scheduled_event, test_scheduled_event)


def test__ScheduledEvent__from_data__caching_under_guild():
    """
    Tests whether ``ScheduledEvent.from_data`` works as intended.
    
    Case: caching under guild.
    """
    scheduled_event_id = 202303160019
    guild_id = 202303160020
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'id': str(scheduled_event_id),
        'guild_id': str(guild_id),
    }
    
    scheduled_event = ScheduledEvent.from_data(data)
    
    vampytest.assert_eq(guild.scheduled_events, {scheduled_event_id: scheduled_event})


def test__ScheduledEvent__from_data__no_strong_cache():
    """
    Tests whether ``ScheduledEvent.from_data`` works as intended.
    
    Case: `strong_cache` given as `False`
    """
    scheduled_event_id = 202306130000
    guild_id = 202306130001
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'id': str(scheduled_event_id),
        'guild_id': str(guild_id),
    }
    
    scheduled_event = ScheduledEvent.from_data(data, strong_cache = False)
    
    vampytest.assert_eq(guild.scheduled_events, None)


def test__ScheduledEvent__to_data():
    """
    Tests whether ``ScheduledEvent.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    scheduled_event_id = 202303160021
    
    channel_id = 202303160022
    description = 'koishi'
    end = DateTime(2016, 3, 10, tzinfo = TimeZone.utc)
    entity_type = ScheduledEventEntityType.location
    image = Icon(IconType.static, 45)
    name = 'komeiji'
    privacy_level = PrivacyLevel.public
    schedule = Schedule(occurrence_spacing = 2)
    start = DateTime(2017, 4, 6, tzinfo = TimeZone.utc)
    status = ScheduledEventStatus.active
    location = 'hell'
    
    creator = User.precreate(202303160023, name = 'Orin')
    entity_id = 202303160024
    guild_id = 202303160025
    sku_ids = [202303160026, 202303160027]
    user_count = 66
    
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        channel_id = channel_id,
        description = description,
        end = end,
        entity_type = entity_type,
        image = image,
        name = name,
        privacy_level = privacy_level,
        schedule = schedule,
        start = start,
        status = status,
        location = location,
        creator = creator,
        entity_id = entity_id,
        guild_id = guild_id,
        sku_ids = sku_ids,
        user_count = user_count,
    )
    
    expected_output = {
        'id': str(scheduled_event_id),
        'channel_id': str(channel_id),
        'description': description,
        'scheduled_end_time': datetime_to_timestamp(end),
        'entity_type': entity_type.value,
        'image': image.as_base_16_hash,
        'name': name,
        'privacy_level': privacy_level.value,
        'recurrence_rule': schedule.to_data(defaults = True, start = start),
        'scheduled_start_time': datetime_to_timestamp(start),
        'status': status.value,
        'entity_metadata': entity_type.metadata_type(location = location).to_data(defaults = True),
        'creator': creator.to_data(defaults = True, include_internals = True),
        'entity_id': str(entity_id),
        'guild_id': str(guild_id),
        'sku_ids': [str(sku_id) for sku_id in sku_ids],
        'user_count': user_count,
    }
    
    vampytest.assert_eq(
        scheduled_event.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__ScheduledEvent__set_attributes():
    """
    Tests whether ``ScheduledEvent._set_attributes`` works as intended.
    """
    channel_id = 202303160028
    description = 'koishi'
    end = DateTime(2016, 3, 10, tzinfo = TimeZone.utc)
    entity_type = ScheduledEventEntityType.location
    image = Icon(IconType.static, 45)
    name = 'komeiji'
    privacy_level = PrivacyLevel.public
    schedule = Schedule(occurrence_spacing = 2)
    start = DateTime(2017, 4, 6, tzinfo = TimeZone.utc)
    status = ScheduledEventStatus.active
    location = 'hell'
    
    creator = User.precreate(202303160029, name = 'Orin')
    entity_id = 202303160030
    guild_id = 202303160031
    sku_ids = [202303160032, 202303160033]
    user_count = 66
    
    data = {
        'channel_id': str(channel_id),
        'description': description,
        'scheduled_end_time': datetime_to_timestamp(end),
        'entity_type': entity_type.value,
        'image': image.as_base_16_hash,
        'name': name,
        'privacy_level': privacy_level.value,
        'recurrence_rule': schedule.to_data(defaults = True, start = start),
        'scheduled_start_time': datetime_to_timestamp(start),
        'status': status.value,
        'entity_metadata': entity_type.metadata_type(location = location).to_data(defaults = True),
        'creator': creator.to_data(defaults = True, include_internals = True),
        'entity_id': str(entity_id),
        'guild_id': str(guild_id),
        'sku_ids': [str(sku_id) for sku_id in sku_ids],
        'user_count': user_count,
    }
    
    scheduled_event = ScheduledEvent()
    scheduled_event._set_attributes(data)
    
    vampytest.assert_eq(scheduled_event.channel_id, channel_id)
    vampytest.assert_eq(scheduled_event.description, description)
    vampytest.assert_eq(scheduled_event.end, end)
    vampytest.assert_eq(scheduled_event.entity_metadata, entity_type.metadata_type(location = location))
    vampytest.assert_is(scheduled_event.entity_type, entity_type)
    vampytest.assert_eq(scheduled_event.image, image)
    vampytest.assert_eq(scheduled_event.name, name)
    vampytest.assert_is(scheduled_event.privacy_level, privacy_level)
    vampytest.assert_eq(scheduled_event.schedule, schedule.copy_with(start = start))
    vampytest.assert_eq(scheduled_event.start, start)
    vampytest.assert_is(scheduled_event.status, status)
        
    vampytest.assert_is(scheduled_event.creator, creator)
    vampytest.assert_eq(scheduled_event.entity_id, entity_id)
    vampytest.assert_eq(scheduled_event.guild_id, guild_id)
    vampytest.assert_eq(scheduled_event.sku_ids, tuple(sku_ids))
    vampytest.assert_eq(scheduled_event.user_count, user_count)


def test__ScheduledEvent__update_attributes():
    """
    Tests whether ``ScheduledEvent._update_attributes`` works as intended.
    """
    channel_id = 202303160034
    description = 'koishi'
    end = DateTime(2016, 3, 10, tzinfo = TimeZone.utc)
    entity_type = ScheduledEventEntityType.location
    image = Icon(IconType.static, 45)
    name = 'komeiji'
    privacy_level = PrivacyLevel.public
    schedule = Schedule(occurrence_spacing = 2)
    start = DateTime(2017, 4, 6, tzinfo = TimeZone.utc)
    status = ScheduledEventStatus.active
    location = 'hell'
    
    entity_id = 202303160035
    sku_ids = [202303160036, 202303160037]
    
    data = {
        'channel_id': str(channel_id),
        'description': description,
        'scheduled_end_time': datetime_to_timestamp(end),
        'entity_type': entity_type.value,
        'image': image.as_base_16_hash,
        'name': name,
        'privacy_level': privacy_level.value,
        'recurrence_rule': schedule.to_data(defaults = True, start = start),
        'scheduled_start_time': datetime_to_timestamp(start),
        'status': status.value,
        'entity_metadata': entity_type.metadata_type(location = location).to_data(defaults = True),
        'entity_id': str(entity_id),
        'sku_ids': [str(sku_id) for sku_id in sku_ids],
    }
    
    scheduled_event = ScheduledEvent()
    scheduled_event._update_attributes(data)
    
    vampytest.assert_eq(scheduled_event.channel_id, channel_id)
    vampytest.assert_eq(scheduled_event.description, description)
    vampytest.assert_eq(scheduled_event.end, end)
    vampytest.assert_eq(scheduled_event.entity_metadata, entity_type.metadata_type(location = location))
    vampytest.assert_is(scheduled_event.entity_type, entity_type)
    vampytest.assert_eq(scheduled_event.image, image)
    vampytest.assert_eq(scheduled_event.name, name)
    vampytest.assert_is(scheduled_event.privacy_level, privacy_level)
    vampytest.assert_eq(scheduled_event.schedule, schedule.copy_with(start = start))
    vampytest.assert_eq(scheduled_event.start, start)
    vampytest.assert_is(scheduled_event.status, status)
        
    vampytest.assert_eq(scheduled_event.entity_id, entity_id)
    vampytest.assert_eq(scheduled_event.sku_ids, tuple(sku_ids))


def test__ScheduledEvent__update_counts_only():
    """
    Tests whether ``ScheduledEvent._update_counts_only`` works as intended.
    """
    user_count = 69
    
    data = {
        'user_count': user_count,
    }
    
    scheduled_event = ScheduledEvent()
    scheduled_event._update_counts_only(data)
    
    vampytest.assert_eq(scheduled_event.user_count, user_count)


def test__ScheduledEvent__difference_update_attributes():
    """
    Tests whether ``ScheduledEvent._difference_update_attributes`` works as intended.
    """
    scheduled_event_id = 202303110038
    
    old_channel_id = 202303160039
    old_description = 'koishi'
    old_end = DateTime(2016, 3, 10, tzinfo = TimeZone.utc)
    old_entity_type = ScheduledEventEntityType.location
    old_image = Icon(IconType.static, 45)
    old_name = 'komeiji'
    old_privacy_level = PrivacyLevel.public
    old_schedule = Schedule(occurrence_spacing = 2)
    old_start = DateTime(2017, 4, 6, tzinfo = TimeZone.utc)
    old_status = ScheduledEventStatus.active
    old_location = 'hell'
    
    old_entity_id = 202303160040
    old_sku_ids = [202303160041, 202303160042]
    
    
    new_channel_id = 202303160043
    new_description = 'yakumo'
    new_end = DateTime(2016, 4, 10, tzinfo = TimeZone.utc)
    new_entity_type = ScheduledEventEntityType.stage
    new_image = Icon(IconType.animated, 46)
    new_name = 'yukari'
    new_privacy_level = PrivacyLevel.guild_only
    new_schedule = Schedule(occurrence_spacing = 3)
    new_start = DateTime(2017, 5, 6, tzinfo = TimeZone.utc)
    new_status = ScheduledEventStatus.cancelled
    new_speaker_ids = [202303160044, 202303160045]
    
    new_entity_id = 202303160046
    new_sku_ids = [202303160047, 202303160048]
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        channel_id = old_channel_id,
        description = old_description,
        end = old_end,
        entity_type = old_entity_type,
        image = old_image,
        name = old_name,
        privacy_level = old_privacy_level,
        schedule = old_schedule,
        start = old_start,
        status = old_status,
        location = old_location,
        entity_id = old_entity_id,
        sku_ids = old_sku_ids,
    )
    
    data = {
        'channel_id': str(new_channel_id),
        'description': new_description,
        'scheduled_end_time': datetime_to_timestamp(new_end),
        'entity_type': new_entity_type.value,
        'image': new_image.as_base_16_hash,
        'name': new_name,
        'privacy_level': new_privacy_level.value,
        'recurrence_rule': new_schedule.to_data(defaults = True, start = new_start),
        'scheduled_start_time': datetime_to_timestamp(new_start),
        'status': new_status.value,
        'entity_metadata': new_entity_type.metadata_type(speaker_ids = new_speaker_ids).to_data(defaults = True),
        'entity_id': str(new_entity_id),
        'sku_ids': [str(sku_id) for sku_id in new_sku_ids],
    }
    
    old_attributes = scheduled_event._difference_update_attributes(data)
    vampytest.assert_eq(scheduled_event.channel_id, new_channel_id)
    vampytest.assert_eq(scheduled_event.description, new_description)
    vampytest.assert_eq(scheduled_event.end, new_end)
    vampytest.assert_eq(
        scheduled_event.entity_metadata,
        new_entity_type.metadata_type(speaker_ids = new_speaker_ids),
    )
    vampytest.assert_is(scheduled_event.entity_type, new_entity_type)
    vampytest.assert_eq(scheduled_event.image, new_image)
    vampytest.assert_eq(scheduled_event.name, new_name)
    vampytest.assert_is(scheduled_event.privacy_level, new_privacy_level)
    vampytest.assert_eq(scheduled_event.schedule, new_schedule.copy_with(start = new_start))
    vampytest.assert_eq(scheduled_event.start, new_start)
    vampytest.assert_is(scheduled_event.status, new_status)
        
    vampytest.assert_eq(scheduled_event.entity_id, new_entity_id)
    vampytest.assert_eq(scheduled_event.sku_ids, tuple(new_sku_ids))
    
    vampytest.assert_eq(
        old_attributes,
        {
            'channel_id': old_channel_id,
            'description': old_description,
            'end': old_end,
            'entity_metadata': old_entity_type.metadata_type(location = old_location),
            'entity_type': old_entity_type,
            'image': old_image,
            'name': old_name,
            'privacy_level': old_privacy_level,
            'schedule': old_schedule,
            'start': old_start,
            'status': old_status,
            'entity_id': old_entity_id,
            'sku_ids': tuple(old_sku_ids),
        },
    )



def test__ScheduledEvent__create_from_data_and_delete__cached():
    """
    Tests whether ``ScheduledEvent._create_from_data_and_delete`` works as intended.
    
    Case: cached.
    """
    client = Client(
        token = 'token_202303170000',
    )
    try:
        scheduled_event_id = 202303170014
        guild_id = 202303170015
        user_count = 69
        
        cached_scheduled_event = ScheduledEvent.precreate(scheduled_event_id, guild_id = guild_id)
        guild = Guild.precreate(guild_id, scheduled_events = [cached_scheduled_event])
        guild.clients = [client]
        
        data = {
            'id': str(scheduled_event_id),
            'guild_id': str(guild_id),
            'user_count': user_count,
        }
        
        scheduled_event = ScheduledEvent._create_from_data_and_delete(data)
        _assert_fields_set(scheduled_event)
        
        vampytest.assert_eq(guild.scheduled_events, None)
        vampytest.assert_is(cached_scheduled_event, scheduled_event)
        
        vampytest.assert_eq(scheduled_event.user_count, user_count)
        
    finally:
        # Cleanup
        client._delete()
        client = None


def test__ScheduledEvent__create_from_data_and_delete__not_cached():
    """
    Tests whether ``ScheduledEvent._create_from_data_and_delete`` works as intended.
    
    Case: not cached.
    """
    scheduled_event_id = 202303170016
    guild_id = 202303170017
    user_count = 69
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'id': str(scheduled_event_id),
        'guild_id': str(guild_id),
        'user_count': user_count,
    }
    
    scheduled_event = ScheduledEvent._create_from_data_and_delete(data)
    _assert_fields_set(scheduled_event)
    
    vampytest.assert_eq(guild.scheduled_events, None)
    vampytest.assert_eq(scheduled_event.user_count, user_count)
    
    test_scheduled_event = ScheduledEvent.from_data(data)
    vampytest.assert_is(scheduled_event, test_scheduled_event)


def test__ScheduledEvent__from_data_is_created__not_cached():
    """
    Tests whether ``ScheduledEvent.from_data_is_created`` works as intended.
    
    Case: not cached.
    """
    scheduled_event_id = 202303170018
    guild_id = 202303170019
    user_count = 69
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'id': str(scheduled_event_id),
        'guild_id': str(guild_id),
        'user_count': user_count,
    }
    
    scheduled_event, is_created = ScheduledEvent.from_data_is_created(data)
    _assert_fields_set(scheduled_event)
    vampytest.assert_instance(is_created, bool)
    vampytest.assert_eq(is_created, True)
    vampytest.assert_eq(scheduled_event.user_count, user_count)
    vampytest.assert_eq(guild.scheduled_events, {scheduled_event_id: scheduled_event})
    
    test_scheduled_event = ScheduledEvent.from_data(data)
    vampytest.assert_is(scheduled_event, test_scheduled_event)


def test__ScheduledEvent__from_data_is_created__cached():
    """
    Tests whether ``ScheduledEvent.from_data_is_created`` works as intended.
    
    Case: cached.
    """
    client = Client(
        token = 'token_202303170001',
    )
    try:
        scheduled_event_id = 202303170020
        guild_id = 202303170021
        user_count = 69
        
        cached_scheduled_event = ScheduledEvent.precreate(scheduled_event_id, guild_id = guild_id)
        guild = Guild.precreate(guild_id, scheduled_events = [cached_scheduled_event])
        guild.clients = [client]
        
        data = {
            'id': str(scheduled_event_id),
            'guild_id': str(guild_id),
            'user_count': user_count,
        }
        
        scheduled_event, is_created = ScheduledEvent.from_data_is_created(data)
        _assert_fields_set(scheduled_event)
        vampytest.assert_is(scheduled_event, cached_scheduled_event)
        
        vampytest.assert_instance(is_created, bool)
        vampytest.assert_eq(is_created, False)
        
        vampytest.assert_eq(scheduled_event.user_count, user_count)
        
        
    finally:
        # Cleanup
        client._delete()
        client = None
