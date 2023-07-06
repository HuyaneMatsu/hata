from .audio_settings import *
from .constants import *
from .fields import *


__all__ = (
    'AUDIO_SETTINGS_DEFAULT',
    *audio_settings.__all__,
    *constants.__all__,
    *fields.__all__,
)


AUDIO_SETTINGS_DEFAULT = AudioSettings(
    channels = 2,
    frame_length = 20,
    sampling_rate = 48000,
)
