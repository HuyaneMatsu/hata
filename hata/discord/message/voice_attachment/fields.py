__all__ = ()

from ...field_putters import float_putter_factory

from ..attachment.fields import (
    put_description, put_waveform, validate_description, validate_duration, validate_name, validate_waveform
)


put_duration = float_putter_factory('duration_secs')
