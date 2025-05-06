import vampytest

from ..fields import put_position


def _iter_options():
    yield 0, False, {'shelf_rank': 0}
    yield 0, True, {'shelf_rank': 0}
    yield 1, False, {'shelf_rank': 1}
    yield 1, True, {'shelf_rank': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_position(position, defaults):
    """
    Tests whether ``put_position`` works as intended.
    
    Parameters
    ----------
    position : `int`
        The position to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_position(position, {}, defaults)
