import vampytest

from ..constants import DURATION_DEFAULT
from ..fields import put_duration


def _iter_options():
    yield DURATION_DEFAULT, False, {}
    yield DURATION_DEFAULT, True, {'duration_secs': DURATION_DEFAULT}
    yield 1.0, False, {'duration_secs': 1.0}
    yield 1.0, True, {'duration_secs': 1.0}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_duration(input_value, defaults):
    """
    Tests whether ``put_duration`` is working as intended.
    
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
    return put_duration(input_value, {}, defaults)
