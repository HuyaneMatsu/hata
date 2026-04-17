import vampytest

from ..fields import validate_palette
from ..preinstanced import Palette


def _iter_options__passing():
    yield None, Palette.black
    yield Palette.violet, Palette.violet
    yield Palette.violet.value, Palette.violet


def _iter_options__palette_error():
    yield 12.6
    yield 0


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__palette_error()).raising(TypeError))
def test__validate_palette(input_value):
    """
    Tests whether ``validate_palette`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``Palette``
    
    Raises
    ------
    TypeError
    """
    output = validate_palette(input_value)
    vampytest.assert_instance(output, Palette)
    return output
