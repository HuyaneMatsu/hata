import vampytest

from ..fields import put_gift_code_flags
from ..flags import GiftCodeFlag


def _iter_options():
    yield (
        GiftCodeFlag(0),
        False,
        {},
    )
    
    yield (
        GiftCodeFlag(0),
        True,
        {
            'gift_code_flags': 0,
        },
    )
    
    yield (
        GiftCodeFlag(1),
        False,
        {
            'gift_code_flags': 1,
        },
    )
    
    yield (
        GiftCodeFlag(1),
        True,
        {
            'gift_code_flags': 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_gift_code_flags(input_value, defaults):
    """
    Tests whether ``put_gift_code_flags`` is working as intended.
    
    Parameters
    ----------
    input_value : ``GiftCodeFlag``
        The value to serialise.
    
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_gift_code_flags(input_value, {}, defaults)
