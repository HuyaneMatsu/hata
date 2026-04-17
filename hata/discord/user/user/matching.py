__all__ = ()


USER_MATCH_WEIGHT_NAME = 1
USER_MATCH_WEIGHT_DISPLAY_NAME = 2
USER_MATCH_WEIGHT_NICK = 3


def _parse_name_with_discriminator(name):
    """
    Tries to parse the user's name and their discriminator from the given name value.
    
    Parameters
    ----------
    name : `str`
        The name value to parse.
    
    Returns
    -------
    user_with_discriminator : `None`, `tuple` (`str`, `int`)
        Returns `None` on unsuccessful parsing.
    """
    separator_index = name.find('#')
    if separator_index < 2:
        return None
    
    if len(name) - separator_index != 5:
        return None
    
    try:
        discriminator = int(name[separator_index + 1 :])
    except ValueError:
        return None
    
    return name[: separator_index], discriminator
  
  
def _is_user_matching_name_with_discriminator(user, name_with_discriminator):
    """
    Returns whether the user matches the given name - discriminator pair.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user we are trying to match.
    name_with_discriminator : `tuple` (`str`, `int`)
        Name - discriminator pair.
    
    Returns
    -------
    is_matching : `bool`
    """
    if user.discriminator != name_with_discriminator[1]:
        return False
   
    if user.name != name_with_discriminator[0]:
        return False
    
    return True


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


def _user_match_sort_key(item):
    """
    Sort key used inside of ``Guild.get_users_like`` to sort users based on their match rate.
    
    Parameters
    ----------
    item : `tuple` (``ClientUserBase``, `tuple` (`int`, `int`, `int`))
        The user and it's match rate.
    
    Returns
    -------
    match_rate : `tuple` (`int`, `int`, `int`)
    """
    return item[1]
