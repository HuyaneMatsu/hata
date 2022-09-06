import vampytest

from .. import ActivitySecrets


def test__ActivitySecrets__from_data__0():
    """
    Tests whether ``ActivitySecrets.from_data`` works as intended.
    
    Case: all fields given.
    """
    join = 'plain'
    match = 'asia'
    spectate = 'senya'
    
    field = ActivitySecrets.from_data({
        'join': join,
        'match': match,
        'spectate': spectate,
    })
    
    vampytest.assert_eq(field.join, join)
    vampytest.assert_eq(field.match, match)
    vampytest.assert_eq(field.spectate, spectate)


def test__ActivitySecrets__from_data__1():
    """
    Tests whether ``ActivitySecrets.from_data`` works as intended.
    
    Case: no fields given.
    """
    field = ActivitySecrets.from_data({})
    
    vampytest.assert_is(field.join, None)
    vampytest.assert_is(field.match, None)
    vampytest.assert_is(field.spectate, None)


def test__ActivitySecrets__to_data__0():
    """
    Tests whether ``ActivitySecrets.to_data`` works as intended.
    
    Case: all fields set.
    """
    join = 'plain'
    match = 'asia'
    spectate = 'senya'
    
    field = ActivitySecrets(
        join = join,
        match = match,
        spectate = spectate,
    )
    
    data = field.to_data()
    
    vampytest.assert_in('join', data)
    vampytest.assert_in('match', data)
    vampytest.assert_in('spectate', data)
    
    vampytest.assert_eq(data['join'], join)
    vampytest.assert_eq(data['match'], match)
    vampytest.assert_eq(data['spectate'], spectate)


def test__ActivitySecrets__to_data__1():
    """
    Tests whether ``ActivitySecrets.to_data`` works as intended.
    
    Case: no fields set.
    """
    field = ActivitySecrets()
    data = field.to_data()
    
    vampytest.assert_not_in('join', data)
    vampytest.assert_not_in('match', data)
    vampytest.assert_not_in('spectate', data)
