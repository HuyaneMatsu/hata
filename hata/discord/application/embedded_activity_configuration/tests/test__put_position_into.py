import vampytest

from ..fields import put_position_into


def _iter_options():
    yield 0, False, {'shelf_rank': 0}
    yield 0, True, {'shelf_rank': 0}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_position_into(position, defaults):
    """
    Tests whether ``put_position_into`` works as intended.
    
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
    return put_position_into(position, {}, defaults)
