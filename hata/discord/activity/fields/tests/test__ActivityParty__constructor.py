import vampytest

from .. import ActivityParty


def test__ActivityParty__new__0():
    """
    Tests whether ``ActivityParty.__new__`` defaults empty values to `None` and whether it also sets the fields to the
    correct type.
    """
    field = ActivityParty(
        party_id = '',
    )
    
    vampytest.assert_is(field.id, None)
    vampytest.assert_instance(field.size, int)
    vampytest.assert_instance(field.max, int)


def test__ActivityParty__new__1():
    """
    Tests whether ``ActivityParty.__new__`` sets string values as expected.
    """
    party_id = 'plain'
    size = 6
    max_ = 12
    
    field = ActivityParty(
        party_id = party_id,
        size = size,
        max_ = max_,
    )
    
    vampytest.assert_eq(field.id, party_id)
    vampytest.assert_eq(field.size, size)
    vampytest.assert_eq(field.max, max_)
