import vampytest

from ..constants import MIN_VALUES_DEFAULT
from ..fields import put_min_values


def _iter_options():
    yield (
        MIN_VALUES_DEFAULT,
        False,
        {},
    )
    
    yield (
        MIN_VALUES_DEFAULT,
        True,
        {
            'min_values': MIN_VALUES_DEFAULT,
        },
    )
    yield (
        10,
        False,
        {
            'min_values': 10,
        },
    )
    
    yield (
        10,
        True,
        {
            'min_values': 10,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_min_values(input_value, defaults):
    """
    Tests whether ``put_min_values`` is working as intended.
    
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
    return put_min_values(input_value, {}, defaults)
