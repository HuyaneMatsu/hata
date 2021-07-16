__all__ = ()

from ..color import Color


def get_banner_color_from_data(data):
    """
    Gets banner color from the given user data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        User data.
    
    Returns
    -------
    banner_color : `None` or `str`
    """
    banner_color = data.get('banner_color', None)
    
    # No banner color.
    if banner_color is None:
        pass
    
    # Old style string format
    elif isinstance(banner_color, str):
        banner_color = Color(banner_color[1:], 16)
    
    # New style int format
    elif isinstance(banner_color, int):
        banner_color = Color(banner_color)
    
    # No more cases
    else:
        banner_color = None
    
    return banner_color
