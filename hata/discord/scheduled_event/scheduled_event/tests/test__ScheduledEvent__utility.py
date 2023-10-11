from datetime import datetime as DateTime

import vampytest

from ....bases import Icon, IconType
from ....channel import Channel
from ....client import Client
from ....guild import Guild
from ....user import User
from ....utils import is_url

from ..preinstanced import PrivacyLevel, ScheduledEventEntityType, ScheduledEventStatus
from ..scheduled_event import ScheduledEvent

from .test__ScheduledEvent__constructor import _assert_fields_set


def test__ScheduledEvent__copy():
    """
    Tests whether ``ScheduledEvent.copy`` works as intended.
    """
    channel_id = 202303160071
    description = 'koishi'
    end = DateTime(2016, 3, 10)
    entity_type = ScheduledEventEntityType.location
    image = Icon(IconType.static, 45)
    name = 'komeiji'
    privacy_level = PrivacyLevel.public
    start = DateTime(2017, 4, 6)
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
        start = start,
        status = status,
        location = location,
    )
    
    copy = scheduled_event.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, scheduled_event)
        
    vampytest.assert_eq(scheduled_event, copy)


def test__ScheduledEvent__copy_with__0():
    """
    Tests whether ``ScheduledEvent.copy_with`` works as intended.
    
    Case: No fields given.
    """
    channel_id = 202303160072
    description = 'koishi'
    end = DateTime(2016, 3, 10)
    entity_type = ScheduledEventEntityType.location
    image = Icon(IconType.static, 45)
    name = 'komeiji'
    privacy_level = PrivacyLevel.public
    start = DateTime(2017, 4, 6)
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
        start = start,
        status = status,
        location = location,
    )
    
    copy = scheduled_event.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, scheduled_event)
        
    vampytest.assert_eq(scheduled_event, copy)


def test__ScheduledEvent__copy_with__1():
    """
    Tests whether ``ScheduledEvent.copy_with`` works as intended.
    
    Case: No fields given.
    """
    old_channel_id = 202303160073
    old_description = 'koishi'
    old_end = DateTime(2016, 3, 10)
    old_entity_type = ScheduledEventEntityType.location
    old_image = Icon(IconType.static, 45)
    old_name = 'komeiji'
    old_privacy_level = PrivacyLevel.public
    old_start = DateTime(2017, 4, 6)
    old_status = ScheduledEventStatus.active
    old_location = 'hell'
    
    new_channel_id = 202303160074
    new_description = 'yakumo'
    new_end = DateTime(2016, 4, 10)
    new_entity_type = ScheduledEventEntityType.stage
    new_image = Icon(IconType.animated, 46)
    new_name = 'yukari'
    new_privacy_level = PrivacyLevel.guild_only
    new_start = DateTime(2017, 5, 6)
    new_status = ScheduledEventStatus.cancelled
    new_speaker_ids = [202303160075, 202303160076]
    
    scheduled_event = ScheduledEvent(
        channel_id = old_channel_id,
        description = old_description,
        end = old_end,
        entity_type = old_entity_type,
        image = old_image,
        name = old_name,
        privacy_level = old_privacy_level,
        start = old_start,
        status = old_status,
        location = old_location,
    )
    
    copy = scheduled_event.copy_with(
        channel_id = new_channel_id,
        description = new_description,
        end = new_end,
        entity_type = new_entity_type,
        image = new_image,
        name = new_name,
        privacy_level = new_privacy_level,
        start = new_start,
        status = new_status,
        speaker_ids = new_speaker_ids,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, scheduled_event)
    
    vampytest.assert_eq(copy.channel_id, new_channel_id)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.end, new_end)
    vampytest.assert_eq(copy.entity_metadata, new_entity_type.metadata_type(speaker_ids = new_speaker_ids))
    vampytest.assert_is(copy.entity_type, new_entity_type)
    vampytest.assert_eq(copy.image, new_image)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_is(copy.privacy_level, new_privacy_level)
    vampytest.assert_eq(copy.start, new_start)
    vampytest.assert_is(copy.status, new_status)


def test__ScheduledEvent__delete():
    """
    Tests whether ``ScheduledEvent._delete`` works as intended.
    """
    scheduled_event_id = 202303160077
    guild_id = 202303160078
    
    guild = Guild.precreate(guild_id)
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        guild_id = guild_id,
    )
    
    guild.scheduled_events = {scheduled_event_id: scheduled_event}
    
    output = scheduled_event._delete()
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    
    vampytest.assert_eq(guild.scheduled_events, {})


def test__ScheduledEvent__partial__0():
    """
    Tests whether ``ScheduledEvent.partial`` works as intended.
    
    Case: Fully partial.
    """
    scheduled_event = ScheduledEvent()
    output = scheduled_event.partial
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__ScheduledEvent__partial__1():
    """
    Tests whether ``ScheduledEvent.partial`` works as intended.
    
    Case: Not linked to its guild.
    """
    scheduled_event_id = 202303160079
    guild_id = 202303160080
    
    guild = Guild.precreate(guild_id)
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        guild_id = guild_id,
    )
    
    output = scheduled_event.partial
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__ScheduledEvent__partial__2():
    """
    Tests whether ``ScheduledEvent.partial`` works as intended.
    
    Case: Linked to its guild & guild not partial.
    """
    client = Client(
        token = 'token_202303160000',
    )
    try:
        scheduled_event_id = 202303160081
        guild_id = 202303160082
        
        guild = Guild.precreate(guild_id)
        guild.clients = [client]
        
        scheduled_event = ScheduledEvent.precreate(
            scheduled_event_id,
            guild_id = guild_id,
        )
        
        guild.scheduled_events = {scheduled_event_id: scheduled_event}
        
        output = scheduled_event.partial
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
        
    finally:
        # Cleanup
        client._delete()
        client = None


