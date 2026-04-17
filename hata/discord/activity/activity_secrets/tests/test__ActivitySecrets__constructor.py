import vampytest

from ..secrets import ActivitySecrets


def _assert_fields_set(field):
    """
    Asserts whether all fields are set of the given activity secret.
    
    Parameters
    ----------
    field : ``ActivitySecrets``
    """
    vampytest.assert_instance(field, ActivitySecrets)
    vampytest.assert_instance(field.join, str, nullable = True)
    vampytest.assert_instance(field.match, str, nullable = True)
    vampytest.assert_instance(field.spectate, str, nullable = True)


def test__ActivitySecrets__new__0():
    """
    Tests whether ``ActivitySecrets.__new__`` works as intended.
    
    Case: No fields given.
    """
    field = ActivitySecrets()
    _assert_fields_set(field)


def test__ActivitySecrets__new__1():
    """
    Tests whether ``ActivitySecrets.__new__`` works as intended.
    
    Case: All fields given.
    """
    join = 'plain'
    match = 'asia'
    spectate = 'senya'
    
    field = ActivitySecrets(
        join = join,
        match = match,
        spectate = spectate,
    )
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.join, join)
    vampytest.assert_eq(field.match, match)
    vampytest.assert_eq(field.spectate, spectate)
