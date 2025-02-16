import vampytest

from ..fields import put_overlay_method_flags
from ..flags import ApplicationOverlayMethodFlags


def _iter_options():
    yield ApplicationOverlayMethodFlags(0), False, {}
    yield ApplicationOverlayMethodFlags(0), True, {'overlay_methods': 0}
    yield ApplicationOverlayMethodFlags(1), False, {'overlay_methods': 1}
    yield ApplicationOverlayMethodFlags(1), True, {'overlay_methods': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_overlay_method_flags(input_value, defaults):
    """
    Tests whether ``put_overlay_method_flags`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationOverlayMethodFlags``
        The value to serialise.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_overlay_method_flags(input_value, {}, defaults)
