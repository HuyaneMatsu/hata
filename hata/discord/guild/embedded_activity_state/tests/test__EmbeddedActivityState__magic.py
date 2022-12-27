import vampytest

from ....activity import Activity, ActivityType

from ..embedded_activity_state import EmbeddedActivityState


def test__EmbeddedActivityState__repr():
    """
    Tests whether ``EmbeddedActivityState.__repr__`` works as intended.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260081)
    channel_id = 202212260082
    guild_id = 202212260083
    user_ids = [202212260084, 202212260085]
    
    
    embedded_activity_state = EmbeddedActivityState(
        activity = activity,
        channel_id = channel_id,
        guild_id = guild_id,
        user_ids = user_ids,
    )
    
    vampytest.assert_instance(repr(embedded_activity_state), str)


def test__EmbeddedActivityState__hash():
    """
    Tests whether ``EmbeddedActivityState.__hash__`` works as intended.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260086)
    channel_id = 202212260087
    guild_id = 202212260088
    user_ids = [202212260089, 202212260090]
    
    
    embedded_activity_state = EmbeddedActivityState(
        activity = activity,
        channel_id = channel_id,
        guild_id = guild_id,
        user_ids = user_ids,
    )
    
    vampytest.assert_instance(hash(embedded_activity_state), int)


def test__EmbeddedActivityState__eq():
    """
    Tests whether ``EmbeddedActivityState.__eq__`` works as intended.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260091)
    channel_id = 202212260092
    guild_id = 202212260093
    user_ids = [202212260094, 202212260095]
    
    keyword_parameters = {
        'activity': activity,
        'channel_id': channel_id,
        'guild_id': guild_id,
        'user_ids': user_ids
    }
    
    embedded_activity_state = EmbeddedActivityState(
        activity = activity,
        channel_id = channel_id,
        guild_id = guild_id,
        user_ids = user_ids,
    )
    
    vampytest.assert_eq(embedded_activity_state, embedded_activity_state)
    vampytest.assert_ne(embedded_activity_state, object())
    
    for field_name, field_value in (
        ('activity', Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260096)),
        ('channel_id', 202212260097),
        ('guild_id', 202212260098),
    ):
        test_embedded_activity_state = EmbeddedActivityState(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(embedded_activity_state, test_embedded_activity_state)
