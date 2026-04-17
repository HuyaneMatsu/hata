import vampytest

from ..payload_renderer import _hash_map_key_sort_key


def test__hash_map_key_sort_key():
    """
    Tests whether ``_hash_map_key_sort_key`` works as intended.
    """
    key = '45'
    value = 46
    
    item = (key, value)
    
    output = _hash_map_key_sort_key(item)
    
    vampytest.assert_eq(output, key)
