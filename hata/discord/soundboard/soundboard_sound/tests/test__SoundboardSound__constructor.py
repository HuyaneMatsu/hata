import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji
from ....user import ClientUserBase

from ..soundboard_sound import SoundboardSound


def _assert_fields_set(sound):
    """
    Asserts whether every fields are set of the given `sound`.
    
    Parameters
    ----------
    sound : ``SoundboardSound``
        The sound to check.
    """
    vampytest.assert_instance(sound, SoundboardSound)
    vampytest.assert_instance(sound._cache_user, ClientUserBase, nullable = True)
    vampytest.assert_instance(sound.available, bool)
    vampytest.assert_instance(sound.emoji, Emoji, nullable = True)
    vampytest.assert_instance(sound.guild_id, int)
    vampytest.assert_instance(sound.name, str)
    vampytest.assert_instance(sound.user_id, int)
    vampytest.assert_instance(sound.volume, float)


def test__SoundboardSound__new__0():
    """
    Tests whether ``SoundboardSound.__new__`` works as intended.
    
    Case : No fields given.
    """
    sound = SoundboardSound()
    _assert_fields_set(sound)


def test__SoundboardSound__new__1():
    """
    Tests whether ``SoundboardSound.__new__`` works as intended.
    
    Case : All fields given.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    user_id = 202305240015
    volume = 0.69
    
    sound = SoundboardSound(
        available = available,
        emoji = emoji,
        name = name,
        user_id = user_id,
        volume = volume,
    )
    _assert_fields_set(sound)
    
    vampytest.assert_eq(sound.available, available)
    vampytest.assert_is(sound.emoji, emoji)
    vampytest.assert_eq(sound.name, name)
    vampytest.assert_eq(sound.user_id, user_id)
    vampytest.assert_eq(sound.volume, volume)


def test__SoundboardSound__precreate__0():
    """
    Tests whether ``SoundboardSound.precreate`` works as intended.
    
    Case : No fields given.
    """
    sound_id = 202305240016
    
    sound = SoundboardSound.precreate(sound_id)
    _assert_fields_set(sound)
    
    vampytest.assert_eq(sound.id, sound_id)


def test__SoundboardSound__precreate__1():
    """
    Tests whether ``SoundboardSound.precreate`` works as intended.
    
    Case : All fields given.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    user_id = 202305240017
    volume = 0.69
    
    sound_id = 202305240018
    guild_id = 202305240019
    
    sound = SoundboardSound.precreate(
        sound_id,
        guild_id = guild_id,
        available = available,
        emoji = emoji,
        name = name,
        user_id = user_id,
        volume = volume,
    )
    _assert_fields_set(sound)
    
    vampytest.assert_eq(sound.available, available)
    vampytest.assert_is(sound.emoji, emoji)
    vampytest.assert_eq(sound.name, name)
    vampytest.assert_eq(sound.user_id, user_id)
    vampytest.assert_eq(sound.volume, volume)
    
    vampytest.assert_eq(sound.id, sound_id)
    vampytest.assert_eq(sound.guild_id, guild_id)


def test__SoundboardSound__precreate__2():
    """
    Tests whether ``SoundboardSound.precreate`` works as intended.
    
    Case : Caching.
    """
    sound_id = 202305240020
    
    sound = SoundboardSound.precreate(sound_id)
    test_sound = SoundboardSound.precreate(sound_id)
    vampytest.assert_is(sound, test_sound)


def test__SoundboardSound__create_empty():
    """
    Tests whether ``SoundboardSound._create_empty`` works as intended.
    """
    sound_id = 202305240021
    guild_id = 202305240022
    
    sound = SoundboardSound._create_empty(sound_id, guild_id)
    _assert_fields_set(sound)
    
    vampytest.assert_eq(sound.id, sound_id)
    vampytest.assert_eq(sound.guild_id, guild_id)
