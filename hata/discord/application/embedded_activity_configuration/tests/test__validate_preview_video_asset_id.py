import vampytest

from ..fields import validate_preview_video_asset_id


def _iter_options__passing():
    preview_video_asset_id = 202312020002
    
    yield 0, 0
    yield preview_video_asset_id, preview_video_asset_id
    yield str(preview_video_asset_id), preview_video_asset_id


def _iter_options__type_error():
    yield None
    yield 12.6


def _iter_options__value_error():
    yield '-1'
    yield '1111111111111111111111'
    yield -1
    yield 1111111111111111111111


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_preview_video_asset_id(input_value):
    """
    Tests whether `validate_preview_video_asset_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `int`
    
    Raising
    -------
    TypeError
    ValueError
    """
    return validate_preview_video_asset_id(input_value)
