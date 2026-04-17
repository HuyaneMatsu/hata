import vampytest

from ..helpers import _hash_function


def test__hash_function():
    """
    Tests whether ``_hash_function`` works as intended.
    """
    def test_function():
        value = 6
        return value
    
    output = _hash_function(test_function)
    vampytest.assert_instance(output, int)
    

def test__hash_function__none():
    """
    Tests whether ``_hash_function`` works as intended.
    
    Case: `None`.
    """
    output = _hash_function(None)
    vampytest.assert_instance(output, int)
