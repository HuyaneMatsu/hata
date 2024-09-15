import vampytest

from ...activity_assets import ActivityAssets

from ..fields import validate_assets


def _iter_options__passing():
    assets = ActivityAssets(image_large = 'hell')
    
    yield None, None
    yield assets, assets


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_assets(input_value):
    """
    Tests whether `validate_assets` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | ActivityAssets`
    
    Raises
    ------
    TypeError
    """
    output = validate_assets(input_value)
    vampytest.assert_instance(output, ActivityAssets, nullable = True)
    return output
