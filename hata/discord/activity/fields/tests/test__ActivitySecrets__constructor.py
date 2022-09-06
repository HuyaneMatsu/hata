import vampytest

from .. import ActivitySecrets


def test__ActivitySecrets__new__0():
    """
    Tests whether ``ActivitySecrets.__new__`` defaults empty values to `None`.
    """
    field = ActivitySecrets(
        join = '',
        match = '',
        spectate = '',
    )
    
    vampytest.assert_is(field.join, None)
    vampytest.assert_is(field.match, None)
    vampytest.assert_is(field.spectate, None)


def test__ActivitySecrets__new__1():
    """
    Tests whether ``ActivitySecrets.__new__`` sets string values as expected.
    """
    join = 'plain'
    match = 'asia'
    spectate = 'senya'
    
    field = ActivitySecrets(
        join = join,
        match = match,
        spectate = spectate,
    )
    
    vampytest.assert_eq(field.join, join)
    vampytest.assert_eq(field.match, match)
    vampytest.assert_eq(field.spectate, spectate)
