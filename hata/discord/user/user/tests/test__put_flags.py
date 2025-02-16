import vampytest

from ..fields import put_flags
from ..flags import UserFlag


def _iter_options():
    yield UserFlag(0), False, {'public_flags': 0}
    yield UserFlag(0), True, {'public_flags': 0}
    yield UserFlag(1), False, {'public_flags': 1}
    yield UserFlag(1), True, {'public_flags': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_flags(input_value, defaults):
    """
    Tests whether ``put_flags`` is working as intended.
    
    Parameters
    ----------
    input_value : ``UserFlag``
        The value to serialise.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_flags(input_value, {}, defaults)
