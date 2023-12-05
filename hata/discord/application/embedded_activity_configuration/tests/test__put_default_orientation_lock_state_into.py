import vampytest

from ..fields import put_default_orientation_lock_state_into
from ..preinstanced import OrientationLockState


def _iter_options():
    yield OrientationLockState.unlocked, False, {'default_orientation_lock_state': OrientationLockState.unlocked.value}
    yield OrientationLockState.unlocked, True, {'default_orientation_lock_state': OrientationLockState.unlocked.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_default_orientation_lock_state_into(input_value, defaults):
    """
    Tests whether ``put_default_orientation_lock_state_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``OrientationLockState``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_default_orientation_lock_state_into(input_value, {}, defaults)
