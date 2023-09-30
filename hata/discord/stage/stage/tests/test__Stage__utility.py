import vampytest

from ....channel import Channel
from ....client import Client
from ....guild import Guild
from ....scheduled_event import PrivacyLevel

from ..stage import Stage

from .test__Stage__constructor import _assert_fields_set


def test__Stage__copy():
    """
    Tests whether ``Stage.copy`` works as intended.
    """
    privacy_level = PrivacyLevel.public
    scheduled_event_id = 202309300002
    topic = 'breaking me softly'
    
    stage = Stage(
        privacy_level = privacy_level,
        scheduled_event_id = scheduled_event_id,
        topic = topic,
    )
    
    copy = stage.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, stage)
        
    vampytest.assert_eq(stage, copy)


def test__Stage__copy_with__0():
    """
    Tests whether ``Stage.copy_with`` works as intended.
    
    Case: No fields given.
    """
    privacy_level = PrivacyLevel.public
    scheduled_event_id = 202309300003
    topic = 'breaking me softly'
    
    stage = Stage(
        privacy_level = privacy_level,
        scheduled_event_id = scheduled_event_id,
        topic = topic,
    )
    
    copy = stage.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, stage)
        
    vampytest.assert_eq(stage, copy)


def test__Stage__copy_with__1():
    """
    Tests whether ``Stage.copy_with`` works as intended.
    
    Case: No fields given.
    """
    old_privacy_level = PrivacyLevel.public
    old_scheduled_event_id = 202309300004
    old_topic = 'breaking me softly'
    
    new_privacy_level = PrivacyLevel.guild_only
    new_scheduled_event_id = 202309300005
    new_topic = 'breaking me softly'
    
    stage = Stage(
        privacy_level = old_privacy_level,
        scheduled_event_id = old_scheduled_event_id,
        topic = old_topic,
    )
    
    copy = stage.copy_with(
        privacy_level = new_privacy_level,
        scheduled_event_id = new_scheduled_event_id,
        topic = new_topic,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, stage)
    
    vampytest.assert_is(copy.privacy_level, new_privacy_level)
    vampytest.assert_eq(copy.scheduled_event_id, new_scheduled_event_id)
    vampytest.assert_eq(copy.topic, new_topic)


def test__Stage__delete():
    """
    Tests whether ``Stage._delete`` works as intended.
    """
    stage_id = 202303110048
    guild_id = 202303110049
    
    guild = Guild.precreate(guild_id)
    
    stage = Stage.precreate(
        stage_id,
        guild_id = guild_id,
    )
    
    guild.stages = {stage_id: stage}
    
    stage._delete()
    
    vampytest.assert_eq(guild.stages, None)


def test__Stage__partial__0():
    """
    Tests whether ``Stage.partial`` works as intended.
    
    Case: Fully partial.
    """
    stage = Stage()
    output = stage.partial
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__Stage__partial__1():
    """
    Tests whether ``Stage.partial`` works as intended.
    
    Case: Not linked to its guild.
    """
    stage_id = 202303110050
    guild_id = 202303110051
    
    guild = Guild.precreate(guild_id)
    
    stage = Stage.precreate(
        stage_id,
        guild_id = guild_id,
    )
    
    output = stage.partial
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__Stage__partial__2():
    """
    Tests whether ``Stage.partial`` works as intended.
    
    Case: Linked to its guild & guild not partial.
    """

    client = Client(
        token = 'token_202303110000',
    )
    try:
        stage_id = 202303110052
        guild_id = 202303110053
        
        guild = Guild.precreate(guild_id)
        guild.clients = [client]
        
        stage = Stage.precreate(
            stage_id,
            guild_id = guild_id,
        )
        
        guild.stages = {stage_id: stage}
        
        output = stage.partial
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
        
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Stage__channel():
    """
    Tests whether ``Stage.channel`` works as intended.
    """
    channel_id = 202303110054
    
    for stage_id, input_value, expected_output in (
        (202303110060, channel_id, Channel.precreate(channel_id)),
    ):
        stage = Stage.precreate(stage_id, channel_id = input_value)
        vampytest.assert_is(stage.channel, expected_output)


def test__Stage__guild():
    """
    Tests whether ``Stage.guild`` works as intended.
    """
    guild_id_0 = 202303110055
    guild_id_1 = 202303110056
    
    for stage_id, input_value, expected_output in (
        (202303110057, 0, None),
        (202303110058, guild_id_0, None),
        (202303110059, guild_id_1, Guild.precreate(guild_id_1)),
    ):
        stage = Stage.precreate(stage_id, guild_id = input_value)
        vampytest.assert_is(stage.guild, expected_output)
