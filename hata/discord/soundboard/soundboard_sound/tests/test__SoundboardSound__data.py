import vampytest

from ....client import Client
from ....core import BUILTIN_EMOJIS
from ....guild import Guild
from ....user import User

from ..soundboard_sound import SoundboardSound

from .test__SoundboardSound__constructor import _assert_fields_set


def test__SoundboardSound__from_data__0():
    """
    Tests whether ``SoundboardSound.from_data`` works as intended.
    
    Case : All fields given.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    user_id = 202305240023
    volume = 0.69
    
    sound_id = 202305240024
    guild_id = 202305240025
    user = User.precreate(user_id, name = 'happy day')
    
    data = {
        'sound_id': str(sound_id),
        'guild_id': str(guild_id),
        'available': available,
        'emoji_name': emoji.unicode,
        'emoji_id': None,
        'name': name,
        'user_id': str(user_id),
        'volume': volume,
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    sound = SoundboardSound.from_data(data)
    _assert_fields_set(sound)
    
    vampytest.assert_eq(sound.available, available)
    vampytest.assert_is(sound.emoji, emoji)
    vampytest.assert_eq(sound.name, name)
    vampytest.assert_eq(sound.user_id, user_id)
    vampytest.assert_eq(sound.volume, volume)
    
    vampytest.assert_eq(sound.id, sound_id)
    vampytest.assert_eq(sound.guild_id, guild_id)
    vampytest.assert_is(sound._cache_user, user)


def test__SoundboardSound__from_data__1():
    """
    Tests whether ``SoundboardSound.from_data`` works as intended.
    
    Case : Caching.
    """
    sound_id = 202305240026
    guild_id = 202305270037
    
    data = {
        'sound_id': str(sound_id),
        'guild_id': str(guild_id),
    }
    
    guild = Guild.precreate(guild_id)
    
    sound = SoundboardSound.from_data(data)
    
    vampytest.assert_eq(guild.soundboard_sounds, {sound_id: sound})
    
    test_sound = SoundboardSound.from_data(data)
    vampytest.assert_is(sound, test_sound)


def test__SoundboardSound__to_data():
    """
    Tests whether ``SoundboardSound.to_data`` works as intended.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    user_id = 202305240027
    volume = 0.69
    
    sound_id = 202305240028
    guild_id = 202305240029
    user = User.precreate(user_id, name = 'happy day')
    
    expected_output = {
        'sound_id': str(sound_id),
        'guild_id': str(guild_id),
        'available': available,
        'emoji_name': emoji.unicode,
        'name': name,
        'user_id': str(user_id),
        'volume': volume,
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    sound = SoundboardSound.precreate(
        sound_id,
        guild_id = guild_id,
        available = available,
        emoji = emoji,
        name = name,
        user_id = user_id,
        volume = volume,
    )
    
    vampytest.assert_eq(
        sound.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__SoundboardSound__set_attributes():
    """
    Tests whether ``SoundboardSound._set_attributes`` works as intended.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    user_id = 202305240030
    volume = 0.69
    
    guild_id = 202305240031
    user = User.precreate(user_id, name = 'happy day')
    
    data = {
        'guild_id': str(guild_id),
        'available': available,
        'emoji_name': emoji.unicode,
        'emoji_id': None,
        'name': name,
        'user_id': str(user_id),
        'volume': volume,
        'user': user.to_data(defaults = True, include_internals = True),
    }
    
    sound = SoundboardSound()
    
    sound._set_attributes(data)
    
    vampytest.assert_eq(sound.available, available)
    vampytest.assert_is(sound.emoji, emoji)
    vampytest.assert_eq(sound.name, name)
    vampytest.assert_eq(sound.user_id, user_id)
    vampytest.assert_eq(sound.volume, volume)
    
    vampytest.assert_eq(sound.guild_id, guild_id)
    vampytest.assert_is(sound._cache_user, user)


def test__SoundboardSound__update_attributes():
    """
    Tests whether ``SoundboardSound._update_attributes`` works as intended.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    volume = 0.69
    
    data = {
        'available': available,
        'emoji_name': emoji.unicode,
        'emoji_id': None,
        'name': name,
        'volume': volume,
    }
    
    sound = SoundboardSound()
    
    sound._update_attributes(data)
    
    vampytest.assert_eq(sound.available, available)
    vampytest.assert_is(sound.emoji, emoji)
    vampytest.assert_eq(sound.name, name)
    vampytest.assert_eq(sound.volume, volume)


def test__SoundboardSound__difference_update_attributes():
    """
    Tests whether ``SoundboardSound._difference_update_attributes`` works as intended.
    """
    old_available = False
    old_emoji = BUILTIN_EMOJIS['heart']
    old_name = 'rember'
    old_volume = 0.69
    
    new_available = True
    new_emoji = BUILTIN_EMOJIS['x']
    new_name = 'happy day'
    new_volume = 0.70
    
    data = {
        'available': new_available,
        'emoji_name': new_emoji.unicode,
        'emoji_id': None,
        'name': new_name,
        'volume': new_volume,
    }
    
    sound = SoundboardSound(
        available = old_available,
        emoji = old_emoji,
        name = old_name,
        volume = old_volume,
    )
    
    output = sound._difference_update_attributes(data)
    
    vampytest.assert_eq(sound.available, new_available)
    vampytest.assert_is(sound.emoji, new_emoji)
    vampytest.assert_eq(sound.name, new_name)
    vampytest.assert_eq(sound.volume, new_volume)
    
    vampytest.assert_eq(
        output,
        {
            'available': old_available,
            'emoji': old_emoji,
            'name': old_name,
            'volume': old_volume,
        },
    )


def test__SoundboardSound__from_data_is_created__0():
    """
    Tests whether ``SoundboardSound.from_data_is_created`` works as intended.
    
    Case: not cached.
    """
    sound_id = 202305270044
    guild_id = 202305270045
    name = 'rember'
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'sound_id': str(sound_id),
        'guild_id': str(guild_id),
        'name': name,
    }
    
    sound, is_created = SoundboardSound.from_data_is_created(data)
    _assert_fields_set(sound)
    vampytest.assert_instance(is_created, bool)
    vampytest.assert_eq(is_created, True)
    vampytest.assert_eq(sound.name, name)
    vampytest.assert_eq(guild.soundboard_sounds, {sound_id: sound})
    
    test_sound = SoundboardSound.from_data(data)
    vampytest.assert_is(sound, test_sound)


def test__SoundboardSound__from_data_is_created__1():
    """
    Tests whether ``SoundboardSound.from_data_is_created`` works as intended.
    
    Case: cached.
    """
    client = Client(
        token = 'token_202305270001',
    )
    try:
        sound_id = 202305270045
        guild_id = 202305270046
        name = 'rember'
        
        cached_sound = SoundboardSound.precreate(sound_id, guild_id = guild_id)
        guild = Guild.precreate(guild_id)
        guild.clients = [client]
        guild.soundboard_sounds = {sound_id: cached_sound}
        
        data = {
            'sound_id': str(sound_id),
            'guild_id': str(guild_id),
            'name': name,
        }
        
        sound, is_created = SoundboardSound.from_data_is_created(data)
        _assert_fields_set(sound)
        vampytest.assert_is(sound, cached_sound)
        
        vampytest.assert_instance(is_created, bool)
        vampytest.assert_eq(is_created, False)
        
        # The sound was already up to date, name should not be updated.
        vampytest.assert_ne(sound.name, name)
        
        
    finally:
        # Cleanup
        client._delete()
        client = None
