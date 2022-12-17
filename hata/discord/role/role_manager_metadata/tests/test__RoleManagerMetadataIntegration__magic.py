import vampytest

from ..integration import RoleManagerMetadataIntegration


def test__RoleManagerMetadataIntegration__repr():
    """
    Tests whether ``RoleManagerMetadataIntegration.__repr__`` works as intended.
    """
    integration_id = 202212160006
    
    metadata = RoleManagerMetadataIntegration(
        integration_id = integration_id,
    )
    
    vampytest.assert_instance(repr(metadata), str)


def test__RoleManagerMetadataIntegration__hash():
    """
    Tests whether ``RoleManagerMetadataIntegration.__hash__`` works as intended.
    """
    integration_id = 202212160007
    
    metadata = RoleManagerMetadataIntegration(
        integration_id = integration_id,
    )
    
    vampytest.assert_instance(hash(metadata), int)


def test__RoleManagerMetadataIntegration__eq():
    """
    Tests whether ``RoleManagerMetadataIntegration.__hash__`` works as intended.
    """
    integration_id = 202212160008
    
    keyword_parameters = {
        'integration_id': integration_id
    }
    
    metadata = RoleManagerMetadataIntegration(**keyword_parameters)
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    for field_name, field_value in (
        ('integration_id', 202212160009),
    ):
        test_metadata = RoleManagerMetadataIntegration(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(metadata, test_metadata)
