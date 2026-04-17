import vampytest

from ..fields import validate_interaction_version
from ..preinstanced import ApplicationInteractionVersion


def _iter_options__passing():
    yield None, ApplicationInteractionVersion.none
    yield ApplicationInteractionVersion.selective, ApplicationInteractionVersion.selective
    yield ApplicationInteractionVersion.selective.value, ApplicationInteractionVersion.selective


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_interaction_version(input_value):
    """
    Tests whether ``validate_interaction_version`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ApplicationInteractionVersion``
    
    Raises
    ------
    TypeError
    """
    output = validate_interaction_version(input_value)
    vampytest.assert_instance(output, ApplicationInteractionVersion)
    return output
