import vampytest

from .. import Activity, ActivityType


def test__Activity__from_data():
    """
    Tests whether ``Activity.from_data`` works as expected.
    """
    state = 'Hollow'
    
    for activity_type in ActivityType.INSTANCES.values():
        if (activity_type is ActivityType.unknown):
            continue
        
        data = {
            'type': activity_type.value,
            'state': state,
        }
        
        activity = Activity.from_data(data)
        
        vampytest.assert_instance(activity, Activity)
        vampytest.assert_is(activity.type, activity_type)
        vampytest.assert_eq(activity.state, state)


def test__Activity__to_data():
    """
    Tests whether ``Activity.to_data`` works as expected.
    """
    name = 'ZYTOKINE'
    activity_type = ActivityType.game
    url = 'https://www.astil.dev/'
    state = 'Hollow'
    session_id = 'Ensemble'
    
    activity = Activity(name, type_ = activity_type, session_id = session_id, state = state, url = url)
    
    data = activity.to_data()
    
    vampytest.assert_in('name', data)
    vampytest.assert_in('type', data)
    vampytest.assert_in('url', data)
    
    vampytest.assert_eq(data['name'], name)
    vampytest.assert_eq(data['type'], activity_type.value)
    vampytest.assert_eq(data['url'], url)


def test__Activity__to_data__user():
    """
    Tests whether `Activity.to_data(user = True)` works as expected.
    """
    name = 'ZYTOKINE'
    activity_type = ActivityType.game
    url = 'https://www.astil.dev/'
    state = 'Hollow'
    session_id = 'Ensemble'
    
    activity = Activity(name, type_ = activity_type, session_id = session_id, state = state, url = url)
    
    data = activity.to_data(user = True)
    
    vampytest.assert_in('name', data)
    vampytest.assert_in('type', data)
    vampytest.assert_in('url', data)
    vampytest.assert_in('state', data)
    
    vampytest.assert_eq(data['name'], name)
    vampytest.assert_eq(data['type'], activity_type.value)
    vampytest.assert_eq(data['url'], url)
    vampytest.assert_eq(data['state'], state)


def test__Activity__to_data__include_internals():
    """
    Tests whether `Activity.to_data(include_internals = True)` works as expected.
    """
    name = 'ZYTOKINE'
    activity_type = ActivityType.game
    url = 'https://www.astil.dev/'
    state = 'Hollow'
    session_id = 'Ensemble'
    
    activity = Activity(name, type_ = activity_type, session_id = session_id, state = state, url = url)
    
    data = activity.to_data(include_internals = True)
    
    vampytest.assert_in('name', data)
    vampytest.assert_in('type', data)
    vampytest.assert_in('url', data)
    vampytest.assert_in('state', data)
    vampytest.assert_in('session_id', data)
    
    vampytest.assert_eq(data['name'], name)
    vampytest.assert_eq(data['type'], activity_type.value)
    vampytest.assert_eq(data['url'], url)
    vampytest.assert_eq(data['state'], state)
    vampytest.assert_eq(data['session_id'], session_id)


def test__Activity__update_attributes():
    """
    Tests whether ``Activity._update_attributes`` works as expected.
    """
    old_name = 'ZYTOKINE'
    new_name = 'Linjin'
    activity_type = ActivityType.game
    old_url = 'https://www.astil.dev/'
    new_url = 'https://www.astil.dev/project/hata/'
    old_state = 'Hollow'
    new_state = 'NEXT'
    old_session_id = 'Ensemble'
    new_session_id = 'LIFE'
    
    activity = Activity(old_name, type_ = activity_type, session_id = old_session_id, state = old_state, url = old_url)
    
    activity._update_attributes({
        'name': new_name,
        'url': new_url,
        'state': new_state,
        'session_id': new_session_id,
    })
    
    vampytest.assert_eq(activity.name, new_name)
    vampytest.assert_eq(activity.url, new_url)
    vampytest.assert_eq(activity.state, new_state)
    vampytest.assert_eq(activity.session_id, new_session_id)


def test__Activity__difference_update_attributes():
    """
    Tests whether ``Activity._difference_update_attributes`` works as expected.
    """
    old_name = 'ZYTOKINE'
    new_name = 'Linjin'
    activity_type = ActivityType.game
    old_url = 'https://www.astil.dev/'
    new_url = 'https://www.astil.dev/project/hata/'
    old_state = 'Hollow'
    new_state = 'NEXT'
    old_session_id = 'Ensemble'
    new_session_id = 'LIFE'
    
    activity = Activity(old_name, type_ = activity_type, session_id = old_session_id, state = old_state, url = old_url)
    
    old_attributes = activity._difference_update_attributes({
        'name': new_name,
        'url': new_url,
        'state': new_state,
        'session_id': new_session_id,
    })
    
    vampytest.assert_eq(activity.name, new_name)
    vampytest.assert_eq(activity.url, new_url)
    vampytest.assert_eq(activity.state, new_state)
    vampytest.assert_eq(activity.session_id, new_session_id)

    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('url', old_attributes)
    vampytest.assert_in('state', old_attributes)
    vampytest.assert_in('session_id', old_attributes)
    
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(old_attributes['url'], old_url)
    vampytest.assert_eq(old_attributes['state'], old_state)
    vampytest.assert_eq(old_attributes['session_id'], old_session_id)
