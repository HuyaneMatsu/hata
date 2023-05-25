import vampytest

from ....core import BUILTIN_EMOJIS
from ....guild import Guild
from ....user import ClientUserBase
from ....utils import is_url

from ..soundboard_sound import SoundBoardSound

from .test__SoundBoardSound__constructor import _assert_fields_set


def test__SoundBoardSound__guild():
    """
    Tests whether ``SoundBoardSound.guild`` works as intended.
    """
    guild_id_0 = 202305240042
    guild_id_1 = 202305240043
    
    guild = Guild.precreate(guild_id_0)
    
    for sound_id, input_guild_id, expected_output in (
        (202305240044, guild_id_0, guild),
        (202305240045, guild_id_1, None),
        (202305240046, 0, None),
    ):
        sound = SoundBoardSound.precreate(sound_id, guild_id = input_guild_id)
        vampytest.assert_is(sound.guild, expected_output)


def test__SoundBoardSound__user():
    """
    Tests whether ``SoundBoardSound.user`` works as intended.
    """
    user_id = 202305240047
    
    sound = SoundBoardSound(user_id = user_id)
    user = sound.user
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    
    test_user = sound.user
    vampytest.assert_is(test_user, user)


def test__SoundBoard__partial():
    """
    Tests whether ``SoundBoard.partial`` works as intended.
    """
    sound = SoundBoardSound()
    output = sound.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)
    
    sound_id = 202305240048
    sound = SoundBoardSound.precreate(sound_id)
    output = sound.partial
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def test__SoundBoardSound__copy():
    """
    Tests whether ``SoundBoardSound.copy`` works as intended.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    user_id = 202305240049
    volume = 0.69
    
    sound = SoundBoardSound(
        available = available,
        emoji = emoji,
        name = name,
        user_id = user_id,
        volume = volume,
    )
    
    copy = sound.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(sound, copy)
    
    vampytest.assert_eq(sound, copy)


def test__SoundBoardSound__copy_with__0():
    """
    Tests whether ``SoundBoardSound.copy_with`` works as intended.
    
    Case: No fields overwritten.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    user_id = 202305240050
    volume = 0.69
    
    sound = SoundBoardSound(
        available = available,
        emoji = emoji,
        name = name,
        user_id = user_id,
        volume = volume,
    )
    
    copy = sound.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(sound, copy)
    
    vampytest.assert_eq(sound, copy)


def test__SoundBoardSound__copy_with__1():
    """
    Tests whether ``SoundBoardSound.copy_with`` works as intended.
    
    Case: All fields overwritten.
    """
    old_available = False
    old_emoji = BUILTIN_EMOJIS['heart']
    old_name = 'rember'
    old_user_id = 202305240051
    old_volume = 0.69
    
    new_available = True
    new_emoji = BUILTIN_EMOJIS['x']
    new_name = 'happy day'
    new_user_id = 202305240052
    new_volume = 0.70
    
    sound = SoundBoardSound(
        available = old_available,
        emoji = old_emoji,
        name = old_name,
        user_id = old_user_id,
        volume = old_volume,
    )
    
    copy = sound.copy_with(
        available = new_available,
        emoji = new_emoji,
        name = new_name,
        user_id = new_user_id,
        volume = new_volume,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(sound, copy)
    
    vampytest.assert_eq(copy.available, new_available)
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.user_id, new_user_id)
    vampytest.assert_eq(copy.volume, new_volume)


def test__SoundBoardSound__url():
    """
    tests whether ``SoundBoardSound.url`` works as intended.
    """
    sound_id = 202305240054
    
    sound = SoundBoardSound.precreate(sound_id)
    output = sound.url
    
    vampytest.assert_instance(output, str)
    vampytest.assert_true(is_url(output))
    vampytest.assert_in(str(sound_id), output)
