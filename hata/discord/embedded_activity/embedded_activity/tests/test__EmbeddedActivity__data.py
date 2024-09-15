import vampytest

from ....client import Client
from ....guild import Guild
from ....user import User

from ...embedded_activity_location import EmbeddedActivityLocation
from ...embedded_activity_user_state import EmbeddedActivityUserState

from ..embedded_activity import EmbeddedActivity

from .test__EmbeddedActivity__constructor import _assert_fields_set


def test__EmbeddedActivity__from_data__new():
    """
    Tests whether ``EmbeddedActivity.from_data`` works as intended.
    
    Case: new.
    """
    embedded_activity_id = 202408020012
    application_id = 202408020013
    guild_id = 202408020014
    launch_id = 202408020015
    location = EmbeddedActivityLocation(channel_id = 202408020016)
    user_states = [
         EmbeddedActivityUserState(user = User.precreate(202408020016)),
         EmbeddedActivityUserState(user = User.precreate(202408020017)),
    ]
    
    data = {
        'instance_id': str(embedded_activity_id),
        'application_id': str(application_id),
        'guild_id': str(guild_id),
        'launch_id': str(launch_id),
        'location': location.to_data(),
        'participants': [user_state.to_data() for user_state in user_states],
    }
    
    embedded_activity = EmbeddedActivity.from_data(data)
    _assert_fields_set(embedded_activity)
    
    vampytest.assert_eq(embedded_activity.id, embedded_activity_id)
    
    vampytest.assert_eq(embedded_activity.application_id, application_id)
    vampytest.assert_eq(embedded_activity.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity.launch_id, launch_id)
    vampytest.assert_eq(embedded_activity.location, location)
    vampytest.assert_eq(embedded_activity.user_states, {user_state.user_id: user_state for user_state in user_states})


def test__EmbeddedActivity__from_data__cache():
    """
    Tests whether ``EmbeddedActivity.from_data`` works as intended.
    
    Case: cache.
    """
    embedded_activity_id = 202408020018
    user_states = [
         EmbeddedActivityUserState(user = User.precreate(202408020040)),
         EmbeddedActivityUserState(user = User.precreate(202408020041)),
    ]
    
    data = {
        'instance_id': str(embedded_activity_id),
        'participants': [user_state.to_data() for user_state in user_states],
    }

    embedded_activity_0 = EmbeddedActivity.from_data(data)
    embedded_activity_1 = EmbeddedActivity.from_data(data)
    
    vampytest.assert_instance(embedded_activity_0, EmbeddedActivity)
    vampytest.assert_is(embedded_activity_0, embedded_activity_1)


def test__EmbeddedActivity__from_data__exists_partial():
    """
    Tests whether ``EmbeddedActivity.from_data`` works as intended.
    
    Case: Exists | partial.
    """
    embedded_activity_id = 202408020019
    guild_id = 202408020020
    location = EmbeddedActivityLocation(channel_id = 202408020021)
    user_states = [
         EmbeddedActivityUserState(user = User.precreate(202408020042)),
         EmbeddedActivityUserState(user = User.precreate(202408020043)),
    ]
    
    embedded_activity_0 = EmbeddedActivity.precreate(embedded_activity_id)
    guild = Guild.precreate(guild_id)
    
    data = {
        'instance_id': str(embedded_activity_id),
        'guild_id': str(guild_id),
        'location': location.to_data(),
        'participants': [user_state.to_data() for user_state in user_states],
    }
    
    embedded_activity_1 = EmbeddedActivity.from_data(data)
    
    _assert_fields_set(embedded_activity_0)
    vampytest.assert_is(embedded_activity_0, embedded_activity_1)
    
    vampytest.assert_eq(embedded_activity_0.location, location)
    vampytest.assert_eq(guild.embedded_activities, {embedded_activity_0})


