__all__ = ()

from ...field_validators import int_conditional_validator_factory

from .constants import CHANNELS_DEFAULT, FRAME_LENGTH_DEFAULT, SAMPLING_RATE_DEFAULT


validate_channels = int_conditional_validator_factory(
    'channels',
    CHANNELS_DEFAULT,
    lambda channels : channels >= 1,
    '>= 1',
)

validate_frame_length = int_conditional_validator_factory(
    'frame_length',
    FRAME_LENGTH_DEFAULT,
    lambda frame_length : frame_length >= 1,
    '>= 1',
)

validate_sampling_rate = int_conditional_validator_factory(
    'sampling_rate',
    SAMPLING_RATE_DEFAULT,
    lambda sampling_rate : sampling_rate >= 1,
    '>= 1',
)
