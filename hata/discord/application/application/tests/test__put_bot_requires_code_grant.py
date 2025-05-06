import vampytest

from ..fields import put_bot_requires_code_grant


def _iter_options():
    yield False, False, {}
    yield False, True, {'bot_require_code_grant': False}
    yield True, False, {'bot_require_code_grant': True}
    yield True, True, {'bot_require_code_grant': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_bot_requires_code_grant(input_value, defaults):
    """
    Tests whether ``put_bot_requires_code_grant`` works as intended.
    
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
    return put_bot_requires_code_grant(input_value, {}, defaults)
