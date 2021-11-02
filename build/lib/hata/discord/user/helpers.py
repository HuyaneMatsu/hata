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
    banner_color = data.get('accent_color', None)
    
    if (banner_color is not None):
        banner_color = Color(banner_color)
    
    return banner_color
