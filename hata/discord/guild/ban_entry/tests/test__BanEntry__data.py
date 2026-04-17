import vampytest

from ....user import User

from ..ban_entry import BanEntry


from .test__BanEntry__constructor import _assert_fields_set


def test__BanEntry__from_data():
    """
    Tests whether ``BanEntry.from_data`` works as intended.
    
    Case: all fields given.
    """
    reason = 'hey mister'
    user = User.precreate(202405010004, name = 'Yuuka')
    
    data = {
        'reason': reason,
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    ban_entry = BanEntry.from_data(data)
    _assert_fields_set(ban_entry)
    
    vampytest.assert_eq(ban_entry.reason, reason)
    vampytest.assert_is(ban_entry.user, user)


def test__BanEntry__to_data():
    """
    Tests whether ``BanEntry.to_data`` works as intended.
    
    Case: Include defaults.
    """
    reason = 'hes mister'
    user = User.precreate(202405010005, name = 'Yuuka')
    
    ban_entry = BanEntry(
        reason = reason,
        user = user,
    )
    expected_output = {
        'reason': reason,
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    vampytest.assert_eq(
        ban_entry.to_data(defaults = True),
        expected_output,
    )
