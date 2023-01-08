import vampytest

from ....guild import Guild
from ....user import User

from ..emoji import Emoji

from .test__Emoji__constructor import _assert_fields_set


def test__Emoji__from_data__0():
    """
    Tests whether ``Emoji.from_data`` works as intended.
    
    Case: Fields.
    """
    emoji_id = 202301010010
    guild_id = 202301010011
    
    animated = True
    available = True
    managed = True
    name = 'eclipse'
    require_colons = True
    role_ids = [202301010012, 202301010013]
    user = User.precreate(202301010014)
    
    data = {
        'id': str(emoji_id),
        'animated': animated,
        'available': available,
        'managed': managed,
        'name': name,
        'require_colons': require_colons,
        'roles': [str(role_id) for role_id in role_ids],
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    emoji = Emoji.from_data(data, guild_id)
    _assert_fields_set(emoji)
    
    vampytest.assert_eq(emoji.id, emoji_id)
    vampytest.assert_eq(emoji.guild_id, guild_id)
    
    vampytest.assert_eq(emoji.animated, animated)
    vampytest.assert_eq(emoji.available, available)
    vampytest.assert_eq(emoji.managed, managed)
    vampytest.assert_eq(emoji.name, name)
    vampytest.assert_eq(emoji.require_colons, require_colons)
    vampytest.assert_eq(emoji.role_ids, tuple(role_ids))
    vampytest.assert_is(emoji.user, user)


def test__Emoji__from_data__1():
    """
    Tests whether ``Emoji.from_data`` works as intended.
    
    Case: Caching.
    """
    emoji_id = 202301010015
    guild_id = 202301010016
    
    data = {
        'id': str(emoji_id),
    }
    
    emoji = Emoji.from_data(data, guild_id)
    test_emoji = Emoji.from_data(data, guild_id)
    vampytest.assert_is(emoji, test_emoji)


def test__Emoji__to_data():
    """
    Tests whether ``Emoji.to_data`` works as intended.
    
    Case: Include defaults and internals.
    """
    emoji_id = 202301010017
    guild_id = 202301010018
    
    animated = True
    available = True
    managed = True
    name = 'eclipse'
    require_colons = True
    role_ids = [202301010019, 202301010020]
    user = User.precreate(202301010021)
    
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
    
    expected_output = {
        'id': str(emoji_id),
        'animated': animated,
        'available': available,
        'managed': managed,
        'name': name,
        'require_colons': require_colons,
        'roles': [str(role_id) for role_id in role_ids],
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    vampytest.assert_eq(
        emoji.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__Emoji__set_attributes():
    """
    Tests whether ``Emoji._set_attributes`` works as intended.
    """
    guild_id = 202301010045
    
    animated = True
    available = True
    managed = True
    name = 'eclipse'
    require_colons = True
    role_ids = [202301010046, 202301010047]
    user = User.precreate(202301010048)
    
    emoji = Emoji()
    
    data = {
        'animated': animated,
        'available': available,
        'managed': managed,
        'name': name,
        'require_colons': require_colons,
        'roles': [str(role_id) for role_id in role_ids],
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    emoji._set_attributes(data, guild_id)
    
    vampytest.assert_eq(emoji.guild_id, guild_id)
    
    vampytest.assert_eq(emoji.animated, animated)
    vampytest.assert_eq(emoji.available, available)
    vampytest.assert_eq(emoji.managed, managed)
    vampytest.assert_eq(emoji.name, name)
    vampytest.assert_eq(emoji.require_colons, require_colons)
    vampytest.assert_eq(emoji.role_ids, tuple(role_ids))
    vampytest.assert_is(emoji.user, user)


def test__Emoji_update__attributes():
    """
    Tests whether ``Emoji._update_attributes`` works as intended.
    """
    animated = True
    available = True
    managed = True
    name = 'eclipse'
    require_colons = True
    role_ids = [202301010049, 202301010050]
    user = User.precreate(202301010051)
    
    emoji = Emoji()
    
    data = {
        'animated': animated,
        'available': available,
        'managed': managed,
        'name': name,
        'require_colons': require_colons,
        'roles': [str(role_id) for role_id in role_ids],
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    emoji._update_attributes(data)
    
    vampytest.assert_eq(emoji.animated, animated)
    vampytest.assert_eq(emoji.available, available)
    vampytest.assert_eq(emoji.managed, managed)
    vampytest.assert_eq(emoji.name, name)
    vampytest.assert_eq(emoji.require_colons, require_colons)
    vampytest.assert_eq(emoji.role_ids, tuple(role_ids))
    vampytest.assert_is(emoji.user, user)


def test__Emoji__difference_update_attributes():
    """
    Tests whether ``Emoji._difference_update_attributes`` works as intended.
    """
    user = User.precreate(202301010054)
    
    old_animated = True
    old_available = True
    old_managed = True
    old_name = 'eclipse'
    old_require_colons = True
    old_role_ids = [202301010052, 202301010053]
    
    new_animated = False
    new_available = False
    new_managed = False
    new_name = 'patchouli'
    new_require_colons = False
    new_role_ids = [202301010055, 202301010056]
    
    emoji = Emoji(
        animated = old_animated,
        available = old_available,
        managed = old_managed,
        name = old_name,
        require_colons = old_require_colons,
        role_ids = old_role_ids,
    )
    
    data = {
        'animated': new_animated,
        'available': new_available,
        'managed': new_managed,
        'name': new_name,
        'require_colons': new_require_colons,
        'roles': [str(role_id) for role_id in new_role_ids],
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    old_attributes = emoji._difference_update_attributes(data)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'animated': old_animated,
            'available': old_available,
            'managed': old_managed,
            'name': old_name,
            'require_colons': old_require_colons,
            'role_ids': tuple(old_role_ids),
        },
    )
    
    vampytest.assert_eq(emoji.animated, new_animated)
    vampytest.assert_eq(emoji.available, new_available)
    vampytest.assert_eq(emoji.managed, new_managed)
    vampytest.assert_eq(emoji.name, new_name)
    vampytest.assert_eq(emoji.require_colons, new_require_colons)
    vampytest.assert_eq(emoji.role_ids, tuple(new_role_ids))
    vampytest.assert_is(emoji.user, user)
