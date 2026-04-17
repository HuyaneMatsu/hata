import vampytest

from ..fields import parse_gift_code_flags
from ..flags import GiftCodeFlag


def _iter_options():
    yield (
        {},
        GiftCodeFlag(0),
    )
    
    yield (
        {
            'gift_code_flags': None,
        },
        GiftCodeFlag(0),
    )
    
    yield (
        {
            'gift_code_flags': 1,
        },
        GiftCodeFlag(1),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_gift_code_flags(input_data):
    """
    Tests whether ``parse_gift_code_flags`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``GiftCodeFlag``
    """
    output = parse_gift_code_flags(input_data)
    vampytest.assert_instance(output, GiftCodeFlag)
    return output
