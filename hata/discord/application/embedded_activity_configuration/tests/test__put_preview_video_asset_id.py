import vampytest

from ..fields import put_preview_video_asset_id


def _iter_options():
    preview_video_asset_id = 202312020001
    
    yield 0, False, {'activity_preview_video_asset_id': None}
    yield 0, True, {'activity_preview_video_asset_id': None}
    yield preview_video_asset_id, False, {'activity_preview_video_asset_id': str(preview_video_asset_id)}
    yield preview_video_asset_id, True, {'activity_preview_video_asset_id': str(preview_video_asset_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_preview_video_asset_id(input_value, defaults):
    """
    Tests whether ``put_preview_video_asset_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_preview_video_asset_id(input_value, {}, defaults)
