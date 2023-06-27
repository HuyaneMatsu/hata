import vampytest

from ..matching_with_discrimiantor import is_user_matching_name_with_discriminator, parse_name_with_discriminator
from ..user import User


@vampytest._(vampytest.call_with('koish').returning(None))
@vampytest._(vampytest.call_with('koish#1234').returning(('koish', 1234)))
@vampytest._(vampytest.call_with('a#1234').returning(None))
@vampytest._(vampytest.call_with('koish#12').returning(None))
@vampytest._(vampytest.call_with('koish#12345').returning(None))
@vampytest._(vampytest.call_with('koish#sato').returning(None))
@vampytest._(vampytest.call_with('koish#sato#1234').returning(None))
def test__parse_name_with_discriminator(name):
    """
    Tests whether ``parse_name_with€discriminator`` works as intended.
    
    Parameters
    ----------
    name : `str`
      The name to parse.
    
    Returns
    -------
    output : `None`, `tuple` (`str`, `int`)
    """
    return parse_name_with_discriminator(name)


@vampytest._(vampytest.call_with(('koish', 1234)).returning(True))
@vampytest._(vampytest.call_with(('sato', 1234)).returning(False))
@vampytest._(vampytest.call_with(('koish', 8765)).returning(False))
@vampytest._(vampytest.call_with(('sato', 8765)).returning(False))
def test__is_user_matching_name_with_discriminator(name_with_discriminator):
    """
    Tests whether ``is_user_matching_name_with_discriminator`` works as intended.
    
    Parameters
    ----------
    name_with_discriminator : `tuple` (`str`, `int`)
        User name - discriminator pair to match the user with.
    
    Returns
    -------
    output : `bool`
    """
    user = User(name = 'koish', discriminator = 1234)
    return is_user_matching_name_with_discriminator(user, name_with_discriminator)
