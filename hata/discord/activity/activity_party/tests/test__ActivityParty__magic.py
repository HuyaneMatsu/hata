import vampytest

from ..party import ActivityParty


def test__ActivityParty__repr():
    """
    Tests whether ``ActivityParty.__repr__`` works as intended.
    """
    field = ActivityParty(
        party_id = 'plain',
        size = 6,
        max_ = 12,
    )
    
    vampytest.assert_instance(repr(field), str)


def test__ActivityParty__eq():
    """
    Tests whether ``ActivityParty.__repr__`` works as intended.
    """
    fields = {
        'party_id': 'plain',
        'size': 6,
        'max_': 12,
    }
    
    field_original = ActivityParty(**fields)
    
    vampytest.assert_eq(field_original, field_original)
    
    for field_name, field_value in (
        ('party_id', 'trance'),
        ('size', 0),
        ('max_', 0),
    ):
        field_altered = ActivityParty(**{**fields, field_name: field_value})
        vampytest.assert_ne(field_original, field_altered)


def test__ActivityParty__hash():
    """
    Tests whether ``ActivityParty.__hash__`` works as intended.
    """
    field = ActivityParty(
        party_id = 'plain',
        size = 6,
        max_ = 12,
    )
    
    vampytest.assert_instance(hash(field), int)


def test__ActivityParty__bool():
    """
    Tests whether ``ActivityParty.__bool__`` works as intended.
    """
    field = ActivityParty()
    
    field_bool = bool(field)
    vampytest.assert_instance(field_bool, bool)
    vampytest.assert_false(field_bool)
    
    
    for field_name, field_value in (
        ('party_id', 'trance'),
        ('size', 6),
        ('max_', 12),
    ):
        field = ActivityParty(**{field_name: field_value})
        
        field_bool = bool(field)
        vampytest.assert_instance(field_bool, bool)
        vampytest.assert_true(field_bool)
