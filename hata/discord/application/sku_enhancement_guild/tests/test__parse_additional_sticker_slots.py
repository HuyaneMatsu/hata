import vampytest

from ..fields import parse_additional_sticker_slots


def _iter_options():
    yield (
        {},
        0,
    )
    
    yield (
        {
            'additional_sticker_slots': None,
        },
        0,
    )
    
    yield (
        {
            'additional_sticker_slots': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_additional_sticker_slots(input_data):
    """
    Tests whether ``parse_additional_sticker_slots`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_additional_sticker_slots(input_data)
    vampytest.assert_instance(output, int)
    return output
