import vampytest

from ..fields import parse_promotion_id


def _iter_options():
    promotion_id = 202607010000
    
    yield (
        {},
        0,
    )
    
    yield (
        {
            'promotion_id': None,
        },
        0,
    )
    
    yield (
        {
            'promotion_id': str(promotion_id),
        },
        promotion_id,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_promotion_id(input_data):
    """
    Tests whether ``parse_promotion_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_promotion_id(input_data)
    vampytest.assert_instance(output, int)
    return output
