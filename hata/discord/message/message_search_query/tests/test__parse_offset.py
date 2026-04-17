import vampytest

from ..constants import OFFSET_DEFAULT
from ..fields import parse_offset


def _iter_options():
    yield (
        {},
        OFFSET_DEFAULT,
    )
    
    yield (
        {
            'offset': None,
        },
        OFFSET_DEFAULT,
    )
    
    yield (
        {
            'offset': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_offset(input_data):
    """
    Tests whether ``parse_offset`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the offset from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_offset(input_data)
    vampytest.assert_instance(output, int)
    return output
