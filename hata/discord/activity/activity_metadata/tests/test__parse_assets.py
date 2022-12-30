import vampytest

from ...activity_assets import ActivityAssets

from ..fields import parse_assets


def test__parse_assets():
    """
    Tests whether ``parse_assets`` works as intended.
    """
    assets = ActivityAssets(image_large = 'hell')
    
    for input_data, expected_output in (
        ({}, None),
        ({'assets': None}, None),
        ({'assets': assets.to_data()}, assets),
    ):
        output = parse_assets(input_data)
        vampytest.assert_eq(output, expected_output)
