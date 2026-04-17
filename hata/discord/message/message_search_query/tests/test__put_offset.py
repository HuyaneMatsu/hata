import vampytest

from ..constants import OFFSET_DEFAULT
from ..fields import put_offset


def _iter_options():
    yield (
        OFFSET_DEFAULT,
        False,
        {},
    )
    
    yield (
        OFFSET_DEFAULT,
        True,
        {
            'offset': OFFSET_DEFAULT,
        },
    )
    
    yield (
        1,
        False,
        {
            'offset': 1,
        },
    )
    
    yield (
        1,
        True,
        {
            'offset': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_offset(offset, defaults):
    """
    Tests whether ``put_offset`` works as intended.
    
    Parameters
    ----------
    offset : `int`
        The offset to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_offset(offset, {}, defaults)
