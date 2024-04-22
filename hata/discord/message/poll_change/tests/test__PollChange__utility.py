import vampytest

from ....poll import Poll

from ..poll_change import PollChange

from ...poll_update import PollUpdate

from .test__PollChange__constructor import _assert_fields_set


def test__PollChange__copy():
    """
    Tests whether ``PollChange.copy`` works as intended.
    """
    added = Poll(duration = 3600)
    updated = PollUpdate(old_attributes = {'a': 'b'})
    removed = Poll(duration = 7200)
    
    poll_change = PollChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    
    copy = poll_change.copy()
    _assert_fields_set(poll_change)
    vampytest.assert_is_not(poll_change, copy)
    vampytest.assert_eq(poll_change, copy)


def test__PollChange__copy_with__no_fields():
    """
    Tests whether ``PollChange.copy_with`` works as intended.
    
    Case: No fields given.
    """
    added = Poll(duration = 3600)
    updated = PollUpdate(old_attributes = {'a': 'b'})
    removed = Poll(duration = 7200)
    
    poll_change = PollChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    
    copy = poll_change.copy_with()
    _assert_fields_set(poll_change)
    vampytest.assert_is_not(poll_change, copy)
    vampytest.assert_eq(poll_change, copy)



def test__PollChange__copy_with__all_fields():
    """
    Tests whether ``PollChange.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_added = Poll(duration = 3600)
    old_updated = PollUpdate(old_attributes = {'a': 'b'})
    old_removed = Poll(duration = 7200)
    
    new_added = Poll(duration = 10800)
    new_updated = PollUpdate(old_attributes = {'b': 'c'})
    new_removed = Poll(duration = 14400)
    
    poll_change = PollChange(
        added = old_added,
        updated = old_updated,
        removed = old_removed,
    )
    
    copy = poll_change.copy_with(
        added = new_added,
        updated = new_updated,
        removed = new_removed,
    )
    
    _assert_fields_set(poll_change)
    vampytest.assert_is_not(poll_change, copy)

    vampytest.assert_eq(copy.added, new_added)
    vampytest.assert_eq(copy.updated, new_updated)
    vampytest.assert_eq(copy.removed, new_removed)
