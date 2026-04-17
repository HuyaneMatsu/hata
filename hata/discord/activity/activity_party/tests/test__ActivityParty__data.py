import vampytest

from ..party import ActivityParty

from .test__ActivityParty__constructor import _assert_fields_set


def test__ActivityParty__from_data__0():
    """
    Tests whether ``ActivityParty.from_data`` works as intended.
    """
    party_id = 'plain'
    size = 6
    max_ = 12
    
    data = {
        'id': party_id,
        'size': [size, max_],
    }
    field = ActivityParty.from_data(data)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.id, party_id)
    vampytest.assert_eq(field.size, size)
    vampytest.assert_eq(field.max, max_)


def test__ActivityParty__to_data():
    """
    Tests whether ``ActivityParty.to_data`` works as intended.
    
    Case: Include defaults.
    """
    party_id = 'plain'
    size = 6
    max_ = 12
    
    field = ActivityParty(
        party_id = party_id,
        size = size,
        max_ = max_,
    )
    
    expected_data = {
        'id': party_id,
        'size': (size, max_),
    }
    
    vampytest.assert_eq(
        field.to_data(defaults = True),
        expected_data,
    )
