import vampytest

from ..secrets import ActivitySecrets

from .test__ActivitySecrets__constructor import _assert_fields_set


def test__ActivitySecrets__copy():
    """
    Tests whether ``ActivitySecrets.copy`` works as intended.
    """
    join = 'plain'
    match = 'asia'
    spectate = 'senya'
    
    field = ActivitySecrets(
        join = join,
        match = match,
        spectate = spectate,
    )
    
    copy = field.copy()
    _assert_fields_set(field)
    vampytest.assert_is_not(copy, field)
    
    vampytest.assert_eq(field, copy)


def test__ActivitySecrets__copy_with__0():
    """
    Tests whether ``ActivitySecrets.copy_with`` works as intended.
    
    Case: No fields given.
    """
    join = 'plain'
    match = 'asia'
    spectate = 'senya'
    
    field = ActivitySecrets(
        join = join,
        match = match,
        spectate = spectate,
    )
    
    copy = field.copy_with()
    _assert_fields_set(field)
    vampytest.assert_is_not(copy, field)
    
    vampytest.assert_eq(field, copy)


def test__ActivitySecrets__copy_with__1():
    """
    Tests whether ``ActivitySecrets.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_join = 'plain'
    old_match = 'asia'
    old_spectate = 'senya'
    new_join = 'important'
    new_match = 'lie'
    new_spectate = 'chata'
    
    field = ActivitySecrets(
        join = old_join,
        match = old_match,
        spectate = old_spectate,
    )
    
    copy = field.copy_with(
        join = new_join,
        match = new_match,
        spectate = new_spectate,
    )
    _assert_fields_set(field)
    vampytest.assert_is_not(copy, field)
    
    vampytest.assert_eq(copy.join, new_join)
    vampytest.assert_eq(copy.match, new_match)
    vampytest.assert_eq(copy.spectate, new_spectate)
