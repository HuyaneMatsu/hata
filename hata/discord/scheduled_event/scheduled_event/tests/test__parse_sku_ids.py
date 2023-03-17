import vampytest

from ..fields import parse_sku_ids


def test__parse_sku_ids():
    """
    Tests whether ``parse_sku_ids`` works as intended.
    """
    sku_id_1 = 202303150006
    sku_id_2 = 202303150007
    
    for input_data, expected_output in (
        ({}, None),
        ({'sku_ids': None}, None),
        ({'sku_ids': []}, None),
        ({'sku_ids': [str(sku_id_1), str(sku_id_2)]}, (sku_id_1, sku_id_2)),
        ({'sku_ids': [str(sku_id_2), str(sku_id_1)]}, (sku_id_1, sku_id_2)),
    ):
        output = parse_sku_ids(input_data)
        vampytest.assert_eq(output, expected_output)
