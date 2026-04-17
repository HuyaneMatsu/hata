import vampytest

from ....client import Client
from ....guild import Guild
from ....user import User

from ...embedded_activity_location import EmbeddedActivityLocation, EmbeddedActivityLocationType
from ...embedded_activity_user_state import EmbeddedActivityUserState

from ..utils import handle_embedded_activity_update_event


def test__handle_embedded_activity_update_event__new():
    """
    Tests whether ``handle_embedded_activity_update_event`` works as intended.
    
    Case: new.
    """
    client_id = 202409040022
    application_id = 202408020149
    embedded_activity_id = 202408020150
    launch_id = 202408020151
    guild_id = 202408020152
    channel_id = 202408020153
    location = EmbeddedActivityLocation(
        channel_id = channel_id,
        guild_id = guild_id,
        location_type = EmbeddedActivityLocationType.guild_channel,
    )
    user_states = [
        EmbeddedActivityUserState(user = User.precreate(202408020154)),
        EmbeddedActivityUserState(user = User.precreate(202408020155)),
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
        
        handle_embedded_activity_update_event(data)
        
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
    finally:
        client._delete()
        client = None


def test__handle_embedded_activity_update_event__update():
    """
    Tests whether ``handle_embedded_activity_update_event`` works as intended.
    
    Case: update.
    """
    client_id = 202409040021
    application_id = 202408020156
    embedded_activity_id = 202408020157
    launch_id = 202408020158
    guild_id = 202408020159
    channel_id = 202408020160
    location = EmbeddedActivityLocation(
        channel_id = channel_id,
        guild_id = guild_id,
        location_type = EmbeddedActivityLocationType.guild_channel,
    )
    user_id_left = 202408020161
    user_id_stood = 202408020162
    user_id_joined = 202408020163
    
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
        
        handle_embedded_activity_update_event(old_data)
        
        embedded_activity = next(iter(guild.embedded_activities))
        
        handle_embedded_activity_update_event(new_data)
        
        vampytest.assert_eq(embedded_activity.id, embedded_activity_id)
        
        vampytest.assert_eq(embedded_activity.application_id, application_id)
        vampytest.assert_eq(embedded_activity.guild_id, guild_id)
        vampytest.assert_eq(embedded_activity.launch_id, launch_id)
        vampytest.assert_eq(embedded_activity.location, location)
        vampytest.assert_eq(
            embedded_activity.user_states,
            {user_state.user_id: user_state for user_state in new_user_states},
        )
    finally:
        client._delete()
        client = None


def test__handle_embedded_activity_update_event__leave():
    """
    Tests whether ``handle_embedded_activity_update_event`` works as intended.
    
    Case: leave.
    """
    client_id = 202409040020
    application_id = 202408020164
    embedded_activity_id = 202408020165
    launch_id = 202408020166
    guild_id = 202408020167
    channel_id = 202408020168
    location = EmbeddedActivityLocation(
        channel_id = channel_id,
        guild_id = guild_id,
        location_type = EmbeddedActivityLocationType.guild_channel,
    )
    user_id_left = 202408020169
    
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
        
        handle_embedded_activity_update_event(old_data)
        
        embedded_activity = next(iter(guild.embedded_activities))
        
        handle_embedded_activity_update_event(new_data)
        
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
    finally:
        client._delete()
        client = None
