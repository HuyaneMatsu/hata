import vampytest

from ....client import Client
from ....guild import Guild
from ....user import User

from ...embedded_activity_location import EmbeddedActivityLocation, EmbeddedActivityLocationType
from ...embedded_activity_user_state import EmbeddedActivityUserState

from ..constants import (
    EMBEDDED_ACTIVITY_UPDATE_CREATE, EMBEDDED_ACTIVITY_UPDATE_DELETE, EMBEDDED_ACTIVITY_UPDATE_USER_ADD,
    EMBEDDED_ACTIVITY_UPDATE_USER_DELETE
)
from ..utils import difference_handle_embedded_activity_update_event


def test__difference_handle_embedded_activity_update_event__new():
    """
    Tests whether ``difference_handle_embedded_activity_update_event`` works as intended.
    
    Case: new.
    """
    client_id = 202409040023
    application_id = 202408020128
    embedded_activity_id = 202408020129
    launch_id = 202408020130
    guild_id = 202408020131
    channel_id = 202408020132
    location = EmbeddedActivityLocation(
        channel_id = channel_id,
        guild_id = guild_id,
        location_type = EmbeddedActivityLocationType.guild_channel,
    )
    user_states = [
        EmbeddedActivityUserState(user = User.precreate(202408020133)),
        EmbeddedActivityUserState(user = User.precreate(202408020134)),
    ]
    guild = Guild.precreate(guild_id)
    
    data = {
        'application_id':str(application_id),
        'instance_id': str(embedded_activity_id),
        'launch_id': str(launch_id),
        'guild_id': str(guild_id),
        'location': location.to_data(),
        'participants': [user_state.to_data() for user_state in user_states], 
    }
    
    client = Client(
        'token_' + str(client_id),
    )
    try:
        guild.clients.append(client)
        
        state, changes = difference_handle_embedded_activity_update_event(data)
        
        embedded_activity = next(iter(guild.embedded_activities))
        
        vampytest.assert_eq(embedded_activity.id, embedded_activity_id)
        
        vampytest.assert_eq(embedded_activity.application_id, application_id)
        vampytest.assert_eq(embedded_activity.guild_id, guild_id)
        vampytest.assert_eq(embedded_activity.launch_id, launch_id)
        vampytest.assert_eq(embedded_activity.location, location)
        vampytest.assert_eq(
            embedded_activity.user_states,
            {user_state.user_id: user_state for user_state in user_states},
        )
        
        vampytest.assert_eq(
            sorted(changes),
            sorted([
                (EMBEDDED_ACTIVITY_UPDATE_CREATE, None),
            ]),
        )
    finally:
        client._delete()
        client = None
        

