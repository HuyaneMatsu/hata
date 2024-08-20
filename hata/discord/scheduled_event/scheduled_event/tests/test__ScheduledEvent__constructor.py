from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType
from ....user import ClientUserBase, User

from ...schedule import Schedule
from ...scheduled_event_entity_metadata import ScheduledEventEntityMetadataBase

from ..preinstanced import PrivacyLevel, ScheduledEventEntityType, ScheduledEventStatus
from ..scheduled_event import ScheduledEvent


def _assert_fields_set(scheduled_event):
    """
    Asserts whether every fields are set of the given scheduled event.
    
    Parameters
    ----------
    scheduled_event : ``ScheduledEvent``
        The scheduled event to check out.
    """
    vampytest.assert_instance(scheduled_event, ScheduledEvent)
    vampytest.assert_instance(scheduled_event.channel_id, int)
    vampytest.assert_instance(scheduled_event.creator, ClientUserBase)
    vampytest.assert_instance(scheduled_event.description, str, nullable = True)
    vampytest.assert_instance(scheduled_event.end, DateTime, nullable = True)
    vampytest.assert_instance(scheduled_event.entity_id, int)
    vampytest.assert_instance(scheduled_event.entity_metadata, ScheduledEventEntityMetadataBase)
    vampytest.assert_instance(scheduled_event.entity_type, ScheduledEventEntityType)
    vampytest.assert_instance(scheduled_event.guild_id, int)
    vampytest.assert_instance(scheduled_event.id, int)
    vampytest.assert_instance(scheduled_event.image, Icon)
    vampytest.assert_instance(scheduled_event.name, str)
    vampytest.assert_instance(scheduled_event.privacy_level, PrivacyLevel)
    vampytest.assert_instance(scheduled_event.schedule, Schedule, nullable = True)
    vampytest.assert_instance(scheduled_event.start, DateTime, nullable = True)
    vampytest.assert_instance(scheduled_event.sku_ids, tuple, nullable = True)
    vampytest.assert_instance(scheduled_event.status, ScheduledEventStatus)
    vampytest.assert_instance(scheduled_event.user_count, int)


def test__ScheduledEvent__new__no_fields():
    """
    Tests whether ``ScheduledEvent.__new__`` works as intended.
    
    Case: No fields given.
    """
    scheduled_event = ScheduledEvent()
    _assert_fields_set(scheduled_event)


def test__ScheduledEvent__new__all_fields():
    """
    Tests whether ``ScheduledEvent.__new__`` works as intended.
    
    Case: All fields given.
    """
    channel_id = 202303160000
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
    
    
    scheduled_event = ScheduledEvent(
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
    )
    _assert_fields_set(scheduled_event)
    
    vampytest.assert_eq(scheduled_event.channel_id, channel_id)
    vampytest.assert_eq(scheduled_event.description, description)
    vampytest.assert_eq(scheduled_event.end, end)
    vampytest.assert_eq(scheduled_event.entity_metadata, entity_type.metadata_type(location = location))
    vampytest.assert_is(scheduled_event.entity_type, entity_type)
    vampytest.assert_eq(scheduled_event.image, image)
    vampytest.assert_eq(scheduled_event.name, name)
    vampytest.assert_is(scheduled_event.privacy_level, privacy_level)
    vampytest.assert_eq(scheduled_event.schedule, schedule)
    vampytest.assert_eq(scheduled_event.start, start)
    vampytest.assert_is(scheduled_event.status, status)


def test__ScheduledEvent__create_empty():
    """
    Tests whether ``ScheduledEvent._create_empty˙˙ works as intended.
    """
    scheduled_event_id = 202303160001
    
    scheduled_event = ScheduledEvent._create_empty(scheduled_event_id)
    _assert_fields_set(scheduled_event)
    
    vampytest.assert_eq(scheduled_event.id, scheduled_event_id)


def test__ScheduledEvent__precreate__no_fields():
    """
    Tests whether ``ScheduledEvent.precreate`` works as intended.
    
    Case: No fields given.
    """
    scheduled_event_id = 202303160002
    
    scheduled_event = ScheduledEvent.precreate(scheduled_event_id)
    _assert_fields_set(scheduled_event)
    
    vampytest.assert_eq(scheduled_event.id, scheduled_event_id)


def test__ScheduledEvent__precreate__all_fields():
    """
    Tests whether ``ScheduledEvent.precreate`` works as intended.
    
    Case: All fields given.
    """
    scheduled_event_id = 202303160003
    
    channel_id = 202303160004
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
    
    creator = User.precreate(202303160005, name = 'Orin')
    entity_id = 202303160006
    guild_id = 202303160007
    sku_ids = [202303160008, 202303160009]
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
    vampytest.assert_eq(scheduled_event.schedule, schedule)
    vampytest.assert_eq(scheduled_event.start, start)
    vampytest.assert_is(scheduled_event.status, status)
        
    vampytest.assert_is(scheduled_event.creator, creator)
    vampytest.assert_eq(scheduled_event.entity_id, entity_id)
    vampytest.assert_eq(scheduled_event.guild_id, guild_id)
    vampytest.assert_eq(scheduled_event.sku_ids, tuple(sku_ids))
    vampytest.assert_eq(scheduled_event.user_count, user_count)


def test__ScheduledEvent__precreate__caching():
    """
    Tests whether ``ScheduledEvent.precreate`` works as intended.
    
    Case: Caching.
    """
    scheduled_event_id = 202303160010
    
    scheduled_event = ScheduledEvent.precreate(scheduled_event_id)
    test_scheduled_event = ScheduledEvent.precreate(scheduled_event_id)
    
    vampytest.assert_is(scheduled_event, test_scheduled_event)
