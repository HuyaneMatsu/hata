import vampytest

from ..fields import validate_font
from ..preinstanced import NameStyleFont


def _iter_options__passing():
    yield None, NameStyleFont.default
    yield NameStyleFont.sakura, NameStyleFont.sakura
    yield NameStyleFont.sakura.value, NameStyleFont.sakura


def _iter_options__font_error():
    yield 12.6
    yield 'a'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__font_error()).raising(TypeError))
def test__validate_font(input_value):
    """
    Tests whether ``validate_font`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``NameStyleFont``
    
    Raises
    ------
    TypeError
    """
    output = validate_font(input_value)
    vampytest.assert_instance(output, NameStyleFont)
    return output
