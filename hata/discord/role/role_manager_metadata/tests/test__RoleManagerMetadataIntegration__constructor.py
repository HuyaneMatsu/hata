import vampytest

from ..integration import RoleManagerMetadataIntegration


def _assert_fields_set(metadata):
    """
    Asserts whether every attributes are set of the given role manager metadata.
    
    Parameters
    ----------
    metadata : ``RoleManagerMetadataIntegration``
        The metadata to assert.
    """
    vampytest.assert_instance(metadata, RoleManagerMetadataIntegration)


def test__RoleManagerMetadataIntegration__new__0():
    """
    Tests whether ``RoleManagerMetadataIntegration.__new__`` works as intended.
    
    Case: No fields given.
    """
    metadata = RoleManagerMetadataIntegration()
    _assert_fields_set(metadata)


def test__RoleManagerMetadataIntegration__new__1():
    """
    Tests whether ``RoleManagerMetadataIntegration.__new__`` works as intended.
    
    Case: all fields given
    """
    integration_id = 202212160003
    
    metadata = RoleManagerMetadataIntegration(
        integration_id = integration_id,
    )
    _assert_fields_set(metadata)
    
    vampytest.assert_eq(metadata.integration_id, integration_id)
