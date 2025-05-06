import vampytest

from ..constants import MIN_LENGTH_DEFAULT
from ..fields import put_min_length


def _iter_options():
    yield (
        MIN_LENGTH_DEFAULT,
        False,
        {},
    )
    
    yield (
        MIN_LENGTH_DEFAULT,
        True,
        {
            'min_length': MIN_LENGTH_DEFAULT,
        },
    )
    yield (
        10,
        False,
        {
            'min_length': 10,
        },
    )
    
    yield (
        10,
        True,
        {
            'min_length': 10,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_min_length(input_value, defaults):
    """
    Tests whether ``put_min_length`` is working as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_min_length(input_value, {}, defaults)
