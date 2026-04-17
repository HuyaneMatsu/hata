import vampytest

from ..constants import MIN_VALUES_DEFAULT
from ..fields import parse_min_values


def _iter_options():
    yield (
        {},
        MIN_VALUES_DEFAULT,
    )
    
    yield (
        {
            'min_values': None,
        },
        MIN_VALUES_DEFAULT,
    )
    
    yield (
        {
            'min_values': 10,
        },
        10,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_min_values(input_data):
    """
    Tests whether ``parse_min_values`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_min_values(input_data)
    vampytest.assert_instance(output, int)
    return output
