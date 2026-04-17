__all__ = ()

from .constants import KEY_LENGTH_MAX


CHARACTER_RANGE = range(b'a'[0], b'z'[0] + 1)


def _convert_character(character):
    """
    Converts the given character to an allowed one if applicable.
    
    Parameters
    ----------
    character : `str`
        The character to convert.
    
    Returns
    -------
    character : `str`
    """
    character = character.casefold()
    if ord(character) in CHARACTER_RANGE:
        return character
    
    if character == '_':
        return character
    
    if character in {'-', ' '}:
        return '_'
    
    return ''


def escape_name_to_key(name):
    """
    Tries to convert the given name.
    
    Parameters
    ----------
    name : `str`
        Metadata name.
    
    Returns
    -------
    escaped : `str`
    """
    return (''.join([_convert_character(character) for character in name]))[:KEY_LENGTH_MAX]
