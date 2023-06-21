__all__ = ()


def _user_date_sort_key(item):
    """
    Sort key used inside ``Guild.get_users_like_ordered`` and in ``Guild.boosters`` to sort users by a specified date.
    
    Parameters
    ----------
    item : `tuple` (``ClientUserBase``, `datetime`)
        The user and it's specific date.
    
    Returns
    -------
    date : `datetime`
    """
    return item[1]


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


def _sticker_match_sort_key(item):
    """
    Sort key used inside of ``Guild.get_stickers_like`` to sort stickers based on their match rate.
    
    Parameters
    ----------
    item : `tuple` (``Sticker``, `tuple` (`bool`, `int`, `int`))
        The sticker and it's match rate.
    
    Returns
    -------
    match_rate : `tuple` (`bool`, `int`, `int`)
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
