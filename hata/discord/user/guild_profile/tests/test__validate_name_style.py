import vampytest

from ...name_style import NameStyle, NameStyleFont

from ..fields import validate_name_style


def _iter_options__passing():
    name_style = NameStyle(font = NameStyleFont.tempo)
    
    yield (None, None)
    yield (name_style, name_style)


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_name_style(input_value):
    """
    Tests whether ``validate_name_style`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``None | NameStyle``
    
    Raises
    ------
    TypeError
    """
    output = validate_name_style(input_value)
    vampytest.assert_instance(output, NameStyle, nullable = True)
    return output
