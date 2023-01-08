import vampytest

from ..fields import put_banner_id_into


def test__put_banner_id_into():
    """
    Tests whether ``put_banner_id_into`` works as intended.
    """
    banner_id = 202301040006
    
    for input_value, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'banner_asset_id': None}),
        (banner_id, False, {'banner_asset_id': str(banner_id)}),
    ):
        output = put_banner_id_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
