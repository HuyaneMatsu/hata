import vampytest

from ..secrets import ActivitySecrets

from .test__ActivitySecrets__constructor import _assert_fields_set


def test__ActivitySecrets__from_data__0():
    """
    Tests whether ``ActivitySecrets.from_data`` works as intended.
    """
    join = 'plain'
    match = 'asia'
    spectate = 'senya'
    
    data = {
        'join': join,
        'match': match,
        'spectate': spectate,
    }
    
    field = ActivitySecrets.from_data(data)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.join, join)
    vampytest.assert_eq(field.match, match)
    vampytest.assert_eq(field.spectate, spectate)


def test__ActivitySecrets__to_data__0():
    """
    Tests whether ``ActivitySecrets.to_data`` works as intended.
    
    Case: include defaults.
    """
    join = 'plain'
    match = 'asia'
    spectate = 'senya'
    
    field = ActivitySecrets(
        join = join,
        match = match,
        spectate = spectate,
    )
    
    expected_output = {
        'join': join,
        'match': match,
        'spectate': spectate,
    }
    
    vampytest.assert_eq(
        field.to_data(defaults = True),
        expected_output,
    )