def test__EmbeddedActivity__from_data__exists_non_partial():
    """
    Tests whether ``EmbeddedActivity.from_data`` works as intended.
    
    Case: Exists | non partial.
    """
    embedded_activity_id = 202408020022
    guild_id = 202408020023
    location = EmbeddedActivityLocation(channel_id = 202408020024)
    client_id = 202408020025
    
    client = Client(
        token = 'token_' + str(client_id),
    )
    
    try:
        embedded_activity_0 = EmbeddedActivity.precreate(embedded_activity_id, guild_id = guild_id)
        guild = Guild.precreate(guild_id, embedded_activities = [embedded_activity_0])
        guild.clients.append(client)
        
        data = {
            'instance_id': str(embedded_activity_id),
            'guild_id': str(guild_id),
            'location': location.to_data()
        }
        
        embedded_activity_1 = EmbeddedActivity.from_data(data)
        
        _assert_fields_set(embedded_activity_0)
        vampytest.assert_is(embedded_activity_0, embedded_activity_1)
        
        vampytest.assert_ne(embedded_activity_0.location, location)
    
    # Cleanup
    finally:
        client._delete()
        client = None
    


def test__EmbeddedActivity__from_data__no_strong_cache():
    """
    Tests whether ``EmbeddedActivity.from_data`` works as intended.
    
    Case: `strong_cache` given as `False`.
    """
    embedded_activity_id = 202408020026
    guild_id = 202408020027
    location = EmbeddedActivityLocation(channel_id = 202408020028)
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'instance_id': str(embedded_activity_id),
        'location': location.to_data()
    }
    
    embedded_activity = EmbeddedActivity.from_data(data, guild_id)
    
    _assert_fields_set(embedded_activity)
    
    vampytest.assert_eq(embedded_activity.location, location)
    vampytest.assert_ne(guild.embedded_activities, {embedded_activity_id: embedded_activity})


def test__EmbeddedActivity__from_data_is_created__new():
    """
    Tests whether ``EmbeddedActivity.from_data_is_created`` works as intended.
    
    Case: New.
    """
    embedded_activity_id = 202408020029
    application_id = 202408020030
    guild_id = 202408020031
    launch_id = 202408020032
    location = EmbeddedActivityLocation(channel_id = 202408020033)
    user_states = [
         EmbeddedActivityUserState(user = User.precreate(202408020034)),
         EmbeddedActivityUserState(user = User.precreate(202408020035)),
    ]
    
    data = {
        'instance_id': str(embedded_activity_id),
        'application_id': str(application_id),
        'guild_id': str(guild_id),
        'launch_id': str(launch_id),
        'location': location.to_data(),
        'participants': [user_state.to_data() for user_state in user_states],
    }
    
    embedded_activity, created = EmbeddedActivity.from_data_is_created(data)
    _assert_fields_set(embedded_activity)
    
    vampytest.assert_eq(embedded_activity.id, embedded_activity_id)
    
    vampytest.assert_eq(embedded_activity.application_id, application_id)
    vampytest.assert_eq(embedded_activity.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity.launch_id, launch_id)
    vampytest.assert_eq(embedded_activity.location, location)
    vampytest.assert_eq(embedded_activity.user_states, {user_state.user_id: user_state for user_state in user_states})
    
    vampytest.assert_instance(created, bool)
    vampytest.assert_eq(created, True)


def test__EmbeddedActivity__from_data_is_created__cache():
    """
    Tests whether ``EmbeddedActivity.from_data_is_created`` works as intended.
    
    Case: cache.
    """
    embedded_activity_id = 202408020039
    user_states = [
         EmbeddedActivityUserState(user = User.precreate(202409040030)),
         EmbeddedActivityUserState(user = User.precreate(202409040031)),
    ]
    
    data = {
        'instance_id': str(embedded_activity_id),
        'participants': [user_state.to_data() for user_state in user_states],
    }

    embedded_activity_0, created = EmbeddedActivity.from_data_is_created(data)
    embedded_activity_1, created = EmbeddedActivity.from_data_is_created(data)
    
    vampytest.assert_instance(embedded_activity_0, EmbeddedActivity)
    vampytest.assert_is(embedded_activity_0, embedded_activity_1)


