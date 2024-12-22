import vampytest

from ..fields import parse_renewal_sku_ids


def _iter_options():
    sku_id_0 = 202412210000
    sku_id_1 = 202412210001
    
    yield {}, None
    yield {'renewal_sku_ids': None}, None
    yield {'renewal_sku_ids': []}, None
    yield {'renewal_sku_ids': [str(sku_id_0), str(sku_id_1)]}, (sku_id_0, sku_id_1)
    yield {'renewal_sku_ids': [str(sku_id_1), str(sku_id_0)]}, (sku_id_0, sku_id_1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_renewal_sku_ids(input_data):
    """
    Tests whether ``parse_renewal_sku_ids`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    output = parse_renewal_sku_ids(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
