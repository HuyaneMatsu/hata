import vampytest

from ...soundboard_sound import SoundboardSound

from ..soundboard_sounds_event import SoundboardSoundsEvent


def _assert_fields_set(soundboard_sounds_event):
    """
    Checks whether every attribute is set of the given soundboard sounds event.
    
    Parameters
    ----------
    soundboard_sounds_event : ``SoundboardSoundsEvent``
        The soundboard sounds event to check.
    """
    vampytest.assert_instance(soundboard_sounds_event, SoundboardSoundsEvent)
    vampytest.assert_instance(soundboard_sounds_event.guild_id, int)
    vampytest.assert_instance(soundboard_sounds_event.sounds, tuple, nullable = True)


def test__SoundboardSoundsEvent__new__0():
    """
    Tests whether ``SoundboardSoundsEvent.__new__`` works as intended.
    
    Case: No fields given.
    """
    soundboard_sounds_event = SoundboardSoundsEvent()
    _assert_fields_set(soundboard_sounds_event)


def test__SoundboardSoundsEvent__new__1():
    """
    Tests whether ``SoundboardSoundsEvent.__new__`` works as intended.
    
    Case: Fields given.
    """
    guild_id = 202305270000
    sounds = [SoundboardSound.precreate(202305270001), SoundboardSound.precreate(202305270002)]
    
    soundboard_sounds_event = SoundboardSoundsEvent(
        guild_id = guild_id,
        sounds = sounds,
    )
    _assert_fields_set(soundboard_sounds_event)
    
    vampytest.assert_eq(soundboard_sounds_event.guild_id, guild_id)
    vampytest.assert_eq(soundboard_sounds_event.sounds, tuple(sounds))
