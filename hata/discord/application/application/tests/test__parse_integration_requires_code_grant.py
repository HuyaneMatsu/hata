import vampytest

from ..fields import parse_integration_requires_code_grant


def _iter_options():
    yield {}, False
    yield {'integration_require_code_grant': False}, False
    yield {'integration_require_code_grant': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_integration_requires_code_grant(input_data):
    """
    Tests whether ``parse_integration_requires_code_grant`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_integration_requires_code_grant(input_data)
