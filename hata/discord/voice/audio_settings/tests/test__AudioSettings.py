import vampytest

from ..audio_settings import AudioSettings


def _assert_fields_set(audio_settings):
    """
    Checks whether the audio settings has all of its fields set.
    
    Parameters
    ----------
    audio_settings : ``AudioSettings``
        The audio settings to check.
    """
    vampytest.assert_instance(audio_settings, AudioSettings)
    vampytest.assert_instance(audio_settings.buffer_type, type)
    vampytest.assert_instance(audio_settings.channels, int)
    vampytest.assert_instance(audio_settings.frame_length, int)
    vampytest.assert_instance(audio_settings.frame_size, int)
    vampytest.assert_instance(audio_settings.samples_per_frame, int)
    vampytest.assert_instance(audio_settings.sampling_rate, int)
    vampytest.assert_instance(audio_settings.sample_size, int)
    

def test__AudioSettings__new__no_fields():
    """
    Tests whether ``AudioSettings.__new__`` works as intended.
    
    Case: No fields given.
    """
    audio_settings = AudioSettings()
    _assert_fields_set(audio_settings)


def test__AudioSettings__new__all_fields():
    """
    Tests whether ``AudioSettings.__new__`` works as intended.
    
    Case: All fields given.
    """
    channels = 4
    frame_length = 40
    sampling_rate = 12000
    
    audio_settings = AudioSettings(
        channels = channels,
        frame_length = frame_length,
        sampling_rate = sampling_rate,
    )
    _assert_fields_set(audio_settings)
    
    vampytest.assert_eq(audio_settings.channels, channels)
    vampytest.assert_eq(audio_settings.frame_length, frame_length)
    vampytest.assert_eq(audio_settings.sampling_rate, sampling_rate)


def test__AudioSettings__eq():
    """
    Tests whether ``AudioSettings.__eq__`` works as intended.
    """
    channels = 4
    frame_length = 40
    sampling_rate = 12000
    
    keyword_parameters = {
        'channels': channels,
        'frame_length': frame_length,
        'sampling_rate': sampling_rate,
    }
    
    audio_settings = AudioSettings(**keyword_parameters)
    vampytest.assert_eq(audio_settings, audio_settings)
    vampytest.assert_ne(audio_settings, object())
    
    for field_name, field_value in (
        ('channels', 2),
        ('frame_length', 20),
        ('sampling_rate', 24000),
    ):
        test_audio_settings = AudioSettings(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(test_audio_settings, audio_settings)


def test__AudioSettings__copy():
    """
    Tests whether ``AudioSettings.copy`` works as intended.
    """
    channels = 4
    frame_length = 40
    sampling_rate = 12000
    
    audio_settings = AudioSettings(
        channels = channels,
        frame_length = frame_length,
        sampling_rate = sampling_rate,
    )
    copy = audio_settings.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, audio_settings)
    vampytest.assert_eq(copy, audio_settings)


def test__AudioSettings__copy_with__no_fields():
    """
    Tests whether ``AudioSettings.copy_with`` works as intended.
    
    Case: No fields given.
    """
    channels = 4
    frame_length = 40
    sampling_rate = 12000
    
    audio_settings = AudioSettings(
        channels = channels,
        frame_length = frame_length,
        sampling_rate = sampling_rate,
    )
    copy = audio_settings.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, audio_settings)
    vampytest.assert_eq(copy, audio_settings)


def test__AudioSettings__copy_with__all_fields():
    """
    Tests whether ``AudioSettings.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_channels = 4
    old_frame_length = 40
    old_sampling_rate = 12000
    
    new_channels = 2
    new_frame_length = 20
    new_sampling_rate = 24000
    
    audio_settings = AudioSettings(
        channels = old_channels,
        frame_length = old_frame_length,
        sampling_rate = old_sampling_rate,
    )
    copy = audio_settings.copy_with(
        channels = new_channels,
        frame_length = new_frame_length,
        sampling_rate = new_sampling_rate,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, audio_settings)
    
    vampytest.assert_eq(copy.channels, new_channels)
    vampytest.assert_eq(copy.frame_length, new_frame_length)
    vampytest.assert_eq(copy.sampling_rate, new_sampling_rate)