def test__EmbeddedActivity__from_data_is_created__exists_partial():
    """
    Tests whether ``EmbeddedActivity.from_data_is_created`` works as intended.
    
    Case: Exists, partial.
    """
    embedded_activity_id = 202408020036
    guild_id = 202408020037
    location = EmbeddedActivityLocation(channel_id = 202408020038)
    user_states = [
         EmbeddedActivityUserState(user = User.precreate(202409040032)),
         EmbeddedActivityUserState(user = User.precreate(202409040033)),
    ]
    
    embedded_activity_0 = EmbeddedActivity.precreate(embedded_activity_id)
    guild = Guild.precreate(guild_id)
    
    data = {
        'instance_id': str(embedded_activity_id),
        'guild_id': str(guild_id),
        'location': location.to_data(),
        'participants': [user_state.to_data() for user_state in user_states],
    }
    
    embedded_activity_1, created = EmbeddedActivity.from_data_is_created(data)
    
    _assert_fields_set(embedded_activity_0)
    vampytest.assert_is(embedded_activity_0, embedded_activity_1)
    
    vampytest.assert_eq(embedded_activity_0.location, location)
    vampytest.assert_eq(guild.embedded_activities, {embedded_activity_0})
    
    vampytest.assert_instance(created, bool)
    vampytest.assert_eq(created, True)


def test__EmbeddedActivity__from_data_is_created__exists_non_partial():
    """
    Tests whether ``EmbeddedActivity.from_data_is_created`` works as intended.
    
    Case: exists, non partial.
    """
    embedded_activity_id = 202408020040
    guild_id = 202408020041
    location = EmbeddedActivityLocation(channel_id = 202408020042)
    client_id = 202408020043
    
    client = Client(
        token = 'token_' + str(client_id),
    )
    
    try:
        embedded_activity_0 = EmbeddedActivity.precreate(embedded_activity_id, guild_id = guild_id)
        guild = Guild.precreate(guild_id, embedded_activities = [embedded_activity_0])
        guild.clients.append(client)
        
        data = {
            'instance_id': str(embedded_activity_id),
            'guild_id': str(guild_id),
            'location': location.to_data()
        }
        
        embedded_activity_1, created = EmbeddedActivity.from_data_is_created(data)
        _assert_fields_set(embedded_activity_0)
        vampytest.assert_is(embedded_activity_0, embedded_activity_1)
        
        vampytest.assert_ne(embedded_activity_0.location, location)
    
        vampytest.assert_instance(created, bool)
        vampytest.assert_eq(created, False)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__EmbeddedActivity__to_data():
    """
    Tests whether ``EmbeddedActivity.to_data`` works as intended.
    """
    embedded_activity_id = 202408020044
    application_id = 202408020045
    guild_id = 202408020046
    launch_id = 202408020047
    location = EmbeddedActivityLocation(channel_id = 202408020048)
    user_states = [
         EmbeddedActivityUserState(user = User.precreate(202408020049)),
         EmbeddedActivityUserState(user = User.precreate(202408020050)),
    ]
    
    embedded_activity = EmbeddedActivity.precreate(
        embedded_activity_id,
        application_id = application_id,
        guild_id = guild_id,
        launch_id = launch_id,
        location = location,
        user_states = user_states,
    )
    
    vampytest.assert_eq(
        embedded_activity.to_data(defaults = True, include_internals = True),
        {
            'instance_id': str(embedded_activity_id),
            'application_id': str(application_id),
            'guild_id': str(guild_id),
            'launch_id': str(launch_id),
            'location': location.to_data(defaults = True),
            'participants': [user_state.to_data(defaults = True) for user_state in user_states],
        },
    )


