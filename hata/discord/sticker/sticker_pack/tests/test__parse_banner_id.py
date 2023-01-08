import vampytest

from ..fields import parse_banner_id


def test__parse_banner_id():
    """
    Tests whether ``parse_banner_id`` works as intended.
    """
    banner_id = 202301050003
    
    for input_data, expected_output in (
        ({}, 0),
        ({'banner_asset_id': None}, 0),
        ({'banner_asset_id': str(banner_id)}, banner_id),
    ):
        output = parse_banner_id(input_data)
        vampytest.assert_eq(output, expected_output)
