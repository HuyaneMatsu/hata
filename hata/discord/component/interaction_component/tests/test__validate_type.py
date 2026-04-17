import vampytest

from ....component import ComponentType

from ..fields import validate_type


def _iter_options__passing():
    yield None, ComponentType.none
    yield ComponentType.button, ComponentType.button
    yield ComponentType.button.value, ComponentType.button


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_type(input_value):
    """
    Tests whether ``validate_type`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Raises
    ------
    TypeError
    
    Returns
    -------
    output : ``ComponentType``
    """
    output = validate_type(input_value)
    vampytest.assert_instance(output, ComponentType)
    return output
