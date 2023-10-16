import vampytest

from ...activity_assets import ActivityAssets

from ..fields import validate_assets


def _iter_options():
    assets = ActivityAssets(image_large = 'hell')
    
    yield (None, None)
    yield (assets, assets)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_assets__passing(input_value):
    """
    Tests whether `validate_assets` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | ActivityAssets`
    """
    return validate_assets(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_assets__type_error(input_value):
    """
    Tests whether `validate_assets` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_assets(input_value)
