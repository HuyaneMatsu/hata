import vampytest

from ....poll import Poll

from ..poll_update import PollUpdate


def _assert_fields_set(poll_update):
    """
    Tests whether all fields are set of the given poll update.
    
    Parameters
    ----------
    poll_update : ``PollUpdate``
        The poll update to check.
    """
    vampytest.assert_instance(poll_update, PollUpdate)
    vampytest.assert_instance(poll_update.poll, Poll)
    vampytest.assert_instance(poll_update.old_attributes, dict)


def test__PollUpdate__new__no_fields():
    """
    Tests whether ``PollUpdate.__new__`` works as intended.
    
    Case: No fields given.
    """
    poll_update = PollUpdate()
    _assert_fields_set(poll_update)


def test__PollUpdate__new__all_fields():
    """
    Tests whether ``PollUpdate.__new__`` works as intended.
    
    Case: All fields given.
    """
    poll = Poll(duration = 3600)
    old_attributes = {'a': 'b'}
    
    poll_update = PollUpdate(
        old_attributes = old_attributes,
        poll = poll,
    )
    _assert_fields_set(poll_update)

    vampytest.assert_eq(poll_update.poll, poll)
    vampytest.assert_eq(poll_update.old_attributes, old_attributes)


def test__PollUpdate__from_fields():
    """
    Tests whether ``PollUpdate.__new__`` works as intended.
    
    Case: All fields given.
    """
    poll = Poll(duration = 3600)
    old_attributes = {'a': 'b'}
    
    poll_update = PollUpdate.from_fields(poll, old_attributes)
    _assert_fields_set(poll_update)

    vampytest.assert_eq(poll_update.poll, poll)
    vampytest.assert_eq(poll_update.old_attributes, old_attributes)
