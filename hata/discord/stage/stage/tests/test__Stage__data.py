import vampytest

from ....guild import Guild
from ....scheduled_event import PrivacyLevel

from ..stage import Stage

from .test__Stage__constructor import _assert_fields_set


def test__Stage__from_data__0():
    """
    Tests whether ``Stage.from_data`` works as intended.
    
    Case: default.
    """
    
    stage_id = 202303110020
    channel_id = 202303110021
    discoverable = True
    guild_id = 202303110022
    invite_code = 'suika'
    privacy_level = PrivacyLevel.public
    scheduled_event_id = 202303110023
    topic = 'breaking me softly'
    
    data = {
        'id': str(stage_id),
        'channel_id': str(channel_id),
        'discoverable_disabled': not discoverable,
        'guild_id': str(guild_id),
        'invite_code': str(invite_code),
        'privacy_level': privacy_level.value,
        'guild_scheduled_event_id': str(scheduled_event_id),
        'topic': topic,
    }
    
    stage = Stage.from_data(data)
    _assert_fields_set(stage)
    
    vampytest.assert_eq(stage.id, stage_id)
    
    vampytest.assert_eq(stage.channel_id, channel_id)
    vampytest.assert_eq(stage.discoverable, discoverable)
    vampytest.assert_eq(stage.guild_id, guild_id)
    vampytest.assert_eq(stage.invite_code, invite_code)
    vampytest.assert_is(stage.privacy_level, privacy_level)
    vampytest.assert_eq(stage.scheduled_event_id, scheduled_event_id)
    vampytest.assert_eq(stage.topic, topic)


def test__Stage__from_data__1():
    """
    Tests whether ``Stage.from_data`` works as intended.
    
    Case: global caching.
    """
    stage_id = 202303110024
    
    data = {
        'id': str(stage_id),
    }
    
    stage = Stage.from_data(data)
    test_stage = Stage.from_data(data)
    
    vampytest.assert_is(stage, test_stage)


def test__Stage__from_data__2():
    """
    Tests whether ``Stage.from_data`` works as intended.
    
    Case: caching under guild.
    """
    stage_id = 202303110024
    guild_id = 202303110047
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'id': str(stage_id),
        'guild_id': str(guild_id),
    }
    
    stage = Stage.from_data(data)
    
    vampytest.assert_eq(guild.stages, {stage_id: stage})


def test__Stage__from_data__3():
    """
    Tests whether ``Stage.from_data`` works as intended.
    
    Case: do not cache into guild.
    """
    stage_id = 202306110012
    guild_id = 202306110013
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'id': str(stage_id),
        'guild_id': str(guild_id),
    }
    
    stage = Stage.from_data(data, strong_cache = False)
    
    vampytest.assert_eq(guild.stages, None)


def test__Stage__to_data():
    """
    Tests whether ``Stage.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    stage_id = 202303110025
    channel_id = 202303110026
    discoverable = True
    guild_id = 202303110027
    invite_code = 'suika'
    privacy_level = PrivacyLevel.public
    scheduled_event_id = 202303110028
    topic = 'breaking me softly'
    
    
    stage = Stage.precreate(
        stage_id,
        channel_id = channel_id,
        discoverable = discoverable,
        guild_id = guild_id,
        invite_code = invite_code,
        privacy_level = privacy_level,
        scheduled_event_id = scheduled_event_id,
        topic = topic,
    )
    
    expected_output = {
        'id': str(stage_id),
        'channel_id': str(channel_id),
        'discoverable_disabled': not discoverable,
        'guild_id': str(guild_id),
        'invite_code': str(invite_code),
        'privacy_level': privacy_level.value,
        'guild_scheduled_event_id': str(scheduled_event_id),
        'topic': topic,
    }
    
    vampytest.assert_eq(
        stage.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__Stage__set_attributes():
    """
    Tests whether ``Stage._set_attributes`` works as intended.
    """
    channel_id = 202303110026
    discoverable = True
    guild_id = 202303110027
    invite_code = 'suika'
    privacy_level = PrivacyLevel.public
    scheduled_event_id = 202303110028
    topic = 'breaking me softly'
    
    data = {
        'channel_id': str(channel_id),
        'discoverable_disabled': not discoverable,
        'guild_id': str(guild_id),
        'invite_code': str(invite_code),
        'privacy_level': privacy_level.value,
        'guild_scheduled_event_id': str(scheduled_event_id),
        'topic': topic,
    }
    
    stage = Stage()
    stage._set_attributes(data)
    
    vampytest.assert_eq(stage.channel_id, channel_id)
    vampytest.assert_eq(stage.discoverable, discoverable)
    vampytest.assert_eq(stage.guild_id, guild_id)
    vampytest.assert_eq(stage.invite_code, invite_code)
    vampytest.assert_is(stage.privacy_level, privacy_level)
    vampytest.assert_eq(stage.scheduled_event_id, scheduled_event_id)
    vampytest.assert_eq(stage.topic, topic)



def test__Stage__update_attributes():
    """
    Tests whether ``Stage._update_attributes`` works as intended.
    """
    discoverable = True
    invite_code = 'suika'
    privacy_level = PrivacyLevel.public
    topic = 'breaking me softly'
    
    data = {
        'discoverable_disabled': not discoverable,
        'invite_code': str(invite_code),
        'privacy_level': privacy_level.value,
        'topic': topic,
    }
    
    stage = Stage()
    stage._update_attributes(data)
    
    vampytest.assert_eq(stage.discoverable, discoverable)
    vampytest.assert_eq(stage.invite_code, invite_code)
    vampytest.assert_is(stage.privacy_level, privacy_level)
    vampytest.assert_eq(stage.topic, topic)


def test__Stage__difference_update_attributes():
    """
    Tests whether ``Stage._difference_update_attributes`` works as intended.
    """
    stage_id = 202303110029
    
    old_discoverable = True
    old_invite_code = 'suika'
    old_privacy_level = PrivacyLevel.public
    old_topic = 'breaking me softly'
    
    new_discoverable = False
    new_invite_code = 'ibuki'
    new_privacy_level = PrivacyLevel.guild_only
    new_topic = 'tipsy oni'
    
    stage = Stage.precreate(
        stage_id,
        discoverable = old_discoverable,
        invite_code = old_invite_code,
        privacy_level = old_privacy_level,
        topic = old_topic,
    )
    
    data = {
        'discoverable_disabled': not new_discoverable,
        'invite_code': str(new_invite_code),
        'privacy_level': new_privacy_level.value,
        'topic': new_topic,
    }
    
    old_attributes = stage._difference_update_attributes(data)
    
    vampytest.assert_eq(stage.discoverable, new_discoverable)
    vampytest.assert_eq(stage.invite_code, new_invite_code)
    vampytest.assert_is(stage.privacy_level, new_privacy_level)
    vampytest.assert_eq(stage.topic, new_topic)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'discoverable': old_discoverable,
            'invite_code': old_invite_code,
            'privacy_level': old_privacy_level,
            'topic': old_topic,
        },
    )