def test__EmbeddedActivity__update_user_states():
    """
    Tests whether ``EmbeddedActivity._update_user_states`` works as intended.
    """
    user_0 = User.precreate(202408020051)
    user_1 = User.precreate(202408020052)
    user_2 = User.precreate(202408020053)
    user_3 = User.precreate(202408020054)
    user_4 = User.precreate(202408020055)
    
    embedded_activity_id = 202408020056
    
    old_user_states = [
         EmbeddedActivityUserState(user = user_0),
         EmbeddedActivityUserState(user = user_1),
         EmbeddedActivityUserState(user = user_2),
    ]
    
    new_user_states = [
         EmbeddedActivityUserState(user = user_2),
         EmbeddedActivityUserState(user = user_3),
         EmbeddedActivityUserState(user = user_4),
    ]
    
    embedded_activity = EmbeddedActivity.precreate(
        embedded_activity_id,
        user_states = old_user_states,
    )
    
    embedded_activity._update_user_states({
        'participants': [user_state.to_data() for user_state in new_user_states],
    })
    
    vampytest.assert_eq(
        embedded_activity.user_states,
        {user_state.user_id: user_state for user_state in new_user_states},
    )
    

def test__EmbeddedActivity__difference_update_user_states():
    """
    Tests whether ``EmbeddedActivity._difference_update_user_states`` works as intended.
    """
    user_0 = User.precreate(202408020057)
    user_1 = User.precreate(202408020058)
    user_2 = User.precreate(202408020059)
    user_3 = User.precreate(202408020060)
    user_4 = User.precreate(202408020061)
    
    embedded_activity_id = 202408020062
    
    old_user_states = [
         EmbeddedActivityUserState(user = user_0),
         EmbeddedActivityUserState(user = user_1),
         EmbeddedActivityUserState(user = user_2),
    ]
    
    new_user_states = [
         EmbeddedActivityUserState(user = user_2),
         EmbeddedActivityUserState(user = user_3),
         EmbeddedActivityUserState(user = user_4),
    ]
    
    embedded_activity = EmbeddedActivity.precreate(
        embedded_activity_id,
        user_states = old_user_states,
    )
    
    output = embedded_activity._difference_update_user_states({
        'participants': [user_state.to_data() for user_state in new_user_states],
    })
    
    vampytest.assert_eq(
        embedded_activity.user_states,
        {user_state.user_id: user_state for user_state in new_user_states},
    )
    
    vampytest.assert_eq(
        output,
        (
            {
                user_3,
                user_4,
            },
            {
                user_0,
                user_1,
            },
        ),
    )


def test__EmbeddedActivity__set_attributes():
    """
    Tests whether ``EmbeddedActivity._set_attributes`` works as intended.
    """
    embedded_activity_id = 202408020043
    application_id = 202408020064
    guild_id = 202408020065
    launch_id = 202408020066
    location = EmbeddedActivityLocation(channel_id = 202408020067)
    user_states = [
         EmbeddedActivityUserState(user = User.precreate(202408020068)),
         EmbeddedActivityUserState(user = User.precreate(202408020069)),
    ]
    
    data = {
        'instance_id': str(embedded_activity_id),
        'application_id': str(application_id),
        'guild_id': str(guild_id),
        'launch_id': str(launch_id),
        'location': location.to_data(),
        'participants': [user_state.to_data() for user_state in user_states],
    }
    
    embedded_activity = EmbeddedActivity._create_empty(embedded_activity_id)
    embedded_activity._set_attributes(data, True, False)
    _assert_fields_set(embedded_activity)
    
    vampytest.assert_eq(embedded_activity.application_id, application_id)
    vampytest.assert_eq(embedded_activity.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity.launch_id, launch_id)
    vampytest.assert_eq(embedded_activity.location, location)
    vampytest.assert_eq(embedded_activity.user_states, {user_state.user_id: user_state for user_state in user_states})
