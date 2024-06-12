
import vampytest

from ..fields import put_spoiler_into


def _iter_options():
    yield False, False, {}
    yield False, True, {'spoiler': False}
    yield True, False, {'spoiler': True}
    yield True, True, {'spoiler': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_spoiler_into(input_value, defaults):
    """
    Tests whether ``put_spoiler_into`` works as intended.
    
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
    return put_spoiler_into(input_value, {}, defaults)
