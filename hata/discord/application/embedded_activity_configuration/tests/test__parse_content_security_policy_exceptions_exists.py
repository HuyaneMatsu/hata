import vampytest

from ..fields import parse_content_security_policy_exceptions_exist


def _iter_options():
    yield {}, False
    yield {'has_csp_exception': False}, False
    yield {'has_csp_exception': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_content_security_policy_exceptions_exist(input_data):
    """
    Tests whether ``parse_content_security_policy_exceptions_exist`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_content_security_policy_exceptions_exist(input_data)
