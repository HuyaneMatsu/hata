__all__ = ('OpusDecoder', 'OpusEncoder', 'OpusError', )

import ctypes, sys
import ctypes.util
import os.path
from math import log10
from types import ModuleType

from .. import __file__ as hata_discord_init_file_path

from .audio_settings import AUDIO_SETTINGS_DEFAULT

opus = None

class OpusError(Exception):
    """
    Exception raised by lib-opus related methods.
    
    Attributes
    ----------
    code : `int`
        Returned error code by lib-opus.
    """
    def __new__(cls, code):
        """
        Raises
        -----
        RuntimeError
            If opus is not loaded.
        """
        if opus is None:
            raise RuntimeError(f'{cls.__name__} cannot be created if opus is not loaded.')
        
        return Exception.__new__(cls)
    
    def __init__(self, code):
        """
        Creates an ``OpusError``
        
        Parameters
        ----------
        code : `int`
            Returned error code by lib-opus.
        """
        self.code = code
        msg = opus.opus_strerror(code).decode('utf-8')
        Exception.__init__(self, msg)


OK = 0
ERROR_CODE_BAD_ARG = -1
ERROR_CODE_BUFFER_TOO_SMALL = -2
ERROR_CODE_INTERNAL_ERROR = -3
ERROR_CODE_INVALID_PACKET = -4
ERROR_CODE_UNIMPLEMENTED = -5
ERROR_CODE_INVALID_STATE = -6
ERROR_CODE_ALLOC_FAIL = -7

APPLICATION_AUDIO = 2049
APPLICATION_VOIP = 2048
APPLICATION_LOW_DELAY = 2051

SET_BITRATE = 4002
SET_BANDWIDTH = 4008
SET_INBAND_FEC = 4012
SET_PACKET_LOSS_PERCENTAGE = 4014
SET_SIGNAL = 4024
SET_GAIN = 4034
GET_LAST_PACKET_DURATION = 4039

BANDWIDTH_NARROW = 1101
BANDWIDTH_MEDIUM = 1102
BANDWIDTH_WIDE = 1103
BANDWIDTH_SUPER_WIDE = 1104
BANDWIDTH_FULL = 1105

SIGNAL_TYPE_AUTO = -1000
SIGNAL_TYPE_VOICE = 3001
SIGNAL_TYPE_MUSIC = 3002


