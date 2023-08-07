import vampytest

from ..fields import parse_type
from ..preinstanced import VerificationScreenStepType


def _iter_options():
    yield {}, VerificationScreenStepType.none
    yield {'field_type': VerificationScreenStepType.rules.value}, VerificationScreenStepType.rules


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    """
    Tests whether ``parse_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``VerificationScreenStepType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, VerificationScreenStepType)
    return output
