import vampytest

from ..fields import validate_type
from ..preinstanced import ConnectionType


def _iter_options_passing():
    yield None, ConnectionType.none
    yield ConnectionType.github, ConnectionType.github
    yield ConnectionType.github.value, ConnectionType.github


def _iter_options_type_error():
    yield 12.6
    yield 0


@vampytest._(vampytest.call_from(_iter_options_passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options_type_error()).raising(TypeError))
def test__validate_type__passing(input_value):
    """
    Tests whether ``validate_type`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ConnectionType``
    
    Raises
    ------
    TypeError
    """
    output = validate_type(input_value)
    vampytest.assert_instance(output, ConnectionType)
    return output
