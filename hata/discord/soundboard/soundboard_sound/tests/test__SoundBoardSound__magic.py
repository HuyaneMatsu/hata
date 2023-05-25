import vampytest

from ....core import BUILTIN_EMOJIS

from ..soundboard_sound import SoundBoardSound


def test__SoundBoardSound__repr():
    """
    Tests whether ``SoundBoardSound.__repr__`` works as intended.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    user_id = 202305240032
    volume = 0.69
    
    sound_id = 202305240033
    guild_id = 202305240034
    
    sound = SoundBoardSound.precreate(
        sound_id,
        guild_id = guild_id,
        available = available,
        emoji = emoji,
        name = name,
        user_id = user_id,
        volume = volume,
    )
    
    vampytest.assert_instance(repr(sound), str)


def test__SoundBoardSound__hash():
    """
    Tests whether ``SoundBoardSound.__hash__`` works as intended.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    user_id = 202305240035
    volume = 0.69
    
    sound_id = 202305240036
    guild_id = 202305240037
    
    keyword_parameters = {
        'available': available,
        'emoji': emoji,
        'name': name,
        'user_id': user_id,
        'volume': volume,
    }
    
    sound = SoundBoardSound.precreate(
        sound_id,
        guild_id = guild_id,
        **keyword_parameters,
    )
    
    vampytest.assert_instance(repr(sound), str)

    sound = SoundBoardSound(**keyword_parameters)
    
    vampytest.assert_instance(repr(sound), str)


def test__SoundBoardSound__eq():
    """
    Tests whether ``SoundBoardSound.__eq__`` works as intended.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    user_id = 202305240038
    volume = 0.69
    
    sound_id = 202305240039
    guild_id = 202305240040
    
    keyword_parameters = {
        'available': available,
        'emoji': emoji,
        'name': name,
        'user_id': user_id,
        'volume': volume,
    }
    
    sound = SoundBoardSound.precreate(
        sound_id,
        guild_id = guild_id,
        **keyword_parameters,
    )
    
    vampytest.assert_eq(sound, sound)
    vampytest.assert_ne(sound, object())
    
    test_sound = SoundBoardSound(**keyword_parameters,)
    
    vampytest.assert_eq(sound, test_sound)
    
    for field_name, field_value in (
        ('available', True),
        ('emoji', BUILTIN_EMOJIS['x']),
        ('name', 'happy day'),
        ('user_id', 202305240041),
        ('volume', 0.70),
    ):
        test_sound = SoundBoardSound(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(test_sound, sound)
