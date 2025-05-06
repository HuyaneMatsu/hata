import vampytest

from ..constants import MAX_VALUES_DEFAULT
from ..fields import parse_max_values


def _iter_options():
    yield (
        {},
        MAX_VALUES_DEFAULT,
    )
    
    yield (
        {
            'max_values': None,
        },
        MAX_VALUES_DEFAULT,
    )
    
    yield (
        {
            'max_values': 10,
        },
        10,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_max_values(input_data):
    """
    Tests whether ``parse_max_values`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_max_values(input_data)
    vampytest.assert_instance(output, int)
    return output
