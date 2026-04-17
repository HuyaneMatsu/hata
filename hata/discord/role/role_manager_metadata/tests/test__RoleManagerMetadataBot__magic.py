import vampytest

from ..bot import RoleManagerMetadataBot


def test__RoleManagerMetadataBot__repr():
    """
    Tests whether ``RoleManagerMetadataBot.__repr__`` works as intended.
    """
    bot_id = 202212160006
    
    metadata = RoleManagerMetadataBot(
        bot_id = bot_id,
    )
    
    vampytest.assert_instance(repr(metadata), str)


def test__RoleManagerMetadataBot__hash():
    """
    Tests whether ``RoleManagerMetadataBot.__hash__`` works as intended.
    """
    bot_id = 202212160007
    
    metadata = RoleManagerMetadataBot(
        bot_id = bot_id,
    )
    
    vampytest.assert_instance(hash(metadata), int)


def test__RoleManagerMetadataBot__eq():
    """
    Tests whether ``RoleManagerMetadataBot.__hash__`` works as intended.
    """
    bot_id = 202212160008
    
    keyword_parameters = {
        'bot_id': bot_id
    }
    
    metadata = RoleManagerMetadataBot(**keyword_parameters)
    
    vampytest.assert_eq(metadata, metadata)
    vampytest.assert_ne(metadata, object())
    
    for field_name, field_value in (
        ('bot_id', 202212160009),
    ):
        test_metadata = RoleManagerMetadataBot(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(metadata, test_metadata)
