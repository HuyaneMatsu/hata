import vampytest

from .. import ActivityParty


def test__ActivityParty__from_data__0():
    """
    Tests whether ``ActivityParty.from_data`` works as intended.
    
    Case: all fields given.
    """
    id_ = 'plain'
    size = 6
    max_ = 12
    
    field = ActivityParty.from_data({
        'id': id_,
        'size': [size, max_],
    })
    
    vampytest.assert_eq(field.id, id_)
    vampytest.assert_eq(field.size, size)
    vampytest.assert_eq(field.max, max_)


def test__ActivityParty__from_data__1():
    """
    Tests whether ``ActivityParty.from_data`` works as intended.
    
    Case: no fields given.
    """
    field = ActivityParty.from_data({})
    
    vampytest.assert_is(field.id, None)
    vampytest.assert_eq(field.size, 0)
    vampytest.assert_eq(field.max, 0)


def test__ActivityParty__to_data__0():
    """
    Tests whether ``ActivityParty.to_data`` works as intended.
    
    Case: all fields set.
    """
    party_id = 'plain'
    size = 6
    max_ = 12
    
    field = ActivityParty(
        party_id = party_id,
        size = size,
        max_ = max_,
    )
    
    data = field.to_data()
    
    vampytest.assert_in('id', data)
    vampytest.assert_in('size', data)
    
    vampytest.assert_eq(data['id'], party_id)
    vampytest.assert_eq(data['size'], [size, max_])


def test__ActivityParty__to_data__1():
    """
    Tests whether ``ActivityParty.to_data`` works as intended.
    
    Case: no fields set.
    """
    field = ActivityParty()
    data = field.to_data()
    
    vampytest.assert_not_in('id', data)
    vampytest.assert_not_in('size', data)
    vampytest.assert_not_in('max', data)
