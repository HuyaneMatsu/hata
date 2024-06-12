import vampytest

from ..fields import validate_spacing_size
from ..preinstanced import SeparatorSpacingSize


def _iter_options__passing():
    yield SeparatorSpacingSize.large, SeparatorSpacingSize.large
    yield SeparatorSpacingSize.large.value, SeparatorSpacingSize.large
    yield None, SeparatorSpacingSize.none


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_spacing_size(input_value):
    """
    Tests whether `validate_spacing_size` works as intended.
    
    Parameters
    ----------
    input_value : `dict<str, object>`
        Value to validate.
    
    Returns
    -------
    output : ``SeparatorSpacingSize``
    
    Raises
    ------
    TypeError
    """
    output = validate_spacing_size(input_value)
    vampytest.assert_instance(output, SeparatorSpacingSize)
    return output
