import vampytest

from ..fields import put_palette
from ..preinstanced import Palette


def _iter_options():
    yield Palette.violet, False, {'palette': Palette.violet.value}
    yield Palette.violet, True, {'palette': Palette.violet.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_palette(input_value, defaults):
    """
    Tests whether ``put_palette`` is working as intended.
    
    Parameters
    ----------
    input_value : ``Palette``
        Input value.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_palette(input_value, {}, defaults)
