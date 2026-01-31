import vampytest

from ..constants import LIMIT_DEFAULT
from ..fields import parse_limit


def _iter_options():
    yield (
        {},
        LIMIT_DEFAULT,
    )
    
    yield (
        {
            'limit': None,
        },
        LIMIT_DEFAULT,
    )
    
    yield (
        {
            'limit': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_limit(input_data):
    """
    Tests whether ``parse_limit`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the limit from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_limit(input_data)
    vampytest.assert_instance(output, int)
    return output
