import vampytest

from ..unicode_type import Unicode


def test__Unicode__repr():
    """
    Tests whether ``Unicode``'ss constructor works as intended.
    """
    unicode = Unicode('owo', '56', False, ('anya',), ('got', 'banned'), ('54', '53'))
    
    vampytest.assert_instance(repr(unicode), str)
