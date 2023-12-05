import vampytest

from ..fields import validate_release_phase
from ..preinstanced import ReleasePhase


def _iter_options_passing():
    yield None, ReleasePhase.global_launch
    yield ReleasePhase.global_launch, ReleasePhase.global_launch
    yield ReleasePhase.global_launch.value, ReleasePhase.global_launch


def _iter_options_type_error():
    yield 12.6
    yield 0


@vampytest._(vampytest.call_from(_iter_options_passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options_type_error()).raising(TypeError))
def test__validate_release_phase__passing(input_value):
    """
    Tests whether ``validate_release_phase`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ReleasePhase``
    
    Raises
    ------
    TypeError
    """
    output = validate_release_phase(input_value)
    vampytest.assert_instance(output, ReleasePhase)
    return output
