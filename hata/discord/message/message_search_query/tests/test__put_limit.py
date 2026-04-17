import vampytest

from ..constants import LIMIT_DEFAULT
from ..fields import put_limit


def _iter_options():
    yield (
        LIMIT_DEFAULT,
        False,
        {},
    )
    
    yield (
        LIMIT_DEFAULT,
        True,
        {
            'limit': LIMIT_DEFAULT,
        },
    )
    
    yield (
        1,
        False,
        {
            'limit': 1,
        },
    )
    
    yield (
        1,
        True,
        {
            'limit': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_limit(limit, defaults):
    """
    Tests whether ``put_limit`` works as intended.
    
    Parameters
    ----------
    limit : `int`
        The limit to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_limit(limit, {}, defaults)
