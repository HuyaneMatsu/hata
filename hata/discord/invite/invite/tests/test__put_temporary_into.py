import vampytest

from ..fields import put_temporary_into


def _iter_options():
    yield False, False, {}
    yield False, True, {'temporary': False}
    yield True, False, {'temporary': True}
    yield True, True, {'temporary': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_temporary_into(input_value, defaults):
    """
    Tests whether ``put_temporary_into`` works as intended.
    
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
    return put_temporary_into(input_value, {}, defaults)
