import vampytest

from ..fields import validate_layout
from ..preinstanced import PollLayout


def _iter_options__passing():
    yield None, PollLayout.none
    yield PollLayout.default, PollLayout.default
    yield PollLayout.default.value, PollLayout.default


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_layout(input_value):
    """
    Validates whether ``validate_layout`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``PollLayout``
    
    Raises
    ------
    TypeError
    """
    output = validate_layout(input_value)
    vampytest.assert_instance(output, PollLayout)
    return output