def load_opus():
    """
    Loads opus.
    
    Raises
    ------
    BaseException
    """
    try:
        if sys.platform == 'win32':
            if sys.maxsize > (1 << 36):
                file_name = 'libopus-0.x64.dll'
            else:
                file_name = 'libopus-0.x86.dll'
            
            file_name = os.path.join(os.path.dirname(os.path.abspath(hata_discord_init_file_path)), 'bin', file_name)
        else:
            file_name = ctypes.util.find_library('opus')
        
        lib_opus = ctypes.cdll.LoadLibrary(file_name)
        
        c_int_ptr = ctypes.POINTER(ctypes.c_int)
        c_int16_ptr = ctypes.POINTER(ctypes.c_int16)
        c_float_ptr = ctypes.POINTER(ctypes.c_float)
        
        EncoderStructPtr = ctypes.POINTER(type('EncoderStruct', (ctypes.Structure,), {},))
        DecoderStructPtr = ctypes.POINTER(type('DecoderStruct', (ctypes.Structure,), {},))
        
        def _err_lt(result, func, args):
            if result < 0:
                raise OpusError(result)
            
            return result
        
        def _err_ne(result, func, args):
            return_code = args[-1]._obj.value
            if return_code < 0:
                raise OpusError(return_code)
            
            return result
        
        functions = []
        
        # register the functions...
        for internal_name, func_name, arg_types, res_type, err_check in (
            ('opus_strerror', 'opus_strerror', (ctypes.c_int,), ctypes.c_char_p, None,),
            ('opus_packet_get_bandwidth', 'opus_packet_get_bandwidth', (ctypes.c_char_p,), ctypes.c_int, _err_lt,),
            ('opus_packet_get_channel_count', 'opus_packet_get_nb_channels', (ctypes.c_char_p,), ctypes.c_int, _err_lt,),
            ('opus_packet_get_frame_count', 'opus_packet_get_nb_frames', (ctypes.c_char_p, ctypes.c_int,), ctypes.c_int, _err_lt,),
            ('opus_packet_get_samples_per_frame', 'opus_packet_get_samples_per_frame', (ctypes.c_char_p, ctypes.c_int,), ctypes.c_int, _err_lt,),
            ('opus_encoder_get_size', 'opus_encoder_get_size', (ctypes.c_int,), ctypes.c_int, None,),
            ('opus_encoder_create', 'opus_encoder_create', (ctypes.c_int, ctypes.c_int, ctypes.c_int, c_int_ptr,), EncoderStructPtr, _err_ne,),
            ('opus_encode', 'opus_encode', (EncoderStructPtr, c_int16_ptr, ctypes.c_int, ctypes.c_char_p, ctypes.c_int32,), ctypes.c_int32, _err_lt,),
            ('opus_encoder_control', 'opus_encoder_ctl', None, ctypes.c_int32, _err_lt,),
            ('opus_encoder_destroy', 'opus_encoder_destroy', (EncoderStructPtr,), None, None,),
            ('opus_decoder_get_size', 'opus_decoder_get_size', (ctypes.c_int,), ctypes.c_int, None,),
            ('opus_decoder_create', 'opus_decoder_create', (ctypes.c_int, ctypes.c_int, c_int_ptr,), DecoderStructPtr, _err_ne,),
            ('opus_decoder_get_sample_count', 'opus_decoder_get_nb_samples', (DecoderStructPtr, ctypes.c_char_p, ctypes.c_int32,), ctypes.c_int, _err_lt,),
            ('opus_decode', 'opus_decode', (DecoderStructPtr, ctypes.c_char_p, ctypes.c_int32, c_int16_ptr, ctypes.c_int, ctypes.c_int,), ctypes.c_int, _err_lt,),
            ('opus_decoder_control', 'opus_decoder_ctl', None, ctypes.c_int32, _err_lt, ),
            ('opus_decoder_destroy', 'opus_decoder_destroy', (DecoderStructPtr,), None, None,),
        ):
            
            func = getattr(lib_opus, func_name)
            
            try:
                if (arg_types is not None):
                    func.argtypes = arg_types
                
                func.restype = res_type
            except KeyError:
                pass
            
            try:
                if (err_check is not None):
                    func.errcheck = err_check
            except KeyError:
                pass
            
            functions.append((internal_name, func))
    except:
        opus = None
        raise
    
    else:
        module_path = f'{__name__}.opus'
        try:
            opus = sys.modules[module_path]
        except KeyError:
            opus = sys.modules[module_path] = ModuleType(module_path)
        
        for name, func in functions:
            setattr(opus, name, func)
    finally:
        try:
            actual_module = sys.modules[__name__]
        except KeyError:
            actual_module = sys.modules[__name__] = ModuleType(__name__)
        
        actual_module.opus = opus

try:
    load_opus()
except BaseException:
    pass


def _set_default_encoder_settings(encoder):
    """
    Sets the default settings to the encoder.
    
    Parameters
    ----------
    encoder : `_ctypes.pointer.LP_EncoderStruct`
        Pointer to the C level encoder.
    """
    opus.opus_encoder_control(encoder, SET_BITRATE, 131072)
    opus.opus_encoder_control(encoder, SET_INBAND_FEC, 1)
    opus.opus_encoder_control(encoder, SET_PACKET_LOSS_PERCENTAGE, 15)
    opus.opus_encoder_control(encoder, SET_BANDWIDTH, BANDWIDTH_FULL)
    opus.opus_encoder_control(encoder, SET_SIGNAL, SIGNAL_TYPE_MUSIC)
        

