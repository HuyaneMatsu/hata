import vampytest

from ..fields import put_flags
from ..flags import ActivityFlag


def _iter_options():
    yield ActivityFlag(0), False, {}
    yield ActivityFlag(0), True, {'flags': 0}
    yield ActivityFlag(1), False, {'flags': 1}
    yield ActivityFlag(1), True, {'flags': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_flags(input_value, defaults):
    """
    Tests whether ``put_flags`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ActivityFlag``
        The value to serialise.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_flags(input_value, {}, defaults)
