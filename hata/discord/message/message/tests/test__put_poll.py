from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....poll import Poll

from ..fields import put_poll


def _iter_options():
    poll = Poll(expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    
    yield None, False, False, {}
    yield None, True, False, {'poll': None}
    yield poll, False, False, {'poll': poll.to_data(defaults = False, include_internals = False)}
    yield poll, True, False, {'poll': poll.to_data(defaults = True, include_internals = False)}
    yield None, False, True, {}
    yield None, True, True, {'poll': None}
    yield poll, False, True, {'poll': poll.to_data(defaults = False, include_internals = True)}
    yield poll, True, True, {'poll': poll.to_data(defaults = True, include_internals = True)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_poll(input_value, defaults, include_internals):
    """
    Tests whether ``put_poll`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | Poll`
        Interaction to serialize.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    include_internals : `bool`
        Whether internal fields should be also included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_poll(input_value, {}, defaults, include_internals = include_internals)
