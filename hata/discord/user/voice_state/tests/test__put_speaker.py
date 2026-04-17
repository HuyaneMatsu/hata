import vampytest

from ..fields import put_speaker


def _iter_options():
    yield False, False, {}
    yield False, True, {'suppress': True}
    yield True, False, {'suppress': False}
    yield True, True, {'suppress': False}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_speaker(input_value, defaults):
    """
    Tests whether ``put_speaker`` works as intended.
    
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
    return put_speaker(input_value, {}, defaults)
