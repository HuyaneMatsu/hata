__all__ = ()

from ....field_parsers import preinstanced_parser_factory
from ....field_validators import preinstanced_validator_factory

from ..preinstanced import VideoQualityMode


VIDEO_QUALITY_MODE_NONE = VideoQualityMode.none
VIDEO_QUALITY_MODE_AUTO = VideoQualityMode.auto

parse_video_quality_mode = preinstanced_parser_factory('video_quality_mode', VideoQualityMode, VideoQualityMode.auto)


def put_video_quality_mode_into(video_quality_mode, data, defaults):
    """
    Puts the `video_quality_mode`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    video_quality_mode : ``VideoQualityMode``
        The video quality of the voice channel.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (
        (video_quality_mode is not VIDEO_QUALITY_MODE_NONE) and
        (video_quality_mode is not VIDEO_QUALITY_MODE_AUTO)
    ):
        if video_quality_mode is VIDEO_QUALITY_MODE_NONE:
            video_quality_mode = VIDEO_QUALITY_MODE_AUTO
        
        data['video_quality_mode'] = video_quality_mode.value
    
    return data


validate_video_quality_mode = preinstanced_validator_factory('video_quality_mode', VideoQualityMode)
