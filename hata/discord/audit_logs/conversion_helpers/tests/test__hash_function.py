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

    
