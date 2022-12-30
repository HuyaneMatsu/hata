import vampytest

from ...activity_assets import ActivityAssets

from ..fields import put_assets_into


def test__put_assets_into():
    """
    Tests whether ``put_assets_into`` is working as intended.
    """
    assets = ActivityAssets(image_large = 'hell')
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (assets, False, {'assets': assets.to_data()}),
        (assets, True, {'assets': assets.to_data(defaults = True)}),
    ):
        data = put_assets_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
