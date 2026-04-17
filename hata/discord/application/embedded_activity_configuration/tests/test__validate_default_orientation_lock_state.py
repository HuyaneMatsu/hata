import vampytest

from ..fields import validate_default_orientation_lock_state
from ..preinstanced import OrientationLockState


def _iter_options__passing():
    yield None, OrientationLockState.none
    yield OrientationLockState.unlocked, OrientationLockState.unlocked
    yield OrientationLockState.unlocked.value, OrientationLockState.unlocked


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_default_orientation_lock_state(input_value):
    """
    Tests whether ``validate_default_orientation_lock_state`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``OrientationLockState``
    
    Raises
    ------
    TypeError
    """
    output = validate_default_orientation_lock_state(input_value)
    vampytest.assert_instance(output, OrientationLockState)
    return output
