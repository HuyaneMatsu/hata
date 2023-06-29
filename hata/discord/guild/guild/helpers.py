__all__ = ()


# ---- channel ----

def _channel_match_sort_key(item):
    """
    Sort key used inside of ``Guild.get_channels_like`` to sort channels based on their match rate.
    
    Parameters
    ----------
    item : `tuple` (``Channel``, `tuple` (`int`, `int`))
        The channel and it's match rate.
    
    Returns
    -------
    match_rate : `tuple` (`int`, `int`)
    """
    return item[1]

# ---- emoji ----

def _emoji_match_sort_key(item):
    """
    Sort key used inside of ``Guild.get_emojis_like`` to sort emojis based on their match rate.
    
    Parameters
    ----------
    item : `tuple` (``Emoji``, `tuple` (`int`, `int`))
        The emoji and it's match rate.
    
    Returns
    -------
    match_rate : `tuple` (`int`, `int`)
    """
    return item[1]


def _strip_emoji_name(name):
    """
    Strips the given emoji name from colon signs.
    
    Parameters
    ----------
    name : `str`
        The name to strip.
    
    Returns
    -------
    name : `str`
    """
    if name.startswith(':'):
        starts_at = 1
    else:
        starts_at = None
    
    if name.endswith(':'):
        ends_at = -1
    else:
        ends_at = None
    
    if (starts_at is not None) or (ends_at is not None):
        name = name[starts_at : ends_at]
    
    return name


# ---- role ----
def _role_match_sort_key(item):
    """
    Sort key used inside of ``Guild.get_roles_like`` to sort roles based on their match rate.
    
    Parameters
    ----------
    item : `tuple` (``Role``, `tuple` (`int`, `int`))
        The role and it's match rate.
    
    Returns
    -------
    match_rate : `tuple` (`int`, `int`)
    """
    return item[1]


# ---- soundboard sound ----

def _soundboard_sound_match_sort_key(item):
    """
    Sort key used inside of ``Guild.get_soundboard_sounds_like`` to sort soundboard sounds based on their match rate.
    
    Parameters
    ----------
    item : `tuple` (``Sticker``, `tuple` (`int`, `int`))
        The soundboard sound and it's match rate.
    
    Returns
    -------
    match_rate : `tuple` (`int`, `int`)
    """
    return item[1]


# ---- sticker ----

STICKER_MATCH_WEIGHT_NAME = 1
STICKER_MATCH_WEIGHT_TAG = 2


def _sticker_match_sort_key(item):
    """
    Sort key used inside of ``Guild.get_stickers_like`` to sort stickers based on their match rate.
    
    Parameters
    ----------
    item : `tuple` (``Sticker``, `tuple` (`int`, `int`, `int`))
        The sticker and it's match rate.
    
    Returns
    -------
    match_rate : `tuple` (`int`, `int`, `int`)
    """
    return item[1]
