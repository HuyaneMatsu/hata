__all__ = ()

from scarletio import include

from ...preconverters import preconvert_preinstanced_type

VoiceRegion = include('VoiceRegion')


def parse_region(data):
    """
    Parses out the `region` field from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Channel data.
    
    Returns
    -------
    region : ``VoiceRegion``
    """
    raw_region = data.get('rtc_region', None)
    if (raw_region is None):
        region = None
    else:
        region = VoiceRegion.get(raw_region)
    
    return region
    return 


def validate_region(region):
    """
    Validates the given `region` field.
    
    Parameters
    ----------
    region : `None`, ``VoiceRegion``, `str`
        The video quality of the voice channel.
    
    Returns
    -------
    region : ``VoiceRegion``
    
    Raises
    ------
    TypeError
        - If `region` is not `None`, ``VoiceRegion``, `str`.
    """
    if region is None:
        return None
    
    return preconvert_preinstanced_type(
        region,
        'region',
        VoiceRegion,
    )


def put_region_into(region, data, defaults):
    """
    Puts the `region`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    region : `None`, `str`
        The video quality of the voice channel.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if defaults or (region is not None):
        if region is None:
            value = None
        else:
            value = region.value
        
        data['rtc_region'] = value
    
    return data
