import vampytest

from ..constants import DURATION_DEFAULT
from ..fields import put_duration


def _iter_options():
    yield DURATION_DEFAULT, False, {}
    yield DURATION_DEFAULT, True, {'duration': DURATION_DEFAULT}
    yield 3600, False, {'duration': 1}
    yield 3600, True, {'duration': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_duration(input_value, defaults):
    """
    Tests whether ``put_duration`` is working as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_duration(input_value, {}, defaults)
