import vampytest

from ..constants import BUTTON_STYLE_DEFAULT
from ..fields import parse_button_style
from ..preinstanced import ButtonStyle


def _iter_options():
    yield {}, BUTTON_STYLE_DEFAULT
    yield {'style':BUTTON_STYLE_DEFAULT.value}, BUTTON_STYLE_DEFAULT
    yield {'style': ButtonStyle.link.value}, ButtonStyle.link


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_button_style(input_data):
    """
    Tests whether ``parse_button_style`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``ButtonStyle``
    """
    output = parse_button_style(input_data)
    vampytest.assert_instance(output, ButtonStyle)
    return output
