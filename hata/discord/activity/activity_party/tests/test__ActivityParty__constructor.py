import vampytest

from ..party import ActivityParty


def _assert_fields_set(field):
    """
    Asserts whether every fields are set of the given activity party instance.
    
    Parameters
    ----------
    field : ``ActivityParty``
        Activity party field.
    """
    vampytest.assert_instance(field, ActivityParty)
    vampytest.assert_instance(field.id, str, nullable = True)
    vampytest.assert_instance(field.size, int)
    vampytest.assert_instance(field.max, int)


def test__ActivityParty__new__0():
    """
    Tests whether ``ActivityParty.__new__`` works as intended.
    
    Case: No fields given.
    """
    field = ActivityParty()
    _assert_fields_set(field)


def test__ActivityParty__new__1():
    """
    Tests whether ``ActivityParty.__new__`` works as intended.
    
    Case: All fields given.
    """
    party_id = 'plain'
    size = 6
    max_ = 12
    
    field = ActivityParty(
        party_id = party_id,
        size = size,
        max_ = max_,
    )
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.id, party_id)
    vampytest.assert_eq(field.size, size)
    vampytest.assert_eq(field.max, max_)
