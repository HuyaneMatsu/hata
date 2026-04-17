import vampytest

from ..base import RoleManagerMetadataBase


def test__RoleManagerMetadataBase__repr():
    """
    Tests whether ``RoleManagerMetadataBase.__repr__`` works as intended.
    """
    metadata = RoleManagerMetadataBase()
    
    vampytest.assert_instance(repr(metadata), str)


def test__RoleManagerMetadataBase__hash():
    """
    Tests whether ``RoleManagerMetadataBase.__hash__`` works as intended.
    """
    metadata = RoleManagerMetadataBase()
    
    vampytest.assert_instance(hash(metadata), int)


def test__RoleManagerMetadataBase__eq():
    """
    Tests whether ``RoleManagerMetadataBase.__hash__`` works as intended.
    """
    keyword_parameters = {}
    
    metadata = RoleManagerMetadataBase(**keyword_parameters)
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    for field_name, field_value in (
    ):
        test_metadata = RoleManagerMetadataBase(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(metadata, test_metadata)
