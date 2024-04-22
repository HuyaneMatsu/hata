import vampytest

from ....poll import Poll

from ..poll_update import PollUpdate

from .test__PollUpdate__constructor import _assert_fields_set


def test__PollUpdate__copy():
    """
    Tests whether ``PollUpdate.copy`` works as intended.
    """
    poll = Poll(duration = 3600)
    old_attributes = {'a': 'b'}
    
    poll_update = PollUpdate(
        poll = poll,
        old_attributes = old_attributes,
    )
    
    copy = poll_update.copy()
    _assert_fields_set(poll_update)
    vampytest.assert_is_not(poll_update, copy)
    vampytest.assert_eq(poll_update, copy)


def test__PollUpdate__copy_with_no_fields():
    """
    Tests whether ``PollUpdate.copy_with`` works as intended.
    
    Case: No fields given.
    """
    poll = Poll(duration = 3600)
    old_attributes = {'a': 'b'}
    
    poll_update = PollUpdate(
        poll = poll,
        old_attributes = old_attributes,
    )
    
    copy = poll_update.copy_with()
    _assert_fields_set(poll_update)
    vampytest.assert_is_not(poll_update, copy)
    vampytest.assert_eq(poll_update, copy)



def test__PollUpdate__copy_with__all_fields():
    """
    Tests whether ``PollUpdate.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_poll = Poll(duration = 3600)
    old_old_attributes = {'a': 'b'}
    
    new_poll = Poll(duration = 7200)
    new_old_attributes = {'b': 'c'}
    
    poll_update = PollUpdate(
        poll = old_poll,
        old_attributes = old_old_attributes,
    )
    
    copy = poll_update.copy_with(
        poll = new_poll,
        old_attributes = new_old_attributes,
    )
    
    _assert_fields_set(poll_update)
    vampytest.assert_is_not(poll_update, copy)

    vampytest.assert_eq(copy.poll, new_poll)
    vampytest.assert_eq(copy.old_attributes, new_old_attributes)