class OpusEncoder:
    """
    Opus encoder of a ``VoiceClient``.
    
    Attributes
    ----------
    _buffer : `CCharArrayType`
        A buffer used by the encoder.
    _encoder : `_ctypes.pointer.LP_EncoderStruct`
        Pointer to the C level encoder.
    audio_settings : ``AudioSettings``
        Audio settings describing how the encoder is set up / should be set up.
    """
    __slots__ = ('_buffer', '_encoder', 'audio_settings')
    
    def __new__(cls, *, audio_settings = ...):
        """
        Creates a new opus encoder.
        
        Parameters
        ----------
        audio_settings : ``AudioSettings``, Optional (Keyword only)
            Audio settings describing how the encoder should be set up.
        
        Raises
        ------
        RuntimeError
            If opus is not loaded.
        """
        if opus is None:
            raise RuntimeError(f'{cls.__name__} cannot be created if opus is not loaded.')
        
        if audio_settings is ...:
            audio_settings = AUDIO_SETTINGS_DEFAULT
        
        encoder = opus.opus_encoder_create(
            audio_settings.sampling_rate, audio_settings.channels, APPLICATION_AUDIO, ctypes.byref(ctypes.c_int())
        )
        _set_default_encoder_settings(encoder)
        
        self = object.__new__(cls)
        self._encoder = encoder
        self._buffer = audio_settings.buffer_type()
        self.audio_settings = audio_settings
        
        return self
    
    
    def __del__(self):
        """Unallocates `self._encoder`."""
        opus.opus_encoder_destroy(self._encoder)
        self._encoder = None
    
    
    def set_bitrate(self, kbps):
        """
        Sets the bitrate of the encoder in kilo bit per second. Can be between `16` and `512`.
        
        Parameters
        ----------
        kbps : `int`
        """
        if kbps < 16:
            kbps = 16
        elif kbps > 512:
            kbps = 512
        
        opus.opus_encoder_control(self._encoder, SET_BITRATE, kbps << 10)
    
    
    def set_bandwidth(self, bandwidth):
        """
        Set's the band-type of the encoder.
        
        Parameters
        ----------
        bandwidth : `int`
            Requested bandwidth's code.
            
            Possible values
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | BANDWIDTH_NARROW      | 1101  |
            +-----------------------+-------+
            | BANDWIDTH_MEDIUM      | 1102  |
            +-----------------------+-------+
            | BANDWIDTH_WIDE        | 1103  |
            +-----------------------+-------+
            | BANDWIDTH_SUPER_WIDE  | 1104  |
            +-----------------------+-------+
            | BANDWIDTH_FULL        | 1105  |
            +-----------------------+-------+
        """
        opus.opus_encoder_control(self._encoder, SET_BANDWIDTH, bandwidth)
    
    
    def set_signal_type(self, signal_type):
        """
        Sets the signal type of the encoder.
        
        Parameters
        ----------
        signal_type : `int`
            Requested signal type.
        
        Possible values
        ---------------
        +-----------------------+-------+
        | Respective name       | Value |
        +=======================+=======+
        | SIGNAL_TYPE_AUTO      | -1000 |
        +-----------------------+-------+
        | SIGNAL_TYPE_VOICE     | 3001  |
        +-----------------------+-------+
        | SIGNAL_TYPE_MUSIC     | 3002  |
        +-----------------------+-------+
        """
        opus.opus_encoder_control(self._encoder, SET_SIGNAL, signal_type)
    
    
    def set_inband_fec(self, enabled):
        """
        Sets the in-band forward error correction of the encoder.
        
        Parameters
        ----------
        enabled : `bool`
            Whether in-band fec should be enabled.
        """
        # do we really need to switch from sub-int-type to int-type?
        opus.opus_encoder_control(self._encoder, SET_INBAND_FEC, int(enabled)) 
    
    def set_expected_packet_loss_percent(self, percentage):
        """
        Sets the expected packet loss percentage of the encoder.
        
        Parameters
        ----------
        percentage : `float`
            The expected packet loss percentage. Should be between `0` and `100`.
        """
        if percentage < 0.0:
            percentage = 0
        elif percentage > 1.0:
            percentage = 100
        else:
            percentage = int(percentage * 100.0)
        
        opus.opus_encoder_control(self._encoder, SET_PACKET_LOSS_PERCENTAGE, percentage)
    
    
    def encode(self, data):
        """
        Encodes the given `PCM` (Pulse Code Modulation) data.
        
        Parameters
        ----------
        data : `bytes-like`
        
        Returns
        -------
        data : `bytes`
        """
        max_data_bytes = len(data)
        data = ctypes.cast(data, ctypes.POINTER(ctypes.c_int16))
        
        buffer = self._buffer
        end = opus.opus_encode(self._encoder, data, self.audio_settings.samples_per_frame, buffer, max_data_bytes)
        return buffer[:end]
    
    
    def set_audio_settings(self, audio_settings):
        """
        Sets a new audio settings to the opus encoder.
        
        Parameters
        ----------
        audio_settings : ``AudioSettings``
            The new audio settings to set.
        """
        if audio_settings == self.audio_settings:
            return
        
        opus.opus_encoder_destroy(self._encoder)
        
        encoder = opus.opus_encoder_create(
            audio_settings.sampling_rate, audio_settings.channels, APPLICATION_AUDIO, ctypes.byref(ctypes.c_int())
        )
        _set_default_encoder_settings(encoder)
        
        self._encoder = encoder
        self._buffer = audio_settings.buffer_type()
        self.audio_settings = audio_settings


