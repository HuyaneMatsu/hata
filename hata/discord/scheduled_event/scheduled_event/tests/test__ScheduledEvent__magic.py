from datetime import datetime as DateTime

import vampytest

from ....bases import Icon, IconType
from ....user import User

from ..preinstanced import PrivacyLevel, ScheduledEventEntityType, ScheduledEventStatus
from ..scheduled_event import ScheduledEvent


def test__ScheduledEvent__repr():
    """
    Tests whether ``ScheduledEvent.__repr__`` works as intended.
    """
    scheduled_event_id = 202303160049
    
    channel_id = 202303160050
    description = 'koishi'
    end = DateTime(2016, 3, 10)
    entity_type = ScheduledEventEntityType.location
    image = Icon(IconType.static, 45)
    name = 'komeiji'
    privacy_level = PrivacyLevel.public
    start = DateTime(2017, 4, 6)
    status = ScheduledEventStatus.active
    location = 'hell'
    
    creator = User.precreate(202303160051, name = 'Orin')
    entity_id = 202303160052
    guild_id = 202303160053
    sku_ids = [202303160054, 202303160055]
    user_count = 66
    
    
    keyword_parameters = {
        'channel_id': channel_id,
        'description': description,
        'end': end,
        'entity_type': entity_type,
        'image': image,
        'name': name,
        'privacy_level': privacy_level,
        'start': start,
        'status': status,
        'location': location,
    }
    
    scheduled_event = ScheduledEvent(
        **keyword_parameters,
    )
    vampytest.assert_instance(repr(scheduled_event), str)
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        **keyword_parameters,
        creator = creator,
        entity_id = entity_id,
        guild_id = guild_id,
        sku_ids = sku_ids,
        user_count = user_count,
    )
    vampytest.assert_instance(repr(scheduled_event), str)


def test__ScheduledEvent__hash():
    """
    Tests whether ``ScheduledEvent.__hash__`` works as intended.
    """
    scheduled_event_id = 202303160056
    
    channel_id = 202303160057
    description = 'koishi'
    end = DateTime(2016, 3, 10)
    entity_type = ScheduledEventEntityType.location
    image = Icon(IconType.static, 45)
    name = 'komeiji'
    privacy_level = PrivacyLevel.public
    start = DateTime(2017, 4, 6)
    status = ScheduledEventStatus.active
    location = 'hell'
    
    creator = User.precreate(202303160058, name = 'Orin')
    entity_id = 202303160059
    guild_id = 202303160060
    sku_ids = [202303160061, 202303160062]
    user_count = 66
    
    keyword_parameters = {
        'channel_id': channel_id,
        'description': description,
        'end': end,
        'entity_type': entity_type,
        'image': image,
        'name': name,
        'privacy_level': privacy_level,
        'start': start,
        'status': status,
        'location': location,
    }
    
    scheduled_event = ScheduledEvent(
        **keyword_parameters,
    )
    vampytest.assert_instance(hash(scheduled_event), int)
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        **keyword_parameters,
        creator = creator,
        entity_id = entity_id,
        guild_id = guild_id,
        sku_ids = sku_ids,
        user_count = user_count,
    )
    vampytest.assert_instance(hash(scheduled_event), int)


def test__ScheduledEvent__eq():
    """
    Tests whether ``ScheduledEvent.__eq__`` works as intended.
    """
    scheduled_event_id = 202303160063
    
    channel_id = 202303160064
    description = 'koishi'
    end = DateTime(2016, 3, 10)
    entity_type = ScheduledEventEntityType.location
    image = Icon(IconType.static, 45)
    name = 'komeiji'
    privacy_level = PrivacyLevel.public
    start = DateTime(2017, 4, 6)
    status = ScheduledEventStatus.active
    location = 'hell'
    
    creator = User.precreate(202303160065, name = 'Orin')
    entity_id = 202303160066
    guild_id = 202303160067
    sku_ids = [202303160068, 202303160069]
    user_count = 66
    
    keyword_parameters = {
        'channel_id': channel_id,
        'description': description,
        'end': end,
        'entity_type': entity_type,
        'image': image,
        'name': name,
        'privacy_level': privacy_level,
        'start': start,
        'status': status,
        'location': location,
    }
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        **keyword_parameters,
        creator = creator,
        entity_id = entity_id,
        guild_id = guild_id,
        sku_ids = sku_ids,
        user_count = user_count,
    )
    vampytest.assert_eq(scheduled_event, scheduled_event)
    vampytest.assert_ne(scheduled_event, object())
    
    test_scheduled_event = ScheduledEvent(**keyword_parameters)
    vampytest.assert_eq(scheduled_event, test_scheduled_event)
    
    
    for field_name, field_value in (
        ('channel_id', 202303160070),
        ('description', 'yakumo'),
        ('end', DateTime(2016, 5, 10)),
        ('entity_type', ScheduledEventEntityType.stage),
        ('image', Icon(IconType.animated, 42)),
        ('name', 'yukari'),
        ('privacy_level', PrivacyLevel.guild_only),
        ('start', DateTime(2016, 3, 12)),
        ('status', ScheduledEventStatus.cancelled),
        ('location', 'beat'),

    ):
        test_keyword_parameters = keyword_parameters.copy()    
        if field_name == 'entity_type':
            test_keyword_parameters.pop('location', None)
        else:
            test_keyword_parameters['location'] = location
        test_keyword_parameters[field_name] = field_value
        
        test_scheduled_event = ScheduledEvent(**test_keyword_parameters)
        vampytest.assert_ne(scheduled_event, test_scheduled_event)
