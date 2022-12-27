import vampytest

from ....activity import Activity, ActivityType

from ..embedded_activity_state import EmbeddedActivityState


def _assert_fields_set(embedded_activity_state):
    """
    Asserts whether every attribute is set of the given embedded activity state.
    
    Parameters
    ----------
    embedded_activity_state : ``EmbeddedActivityState``
        The embedded activity state to check.
    """
    vampytest.assert_instance(embedded_activity_state, EmbeddedActivityState)
    vampytest.assert_instance(embedded_activity_state.activity, Activity)
    vampytest.assert_instance(embedded_activity_state.channel_id, int)
    vampytest.assert_instance(embedded_activity_state.guild_id, int)
    vampytest.assert_instance(embedded_activity_state.user_ids, set)


def test__EmbeddedActivityState__new__0():
    """
    Tests whether ``EmbeddedActivityState.__new__`` works as intended.
    
    Case: No fields given.
    """
    embedded_activity_state = EmbeddedActivityState()
    _assert_fields_set(embedded_activity_state)


def test__EmbeddedActivityState__new__1():
    """
    Tests whether ``EmbeddedActivityState.__new__`` works as intended.
    
    Case: All fields given.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260050)
    channel_id = 202212260041
    guild_id = 202212260042
    user_ids = [202212260043, 202212260044]
    
    
    embedded_activity_state = EmbeddedActivityState(
        activity = activity,
        channel_id = channel_id,
        guild_id = guild_id,
        user_ids = user_ids,
    )
    _assert_fields_set(embedded_activity_state)
    
    vampytest.assert_eq(embedded_activity_state.activity, activity)
    vampytest.assert_eq(embedded_activity_state.channel_id, channel_id)
    vampytest.assert_eq(embedded_activity_state.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity_state.user_ids, set(user_ids))
