import vampytest

from ..fields import parse_palette
from ..preinstanced import Palette


def _iter_options():
    yield {}, Palette.black
    yield {'palette': Palette.violet.value}, Palette.violet


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_palette(input_data):
    """
    Tests whether ``parse_palette`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``Palette``
    """
    output = parse_palette(input_data)
    vampytest.assert_instance(output, Palette)
    return output
