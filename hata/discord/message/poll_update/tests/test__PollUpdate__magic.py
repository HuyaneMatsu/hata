import vampytest

from ....poll import Poll

from ..poll_update import PollUpdate


def test__PollUpdate__repr():
    """
    Tests whether ``PollUpdate.__repr__`` works as intended.
    """
    poll = Poll(duration = 3600)
    old_attributes = {'a': 'b'}
    
    poll_update = PollUpdate(
        poll = poll,
        old_attributes = old_attributes,
    )
    vampytest.assert_instance(repr(poll_update), str)


def test__PollUpdate__hash():
    """
    Tests whether ``PollUpdate.__hash__`` works as intended.
    """
    poll = Poll(duration = 3600)
    old_attributes = {'a': 'b'}
    
    poll_update = PollUpdate(
        poll = poll,
        old_attributes = old_attributes,
    )
    vampytest.assert_instance(hash(poll_update), int)


def test__PollUpdate__eq():
    """
    Tests whether ``PollUpdate.__eq__`` works as intended.
    """
    poll = Poll(duration = 3600)
    old_attributes = {'a': 'b'}
    
    keyword_parameters = {    
        'poll': poll,
        'old_attributes': old_attributes,
    }
    
    poll_update = PollUpdate(**keyword_parameters)
    vampytest.assert_eq(poll_update, poll_update)
    vampytest.assert_ne(poll_update, object())
    
    for field_name, field_value in (
        ('poll',  Poll(duration = 7200)),
        ('old_attributes', {'everyone': 'lies'}),
    ):
        test_poll_update = PollUpdate(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(poll_update, test_poll_update)


def test__PollUpdate__unpack():
    """
    Tests whether ``PollUpdate`` unpacking works as intended.
    """
    poll = Poll(duration = 3600)
    old_attributes = {'a': 'b'}
    
    poll_update = PollUpdate(
        poll = poll,
        old_attributes = old_attributes,
    )
    
    unpacked = [*poll_update]
    vampytest.assert_eq(len(unpacked), len(poll_update))
