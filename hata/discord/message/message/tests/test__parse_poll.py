from datetime import datetime as DateTime

import vampytest

from ....poll import Poll

from ..fields import parse_poll


def _iter_options():
    poll_0 = Poll(expires_at = DateTime(2016, 5, 14))
    poll_1 = Poll(expires_at = DateTime(2016, 5, 15))
    
    yield {}, None, None
    yield {'poll': None}, None, None
    yield {'poll': poll_0.to_data(include_internals = True)}, poll_0, poll_0
    yield {'poll': poll_0.to_data(include_internals = True)}, None, poll_0
    yield {'poll': poll_0.to_data(include_internals = True)}, poll_1, poll_0
    yield {'poll': None}, poll_1, None


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_poll(input_data, old_poll):
    """
    Tests whether ``parse_poll`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    old_poll : `None | Poll`
        Old poll.
    
    Returns
    -------
    output : `None | Poll`
    """
    if (old_poll is not None):
        old_poll = old_poll.copy()
    
    return parse_poll(input_data, old_poll)
