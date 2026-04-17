import vampytest

from ..booster import RoleManagerMetadataBooster


def test__RoleManagerMetadataBooster__repr():
    """
    Tests whether ``RoleManagerMetadataBooster.__repr__`` works as intended.
    """
    metadata = RoleManagerMetadataBooster()
    
    vampytest.assert_instance(repr(metadata), str)


def test__RoleManagerMetadataBooster__hash():
    """
    Tests whether ``RoleManagerMetadataBooster.__hash__`` works as intended.
    """
    metadata = RoleManagerMetadataBooster()
    
    vampytest.assert_instance(hash(metadata), int)


def test__RoleManagerMetadataBooster__eq():
    """
    Tests whether ``RoleManagerMetadataBooster.__hash__`` works as intended.
    """
    keyword_parameters = {}
    
    metadata = RoleManagerMetadataBooster(**keyword_parameters)
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    for field_name, field_value in (
    ):
        test_metadata = RoleManagerMetadataBooster(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(metadata, test_metadata)
