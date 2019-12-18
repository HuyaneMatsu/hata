# -*- coding: utf-8 -*-
__all__ = ('OpusError', )

import ctypes
import ctypes.util
import sys
import os.path
from math import log10

class OpusError(Exception):
    def __init__(self,code):
        self.code=code
        msg=opus.opus_strerror(self.code).decode('utf-8')
        Exception.__init__(self,msg)

OK                      =    0
BAD_ARG                 =   -1
APPLICATION_AUDIO       = 2049
APPLICATION_VOIP        = 2048
APPLICATION_LOWDELAY    = 2051
CTL_SET_BITRATE         = 4002
CTL_SET_BANDWIDTH       = 4008
CTL_SET_FEC             = 4012
CTL_SET_PLP             = 4014
CTL_SET_SIGNAL          = 4024
CTL_SET_GAIN            = 4034
CTL_LAST_PACKET_DURATION= 4039

band_ctl = {
    'narrow'    :  1101,
    'medium'    :  1102,
    'wide'      :  1103,
    'superwide' :  1104,
    'full'      :  1105,
        }

signal_ctl = {
    'auto'      : -1000,
    'voice'     :  3001,
    'music'     :  3002,
        }

c_int_ptr   = ctypes.POINTER(ctypes.c_int)
c_int16_ptr = ctypes.POINTER(ctypes.c_int16)
c_float_ptr = ctypes.POINTER(ctypes.c_float)

class EncoderStruct(ctypes.Structure):
    pass

class DecoderStruct(ctypes.Structure):
    pass

EncoderStructPtr=ctypes.POINTER(EncoderStruct)
DecoderStructPtr=ctypes.POINTER(DecoderStruct)

def _err_lt(result,func,args):
    if result<0:
        raise OpusError(result)
    return result

def _err_ne(result,func,args):
    ret = args[-1]._obj
    if ret.value!=0:
        raise OpusError(ret.value)
    return result

try:
    if sys.platform=='win32':
        filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bin', f'libopus-0.{"x64" if sys.maxsize>(1<<36) else "x86"}.dll')
    else:
        filename=ctypes.util.find_library('opus')

    opus=ctypes.cdll.LoadLibrary(filename)

    # register the functions...
    for item in (
            ('opus_strerror',                       (ctypes.c_int,),                                                                            ctypes.c_char_p,    None,   ),
            ('opus_packet_get_bandwidth',           (ctypes.c_char_p,),                                                                         ctypes.c_int,       _err_lt,),
            ('opus_packet_get_nb_channels',         (ctypes.c_char_p,),                                                                         ctypes.c_int,       _err_lt,),
            ('opus_packet_get_nb_frames',           (ctypes.c_char_p,ctypes.c_int,),                                                            ctypes.c_int,       _err_lt,),
            ('opus_packet_get_samples_per_frame',   (ctypes.c_char_p,ctypes.c_int,),                                                            ctypes.c_int,       _err_lt,),
            ('opus_encoder_get_size',               (ctypes.c_int,),                                                                            ctypes.c_int,       None,   ),
            ('opus_encoder_create',                 (ctypes.c_int,ctypes.c_int,ctypes.c_int,c_int_ptr,),                                        EncoderStructPtr,   _err_ne,),
            ('opus_encode',                         (EncoderStructPtr,c_int16_ptr,ctypes.c_int,ctypes.c_char_p,ctypes.c_int32,),                ctypes.c_int32,     _err_lt,),
            ('opus_encoder_ctl',                    None,                                                                                       ctypes.c_int32,     _err_lt,),
            ('opus_encoder_destroy',                (EncoderStructPtr,),                                                                        None,               None,   ),
            ('opus_decoder_get_size',               (ctypes.c_int,),                                                                            ctypes.c_int,       None,   ),
            ('opus_decoder_create',                 (ctypes.c_int,ctypes.c_int,c_int_ptr,),                                                     DecoderStructPtr,   _err_ne,),
            ('opus_decoder_get_nb_samples',         (DecoderStructPtr,ctypes.c_char_p,ctypes.c_int32,),                                         ctypes.c_int,       _err_lt,),
            ('opus_decode',                         (DecoderStructPtr,ctypes.c_char_p,ctypes.c_int32,c_int16_ptr,ctypes.c_int,ctypes.c_int,),   ctypes.c_int,       _err_lt,),
            ('opus_decoder_ctl',                    None,                                                                                       ctypes.c_int32,     _err_lt,),
            ('opus_decoder_destroy',                (DecoderStructPtr,),                                                                        None,               None,   ),
                ):
        func=getattr(opus,item[0])
        
        try:
            if item[1] is not None:
                func.argtypes=item[1]

            func.restype=item[2]
        except KeyError:
            pass

        try:
            if item[3] is not None:
                func.errcheck = item[3]
        except KeyError:
            pass
        
except BaseException:
    opus=None

for name in ('filename', 'item', 'func'):
    try:
        del globals()[name]
    except KeyError:
        pass

del name

