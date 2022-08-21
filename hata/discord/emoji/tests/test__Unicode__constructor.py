import vampytest

from ..unicode_type import Unicode


def test__Unicode__repr():
    """
    Tests whether ``Unicode``'ss constructor works as intended.
    """
    unicode = Unicode('owo', b'56', False, ('anya',), ('got', 'banned'))
    
    vampytest.assert_instance(repr(unicode), str)
