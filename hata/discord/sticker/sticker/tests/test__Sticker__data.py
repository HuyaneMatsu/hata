import vampytest

from ....user import User

from ..preinstanced import StickerFormat, StickerType
from ..sticker import Sticker

from .test__Sticker__constructor import _assert_fields_set


def test__Sticker__from_data__0():
    """
    Tests whether ``Sticker.from_data`` works as intended.
    
    Case: default.
    """
    sticker_id = 202201070009
    guild_id = 202201070010
    
    available = True
    description = 'komeiji'
    name = 'koishi'
    pack_id = 202201070011
    sort_value = 4
    sticker_format = StickerFormat.png
    sticker_type = StickerType.guild
    tags = ['rin', 'okuu']
    user = User.precreate(202201070012)
    
    data = {
        'id': str(sticker_id),
        'guild_id': str(guild_id),
        'available': available,
        'description': description,
        'name': name,
        'pack_id': str(pack_id),
        'sort_value': sort_value,
        'format_type': sticker_format.value,
        'type': sticker_type.value,
        'tags': ', '.join(tags),
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    sticker = Sticker.from_data(data)
    _assert_fields_set(sticker)
    
    vampytest.assert_eq(sticker.available, available)
    vampytest.assert_eq(sticker.description, description)
    vampytest.assert_is(sticker.format, sticker_format)
    vampytest.assert_eq(sticker.name, name)
    vampytest.assert_eq(sticker.pack_id, pack_id)
    vampytest.assert_eq(sticker.sort_value, sort_value)
    vampytest.assert_eq(sticker.tags, frozenset(tags))
    vampytest.assert_is(sticker.type, sticker_type)
    vampytest.assert_is(sticker.user, user)
    
    vampytest.assert_eq(sticker.id, sticker_id)
    vampytest.assert_eq(sticker.guild_id, guild_id)


def test__Sticker__from_data__1():
    """
    Tests whether ``Sticker.from_data`` works as intended.
    
    Case: default.
    """
    sticker_id = 202201070013
    
    data = {
        'id': str(sticker_id),
    }
    
    sticker = Sticker.from_data(data)
    test_sticker = Sticker.from_data(data)
    
    vampytest.assert_is(sticker, test_sticker)


def test__Sticker__to_data():
    """
    Tests whether ``Sticker.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    sticker_id = 202201070016
    guild_id = 202201070017
    
    available = True
    description = 'komeiji'
    name = 'koishi'
    pack_id = 202201070018
    sort_value = 4
    sticker_format = StickerFormat.png
    sticker_type = StickerType.guild
    tags = ['orin']
    user = User.precreate(202201070019)
    
    sticker = Sticker.precreate(
        sticker_id,
        guild_id = guild_id,
        available = available,
        description = description,
        name = name,
        pack_id = pack_id,
        sort_value = sort_value,
        sticker_format = sticker_format,
        sticker_type = sticker_type,
        tags = tags,
        user = user,
    )
    
    expected_output = {
        'id': str(sticker_id),
        'guild_id': str(guild_id),
        'available': available,
        'description': description,
        'name': name,
        'pack_id': str(pack_id),
        'sort_value': sort_value,
        'format_type': sticker_format.value,
        'type': sticker_type.value,
        'tags': ', '.join(tags),
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    vampytest.assert_eq(
        sticker.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__Sticker__set_attributes():
    """
    Tests whether ``Sticker._set_attributes`` works as intended.
    """
    guild_id = 202201070021
    
    available = True
    description = 'komeiji'
    name = 'koishi'
    pack_id = 202201070022
    sort_value = 4
    sticker_format = StickerFormat.png
    sticker_type = StickerType.guild
    tags = ['rin', 'okuu']
    user = User.precreate(202201070023)
    
    data = {
        'guild_id': str(guild_id),
        'available': available,
        'description': description,
        'name': name,
        'pack_id': str(pack_id),
        'sort_value': sort_value,
        'format_type': sticker_format.value,
        'type': sticker_type.value,
        'tags': ', '.join(tags),
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    sticker = Sticker()
    sticker._set_attributes(data)
    
    vampytest.assert_eq(sticker.available, available)
    vampytest.assert_eq(sticker.description, description)
    vampytest.assert_is(sticker.format, sticker_format)
    vampytest.assert_eq(sticker.name, name)
    vampytest.assert_eq(sticker.pack_id, pack_id)
    vampytest.assert_eq(sticker.sort_value, sort_value)
    vampytest.assert_eq(sticker.tags, frozenset(tags))
    vampytest.assert_is(sticker.type, sticker_type)
    vampytest.assert_is(sticker.user, user)
    
    vampytest.assert_eq(sticker.guild_id, guild_id)


def test__Sticker__update_attributes():
    """
    Tests whether ``Sticker._update_attributes`` works as intended.
    """
    available = True
    description = 'komeiji'
    name = 'koishi'
    sort_value = 4
    tags = ['rin', 'okuu']
    user = User.precreate(202201070024)
    
    data = {
        'available': available,
        'description': description,
        'name': name,
        'sort_value': sort_value,
        'tags': ', '.join(tags),
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    sticker = Sticker()
    sticker._update_attributes(data)
    
    vampytest.assert_eq(sticker.available, available)
    vampytest.assert_eq(sticker.description, description)
    vampytest.assert_eq(sticker.name, name)
    vampytest.assert_eq(sticker.sort_value, sort_value)
    vampytest.assert_eq(sticker.tags, frozenset(tags))
    vampytest.assert_is(sticker.user, user)



def test__Sticker__difference_update_attributes():
    """
    Tests whether ``Sticker._difference_update_attributes`` works as intended.
    """
    old_available = True
    old_description = 'komeiji'
    old_name = 'koishi'
    old_sort_value = 4
    old_tags = ['rin', 'okuu']
    new_available = False
    new_description = 'third'
    new_name = 'eye'
    new_sort_value = 2
    new_tags = ['orin',]
    
    user = User.precreate(202201070025)
    
    data = {
        'available': new_available,
        'description': new_description,
        'name': new_name,
        'sort_value': new_sort_value,
        'tags': ', '.join(new_tags),
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    sticker = Sticker(
        available = old_available,
        description = old_description,
        name = old_name,
        sort_value = old_sort_value,
        tags = old_tags,
    )
    
    old_attributes = sticker._difference_update_attributes(data)
    
    vampytest.assert_eq(sticker.available, new_available)
    vampytest.assert_eq(sticker.description, new_description)
    vampytest.assert_eq(sticker.name, new_name)
    vampytest.assert_eq(sticker.sort_value, new_sort_value)
    vampytest.assert_eq(sticker.tags, frozenset(new_tags))
    vampytest.assert_is(sticker.user, user)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'available': old_available,
            'description': old_description,
            'name': old_name,
            'sort_value': old_sort_value,
            'tags': frozenset(old_tags),
        },
    )
