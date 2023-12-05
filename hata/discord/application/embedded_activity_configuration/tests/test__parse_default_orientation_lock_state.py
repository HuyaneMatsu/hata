import vampytest

from ..fields import parse_default_orientation_lock_state
from ..preinstanced import OrientationLockState


def _iter_options():
    yield {}, OrientationLockState.none
    yield {'default_orientation_lock_state': OrientationLockState.unlocked.value}, OrientationLockState.unlocked


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_default_orientation_lock_state(input_data):
    """
    Tests whether ``parse_default_orientation_lock_state`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``OrientationLockState``
    """
    output = parse_default_orientation_lock_state(input_data)
    vampytest.assert_instance(output, OrientationLockState)
    return output
