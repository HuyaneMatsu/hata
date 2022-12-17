import vampytest

from ....integration import Integration

from ..integration import RoleManagerMetadataIntegration

from .test__RoleManagerMetadataIntegration__constructor import _assert_is_every_attribute_set


def test__RoleManagerMetadataIntegration__copy():
    """
    Tests whether ``RoleManagerMetadataIntegration.copy`` works as intended.
    """
    integration_id = 202212160009
    metadata = RoleManagerMetadataIntegration(
        integration_id = integration_id,
    )
    copy = metadata.copy()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(copy, metadata)
    vampytest.assert_is_not(copy, metadata)


def test__RoleManagerMetadataIntegration__copy_with__0():
    """
    Tests whether ``RoleManagerMetadataIntegration.to_data`` works as intended.
    
    Case: No fields given.
    """
    integration_id = 202212160010
    
    metadata = RoleManagerMetadataIntegration(
        integration_id = integration_id,
    )
    copy = metadata.copy_with()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(copy, metadata)
    vampytest.assert_is_not(copy, metadata)

def test__RoleManagerMetadataIntegration__copy_with__1():
    """
    Tests whether ``RoleManagerMetadataIntegration.to_data`` works as intended.
    
    Case: All fields given.
    """
    old_integration_id = 202212160011
    new_integration_id = 202212160012
    
    metadata = RoleManagerMetadataIntegration(
        integration_id = old_integration_id,
    )
    copy = metadata.copy_with(
        integration_id = new_integration_id,
    )
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_is_not(copy, metadata)
    
    vampytest.assert_eq(copy.integration_id, new_integration_id)


def test__RoleManagerMetadataIntegration__manager_id():
    """
    Tests whether ``RoleManagerMetadataIntegration.manager_id`` works as intended.
    """
    integration_id = 202212160013
    
    metadata = RoleManagerMetadataIntegration(
        integration_id = integration_id,
    )
    vampytest.assert_eq(metadata.manager_id, integration_id)


def test__RoleManagerMetadataIntegration__manager():
    """
    Tests whether ``RoleManagerMetadataIntegration.manager`` works as intended.
    """
    integration_id = 202212160014
    
    metadata = RoleManagerMetadataIntegration(
        integration_id = integration_id,
    )
    vampytest.assert_is(metadata.manager, Integration.precreate(integration_id))
