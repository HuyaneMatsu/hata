import vampytest

from ..fields import put_integration_requires_code_grant_into


def _iter_options():
    yield False, False, {}
    yield False, True, {'integration_require_code_grant': False}
    yield True, False, {'integration_require_code_grant': True}
    yield True, True, {'integration_require_code_grant': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_integration_requires_code_grant_into(input_value, defaults):
    """
    Tests whether ``put_integration_requires_code_grant_into`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_integration_requires_code_grant_into(input_value, {}, defaults)
