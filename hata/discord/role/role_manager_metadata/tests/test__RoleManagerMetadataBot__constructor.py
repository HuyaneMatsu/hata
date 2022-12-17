import vampytest

from ..bot import RoleManagerMetadataBot


def _assert_is_every_attribute_set(metadata):
    """
    Asserts whether every attributes are set of the given role manager metadata.
    
    Parameters
    ----------
    metadata : ``RoleManagerMetadataBot``
        The metadata to assert.
    """
    vampytest.assert_instance(metadata, RoleManagerMetadataBot)


def test__RoleManagerMetadataBot__new__0():
    """
    Tests whether ``RoleManagerMetadataBot.__new__`` works as intended.
    
    Case: No fields given.
    """
    metadata = RoleManagerMetadataBot()
    _assert_is_every_attribute_set(metadata)


def test__RoleManagerMetadataBot__new__1():
    """
    Tests whether ``RoleManagerMetadataBot.__new__`` works as intended.
    
    Case: all fields given
    """
    bot_id = 202212160003
    
    metadata = RoleManagerMetadataBot(
        bot_id = bot_id,
    )
    _assert_is_every_attribute_set(metadata)
    
    vampytest.assert_eq(metadata.bot_id, bot_id)
