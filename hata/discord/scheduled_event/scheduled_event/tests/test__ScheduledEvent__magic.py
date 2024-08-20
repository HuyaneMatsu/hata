from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bases import Icon, IconType
from ....user import User

from ...schedule import Schedule

from ..preinstanced import PrivacyLevel, ScheduledEventEntityType, ScheduledEventStatus
from ..scheduled_event import ScheduledEvent


def test__ScheduledEvent__repr():
    """
    Tests whether ``ScheduledEvent.__repr__`` works as intended.
    """
    scheduled_event_id = 202303160049
    
    channel_id = 202303160050
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
        'schedule': schedule,
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
    end = DateTime(2016, 3, 10, tzinfo = TimeZone.utc)
    entity_type = ScheduledEventEntityType.location
    image = Icon(IconType.static, 45)
    name = 'komeiji'
    privacy_level = PrivacyLevel.public
    schedule = Schedule(occurrence_spacing = 2)
    start = DateTime(2017, 4, 6, tzinfo = TimeZone.utc)
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
        'schedule': schedule,
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


def _iter_options__eq():
    channel_id = 202303160064
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
    
    keyword_parameters = {
        'channel_id': channel_id,
        'description': description,
        'end': end,
        'entity_type': entity_type,
        'image': image,
        'name': name,
        'privacy_level': privacy_level,
        'schedule': schedule,
        'start': start,
        'status': status,
        'location': location,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'channel_id': 202303160070,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description': 'yakumo',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'end': DateTime(2016, 5, 10, tzinfo = TimeZone.utc),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **{key: value for key, value in keyword_parameters.items() if key != 'location'},
            'entity_type': ScheduledEventEntityType.stage,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'image': Icon(IconType.animated, 42),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'yukari',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'privacy_level': PrivacyLevel.guild_only,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'schedule': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'start': DateTime(2016, 3, 12, tzinfo = TimeZone.utc),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'status': ScheduledEventStatus.cancelled,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'location': 'beat',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ScheduledEvent__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ScheduledEvent.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    scheduled_event_0 = ScheduledEvent(**keyword_parameters_0)
    scheduled_event_1 = ScheduledEvent(**keyword_parameters_1)
    
    output = scheduled_event_0 == scheduled_event_1
    vampytest.assert_instance(output, bool)
    return output


def test__ScheduledEvent__eq__non_partial():
    """
    Tests whether ``ScheduledEvent.__eq__`` works as intended.
    
    Case: Testing against non partial instance.
    """
    scheduled_event_id = 202303160063
    name = 'hey mister'
    
    creator = User.precreate(202303160065, name = 'Orin')
    entity_id = 202303160066
    guild_id = 202303160067
    sku_ids = [202303160068, 202303160069]
    user_count = 66
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        name = name,
        creator = creator,
        entity_id = entity_id,
        guild_id = guild_id,
        sku_ids = sku_ids,
        user_count = user_count,
    )
    
    vampytest.assert_eq(scheduled_event, scheduled_event)
    vampytest.assert_ne(scheduled_event, object())
    
    vampytest.assert_ne(scheduled_event, ScheduledEvent())
    vampytest.assert_eq(scheduled_event, ScheduledEvent(name = name))
