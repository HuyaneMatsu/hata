import vampytest

from ..fields import parse_mfa_enabled


def _iter_options():
    yield {}, False
    yield {'mfa_enabled': False}, False
    yield {'mfa_enabled': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_mfa_enabled(input_data):
    """
    Tests whether ``parse_mfa_enabled`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_mfa_enabled(input_data)
    
