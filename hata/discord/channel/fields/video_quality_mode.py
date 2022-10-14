__all__ = ()

from ...preconverters import preconvert_preinstanced_type

from ..preinstanced import VideoQualityMode


VIDEO_QUALITY_MODE_NONE = VideoQualityMode.none
VIDEO_QUALITY_MODE_AUTO = VideoQualityMode.auto


def parse_video_quality_mode(data):
    """
    Parses out the `video_quality_mode` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    video_quality_mode : ``VideoQualityMode``
    """
    return VideoQualityMode.get(data.get('video_quality_mode', 1))


def validate_video_quality_mode(video_quality_mode):
    """
    Validates the given `video_quality_mode` field.
    
    Parameters
    ----------
    video_quality_mode : ``VideoQualityMode``, `int`
        The video quality of the voice channel.
    
    Returns
    -------
    video_quality_mode : ``VideoQualityMode``
    
    Raises
    ------
    TypeError
        - If `video_quality_mode` is not ``VideoQualityMode``, `int`.
    """
    return preconvert_preinstanced_type(
        video_quality_mode,
        'video_quality_mode',
        VideoQualityMode,
    )


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
