__all__ = ('create_auto_custom_id', 'create_identifier_custom_id_from_name')

from base64 import b85encode as to_base85
from os import urandom as random_bytes


def create_auto_custom_id():
    """
    Creates a random custom identifier for components.
    
    Returns
    -------
    custom_id : `str`
        The created custom id.
    """
    return to_base85(random_bytes(64)).decode()


def create_identifier_custom_id_from_name(name):
    """
    Tries to turn the given name into an identifier. The identifier is always lower case. Spaces and minus signs are
    turned to underscore.
    
    Parameters
    ----------
    name : `str`
        The name of a custom_id.
    
    Returns
    -------
    custom_id : `str`
        The created custom id.
    """
    return name.casefold().replace(' ', '_').replace('-', '_')