def test__ScheduledEvent__channel():
    """
    Tests whether ``ScheduledEvent.channel`` works as intended.
    """
    channel_id = 202303160083
    
    for scheduled_event_id, input_value, expected_output in (
        (202303160090, 0, None),
        (202303160084, channel_id, Channel.precreate(channel_id)),
    ):
        scheduled_event = ScheduledEvent.precreate(scheduled_event_id, channel_id = input_value)
        vampytest.assert_is(scheduled_event.channel, expected_output)


def _iter_options__guild():
    guild_id_0 = 202303160085
    guild_id_1 = 202303160086
    
    yield (202303160087, 0, None)
    yield (202303160088, guild_id_0, None)
    yield (202303160089, guild_id_1, Guild.precreate(guild_id_1))
    

@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__ScheduledEvent__guild(scheduled_event_id, guild_id):
    """
    Tests whether ``ScheduledEvent.guild`` works as intended.
    
    Parameters
    ----------
    scheduled_event_id : `int`
        Identifier of teh scheduled event to create.
    guild_id : `int`
        The guild's identifier.
    
    Returns
    -------
    output : `None | Guild`
    """
    scheduled_event = ScheduledEvent.precreate(scheduled_event_id, guild_id = guild_id)
    return scheduled_event.guild


def test__ScheduledEvent__creator_id():
    """
    Tests whether ``ScheduledEvent.creator_id`` works as intended.
    """
    scheduled_event_id = 202303170000
    creator_id = 202303170001
    creator = User.precreate(creator_id, name = 'orin')
    
    scheduled_event = ScheduledEvent.precreate(scheduled_event_id, creator = creator)
    
    output = scheduled_event.creator_id
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, creator_id)


def test__ScheduledEvent__iter_sku_ids():
    """
    Tests whether ``ScheduledEvent.iter_sku_ids`` works as intended.
    """
    sku_id_0 = 202303170002
    sku_id_1 = 202303170003
    
    for scheduled_event_id, input_value, expected_output in (
        (202303170004, None, []),
        (202303170005, [sku_id_0], [sku_id_0]),
        (202303170006, [sku_id_0, sku_id_1], [sku_id_0, sku_id_1]),
    ):
        scheduled_event = ScheduledEvent.precreate(scheduled_event_id, sku_ids = input_value)
        vampytest.assert_eq([*scheduled_event.iter_sku_ids()], expected_output)


def test__ScheduledEvent__entity__0():
    """
    Tests whether ``ScheduledEvent.entity`` works as intended.
    
    Case: No id, but type.
    """
    scheduled_event_id = 202303170007
    entity_id = 0
    entity_type = ScheduledEventEntityType.stage
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        entity_id = entity_id,
        entity_type = entity_type,
    )
    
    output = scheduled_event.entity
    vampytest.assert_is(output, None)
    

def test__ScheduledEvent__entity__1():
    """
    Tests whether ``ScheduledEvent.entity`` works as intended.
    
    Case: id, but not type.
    """
    scheduled_event_id = 202303170008
    entity_id = 202303170009
    entity_type = ScheduledEventEntityType.none
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        entity_id = entity_id,
        entity_type = entity_type,
    )
    
    output = scheduled_event.entity
    vampytest.assert_is(output, None)
    

def test__ScheduledEvent__entity__2():
    """
    Tests whether ``ScheduledEvent.entity`` works as intended.
    
    Case: voice channel.
    """
    scheduled_event_id = 202303170010
    entity_id = 202303170011
    entity_type = ScheduledEventEntityType.voice
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        entity_id = entity_id,
        entity_type = entity_type,
    )
    
    output = scheduled_event.entity
    vampytest.assert_instance(output, Channel)
    vampytest.assert_true(output.is_guild_voice())
    vampytest.assert_eq(output.id, entity_id)


def test__ScheduledEvent__entity__3():
    """
    Tests whether ``ScheduledEvent.entity`` works as intended.
    
    Case: stage channel.
    """
    scheduled_event_id = 202303170012
    entity_id = 202303170013
    entity_type = ScheduledEventEntityType.stage
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        entity_id = entity_id,
        entity_type = entity_type,
    )
    
    output = scheduled_event.entity
    vampytest.assert_instance(output, Channel)
    vampytest.assert_true(output.is_guild_stage())
    vampytest.assert_eq(output.id, entity_id)


def test__ScheduledEvent__url():
    """
    Tests whether ``ScheduledEvent.url`` works as intended.
    
    Case: stage channel.
    """
    scheduled_event_id = 202303190000
    guild_id = 202303190001
    
    scheduled_event = ScheduledEvent.precreate(
        scheduled_event_id,
        guild_id = guild_id,
    )
    
    output = scheduled_event.url
    vampytest.assert_instance(output, str)
    vampytest.assert_true(is_url(output))
    vampytest.assert_in(str(scheduled_event_id), output)
    vampytest.assert_in(str(guild_id), output)
