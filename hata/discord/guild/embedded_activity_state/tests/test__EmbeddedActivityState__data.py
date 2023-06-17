import vampytest

from ....activity import Activity, ActivityType

from ...guild import Guild

from ..embedded_activity_state import EmbeddedActivityState

from .test__EmbeddedActivityState__constructor import _assert_fields_set


def test__EmbeddedActivityState__from_data__0():
    """
    Tests whether ``EmbeddedActivityState.from_data`` works as intended.
    
    Case: Default.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260049)
    channel_id = 202212260045
    guild_id = 202212260046
    user_ids = [202212260047, 202212260048]
    
    data = {
        'embedded_activity': activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'users': [str(user_id) for user_id in user_ids],
    }
    
    embedded_activity_state = EmbeddedActivityState.from_data(data)
    _assert_fields_set(embedded_activity_state)
    
    vampytest.assert_eq(embedded_activity_state.activity, activity)
    vampytest.assert_eq(embedded_activity_state.channel_id, channel_id)
    vampytest.assert_eq(embedded_activity_state.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity_state.user_ids, set(user_ids))


def test__EmbeddedActivityState__from_data__1():
    """
    Tests whether ``EmbeddedActivityState.from_data`` works as intended.
    
    Case: Guild id as parameter.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260066)
    channel_id = 202212260067
    guild_id = 202212260068
    user_ids = [202212260069, 202212260070]
    
    data = {
        'embedded_activity': activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'users': [str(user_id) for user_id in user_ids],
    }
    
    embedded_activity_state = EmbeddedActivityState.from_data(data, guild_id)
    _assert_fields_set(embedded_activity_state)
    
    vampytest.assert_eq(embedded_activity_state.activity, activity)
    vampytest.assert_eq(embedded_activity_state.channel_id, channel_id)
    vampytest.assert_eq(embedded_activity_state.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity_state.user_ids, set(user_ids))



def test__EmbeddedActivityState__from_data__2():
    """
    Tests whether ``EmbeddedActivityState.from_data`` works as intended.
    
    Case: Caching.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260051)
    channel_id = 202212260052
    guild_id = 202212260053
    user_ids = [202212260054, 202212260055]
    
    data = {
        'embedded_activity': activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'users': [str(user_id) for user_id in user_ids],
    }
    
    guild = Guild.precreate(guild_id)
    
    embedded_activity_state = EmbeddedActivityState.from_data(data)
    test_embedded_activity_state = EmbeddedActivityState.from_data(data)
    
    vampytest.assert_is(embedded_activity_state, test_embedded_activity_state)
    vampytest.assert_eq(guild.embedded_activity_states, {embedded_activity_state})


def test__EmbeddedActivityState__from_data__3():
    """
    Tests whether ``EmbeddedActivityState.from_data`` works as intended.
    
    Case: Caching, `strong_cache` given as `False`.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202306160010)
    channel_id = 202306160011
    guild_id = 202306160012
    user_ids = [202306160013, 202306160014]
    
    data = {
        'embedded_activity': activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'users': [str(user_id) for user_id in user_ids],
    }
    
    guild = Guild.precreate(guild_id)
    
    embedded_activity_state = EmbeddedActivityState.from_data(data, strong_cache = False)
    
    vampytest.assert_eq(guild.embedded_activity_states, None)


def test__EmbeddedActivityState__from_data_is_created__0():
    """
    Tests whether ``EmbeddedActivityState.from_data_is_created`` works as intended.
    
    Case: Default.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260056)
    channel_id = 202212260057
    guild_id = 202212260058
    user_ids = [202212260059, 202212260060]
    
    data = {
        'embedded_activity': activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'users': [str(user_id) for user_id in user_ids],
    }
    
    embedded_activity_state, is_created = EmbeddedActivityState.from_data_is_created(data)
    _assert_fields_set(embedded_activity_state)
    vampytest.assert_instance(is_created, bool)
    
    vampytest.assert_eq(embedded_activity_state.activity, activity)
    vampytest.assert_eq(embedded_activity_state.channel_id, channel_id)
    vampytest.assert_eq(embedded_activity_state.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity_state.user_ids, set(user_ids))


def test__EmbeddedActivityState__from_data_is_created__1():
    """
    Tests whether ``EmbeddedActivityState.from_data_is_created`` works as intended.
    
    Case: Default.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260071)
    channel_id = 202212260072
    guild_id = 202212260073
    user_ids = [202212260074, 202212260075]
    
    data = {
        'embedded_activity': activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'users': [str(user_id) for user_id in user_ids],
    }
    
    embedded_activity_state, is_created = EmbeddedActivityState.from_data_is_created(data, guild_id)
    _assert_fields_set(embedded_activity_state)
    vampytest.assert_instance(is_created, bool)
    
    vampytest.assert_eq(embedded_activity_state.activity, activity)
    vampytest.assert_eq(embedded_activity_state.channel_id, channel_id)
    vampytest.assert_eq(embedded_activity_state.guild_id, guild_id)
    vampytest.assert_eq(embedded_activity_state.user_ids, set(user_ids))


