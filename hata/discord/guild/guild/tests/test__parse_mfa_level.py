import vampytest

from ..fields import parse_mfa_level
from ..preinstanced import MfaLevel


def _iter_options():
    yield {}, MfaLevel.none
    yield {'mfa_level': MfaLevel.elevated.value}, MfaLevel.elevated


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_mfa_level(input_data):
    """
    Tests whether ``parse_mfa_level`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``MfaLevel``
    """
    output = parse_mfa_level(input_data)
    vampytest.assert_instance(output, MfaLevel)
    return output
