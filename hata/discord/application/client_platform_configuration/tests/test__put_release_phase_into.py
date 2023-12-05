import vampytest

from ..fields import put_release_phase_into
from ..preinstanced import ReleasePhase


def _iter_options():
    yield ReleasePhase.global_launch, False, {'release_phase': ReleasePhase.global_launch.value}
    yield ReleasePhase.global_launch, True, {'release_phase': ReleasePhase.global_launch.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_release_phase_into(input_value, defaults):
    """
    Tests whether ``put_release_phase_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ReleasePhase``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_release_phase_into(input_value, {}, defaults)
