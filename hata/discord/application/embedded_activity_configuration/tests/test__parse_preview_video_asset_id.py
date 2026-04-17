import vampytest

from ..fields import parse_preview_video_asset_id


def _iter_options():
    preview_video_asset_id = 202312020000
    
    yield {}, 0
    yield {'activity_preview_video_asset_id': None}, 0
    yield {'activity_preview_video_asset_id': str(preview_video_asset_id)}, preview_video_asset_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_preview_video_asset_id(input_data):
    """
    Tests whether ``parse_preview_video_asset_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    return parse_preview_video_asset_id(input_data)
