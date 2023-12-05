import vampytest

from ..fields import validate_label_type
from ..preinstanced import LabelType


def _iter_options_passing():
    yield None, LabelType.none
    yield LabelType.new, LabelType.new
    yield LabelType.new.value, LabelType.new


def _iter_options_type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options_passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options_type_error()).raising(TypeError))
def test__validate_label_type__passing(input_value):
    """
    Tests whether ``validate_label_type`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``LabelType``
    
    Raises
    ------
    TypeError
    """
    output = validate_label_type(input_value)
    vampytest.assert_instance(output, LabelType)
    return output
