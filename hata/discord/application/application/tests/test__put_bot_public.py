import vampytest

from ..fields import put_bot_public


def _iter_options():
    yield False, False, {}
    yield False, True, {'bot_public': False}
    yield True, False, {'bot_public': True}
    yield True, True, {'bot_public': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_bot_public(input_value, defaults):
    """
    Tests whether ``put_bot_public`` works as intended.
    
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
    return put_bot_public(input_value, {}, defaults)
