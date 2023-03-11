import vampytest

from ...scheduled_event import PrivacyLevel

from ..stage import Stage


def test__Stage__repr():
    """
    Tests whether ``Stage.__repr__`` works as intended.
    """
    stage_id = 202303110030
    channel_id = 202303110031
    discoverable = True
    guild_id = 202303110032
    invite_code = 'suika'
    privacy_level = PrivacyLevel.public
    scheduled_event_id = 202303110033
    topic = 'breaking me softly'
    
    stage = Stage(
        privacy_level = privacy_level,
        topic = topic,
    )
    vampytest.assert_instance(repr(stage), str)
    
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
    vampytest.assert_instance(repr(stage), str)


def test__Stage__hash():
    """
    Tests whether ``Stage.__hash__`` works as intended.
    """
    stage_id = 202303110034
    channel_id = 202303110035
    discoverable = True
    guild_id = 202303110036
    invite_code = 'suika'
    privacy_level = PrivacyLevel.public
    scheduled_event_id = 202303110037
    topic = 'breaking me softly'
    
    stage = Stage(
        privacy_level = privacy_level,
        topic = topic,
    )
    vampytest.assert_instance(hash(stage), int)
    
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
    vampytest.assert_instance(hash(stage), int)


def test__Stage__eq():
    """
    Tests whether ``Stage.__eq__`` works as intended.
    """
    stage_id = 202303110038
    channel_id = 202303110039
    discoverable = True
    guild_id = 202303110040
    invite_code = 'suika'
    privacy_level = PrivacyLevel.public
    scheduled_event_id = 202303110041
    topic = 'breaking me softly'
    
    keyword_parameters = {
        'privacy_level': privacy_level,
        'topic': topic,
    }
    
    stage = Stage.precreate(
        stage_id,
        **keyword_parameters,
        channel_id = channel_id,
        discoverable = discoverable,
        guild_id = guild_id,
        invite_code = invite_code,
        scheduled_event_id = scheduled_event_id,
    )
    vampytest.assert_eq(stage, stage)
    vampytest.assert_ne(stage, object())
    
    test_stage = Stage(**keyword_parameters)
    vampytest.assert_eq(stage, test_stage)
    
    
    for field_name, field_value in (
        ('privacy_level', PrivacyLevel.guild_only),
        ('topic', 'tipsy oni'),

    ):
        test_stage = Stage(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(stage, test_stage)
