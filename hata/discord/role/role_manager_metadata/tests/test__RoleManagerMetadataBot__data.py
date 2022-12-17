import vampytest

from ..bot import RoleManagerMetadataBot

from .test__RoleManagerMetadataBot__constructor import _assert_is_every_attribute_set


def test__RoleManagerMetadataBot__from_data():
    """
    Tests whether ``RoleManagerMetadataBot.from_data`` works as intended.
    """
    bot_id = 202212160004
    
    data = {
        'bot_id': str(bot_id)
    }
    
    metadata = RoleManagerMetadataBot.from_data(data)
    _assert_is_every_attribute_set(metadata)
    
    vampytest.assert_eq(metadata.bot_id, bot_id)


def test__RoleManagerMetadataBot__to_data():
    """
    Tests whether ``RoleManagerMetadataBot.to_data`` works as intended.
    """
    bot_id = 202212160005
    
    metadata = RoleManagerMetadataBot(
        bot_id = bot_id
    )
    
    expected_data = {
        'bot_id': str(bot_id),
    }
    
    vampytest.assert_eq(
        metadata.to_data(defaults = True),
        expected_data
    )
