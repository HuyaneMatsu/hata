import vampytest

from ..integration import RoleManagerMetadataIntegration

from .test__RoleManagerMetadataIntegration__constructor import _assert_fields_set


def test__RoleManagerMetadataIntegration__from_data():
    """
    Tests whether ``RoleManagerMetadataIntegration.from_data`` works as intended.
    """
    integration_id = 202212160004
    
    data = {
        'integration_id': str(integration_id)
    }
    
    metadata = RoleManagerMetadataIntegration.from_data(data)
    _assert_fields_set(metadata)
    
    vampytest.assert_eq(metadata.integration_id, integration_id)


def test__RoleManagerMetadataIntegration__to_data():
    """
    Tests whether ``RoleManagerMetadataIntegration.to_data`` works as intended.
    """
    integration_id = 202212160005
    
    metadata = RoleManagerMetadataIntegration(
        integration_id = integration_id
    )
    
    expected_data = {
        'integration_id': str(integration_id),
    }
    
    vampytest.assert_eq(
        metadata.to_data(defaults = True),
        expected_data
    )