def test__difference_handle_embedded_activity_update_event__update():
    """
    Tests whether ``difference_handle_embedded_activity_update_event`` works as intended.
    
    Case: update.
    """
    client_id = 202409040024
    application_id = 202408020135
    embedded_activity_id = 202408020136
    launch_id = 202408020137
    guild_id = 202408020138
    channel_id = 202408020139
    location = EmbeddedActivityLocation(
        channel_id = channel_id,
        guild_id = guild_id,
        location_type = EmbeddedActivityLocationType.guild_channel,
    )
    user_id_left = 202408020140
    user_id_stood = 202408020141
    user_id_joined = 202408020142
    
    user_left = User.precreate(user_id_left)
    user_stood = User.precreate(user_id_stood)
    user_joined = User.precreate(user_id_joined)
    
    old_user_states = [
        EmbeddedActivityUserState(user = user_left),
        EmbeddedActivityUserState(user = user_stood),
    ]
    new_user_states = [
        EmbeddedActivityUserState(user = user_joined),
        EmbeddedActivityUserState(user = user_stood),
    ]
    
    guild = Guild.precreate(guild_id)
    
    old_data = {
        'application_id':str(application_id),
        'instance_id': str(embedded_activity_id),
        'launch_id': str(launch_id),
        'guild_id': str(guild_id),
        'location': location.to_data(),
        'participants': [user_state.to_data() for user_state in old_user_states], 
    }
    
    new_data = {
        'application_id':str(application_id),
        'instance_id': str(embedded_activity_id),
        'launch_id': str(launch_id),
        'guild_id': str(guild_id),
        'location': location.to_data(),
        'participants': [user_state.to_data() for user_state in new_user_states], 
    }
    
    client = Client(
        'token_' + str(client_id),
    )
    try:
        guild.clients.append(client)
    
        difference_handle_embedded_activity_update_event(old_data)
        
        embedded_activity = next(iter(guild.embedded_activities))
        
        state, changes = difference_handle_embedded_activity_update_event(new_data)
        
        vampytest.assert_eq(embedded_activity.id, embedded_activity_id)
        
        vampytest.assert_eq(embedded_activity.application_id, application_id)
        vampytest.assert_eq(embedded_activity.guild_id, guild_id)
        vampytest.assert_eq(embedded_activity.launch_id, launch_id)
        vampytest.assert_eq(embedded_activity.location, location)
        vampytest.assert_eq(
            embedded_activity.user_states,
            {user_state.user_id: user_state for user_state in new_user_states},
        )
        
        vampytest.assert_eq(
            sorted(changes),
            sorted([
                (EMBEDDED_ACTIVITY_UPDATE_USER_ADD, user_joined),
                (EMBEDDED_ACTIVITY_UPDATE_USER_DELETE, user_left),
            ]),
        )
    finally:
        client._delete()
        client = None


def test__difference_handle_embedded_activity_update_event__leave():
    """
    Tests whether ``difference_handle_embedded_activity_update_event`` works as intended.
    
    Case: leave.
    """
    client_id = 202409040025
    application_id = 202408020143
    embedded_activity_id = 202408020144
    launch_id = 202408020145
    guild_id = 202408020146
    channel_id = 202408020147
    location = EmbeddedActivityLocation(
        channel_id = channel_id,
        guild_id = guild_id,
        location_type = EmbeddedActivityLocationType.guild_channel,
    )
    user_id_left = 202408020148
    
    user_left = User.precreate(user_id_left)
    
    old_user_states = [
        EmbeddedActivityUserState(user = user_left),
    ]
    new_user_states = []
    
    guild = Guild.precreate(guild_id)
    
    old_data = {
        'application_id':str(application_id),
        'instance_id': str(embedded_activity_id),
        'launch_id': str(launch_id),
        'guild_id': str(guild_id),
        'location': location.to_data(),
        'participants': [user_state.to_data() for user_state in old_user_states], 
    }
    
    new_data = {
        'application_id':str(application_id),
        'instance_id': str(embedded_activity_id),
        'launch_id': str(launch_id),
        'guild_id': str(guild_id),
        'location': location.to_data(),
        'participants': [user_state.to_data() for user_state in new_user_states], 
    }
    
    client = Client(
        'token_' + str(client_id),
    )
    try:
        guild.clients.append(client)
        
        difference_handle_embedded_activity_update_event(old_data)
        
        embedded_activity = next(iter(guild.embedded_activities))
        
        state, changes = difference_handle_embedded_activity_update_event(new_data)
        
        vampytest.assert_eq(guild.embedded_activities, None)
        
        vampytest.assert_eq(embedded_activity.id, embedded_activity_id)
        
        vampytest.assert_eq(embedded_activity.application_id, application_id)
        vampytest.assert_eq(embedded_activity.guild_id, guild_id)
        vampytest.assert_eq(embedded_activity.launch_id, launch_id)
        vampytest.assert_eq(embedded_activity.location, location)
        vampytest.assert_eq(
            embedded_activity.user_states,
            {user_state.user_id: user_state for user_state in new_user_states},
        )
        
        vampytest.assert_eq(
            sorted(changes),
            sorted([
                (EMBEDDED_ACTIVITY_UPDATE_USER_DELETE, user_left),
                (EMBEDDED_ACTIVITY_UPDATE_DELETE, None),
            ]),
        )
    finally:
        client._delete()
        client = None
