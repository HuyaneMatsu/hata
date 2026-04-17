import vampytest

from ..party import ActivityParty

from .test__ActivityParty__constructor import _assert_fields_set


def test__ActivityParty__copy():
    """
    Tests whether ``ActivityParty.copy`` works as intended.
    """
    party_id = 'plain'
    size = 6
    max_ = 12
    
    field = ActivityParty(
        party_id = party_id,
        size = size,
        max_ = max_,
    )
    copy = field.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__ActivityParty__copy_with__0():
    """
    Tests whether ``ActivityParty.copy_with`` works as intended.
    
    Case: No fields given.
    """
    party_id = 'plain'
    size = 6
    max_ = 12
    
    field = ActivityParty(
        party_id = party_id,
        size = size,
        max_ = max_,
    )
    copy = field.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__ActivityParty__copy_with__1():
    """
    Tests whether ``ActivityParty.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_party_id = 'plain'
    old_size = 6
    old_max = 12
    new_party_id = 'asia'
    new_size = 1
    new_max = 8
    
    field = ActivityParty(
        party_id = old_party_id,
        size = old_size,
        max_ = old_max,
    )
    copy = field.copy_with(
        party_id = new_party_id,
        size = new_size,
        max_ = new_max,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(copy.id, new_party_id)
    vampytest.assert_eq(copy.size, new_size)
    vampytest.assert_eq(copy.max, new_max)