SAMPLING_RATE       = 48000 #this is the max sadly
CHANNELS            = 2
FRAME_LENGTH        = 20
SAMPLE_SIZE         = 4 # (bit_rate / 8) * CHANNELS (bit_rate == 16)
SAMPLES_PER_FRAME   = (SAMPLING_RATE/1000*FRAME_LENGTH).__int__()
FRAME_SIZE          = SAMPLES_PER_FRAME*SAMPLE_SIZE
BUFFER_SIZE         = 3840
BUFFER_TYPE         = (ctypes.c_char*BUFFER_SIZE)

        
if opus is None:
    OpusEncoder=None
    OpusDecoder=None
else:
    class OpusEncoder(object):
        __slots__=('state', 'buffer',)
        def __new__(cls):
            state=opus.opus_encoder_create(SAMPLING_RATE,CHANNELS,APPLICATION_AUDIO,ctypes.byref(ctypes.c_int()))

            self=object.__new__(cls)
            self.state      = state
            self.buffer     = BUFFER_TYPE()

            opus.opus_encoder_ctl(state,CTL_SET_BITRATE,131072)
            opus.opus_encoder_ctl(state,CTL_SET_FEC,1)
            opus.opus_encoder_ctl(state,CTL_SET_PLP,15)
            opus.opus_encoder_ctl(state,CTL_SET_BANDWIDTH,1105)
            opus.opus_encoder_ctl(state,CTL_SET_SIGNAL,3002)
            
            return self

        def __del__(self):
            opus.opus_encoder_destroy(self.state)
            self.state=NotImplemented

        def set_bitrate(self,kbps):
            if kbps<16:
                kbps=16
            elif kbps>512:
                kbps=512
                
            opus.opus_encoder_ctl(self.state,CTL_SET_BITRATE,kbps<<10)

        def set_bandwidth(self,req):
            if req not in band_ctl:
                raise KeyError(f'{req} is not a valid bandwidth setting. Try one of: {", ".join(band_ctl)}')

            opus.opus_encoder_ctl(self.state,CTL_SET_BANDWIDTH,band_ctl[req])

        def set_signal_type(self,req):
            if req not in signal_ctl:
                raise KeyError(f'{req} is not a valid signal setting. Try one of: {", ".join(signal_ctl)}')

            opus.opus_encoder_ctl(self.state,CTL_SET_SIGNAL,signal_ctl[req])

        def set_fec(self,enabled):
            opus.opus_encoder_ctl(self.state,CTL_SET_FEC,int(enabled)) #do we really need to switch from sub-int-type to int-type?

        def set_expected_packet_loss_percent(self,percentage):
            if percentage<.0:
                percentage=0
            elif percentage>1.:
                percentage=100
            else:
                percentage=(percentage*100.).__int__()
            
            opus.opus_encoder_ctl(self.state,CTL_SET_PLP,percentage)

        def encode(self,pcm):
            max_data_bytes=len(pcm)
            pcm=ctypes.cast(pcm,c_int16_ptr)

            buffer=self.buffer
            ret=opus.opus_encode(self.state,pcm,SAMPLES_PER_FRAME,buffer,max_data_bytes)
            return buffer[:ret]


    class OpusDecoder(object):
        __slots__=('state',)

        def __new__(cls):
            state=opus.opus_decoder_create(SAMPLING_RATE,CHANNELS,ctypes.byref(ctypes.c_int()))

            self=object.__new__(cls)
            self.state      = state

            return self

        def __del__(self):
            opus.opus_decoder_destroy(self.state)
            self.state=NotImplemented

        @staticmethod
        def packet_get_nb_frames(data):
            return opus.opus_packet_get_nb_frames(data,len(data)) #number of frames

        @staticmethod
        def packet_get_nb_channels(data):
            return opus.opus_packet_get_nb_channels(data) #number of channels

        @staticmethod
        def packet_get_samples_per_frame(data):
            return opus.opus_packet_get_samples_per_frame(data,SAMPLING_RATE) #number of samples

        def _set_gain(self, adjustment):
            return opus.opus_decoder_ctl(self.state,CTL_SET_GAIN,adjustment)

        def set_gain(self,value): #sets decibel
            value=(256*value).__int__()
            if value>32767:
                value=32767
            elif value<-32768:
                value=-32768
                
            return self._set_gain(value)

        def set_volume(self,value):
            # Sets the output volume as a float percent, i.e. 0.5 for 50%, 1.75 for 175%, etc
            return self.set_gain(20*log10(value)) # amplitude ratio

        def _get_last_packet_duration(self):
            obj=ctypes.c_int32()
            opus.opus_decoder_ctl(self.state,CTL_LAST_PACKET_DURATION,ctypes.byref(obj))
            return obj.value

        def decode(self,data):
            frames=self.packet_get_nb_frames(data)
            samples_per_frame=self.packet_get_samples_per_frame(data)
            frame_size=frames*samples_per_frame

            #this is like cancer
            pcm=(ctypes.c_int16*(frame_size*CHANNELS))()
            pcm_ptr=ctypes.cast(pcm,ctypes.POINTER(ctypes.c_int16))
            
            result=opus.opus_decode(self.state,data,len(data),pcm_ptr,frame_size,True)
            return bytes(pcm)

    
