import vampytest

from ...activity_assets import ActivityAssets

from ..fields import validate_assets


def test__validate_assets__0():
    """
    Tests whether `validate_assets` works as intended.
    
    Case: passing.
    """
    assets = ActivityAssets(image_large = 'hell')
    
    for input_value, expected_output in (
        (None, None),
        (assets, assets),
    ):
        output = validate_assets(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_assets__1():
    """
    Tests whether `validate_assets` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_assets(input_value)
