import vampytest

from ..fields import parse_overlay_method_flags
from ..flags import ApplicationOverlayMethodFlags


def _iter_options():
    yield {}, ApplicationOverlayMethodFlags(0)
    yield {'overlay_methods': None}, ApplicationOverlayMethodFlags(0)
    yield {'overlay_methods': 1}, ApplicationOverlayMethodFlags(1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_overlay_method_flags(input_data):
    """
    Tests whether ``parse_overlay_method_flags`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the overlay_method_flags from.
    
    Returns
    -------
    output : ``ApplicationOverlayMethodFlags``
    """
    output = parse_overlay_method_flags(input_data)
    vampytest.assert_instance(output, ApplicationOverlayMethodFlags)
    return output
