import vampytest

from ..constants import SLOP_DEFAULT
from ..fields import put_slop


def _iter_options():
    yield (
        SLOP_DEFAULT,
        False,
        {},
    )
    
    yield (
        SLOP_DEFAULT,
        True,
        {
            'slop': SLOP_DEFAULT,
        },
    )
    
    yield (
        1,
        False,
        {
            'slop': 1,
        },
    )
    
    yield (
        1,
        True,
        {
            'slop': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_slop(slop, defaults):
    """
    Tests whether ``put_slop`` works as intended.
    
    Parameters
    ----------
    slop : `int`
        The slop to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_slop(slop, {}, defaults)
