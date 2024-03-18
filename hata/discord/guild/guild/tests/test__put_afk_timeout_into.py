import vampytest

from ..constants import AFK_TIMEOUT_DEFAULT
from ..fields import put_afk_timeout_into


def _iter_options():
    yield AFK_TIMEOUT_DEFAULT, False, {}
    yield AFK_TIMEOUT_DEFAULT, True, {'afk_timeout': AFK_TIMEOUT_DEFAULT}
    yield 60, False, {'afk_timeout': 60}
    yield 60, True, {'afk_timeout': 60}
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_afk_timeout_into(input_value, defaults):
    """
    Tests whether ``put_afk_timeout_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialize.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_afk_timeout_into(input_value, {}, defaults)