def test__EmbeddedActivityState__from_data_is_created__2():
    """
    Tests whether ``EmbeddedActivityState.from_data_is_created`` works as intended.
    
    Case: Caching.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260061)
    channel_id = 202212260062
    guild_id = 202212260063
    user_ids = [202212260064, 202212260065]
    
    data = {
        'embedded_activity': activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'users': [str(user_id) for user_id in user_ids],
    }
    
    guild = Guild.precreate(guild_id)
    
    embedded_activity_state, is_created = EmbeddedActivityState.from_data_is_created(data)
    test_embedded_activity_state, test_is_created = EmbeddedActivityState.from_data_is_created(data)
    
    vampytest.assert_is(embedded_activity_state, test_embedded_activity_state)
    vampytest.assert_eq(guild.embedded_activity_states, {embedded_activity_state})
    vampytest.assert_eq(is_created, True)
    vampytest.assert_eq(test_is_created, False)


def test__EmbeddedActivityState__to_data():
    """
    Tests whether ``EmbeddedActivityState.to_data`` works as intended.
    
    Case: Caching.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260076)
    channel_id = 202212260077
    guild_id = 202212260078
    user_ids = [202212260079, 2022122600780]
    
    expected_output = {
        'embedded_activity': activity.to_data(include_internals = True, user = True),
        'channel_id': str(channel_id),
        'guild_id': str(guild_id),
        'users': {str(user_id) for user_id in user_ids},
    }
    
    embedded_activity_state = EmbeddedActivityState(
        activity = activity,
        channel_id = channel_id,
        guild_id = guild_id,
        user_ids = user_ids,
    )
    
    data = embedded_activity_state.to_data(defaults = True)
    data['users'] = set(data['users']) # pain
    
    vampytest.assert_eq(
        data,
        expected_output,
    )


def test__EmbeddedActivityState__update_user_ids():
    """
    Tests whether ``EmbeddedActivityState._update_user_ids`` works as intended.
    """
    old_user_ids = [202212260127, 202212260128]
    new_user_ids = [202212260128, 202212260129]
    
    embedded_activity_state = EmbeddedActivityState(
        user_ids = old_user_ids,
    )
    
    data = {'users': [str(user_id) for user_id in new_user_ids]}
    embedded_activity_state._update_user_ids(data)
    vampytest.assert_eq(embedded_activity_state.user_ids, set(new_user_ids))
    

def test__EmbeddedActivityState__difference_update_user_ids():
    """
    Tests whether ``EmbeddedActivityState._update_user_ids`` works as intended.
    """
    user_id_left = 202212260130
    user_id_stood = 202212260131
    user_id_joined = 202212260132
    old_user_ids = [user_id_left, user_id_stood]
    new_user_ids = [user_id_stood, user_id_joined]
    
    embedded_activity_state = EmbeddedActivityState(
        user_ids = old_user_ids,
    )
    
    data = {'users': [str(user_id) for user_id in new_user_ids]}
    joined_user_ids, left_user_ids = embedded_activity_state._difference_update_user_ids(data)
    vampytest.assert_eq(embedded_activity_state.user_ids, set(new_user_ids))
    vampytest.assert_eq(joined_user_ids, {user_id_joined})
    vampytest.assert_eq(left_user_ids, {user_id_left})


def test__EmbeddedActivityState__update_activity():
    """
    Tests whether ``EmbeddedActivityState._update_activity`` works as intended.
    """
    old_activity = Activity('tsuki', activity_type = ActivityType.competing)
    new_activity = Activity('shiki', activity_type = ActivityType.game)
    
    embedded_activity_state = EmbeddedActivityState(
        activity = old_activity,
    )
    
    data = {'embedded_activity': new_activity.to_data(include_internals = True, user = True)}
    embedded_activity_state._update_activity(data)
    vampytest.assert_eq(embedded_activity_state.activity, new_activity)


def test__EmbeddedActivityState__difference_update_activity():
    """
    Tests whether ``EmbeddedActivityState._difference_update_activity`` works as intended.
    """
    old_activity = Activity('tsuki', activity_type = ActivityType.competing)
    new_activity = Activity('shiki', activity_type = ActivityType.game)
    
    embedded_activity_state = EmbeddedActivityState(
        activity = old_activity,
    )
    
    data = {'embedded_activity': new_activity.to_data(include_internals = True, user = True)}
    old_attributes = embedded_activity_state._difference_update_activity(data)
    vampytest.assert_eq(embedded_activity_state.activity, new_activity)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'name': 'tsuki',
            'type': ActivityType.competing,
        }
    )
