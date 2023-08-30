import vampytest

from ..base import RoleManagerMetadataBase


def _assert_fields_set(metadata):
    """
    Asserts whether every attributes are set of the given role manager metadata.
    
    Parameters
    ----------
    metadata : ``RoleManagerMetadataBase``
        The metadata to assert.
    """
    vampytest.assert_instance(metadata, RoleManagerMetadataBase)


def test__RoleManagerMetadataBase__new__0():
    """
    Tests whether ``RoleManagerMetadataBase.__new__`` works as intended.
    """
    metadata = RoleManagerMetadataBase()
    _assert_fields_set(metadata)
