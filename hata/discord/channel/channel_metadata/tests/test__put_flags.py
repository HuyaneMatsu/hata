import vampytest

from ..fields import put_flags
from ..flags import ChannelFlag


def _iter_options():
    yield ChannelFlag(0), False, {}
    yield ChannelFlag(0), True, {'flags': 0}
    yield ChannelFlag(1), False, {'flags': 1}
    yield ChannelFlag(1), True, {'flags': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_flags(input_value, defaults):
    """
    Tests whether ``put_flags`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ChannelFlag``
        The value to serialise.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_flags(input_value, {}, defaults)
