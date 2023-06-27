__all__ = ()


def parse_name_with_discriminator(name):
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
  
  
def is_user_matching_name_with_discriminator(user, name_with_discriminator):
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
