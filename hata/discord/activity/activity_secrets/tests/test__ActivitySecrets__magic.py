import vampytest

from .. import ActivitySecrets


def test__ActivitySecrets__repr():
    """
    Tests whether ``ActivitySecrets.__repr__`` works as intended.
    """
    field = ActivitySecrets(
        join = 'plain',
        match = 'asia',
        spectate = 'senya',
    )
    
    vampytest.assert_instance(repr(field), str)


def test__ActivitySecrets__eq():
    """
    Tests whether ``ActivitySecrets.__repr__`` works as intended.
    """
    fields = {
        'join': 'plain',
        'match': 'asia',
        'spectate': 'senya',
    }
    
    field_original = ActivitySecrets(**fields)
    
    vampytest.assert_eq(field_original, field_original)
    
    for field_name in (
        'join',
        'match',
        'spectate',
    ):
        field_altered = ActivitySecrets(**{**fields, field_name: None})
        vampytest.assert_ne(field_original, field_altered)


def test__ActivitySecrets__hash():
    """
    Tests whether ``ActivitySecrets.__hash__`` works as intended.
    """
    field = ActivitySecrets(
        join = 'plain',
        match = 'asia',
        spectate = 'senya',
    )
    
    vampytest.assert_instance(hash(field), int)


def test__ActivitySecrets__bool():
    """
    Tests whether ``ActivitySecrets.__bool__`` works as intended.
    """
    field = ActivitySecrets()
    
    field_bool = bool(field)
    vampytest.assert_instance(field_bool, bool)
    vampytest.assert_false(field_bool)
    
    
    for field_name in (
        'join',
        'match',
        'spectate',
    ):
        field = ActivitySecrets(**{field_name: 'trance'})
        
        field_bool = bool(field)
        vampytest.assert_instance(field_bool, bool)
        vampytest.assert_true(field_bool)
