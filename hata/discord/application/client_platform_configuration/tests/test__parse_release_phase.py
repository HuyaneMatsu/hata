import vampytest

from ..fields import parse_release_phase
from ..preinstanced import ReleasePhase


def _iter_options():
    yield {}, ReleasePhase.global_launch
    yield {'release_phase': ReleasePhase.global_launch.value}, ReleasePhase.global_launch


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_release_phase(input_data):
    """
    Tests whether ``parse_release_phase`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ReleasePhase``
    """
    output = parse_release_phase(input_data)
    vampytest.assert_instance(output, ReleasePhase)
    return output
