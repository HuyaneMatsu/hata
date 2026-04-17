import vampytest

from ....user import User

from ...embedded_activity_location import EmbeddedActivityLocation
from ...embedded_activity_user_state import EmbeddedActivityUserState

from ..embedded_activity import EmbeddedActivity


def _assert_fields_set(embedded_activity):
    """
    Asserts whether every attribute is set of the given embedded activity.
    
    Parameters
    ----------
    embedded_activity : ``EmbeddedActivity``
        The embedded activity to check.
    """
    vampytest.assert_instance(embedded_activity, EmbeddedActivity)
    vampytest.assert_instance(embedded_activity.application_id, int)
    vampytest.assert_instance(embedded_activity.guild_id, int)
    vampytest.assert_instance(embedded_activity.id, int)
    vampytest.assert_instance(embedded_activity.launch_id, int)
    vampytest.assert_instance(embedded_activity.location, EmbeddedActivityLocation, nullable = True)
    vampytest.assert_instance(embedded_activity.user_states, dict)


def test__EmbeddedActivity__new__no_fields():
    """
    Tests whether ``EmbeddedActivity.__new__`` works as intended.
    
    Case: No fields given.
    """
    embedded_activity = EmbeddedActivity()
    _assert_fields_set(embedded_activity)


def test__EmbeddedActivity__new__all_fields():
    """
    Tests whether ``EmbeddedActivity.__new__`` works as intended.
    
    Case: All fields given.
    """
    application_id = 202408020000
    location = EmbeddedActivityLocation(channel_id = 202408020001)
    
    embedded_activity = EmbeddedActivity(
        application_id = application_id,
        location = location,
    )
    _assert_fields_set(embedded_activity)
    
    vampytest.assert_eq(embedded_activity.application_id, application_id)
    vampytest.assert_eq(embedded_activity.location, location)


def test__EmbeddedActivity__create_empty():
    """
    Tests whether ``EmbeddedActivity._create_empty`` works as intended.
    """
    embedded_activity_id = 202408020002
    
    embedded_activity = EmbeddedActivity._create_empty(embedded_activity_id)
    _assert_fields_set(embedded_activity)
    
    vampytest.assert_eq(embedded_activity.id, embedded_activity_id)


def test__EmbeddedActivity__precreate__no_fields():
    """
    Tests whether ``EmbeddedActivity.precreate`` works as intended.
    
    Case: No fields given.
    """
    embedded_activity_id = 202408020003
    
    embedded_activity = EmbeddedActivity.precreate(embedded_activity_id)
    _assert_fields_set(embedded_activity)
    
    vampytest.assert_eq(embedded_activity.id, embedded_activity_id)


def test__EmbeddedActivity__precreate__all_fields():
    """
    Tests whether ``EmbeddedActivity.precreate`` works as intended.
    
    Case: All fields given.
    """
    embedded_activity_id = 202408020004
    application_id = 202408020005
    guild_id = 202408020006
    launch_id = 202408020007
    location = EmbeddedActivityLocation(channel_id = 202408020008)
    user_states = [
         EmbeddedActivityUserState(user = User.precreate(202408020009)),
         EmbeddedActivityUserState(user = User.precreate(202408020010)),
    ]
    
    embedded_activity = EmbeddedActivity.precreate(
        embedded_activity_id,
        application_id = application_id,
        guild_id = guild_id,
        launch_id = launch_id,
        location = location,
        user_states = user_states,
    )
    _assert_fields_set(embedded_activity)
    
    vampytest.assert_eq(embedded_activity.id, embedded_activity_id)
    
    vampytest.assert_eq(embedded_activity.application_id, application_id)
    vampytest.assert_eq(embedded_activity.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity.launch_id, launch_id)
    vampytest.assert_eq(embedded_activity.location, location)
    vampytest.assert_eq(embedded_activity.user_states, {user_state.user_id: user_state for user_state in user_states})


def test__EmbeddedActivity__precreate__caching():
    """
    Tests whether ``EmbeddedActivity.precreate`` works as intended.
    
    Case: Caching.
    """
    embedded_activity_id = 202408020011
    
    embedded_activity_0 = EmbeddedActivity.precreate(embedded_activity_id)
    embedded_activity_1 = EmbeddedActivity.precreate(embedded_activity_id)
    
    vampytest.assert_instance(embedded_activity_0, EmbeddedActivity)
    vampytest.assert_is(embedded_activity_0, embedded_activity_1)
