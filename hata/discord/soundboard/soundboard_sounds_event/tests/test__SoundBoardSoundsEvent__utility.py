import vampytest

from ....guild import Guild

from ...soundboard_sound import SoundBoardSound

from ..soundboard_sounds_event import SoundBoardSoundsEvent

from .test__SoundBoardSoundsEvent__constructor import _assert_fields_set


def test__SoundBoardSoundsEvent__copy():
    """
    Tests whether ``SoundBoardSoundsEvent.copy`` works as intended.
    """
    guild_id = 202305270021
    sounds = [SoundBoardSound.precreate(202305270022), SoundBoardSound.precreate(202305270023)]
    
    soundboard_sounds_event = SoundBoardSoundsEvent(
        guild_id = guild_id,
        sounds = sounds,
    )
    
    copy = soundboard_sounds_event.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(soundboard_sounds_event, copy)

    vampytest.assert_eq(soundboard_sounds_event, copy)


def test__SoundBoardSoundsEvent__copy_with__0():
    """
    Tests whether ``SoundBoardSoundsEvent.copy_with`` works as intended.
    
    Case: no fields given.
    """
    guild_id = 202305270024
    sounds = [SoundBoardSound.precreate(202305270025), SoundBoardSound.precreate(202305270026)]
    
    soundboard_sounds_event = SoundBoardSoundsEvent(
        guild_id = guild_id,
        sounds = sounds,
    )
    copy = soundboard_sounds_event.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(soundboard_sounds_event, copy)

    vampytest.assert_eq(soundboard_sounds_event, copy)


def test__SoundBoardSoundsEvent__copy_with__1():
    """
    Tests whether ``SoundBoardSoundsEvent.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_guild_id = 202305270027
    old_sounds = [SoundBoardSound.precreate(202305270028), SoundBoardSound.precreate(202305270029)]
    
    new_guild_id = 202305270030
    new_sounds = [SoundBoardSound.precreate(202305270031), SoundBoardSound.precreate(202305270032)]
    
    soundboard_sounds_event = SoundBoardSoundsEvent(
        guild_id = old_guild_id,
        sounds = old_sounds,
    )
    copy = soundboard_sounds_event.copy_with(
        guild_id = new_guild_id,
        sounds = new_sounds,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(soundboard_sounds_event, copy)
    
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.sounds, tuple(new_sounds))


def test__SoundBoardSoundsEvent__guild__0():
    """
    Tests whether ``SoundBoardSoundsEvent.guild`` works as intended.
    
    Case: Not cached.
    """
    guild_id = 202305270033
    
    soundboard_sounds_event = SoundBoardSoundsEvent(guild_id = guild_id)
    
    output = soundboard_sounds_event.guild
    vampytest.assert_is(output, None)


def test__SoundBoardSoundsEvent__guild__1():
    """
    Tests whether ``SoundBoardSoundsEvent.guild`` works as intended.
    
    Case: Cached.
    """
    guild_id = 202305270034
    
    guild = Guild.precreate(guild_id)
    
    soundboard_sounds_event = SoundBoardSoundsEvent(guild_id = guild_id)
    
    vampytest.assert_is(soundboard_sounds_event.guild, guild)


def test__SoundBoardSoundsEvent__iter_sounds():
    """
    Tests whether ``SoundBoardSoundsEvent.iter_sounds`` works as intended.
    """
    sound_0 = SoundBoardSound.precreate(202305270035)
    sound_1 = SoundBoardSound.precreate(202305270036)
    
    for input_value, expected_output in (
        (None, []),
        ([sound_0], [sound_0]),
        ([sound_0, sound_1], [sound_0, sound_1]),
    ):
        soundboard_sounds_event = SoundBoardSoundsEvent(sounds = input_value)
        vampytest.assert_eq([*soundboard_sounds_event.iter_sounds()], expected_output)
