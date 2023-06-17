import vampytest

from ....activity import Activity, ActivityType

from ...guild import Guild

from ..utils import handle_embedded_activity_update_event


def test__handle_embedded_activity_update_event__0():
    """
    Tests whether ``handle_embedded_activity_update_event`` works as intended.
    
    Case: new.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212270000)
    channel_id = 202212270001
    guild_id = 202212270002
    user_ids = [202212270003, 202212270004]
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'embedded_activity': activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'users': [str(user_id) for user_id in user_ids],
    }
    
    handle_embedded_activity_update_event(data)
    
    embedded_activity_state = next(iter(guild.embedded_activity_states))
    
    vampytest.assert_eq(embedded_activity_state.activity, activity)
    vampytest.assert_eq(embedded_activity_state.channel_id, channel_id)
    vampytest.assert_eq(embedded_activity_state.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity_state.user_ids, set(user_ids))


def test__handle_embedded_activity_update_event__1():
    """
    Tests whether ``handle_embedded_activity_update_event`` works as intended.
    
    Case: update.
    """
    old_activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212270005)
    old_user_ids = [202212270006, 202212270007]
    new_activity = Activity('shiki', activity_type = ActivityType.competing, application_id = 202212270005)
    new_user_ids = [202212270007, 202212270008]
    
    channel_id = 202212270008
    guild_id = 202212270009
    
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
    
    handle_embedded_activity_update_event(old_data)
    
    embedded_activity_state = next(iter(guild.embedded_activity_states))
    
    handle_embedded_activity_update_event(new_data)
    
    vampytest.assert_eq(embedded_activity_state.activity, new_activity)
    vampytest.assert_eq(embedded_activity_state.channel_id, channel_id)
    vampytest.assert_eq(embedded_activity_state.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity_state.user_ids, set(new_user_ids))
