__all__ = ('AudioSettings',)

from ctypes import c_char as CCharType

from scarletio import RichAttributeErrorBaseType

from .constants import CHANNELS_DEFAULT, FRAME_LENGTH_DEFAULT, SAMPLING_RATE_DEFAULT
from .fields import validate_channels, validate_frame_length, validate_sampling_rate


class AudioSettings(RichAttributeErrorBaseType):
    """
    Attributes
    ----------
    buffer_type : `type<CCharArrayType>`
        C char array type for creating buffer.
    
    channels : `int`
        The number of channels. (1 if mono, 2 if stereo.)
    
    frame_length : `int`
        The length of a frame in milliseconds.
    
    frame_size : `int`
        The size of a frame in bytes.
    
    sampling_rate : `int`
        The number of samples per second that are taken of a waveform to create a digital signal.
        The higher the sample rate, the more snapshots are captured in the audio signal.
    
    sample_size : `int`
        The number of bits used to describe each sample.
        A sample is a value represented in `i16`. Each channel has their own samples.
    
    samples_per_frame : `int`
        The amount of samples that are in each frame.
    """
    __slots__ = (
        'buffer_type', 'channels', 'frame_length', 'frame_size', 'samples_per_frame', 'sampling_rate', 'sample_size'
    )
    
    def __new__(
        cls,
        *,
        channels = ...,
        frame_length = ...,
        sampling_rate = ...,
    ):
        """
        Creates a new audio setting.
        
        Parameters
        ----------
        channels : `int`, Optional (Keyword only)
            The number of channels.
        frame_length : `int`, Optional (Keyword only)
            The length of a frame in milliseconds.
        sampling_rate : `int`, Optional (Keyword only)
            The number of samples per second that are taken of a waveform to create a digital signal.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # channels
        if channels is ...:
            channels = CHANNELS_DEFAULT
        else:
            channels = validate_channels(channels)
        
        # frame_length
        if frame_length is ...:
            frame_length = FRAME_LENGTH_DEFAULT
        else:
            frame_length = validate_frame_length(frame_length)
        
        # sampling_rate
        if sampling_rate is ...:
            sampling_rate = SAMPLING_RATE_DEFAULT
        else:
            sampling_rate = validate_sampling_rate(sampling_rate)
        
        # Do math
        sample_size = 2 * channels # sizeof(i16) * channels
        samples_per_frame = int(sampling_rate / 1000 * frame_length)
        frame_size = samples_per_frame * sample_size
        buffer_type = CCharType * frame_size
        
        # Construct
        self = object.__new__(cls)
        self.buffer_type = buffer_type
        self.channels = channels
        self.frame_length = frame_length
        self.frame_size = frame_size
        self.samples_per_frame = samples_per_frame
        self.sampling_rate = sampling_rate
        self.sample_size = sample_size
        return self
    
    
    def __eq__(self, other):
        """Returns whether the two audio settings are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.channels != other.channels:
            return False
        
        if self.frame_length != other.frame_length:
            return False
        
        if self.sampling_rate != other.sampling_rate:
            return False
        
        return True
    
    
    def __repr__(self):
        """Returns the audio settings representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' channels = ')
        repr_parts.append(repr(self.channels))
        
        repr_parts.append(', frame_length = ')
        repr_parts.append(repr(self.frame_length))
        
        repr_parts.append(', sampling_rate = ')
        repr_parts.append(repr(self.sampling_rate))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def copy(self):
        """
        Copies the audio settings.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.buffer_type = self.buffer_type
        new.channels = self.channels
        new.frame_length = self.frame_length
        new.frame_size = self.frame_size
        new.samples_per_frame = self.samples_per_frame
        new.sampling_rate = self.sampling_rate
        new.sample_size = self.sample_size
        return new
    
    
    def copy_with(
        self,
        *,
        channels = ...,
        frame_length = ...,
        sampling_rate = ...,
    ):
        """
        Copies the audio settings with the given fields.
        
        Parameters
        ----------
        channels : `int`, Optional (Keyword only)
            The number of channels.
        frame_length : `int`, Optional (Keyword only)
            The length of a frame in milliseconds.
        sampling_rate : `int`, Optional (Keyword only)
            The number of samples per second that are taken of a waveform to create a digital signal.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # channels
        if channels is ...:
            channels = self.channels
        else:
            channels = validate_channels(channels)
        
        # frame_length
        if frame_length is ...:
            frame_length = self.frame_length
        else:
            frame_length = validate_frame_length(frame_length)
        
        # sampling_rate
        if sampling_rate is ...:
            sampling_rate = self.sampling_rate
        else:
            sampling_rate = validate_sampling_rate(sampling_rate)
        
        # Do math
        sample_size = 2 * channels # sizeof(i16) * channels
        samples_per_frame = int(sampling_rate / 1000 * frame_length)
        frame_size = samples_per_frame * sample_size
        buffer_type = CCharType * frame_size
        
        # Construct
        new = object.__new__(type(self))
        new.buffer_type = buffer_type
        new.channels = channels
        new.frame_length = frame_length
        new.frame_size = frame_size
        new.samples_per_frame = samples_per_frame
        new.sampling_rate = sampling_rate
        new.sample_size = sample_size
        return new
