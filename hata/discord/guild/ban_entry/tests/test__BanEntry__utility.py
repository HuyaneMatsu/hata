import vampytest

from ....user import User

from ..ban_entry import BanEntry

from .test__BanEntry__constructor import _assert_fields_set


def test__BanEntry__copy():
    """
    Tests whether ``BanEntry.copy`` works as intended.
    """
    reason = 'hey mister'
    user = User.precreate(202405010010, name = 'Yuuka')
    
    ban_entry = BanEntry(
        reason = reason,
        user = user,
    )
    
    copy = ban_entry.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(ban_entry, copy)

    vampytest.assert_eq(ban_entry, copy)


def test__BanEntry__copy_with__no_fields():
    """
    Tests whether ``BanEntry.copy_with`` works as intended.
    
    Case: no fields given.
    """
    reason = 'hey mister'
    user = User.precreate(202405010011, name = 'Yuuka')
    
    ban_entry = BanEntry(
        reason = reason,
        user = user,
    )
    
    copy = ban_entry.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(ban_entry, copy)

    vampytest.assert_eq(ban_entry, copy)


def test__BanEntry__copy_with__all_fields():
    """
    Tests whether ``BanEntry.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_reason = 'hey mister'
    old_user = User.precreate(202405010012, name = 'Yuuka')
    
    new_reason = 'hey sister'
    new_user = User.precreate(202405010013, name = 'Yuuma')
    
    ban_entry = BanEntry(
        reason = old_reason,
        user = old_user,
    )
    
    copy = ban_entry.copy_with(
        reason = new_reason,
        user = new_user,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(ban_entry, copy)
    
    vampytest.assert_eq(copy.reason, new_reason)
    vampytest.assert_is(copy.user, new_user)
