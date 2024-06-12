import vampytest

from ..fields import put_divider_into


def _iter_options():
    yield False, False, {'divider': False}
    yield False, True, {'divider': False}
    yield True, False, {}
    yield True, True, {'divider': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_divider_into(input_value, defaults):
    """
    Tests whether ``put_divider_into`` works as intended.
    
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
    return put_divider_into(input_value, {}, defaults)
