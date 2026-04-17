import vampytest

from ..fields import put_finalized


def _iter_options():
    yield False, False, {'results': {'is_finalized': False}}
    yield False, True, {'results': {'is_finalized': False}}
    yield True, False, {'results': {'is_finalized': True}}
    yield True, True, {'results': {'is_finalized': True}}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_finalized(input_value, defaults):
    """
    Tests whether ``put_finalized`` works as intended.
    
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
    return put_finalized(input_value, {}, defaults)
