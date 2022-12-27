import vampytest

from ....activity import Activity, ActivityType

from ...guild import Guild

from ..constants import (
    EMBEDDED_ACTIVITY_UPDATE_CREATE, EMBEDDED_ACTIVITY_UPDATE_DELETE, EMBEDDED_ACTIVITY_UPDATE_UPDATE,
    EMBEDDED_ACTIVITY_UPDATE_USER_ADD, EMBEDDED_ACTIVITY_UPDATE_USER_DELETE
)
from ..utils import difference_handle_embedded_activity_update_event


def test__difference_handle_embedded_activity_update_event__0():
    """
    Tests whether ``difference_handle_embedded_activity_update_event`` works as intended.
    
    Case: new.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212270010)
    channel_id = 202212270011
    guild_id = 202212270012
    user_ids = [202212270013, 202212270014]
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'embedded_activity': activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'users': [str(user_id) for user_id in user_ids],
    }
    
    state, changes = difference_handle_embedded_activity_update_event(data)
    
    embedded_activity_state = next(iter(guild._embedded_activity_states))
    
    vampytest.assert_is(state, embedded_activity_state)
    vampytest.assert_eq(embedded_activity_state.activity, activity)
    vampytest.assert_eq(embedded_activity_state.channel_id, channel_id)
    vampytest.assert_eq(embedded_activity_state.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity_state.user_ids, set(user_ids))
    
    vampytest.assert_eq(
        sorted(changes),
        sorted([
            (EMBEDDED_ACTIVITY_UPDATE_CREATE, None),
        ]),
    )
        

def test__difference_handle_embedded_activity_update_event__1():
    """
    Tests whether ``difference_handle_embedded_activity_update_event`` works as intended.
    
    Case: update.
    """
    user_id_left = 202212270016
    user_id_stood = 202212270017
    user_id_joined = 202212270018
    
    old_activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212270015)
    old_user_ids = [user_id_left, user_id_stood]
    new_activity = Activity('shiki', activity_type = ActivityType.competing, application_id = 202212270015)
    new_user_ids = [user_id_stood, user_id_joined]
    
    channel_id = 202212270018
    guild_id = 2022122700019
    
    guild = Guild.precreate(guild_id)
    
    old_data = {
        'embedded_activity': old_activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'users': [str(user_id) for user_id in old_user_ids],
    }
    
    new_data = {
        'embedded_activity': new_activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'users': [str(user_id) for user_id in new_user_ids],
    }
    
    difference_handle_embedded_activity_update_event(old_data)
    
    embedded_activity_state = next(iter(guild._embedded_activity_states))
    
    state, changes = difference_handle_embedded_activity_update_event(new_data)
    
    vampytest.assert_is(state, embedded_activity_state)
    vampytest.assert_eq(embedded_activity_state.activity, new_activity)
    vampytest.assert_eq(embedded_activity_state.channel_id, channel_id)
    vampytest.assert_eq(embedded_activity_state.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity_state.user_ids, set(new_user_ids))
    
    vampytest.assert_eq(
        sorted(changes),
        sorted([
            (EMBEDDED_ACTIVITY_UPDATE_USER_ADD, user_id_joined),
            (EMBEDDED_ACTIVITY_UPDATE_USER_DELETE, user_id_left),
            (EMBEDDED_ACTIVITY_UPDATE_UPDATE, {'name': 'tsuki'}),
        ]),
    )


def test__difference_handle_embedded_activity_update_event__2():
    """
    Tests whether ``difference_handle_embedded_activity_update_event`` works as intended.
    
    Case: update.
    """
    user_id_left = 202212270020
    
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212270021)
    old_user_ids = [user_id_left]
    new_user_ids = []
    
    channel_id = 202212270022
    guild_id = 2022122700023
    
    guild = Guild.precreate(guild_id)
    
    old_data = {
        'embedded_activity': activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'users': [str(user_id) for user_id in old_user_ids],
    }
    
    new_data = {
        'embedded_activity': activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'users': [str(user_id) for user_id in new_user_ids],
    }
    
    difference_handle_embedded_activity_update_event(old_data)
    
    embedded_activity_state = next(iter(guild._embedded_activity_states))
    
    state, changes = difference_handle_embedded_activity_update_event(new_data)
    
    vampytest.assert_is(state, embedded_activity_state)
    vampytest.assert_eq(embedded_activity_state.activity, activity)
    vampytest.assert_eq(embedded_activity_state.channel_id, channel_id)
    vampytest.assert_eq(embedded_activity_state.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity_state.user_ids, set(new_user_ids))
    
    vampytest.assert_eq(
        sorted(changes),
        sorted([
            (EMBEDDED_ACTIVITY_UPDATE_USER_DELETE, user_id_left),
            (EMBEDDED_ACTIVITY_UPDATE_DELETE, None),
        ]),
    )
