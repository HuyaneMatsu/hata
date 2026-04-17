import vampytest

from ....user import User

from ..emoji import Emoji


def test__Emoji__repr():
    """
    Tests whether ``Emoji.__repr__`` works as intended.
    
    Case: All fields given.
    """
    emoji_id = 202301010022
    guild_id = 202301010023
    
    animated = True
    available = True
    managed = True
    name = 'eclipse'
    require_colons = True
    role_ids = [202301010024, 202301010025]
    user = User.precreate(202301010026)
    
    emoji = Emoji.precreate(
        emoji_id,
        guild_id = guild_id,
        animated = animated,
        available = available,
        managed = managed,
        name = name,
        require_colons = require_colons,
        role_ids = role_ids,
        user = user,
    )
    
    vampytest.assert_instance(repr(emoji), str)


def test__Emoji__format():
    """
    Tests whether ``Emoji.__format__`` works as intended.
    
    Case: All fields given.
    """
    emoji = Emoji()
    
    vampytest.assert_instance(format(emoji, ''), str)
    vampytest.assert_instance(format(emoji, 'e'), str)
    vampytest.assert_instance(format(emoji, 'r'), str)
    vampytest.assert_instance(format(emoji, 'c'), str)


def test__Emoji__hash():
    """
    Tests whether ``Emoji.__repr__`` works as intended.
    
    Case: All fields given.
    """
    emoji_id = 202301010027
    guild_id = 202301010028
    
    animated = True
    available = True
    managed = True
    name = 'eclipse'
    require_colons = True
    role_ids = [202301010029, 202301010030]
    user = User.precreate(202301010031)
    
    keyword_parameters = {
        'animated': animated,
        'available': available,
        'managed': managed,
        'name': name,
        'require_colons': require_colons,
        'role_ids': role_ids,
        'user': user,
    }
    
    emoji = Emoji.precreate(
        emoji_id,
        guild_id = guild_id,
        **keyword_parameters,
    )
    
    vampytest.assert_instance(hash(emoji), int)


    emoji = Emoji(
        **keyword_parameters,
    )
    
    vampytest.assert_instance(hash(emoji), int)


def test__Emoji__eq():
    """
    Tests whether ``Emoji.__eq__`` works as intended.
    """
    emoji_id_0 = 202301010032
    emoji_id_1 =  202301010037
    guild_id = 202301010033
    
    animated = True
    available = True
    managed = True
    name = 'eclipse'
    require_colons = True
    role_ids = [202301010034, 202301010035]
    user = User.precreate(202301010036)
    
    keyword_parameters = {
        'animated': animated,
        'available': available,
        'managed': managed,
        'name': name,
        'require_colons': require_colons,
        'role_ids': role_ids,
        'user': user,
    }
    
    emoji = Emoji.precreate(
        emoji_id_0,
        guild_id = guild_id,
        **keyword_parameters,
    )
    vampytest.assert_eq(emoji, emoji)
    vampytest.assert_ne(emoji, object())
    
    test_emoji = Emoji.precreate(
        emoji_id_1,
        guild_id = guild_id,
        **keyword_parameters,
    )
    vampytest.assert_ne(emoji, test_emoji)
    
    test_emoji = Emoji(**keyword_parameters)
    vampytest.assert_eq(emoji, test_emoji)
    
    for field_name, field_value in (
        ('animated', False),
        ('available', False),
        ('managed', False),
        ('name', 'azuki'),
        ('require_colons', False),
        ('role_ids', None),
        ('user', None),
    ):
        test_emoji = Emoji(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(emoji, test_emoji)
