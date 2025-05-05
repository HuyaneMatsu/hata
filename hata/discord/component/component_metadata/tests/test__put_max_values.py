import vampytest

from ..constants import MAX_VALUES_DEFAULT
from ..fields import put_max_values


def _iter_options():
    yield (
        MAX_VALUES_DEFAULT,
        False,
        {},
    )
    
    yield (
        MAX_VALUES_DEFAULT,
        True,
        {
            'max_values': MAX_VALUES_DEFAULT,
        },
    )
    yield (
        10,
        False,
        {
            'max_values': 10,
        },
    )
    
    yield (
        10,
        True,
        {
            'max_values': 10,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_max_values(input_value, defaults):
    """
    Tests whether ``put_max_values`` is working as intended.
    
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
    return put_max_values(input_value, {}, defaults)
