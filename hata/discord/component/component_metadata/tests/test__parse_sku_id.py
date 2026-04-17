import vampytest

from ..fields import parse_sku_id


def _iter_options():
    sku_id = 202405180070

    yield {}, 0
    yield {'sku_id': None}, 0
    yield {'sku_id': str(sku_id)}, sku_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_sku_id(input_data):
    """
    Tests whether ``parse_sku_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_sku_id(input_data)
    vampytest.assert_instance(output, int)
    return output
