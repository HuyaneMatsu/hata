import vampytest

from ..fields import parse_sku_ids


def _iter_options():
    sku_id_0 = 202303150006
    sku_id_1 = 202303150007
    
    yield {}, None
    yield {'sku_ids': None}, None
    yield {'sku_ids': []}, None
    yield {'sku_ids': [str(sku_id_0), str(sku_id_1)]}, (sku_id_0, sku_id_1)
    yield {'sku_ids': [str(sku_id_1), str(sku_id_0)]}, (sku_id_0, sku_id_1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_sku_ids(input_data):
    """
    Tests whether ``parse_sku_ids`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    output = parse_sku_ids(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
