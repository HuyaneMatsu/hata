from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_timestamp

from ..fields import put_direct_message_spam_detected_at_into


def _iter_options():
    until = DateTime(2016, 5, 14)
    
    yield None, False, {}
    yield None, True, {'dm_spam_detected_at': None}
    yield until, False, {'dm_spam_detected_at': datetime_to_timestamp(until)}
    yield until, True, {'dm_spam_detected_at': datetime_to_timestamp(until)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_direct_message_spam_detected_at_into(input_value, defaults):
    """
    Tests whether ``put_direct_message_spam_detected_at_into`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_direct_message_spam_detected_at_into(input_value, {}, defaults)
