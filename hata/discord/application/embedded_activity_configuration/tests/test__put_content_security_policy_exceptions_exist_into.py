import vampytest

from ..fields import put_content_security_policy_exceptions_exist_into


def _iter_options():
    yield False, False, {'has_csp_exception': False}
    yield False, True, {'has_csp_exception': False}
    yield True, False, {'has_csp_exception': True}
    yield True, True, {'has_csp_exception': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_content_security_policy_exceptions_exist_into(input_value, defaults):
    """
    Tests whether ``put_content_security_policy_exceptions_exist_into`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_content_security_policy_exceptions_exist_into(input_value, {}, defaults)
