import vampytest

from ....poll import Poll

from ...poll_update import PollUpdate

from ..poll_change import PollChange


def test__PollChange__repr():
    """
    Tests whether ``PollChange.__repr__`` works as intended.
    """
    added = Poll(duration = 3600)
    updated = PollUpdate(old_attributes = {'a': 'b'})
    removed = Poll(duration = 7200)
    
    poll_change = PollChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    vampytest.assert_instance(repr(poll_change), str)


def test__PollChange__hash():
    """
    Tests whether ``PollChange.__hash__`` works as intended.
    """
    added = Poll(duration = 3600)
    updated = PollUpdate(old_attributes = {'a': 'b'})
    removed = Poll(duration = 7200)
    
    poll_change = PollChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    vampytest.assert_instance(hash(poll_change), int)


def test__PollChange__eq():
    """
    Tests whether ``PollChange.__eq__`` works as intended.
    """
    added = Poll(duration = 3600)
    updated = PollUpdate(old_attributes = {'a': 'b'})
    removed = Poll(duration = 7200)
    
    keyword_parameters = {    
        'added': added,
        'updated': updated,
        'removed': removed,
    }
    
    poll_change = PollChange(**keyword_parameters)
    vampytest.assert_eq(poll_change, poll_change)
    vampytest.assert_ne(poll_change, object())
    
    for field_name, field_value in (
        ('added',  None),
        ('updated', None),
        ('removed', None),
    ):
        test_poll_change = PollChange(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(poll_change, test_poll_change)


def test__PollChange__unpack():
    """
    Tests whether ``PollChange`` unpacking works as intended.
    """
    added = Poll(duration = 3600)
    updated = PollUpdate(old_attributes = {'a': 'b'})
    removed = Poll(duration = 7200)
    
    poll_change = PollChange(
        added = added,
        updated = updated,
        removed = removed,
    )
    
    unpacked = [*poll_change]
    vampytest.assert_eq(len(unpacked), len(poll_change))