class OpusDecoder:
    """
    Opus decoder of a ``VoiceClient``.
    
    Attributes
    ----------
    _buffer : `CCharArrayType`
        A buffer used by the decoder.
    _decoder : `_ctypes.pointer.LP_DecoderStruct`
        Pointer to the C level decoder.
    audio_settings : ``AudioSettings``
        Audio settings describing how the decoder is set up / should be set up.
    """
    __slots__ = ('audio_settings', '_buffer', '_decoder',)
    
    def __new__(cls, *, audio_settings = ...):
        """
        Creates a new opus decoder.
        
        Parameters
        ----------
        audio_settings : ``AudioSettings``, Optional (Keyword only)
            Audio settings describing how the decoder should be set up.
        
        Raises
        ------
        RuntimeError
            If opus is not loaded.
        """
        if opus is None:
            raise RuntimeError(f'{cls.__name__} cannot be created if opus is not loaded.')
        
        if audio_settings is ...:
            audio_settings = AUDIO_SETTINGS_DEFAULT
        
        decoder = opus.opus_decoder_create(audio_settings.sampling_rate, audio_settings.channels, ctypes.byref(ctypes.c_int()))
        
        self = object.__new__(cls)
        self._decoder = decoder
        self._buffer = audio_settings.buffer_type()
        self.audio_settings = audio_settings
        return self
    
    
    def __del__(self):
        """Unallocates `self._decoder`."""
        opus.opus_decoder_destroy(self._decoder)
        self._decoder = None
    
    
    def packet_get_frame_count(self, data):
        """
        Returns the number of frames of the given packet.
        
        Parameters
        ----------
        data : `bytes-like`

        Returns
        -------
        frame_count : `int`
        """
        return opus.opus_packet_get_frame_count(data, len(data))
    
    
    def packet_get_channel_count(self, data):
        """
        Returns the number of channels of the given packet.
        
        Parameters
        ----------
        data : `bytes-like`

        Returns
        -------
        channel_count : `int`
        """
        return opus.opus_packet_get_channel_count(data) # number of channels
    
    
    def packet_get_samples_per_frame(self, data):
        """
        Returns the number of samples per frame for the given data.
        
        Parameters
        ----------
        data : `bytes-like`
        
        Returns
        -------
        samples_per_frame : `int`
        """
        return opus.opus_packet_get_samples_per_frame(data, self.audio_settings.sampling_rate)
    
    
    def set_gain(self, adjustment): #sets decibel
        """
        Sets the gain of the decoder in decibel
        
        Parameters
        ----------
        adjustment : `float`
        """
        adjustment = int(256 * adjustment)
        if adjustment > 32767:
            adjustment = 32767
        elif adjustment < -32768:
            adjustment = -32768
        
        opus.opus_decoder_control(self._decoder, SET_GAIN, adjustment)
    
    
    def set_volume_percent(self, percent):
        """
        Sets the output's volume percentage of the decoder.
        
        Parameters
        ----------
        percent : `float`
        """
        return self.set_gain(20.0 * log10(percent)) # amplitude ratio
    
    
    def _get_last_packet_duration(self):
        """
        Returns the last packet's duration
        
        Returns
        -------
        duration : `int`
        """
        obj = ctypes.c_int32()
        opus.opus_decoder_control(self._decoder, GET_LAST_PACKET_DURATION, ctypes.byref(obj))
        return obj.value
    
    
    def decode(self, data):
        """
        Decodes the given `PCM` (Pulse Code Modulation) data.
        
        Parameters
        ----------
        data : `bytes-like`
        
        Returns
        -------
        data : `bytes`
        """
        frame_size = self.packet_get_frame_count(data) * self.packet_get_samples_per_frame(data)
        
        buffer = self._buffer
        buffer_ptr = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_int16))
        
        end = opus.opus_decode(self._decoder, data, len(data), buffer_ptr, frame_size, True)
        return bytes(buffer[:((end << 1) * self.audio_settings.channels)])
    
    
    def set_audio_settings(self, audio_settings):
        """
        Sets a new audio settings to the opus decoder.
        
        Parameters
        ----------
        audio_settings : ``AudioSettings``
            The new audio settings to set.
        """
        if audio_settings == self.audio_settings:
            return
        
        opus.opus_decoder_destroy(self._decoder)
        
        decoder = opus.opus_decoder_create(
            audio_settings.sampling_rate, audio_settings.channels, ctypes.byref(ctypes.c_int())
        )
        
        self._decoder = decoder
        self._buffer = audio_settings.buffer_type()
        self.audio_settings = audio_settings
