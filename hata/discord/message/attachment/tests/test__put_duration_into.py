import vampytest

from ..constants import DURATION_DEFAULT
from ..fields import put_duration_into


def _iter_options():
    yield DURATION_DEFAULT, False, {}
    yield DURATION_DEFAULT, True, {'duration_sec': DURATION_DEFAULT}
    yield 1.0, False, {'duration_sec': 1.0}
    yield 1.0, True, {'duration_sec': 1.0}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_duration_into(input_value, defaults):
    """
    Tests whether ``put_duration_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `float`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_duration_into(input_value, {}, defaults)
