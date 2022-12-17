import vampytest

from ....user import User

from ..bot import RoleManagerMetadataBot

from .test__RoleManagerMetadataBot__constructor import _assert_is_every_attribute_set


def test__RoleManagerMetadataBot__copy():
    """
    Tests whether ``RoleManagerMetadataBot.copy`` works as intended.
    """
    bot_id = 202212160009
    metadata = RoleManagerMetadataBot(
        bot_id = bot_id,
    )
    copy = metadata.copy()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(copy, metadata)
    vampytest.assert_is_not(copy, metadata)


def test__RoleManagerMetadataBot__copy_with__0():
    """
    Tests whether ``RoleManagerMetadataBot.to_data`` works as intended.
    
    Case: No fields given.
    """
    bot_id = 202212160010
    
    metadata = RoleManagerMetadataBot(
        bot_id = bot_id,
    )
    copy = metadata.copy_with()
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_eq(copy, metadata)
    vampytest.assert_is_not(copy, metadata)

def test__RoleManagerMetadataBot__copy_with__1():
    """
    Tests whether ``RoleManagerMetadataBot.to_data`` works as intended.
    
    Case: All fields given.
    """
    old_bot_id = 202212160011
    new_bot_id = 202212160012
    
    metadata = RoleManagerMetadataBot(
        bot_id = old_bot_id,
    )
    copy = metadata.copy_with(
        bot_id = new_bot_id,
    )
    _assert_is_every_attribute_set(copy)
    
    vampytest.assert_is_not(copy, metadata)
    
    vampytest.assert_eq(copy.bot_id, new_bot_id)


def test__RoleManagerMetadataBot__manager_id():
    """
    Tests whether ``RoleManagerMetadataBot.manager_id`` works as intended.
    """
    bot_id = 202212160013
    
    metadata = RoleManagerMetadataBot(
        bot_id = bot_id,
    )
    vampytest.assert_eq(metadata.manager_id, bot_id)


def test__RoleManagerMetadataBot__manager():
    """
    Tests whether ``RoleManagerMetadataBot.manager`` works as intended.
    """
    bot_id = 202212160014
    
    metadata = RoleManagerMetadataBot(
        bot_id = bot_id,
    )
    vampytest.assert_is(metadata.manager, User.precreate(bot_id))
