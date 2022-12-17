import vampytest

from ..booster import RoleManagerMetadataBooster


def _assert_is_every_attribute_set(metadata):
    """
    Asserts whether every attributes are set of the given role manager metadata.
    
    Parameters
    ----------
    metadata : ``RoleManagerMetadataBooster``
        The metadata to assert.
    """
    vampytest.assert_instance(metadata, RoleManagerMetadataBooster)


def test__RoleManagerMetadataBooster__new__0():
    """
    Tests whether ``RoleManagerMetadataBooster.__new__`` works as intended.
    """
    metadata = RoleManagerMetadataBooster()
    _assert_is_every_attribute_set(metadata)
