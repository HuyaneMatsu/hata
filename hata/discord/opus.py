# -*- coding: utf-8 -*-
__all__ = ('OpusDecoder', 'OpusEncoder', 'OpusError', )

import ctypes, sys
import ctypes.util
import os.path
from math import log10
from types import ModuleType

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
            raise RuntimeError(f'{cls.__name__} cannot be created if opus is not loaded')
        
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
    Any
    """
    try:
        if sys.platform == 'win32':
            filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', f'libopus-0.{"x64" if sys.maxsize>(1<<36) else "x86"}.dll')
        else:
            filename = ctypes.util.find_library('opus')
        
        lib_opus = ctypes.cdll.LoadLibrary(filename)
        
        c_int_ptr = ctypes.POINTER(ctypes.c_int)
        c_int16_ptr = ctypes.POINTER(ctypes.c_int16)
        c_float_ptr = ctypes.POINTER(ctypes.c_float)
        
        EncoderStructPtr=ctypes.POINTER(type('EncoderStruct', (ctypes.Structure,), {},))
        DecoderStructPtr=ctypes.POINTER(type('DecoderStruct', (ctypes.Structure,), {},))
        
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

SAMPLING_RATE = 48000 #this is the max sadly
CHANNELS = 2
FRAME_LENGTH = 20
SAMPLE_SIZE = 4 # (bit_rate / 8) * CHANNELS (bit_rate == 16)
SAMPLES_PER_FRAME = int(SAMPLING_RATE/1000*FRAME_LENGTH)
FRAME_SIZE = SAMPLES_PER_FRAME*SAMPLE_SIZE
BUFFER_SIZE = 3840
BUFFER_TYPE = ctypes.c_char*BUFFER_SIZE

class OpusEncoder:
    """
    Opus encoder of a ``VoiceClient``.
    
    Attributes
    ----------
    _buffer : `_ctypes.array.c_char_Array_3840`
        A buffer used by the encoder.
    _encoder : `_ctypes.pointer.LP_EncoderStruct`
        Pointer to the C level encoder.
    """
    __slots__ = ('_buffer', '_encoder', )
    def __new__(cls):
        """
        Creates a new opus decoder.
        
        Returns
        -------
        self : ``OpusEncoder``
        
        Raises
        ------
        RuntimeError
            If opus is not loaded.
        """
        if opus is None:
            raise RuntimeError(f'{cls.__name__} cannot be created if opus is not loaded')
        
        encoder = opus.opus_encoder_create(SAMPLING_RATE, CHANNELS, APPLICATION_AUDIO, ctypes.byref(ctypes.c_int()))
        
        self=object.__new__(cls)
        self._encoder = encoder
        self._buffer = BUFFER_TYPE()
        
        opus.opus_encoder_control(encoder, SET_BITRATE, 131072)
        opus.opus_encoder_control(encoder, SET_INBAND_FEC, 1)
        opus.opus_encoder_control(encoder, SET_PACKET_LOSS_PERCENTAGE, 15)
        opus.opus_encoder_control(encoder, SET_BANDWIDTH, BANDWIDTH_FULL)
        opus.opus_encoder_control(encoder, SET_SIGNAL, SIGNAL_TYPE_MUSIC)
        
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
        
        opus.opus_encoder_control(self._encoder, SET_BITRATE, kbps<<10)

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
        opus.opus_encoder_control(self._encoder, SET_INBAND_FEC, int(enabled)) #do we really need to switch from sub-int-type to int-type?
    
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
            percentage = int(percentage*100.0)
        
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
        end = opus.opus_encode(self._encoder, data, SAMPLES_PER_FRAME, buffer, max_data_bytes)
        return buffer[:end]

class OpusDecoder:
    """
    Opus decoder of a ``VoiceClient``.
    
    Attributes
    ----------
    _buffer : `_ctypes.array.c_char_Array_3840`
        A buffer used by the encoder.
    _decoder : `_ctypes.pointer.LP_DecoderStruct`
        Pointer to the C level decoder.
    """
    __slots__ = ('_buffer', '_decoder',)
    
    def __new__(cls):
        """
        Creates a new opus decoder.
        
        Returns
        -------
        self : ``OpusDecoder``
        
        Raises
        ------
        RuntimeError
            If opus is not loaded.
        """
        if opus is None:
            raise RuntimeError(f'{cls.__name__} cannot be created if opus is not loaded')
        
        decoder = opus.opus_decoder_create(SAMPLING_RATE, CHANNELS, ctypes.byref(ctypes.c_int()))
        
        self = object.__new__(cls)
        self._decoder = decoder
        self._buffer = BUFFER_TYPE()
        
        return self
    
    def __del__(self):
        """Unallocates `self._decoder`."""
        opus.opus_decoder_destroy(self._decoder)
        self._decoder = None
    
    @staticmethod
    def packet_get_frame_count(data):
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
    
    @staticmethod
    def packet_get_channel_count(data):
        """
        Returns the number of channels of the given packet.
        
        Parameters
        ----------
        data : `bytes-like`

        Returns
        -------
        channel_count : `int`
        """
        return opus.opus_packet_get_channel_count(data) #number of channels

    @staticmethod
    def packet_get_samples_per_frame(data):
        """
        Returns the number of samples per frame for the given data.
        
        Parameters
        ----------
        data : `bytes-like`
        
        Returns
        -------
        samples_per_frame : `int`
        """
        return opus.opus_packet_get_samples_per_frame(data, SAMPLING_RATE)
    
    def set_gain(self, adjustment): #sets decibel
        """
        Sets the gain of the decoder in decibel
        
        Parameters
        ----------
        adjustment : `float`
        """
        adjustment = int(256*adjustment)
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
        return self.set_gain(20.0*log10(percent)) # amplitude ratio
    
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
        frame_size = self.packet_get_frame_count(data)*self.packet_get_samples_per_frame(data)
        
        buffer = self._buffer
        buffer_ptr = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_int16))
        
        end = opus.opus_decode(self._decoder, data, len(data), buffer_ptr, frame_size, True)
        return bytes(buffer[:((end<<1)*CHANNELS)])
