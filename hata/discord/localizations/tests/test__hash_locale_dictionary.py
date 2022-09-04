import vampytest

from .. import Locale
from ..utils import hash_locale_dictionary


def test__hash_locale_dictionary():
    """
    Tests whether ``hash_locale_dictionary`` works as intended.
    """
    dictionary = {
        Locale.thai: 'hash',
        Locale.czech: 'bash',
    }
    
    hash_value = hash_locale_dictionary(dictionary)
    vampytest.assert_instance(hash_value, int)
