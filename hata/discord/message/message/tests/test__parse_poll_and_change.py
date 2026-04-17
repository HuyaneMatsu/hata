from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....poll import Poll

from ...poll_change import PollChange
from ...poll_update import PollUpdate

from ..fields import parse_poll_and_change


def _iter_options():
    poll_0 = Poll(expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    poll_1 = Poll(expires_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc))
    
    yield {}, None, (None, None)
    yield {'poll': None}, None, (None, None)
    yield {'poll': poll_0.to_data(include_internals = True)}, poll_0, (poll_0, None)
    yield (
        {'poll': poll_0.to_data(include_internals = True)}, None,
        (poll_0, PollChange.from_fields(poll_0, None, None)),
    )
    yield (
        {'poll': poll_0.to_data(include_internals = True)}, poll_1,
        (poll_0, PollChange.from_fields(None, PollUpdate.from_fields(poll_0, {'expires_at': poll_1.expires_at}), None)),
    )
    yield (
        {'poll': None}, poll_1,
        (None, PollChange.from_fields(None, None, poll_1)),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_poll_and_change(input_data, old_poll):
    """
    Tests whether ``parse_poll_and_change`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    old_poll : `None | Poll`
        Old poll.
    
    Returns
    -------
    output : `(None | Poll, None | PollChange)`
    """
    if (old_poll is not None):
        old_poll = old_poll.copy()
    
    return parse_poll_and_change(input_data, old_poll)
