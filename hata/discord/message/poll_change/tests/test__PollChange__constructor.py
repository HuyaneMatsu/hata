import vampytest

from ....poll import Poll

from ...poll_update import PollUpdate

from ..poll_change import PollChange


def _assert_fields_set(poll_change):
    """
    Tests whether all fields are set of the given poll change.
    
    Parameters
    ----------
    poll_change : ``PollChange``
        The poll change to check.
    """
    vampytest.assert_instance(poll_change, PollChange)
    vampytest.assert_instance(poll_change.added, Poll, nullable = True)
    vampytest.assert_instance(poll_change.updated, PollUpdate, nullable = True)
    vampytest.assert_instance(poll_change.removed, Poll, nullable = True)


def test__PollChange__new__no_fields():
    """
    Tests whether ``PollChange.__new__`` works as intended.
    
    Case: No fields given.
    """
    poll_change = PollChange()
    _assert_fields_set(poll_change)


def test__PollChange__new__all_fields():
    """
    Tests whether ``PollChange.__new__`` works as intended.
    
    Case: All fields given.
    """
    added = Poll(duration = 3600)
    updated = PollUpdate(old_attributes = {'a': 'b'})
    removed = Poll(duration = 7200)
    
    poll_change = PollChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    _assert_fields_set(poll_change)

    vampytest.assert_eq(poll_change.added, added)
    vampytest.assert_eq(poll_change.updated, updated)
    vampytest.assert_eq(poll_change.removed, removed)


def test__PollChange__from_fields():
    """
    Tests whether ``PollChange.__new__`` works as intended.
    
    Case: All fields given.
    """
    added = Poll(duration = 3600)
    updated = PollUpdate(old_attributes = {'a': 'b'})
    removed = Poll(duration = 7200)
    
    poll_change = PollChange.from_fields(added, updated, removed)
    _assert_fields_set(poll_change)

    vampytest.assert_eq(poll_change.added, added)
    vampytest.assert_eq(poll_change.updated, updated)
    vampytest.assert_eq(poll_change.removed, removed)
