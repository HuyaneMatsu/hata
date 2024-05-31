import vampytest

from ..fields import put_flags_into
from ..flags import SKUFlag


def _iter_options():
    yield SKUFlag(0), False, {}
    yield SKUFlag(0), True, {'flags': 0}
    yield SKUFlag(1), False, {'flags': 1}
    yield SKUFlag(1), True, {'flags': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_flags_into(input_value, defaults):
    """
    Tests whether ``put_flags_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``SKUFlag``
        The value to serialise.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_flags_into(input_value, {}, defaults)
