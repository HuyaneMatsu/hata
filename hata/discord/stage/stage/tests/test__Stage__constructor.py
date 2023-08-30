import vampytest

from ....scheduled_event import PrivacyLevel

from ..stage import Stage


def _assert_fields_set(stage):
    """
    Asserts whether every fields are set of the given stage.
    
    Parameters
    ----------
    stage : ``Stage``
        The stage to check out.
    """
    vampytest.assert_instance(stage, Stage)
    vampytest.assert_instance(stage.channel_id, int)
    vampytest.assert_instance(stage.discoverable, bool)
    vampytest.assert_instance(stage.guild_id, int)
    vampytest.assert_instance(stage.id, int)
    vampytest.assert_instance(stage.invite_code, str, nullable = True)
    vampytest.assert_instance(stage.privacy_level, PrivacyLevel)
    vampytest.assert_instance(stage.scheduled_event_id, int)
    vampytest.assert_instance(stage.topic, str, nullable = True)


def test__Stage__new__0():
    """
    Tests whether ``Stage.__new__`` works as intended.
    
    Case: No fields given.
    """
    stage = Stage()
    _assert_fields_set(stage)


def test__Stage__new__1():
    """
    Tests whether ``Stage.__new__`` works as intended.
    
    Case: All fields given.
    """
    privacy_level = PrivacyLevel.public
    topic = 'breaking me softly'
    
    stage = Stage(
        privacy_level = privacy_level,
        topic = topic,
    )
    _assert_fields_set(stage)
    
    vampytest.assert_is(stage.privacy_level, privacy_level)
    vampytest.assert_eq(stage.topic, topic)


def test__Stage__create_empty():
    """
    Tests whether ``Stage._create_empty˙˙ works as intended.
    """
    stage_id = 202303110013
    
    stage = Stage._create_empty(stage_id)
    _assert_fields_set(stage)
    
    vampytest.assert_eq(stage.id, stage_id)


def test__Stage__precreate__0():
    """
    Tests whether ``Stage.precreate`` works as intended.
    
    Case: No fields given.
    """
    stage_id = 202303110014
    
    stage = Stage.precreate(stage_id)
    _assert_fields_set(stage)
    
    vampytest.assert_eq(stage.id, stage_id)


def test__Stage__precreate__1():
    """
    Tests whether ``Stage.precreate`` works as intended.
    
    Case: All fields given.
    """
    stage_id = 202303110015
    channel_id = 202303110016
    discoverable = True
    guild_id = 202303110017
    invite_code = 'suika'
    privacy_level = PrivacyLevel.public
    scheduled_event_id = 202303110018
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
    _assert_fields_set(stage)
    
    vampytest.assert_eq(stage.id, stage_id)
    
    vampytest.assert_eq(stage.channel_id, channel_id)
    vampytest.assert_eq(stage.discoverable, discoverable)
    vampytest.assert_eq(stage.guild_id, guild_id)
    vampytest.assert_eq(stage.invite_code, invite_code)
    vampytest.assert_is(stage.privacy_level, privacy_level)
    vampytest.assert_eq(stage.scheduled_event_id, scheduled_event_id)
    vampytest.assert_eq(stage.topic, topic)


def test__Stage__precreate__2():
    """
    Tests whether ``Stage.precreate`` works as intended.
    
    Case: Caching.
    """
    stage_id = 202303110019
    
    stage = Stage.precreate(stage_id)
    test_stage = Stage.precreate(stage_id)
    
    vampytest.assert_is(stage, test_stage)
