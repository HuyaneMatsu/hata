import vampytest

from ..constants import MAX_LENGTH_DEFAULT
from ..fields import put_max_length


def _iter_options():
    yield (
        MAX_LENGTH_DEFAULT,
        False,
        {},
    )
    
    yield (
        MAX_LENGTH_DEFAULT,
        True,
        {
            'max_length': MAX_LENGTH_DEFAULT,
        },
    )
    yield (
        10,
        False,
        {
            'max_length': 10,
        },
    )
    
    yield (
        10,
        True,
        {
            'max_length': 10,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_max_length(input_value, defaults):
    """
    Tests whether ``put_max_length`` is working as intended.
    
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
    return put_max_length(input_value, {}, defaults)
