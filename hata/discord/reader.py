# -*- coding: utf-8 -*-
import sys
from threading import Thread
from select import select
from socket import error as SocketError
from collections import deque

from ..backend.dereaddons_local import WeakReferer
from ..backend.futures import render_exc_to_list

from .opus import OpusDecoder, opus
from .player import AudioSource

#poll is not on windows, but if u want i can add an optimized case for linux
#it is just dumb, how much times i need to copy data instead of slicing it with memoryview

if opus is None:
    DECODER = None
else:
    DECODER = OpusDecoder()

EMPTY_VOICE_FRAME_ENCODED = b'\xf8\xff\xfe'
EMPTY_VOICE_FRAME_DECODED = b'\x00'*3840

class Array_uint_32b(object): #TODO : ask python to implement arrays already
    """
    Implements an uint32 array casted on bytes.
    
    Attributes
    ----------
    _data : `bytes`
        The source `bytes` object.
    _offset : `int`
        The first byte what is inside of the array.
    _limit : `int`
        The first byte, what is not inside of the array after `._offset`.
    """
    __slots__ = ('_data', '_offset', '_limit')
    def __init__(self, data, offset, limit):
        """
        Creates a new uint32 array from the given parameters.
        
        Parameters
        ----------
        data : `bytes`
            The source `bytes` object.
        offset : `int`
            The first byte what is inside of the array.
        limit : `int`
            The first byte, what is not inside of the array after `._offset`.
        """
        self._data = data
        self._offset = offset
        self._limit = limit
    
    def __len__(self):
        """Returns the array's length"""
        limit = self._limit
        offset = self._offset
        value = (limit-offset)>>2
        
        return value
    
    def __getitem__(self, index):
        """Returns the element of the array at the given index."""
        index = index<<2
        offset = self._offset+index
        value = int.from_bytes(self._data[offset:offset+4], 'big')
        
        return value
    
    def __iter__(self):
        """Iterated over the array's elements."""
        data = self._data
        offset = self._offset
        limit = self._limit
        
        while True:
            if offset == limit:
                break
            value = int.from_bytes(data[offset:offset+4], 'big')
            yield value
            
            offset = offset+4

class PacketBase(object):
    """
    Base class for packet subclasses.
    """
    __slots__ = ()

class VoicePacket(PacketBase):
    """
    Represents a voice packet.
    
    Attributes
    ----------
    decoded : `str`
    """
    __slots__ = ('decoded', 'encoded')
    
    def __init__(self, data):
        """
        Creates a new ``VoicePacket`` from the given data.
        
        Parameters
        ----------
        data : `bytes`
            Not yet decoded voice data.
        """
        self.encoded = data
        self.decoded = None
    
    def __repr__(self):
        """ Returns the voice packet's representation."""
        return (f'<{self.__class__.__name__} decoded={self.decoded is not None}>')

# http://www.rfcreader.com/#rfc3550_line548
class RTPPacket(PacketBase):
    """
    Represents an RTP packet: http://www.rfcreader.com/#rfc3550_line548.
    
    Attributes
    ----------
    _data : `bytes`
        The raw data of the packet on what it is casted on.
    _offset1 : `int`
        Offset of the received data marking the end of the CSRC identifiers and the start of the encrypted data.
    _offset2 : `int`
        Offset of the descrypted data marking the end of the extensions (?) and the start of the descrypted data.
    _decrypted : `bytes`
        Descrypted data of the RTP packet.
    """
    __slots__ = ('_data', '_offset1', '_offset2', '_decrypted',)
    
    def __init__(self, data, voice_client):
        self._data =data
        offset = 12
        cc = self.cc
        if cc:
            offset = offset+(cc<<2)
        self._offset1 = offset
        
        nonce = data[:12]+b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        decrypted = voice_client._secret_box.decrypt(data[offset:], nonce)
        self._decrypted = decrypted
        
        if self.extended:
            extension=int.from_bytes(decrypted[2:4], 'big')
            offset = (extension<<2)+4
        else:
            offset = 0
        
        self._offset2 = offset
    
    @property
    def data(self):
        return memoryview(self._data)[self._offset1:]
    
    @property
    def decrypted(self):
        return memoryview(self._decrypted)[self._offset2:]
    
    @property
    def csrcs(self):
        return Array_uint_32b(self._data, 12, self._offset1)
    
    @property
    def extension_profile(self):
        if not self.extended:
            return 0
        
        profile = int.from_bytes(self._decrypted[0:2], 'big')
        return profile
    
    @property
    def extension_length(self):
        if not self.extended:
            return 0
        
        length = int.from_bytes(self._decrypted[2:4], 'big')
        return length
    
    @property
    def extension_values(self):
        limit = self._offset2
        if limit <= 4:
            return None
        return Array_uint_32b(self._decrypted, 4, limit)
    
    @property
    def version(self):
        return self._data[0]>>6
    
    @property
    def padding(self):
        return (self._data[0]&0b00100000)>>5
    
    @property
    def extended(self):
        return (self._data[0]&0b00010000)>>4
    
    @property
    def cc(self):
        return self._data[0]&0b00001111
    
    @property
    def marker(self):
        return (self._data[1]&0b10000000)>>7
    
    @property
    def payload(self):
        return self._data[1]&0b01111111
    
    @property
    def timestamp(self):
        return int.from_bytes(self._data[4:8], 'big')
    
    @property
    def source(self):
        return int.from_bytes(self._data[8:12], 'big')
    
    @property
    def sequence(self):
        return int.from_bytes(self._data[2:4], 'big')
    
    @property
    def header(self):
        return memoryview(self._data)[:12]

    def __repr__(self):
        return (f'<{self.__class__.__name__} timestamp={self.timestamp}, source={self.source}, sequence='
            f'{self.sequence}, size={len(self.data)}>')

#NOT USED

###http://www.rfcreader.com/#rfc3550_line855
##class RTCPPacket(PacketBase):
##    __slots__ = ('_data')
##    type = 0
##
##    def __init__(self,data):
##        self._data = data
##
##    @property
##    def version(self):
##        return self._data[0]>>6
##
##    @property
##    def padding(self):
##        return (self._data[0]&0b00100000)>>5
##
##    @property
##    def length(self):
##        return int.from_bytes(self._data[2:4], 'big')
##
##    @property
##    def report_count(self):
##        return self._data[0]&0b00011111
##
##    @property
##    def source(self):
##        return int.from_bytes(self._data[4:8], 'big')
##
##class _RPReport(self):
##    __slots__ = ('_data','_offset')
##    def __init__(self, data, offset):
##        self._data = data
##        self._offset = offset
##
##    @property
##    def source(self):
##        offset = self._offset
##        return int.from_bytes(self._data[offset:offset+4], 'big')
##
##    @property
##    def loss_percent(self):
##        offset = self._offset
##        return self._data[offset+4]
##
##    @property
##    def loss_total(self):
##        offset = self._offset+5
##        return int.from_bytes(self._data[offset:offset+3], 'big')
##
##    @property
##    def last_sequence(self):
##        offset = self._offset+8
##        return int.from_bytes(self._data[offset:offset+4], 'big')
##
##    @property
##    def jitter(self):
##        offset = self._offset+12
##        return int.from_bytes(self._data[offset:offset+4], 'big')
##
##    @property
##    def lsr(self):
##        offset = self._offset+16
##        return int.from_bytes(self._data[offset:offset+4], 'big')
##
##    @property
##    def dlsr(self):
##        offset = self._offset+20
##        return int.from_bytes(self._data[offset:offset+4], 'big')
##        
###http://www.rfcreader.com/#rfc3550_line1614
##class SenderReportPacket(RTCPPacket):
##    __slots__ = ('_descripted', '_offset1')
##    type = 200
##    
##    def __init__(self, data, voice_client):
##        data_shard = data[:8]
##        self._data = data_shard
##        
##        nonce = data_shard+b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
##        descripted = voice_client._secret_box.decrypt(data[8:], nonce)
##        self._descripted = descripted
##        
##        report_count = data_shard[0]&0b00011111
##        offset = (report_count*24)+20
##        self._offset1 = offset
##
##    def __repr__(self):
##        return (f'<{self.__class__.__name__} timestamp={self.timestamp}, length={self.length}, reports='
##            f'{self.report_count}>')
##    
##    @property
##    def descripted(self):
##        return memoryview(self._descripted)[24:]
##    
##    @property
##    def info_ntp_ts_msw(self):
##        return int.from_bytes(self._descripted[0:4], 'big')
##
##    @property
##    def info_ntp_ts_lsw(self):
##        return int.from_bytes(self._descripted[4:8], 'big')
##
##    @property
##    def info_ntp_ts(self):
##        low = int.from_bytes(self._descripted[4:8], 'big')
##        low = low/(1<<low.bit_length())
##        
##        high = int.from_bytes(self._descripted[0:4], 'big')
##        
##        return high+low
##
##    @property
##    def info_rtp_ts(self):
##        return int.from_bytes(self._descripted[8:12], 'big')
##
##    @property
##    def info_sequence(self):
##        return int.from_bytes(self._descripted[12:16], 'big')
##
##    @property
##    def info_octet(self):
##        return int.from_bytes(self._descripted[16:20], 'big')
##
##    @property
##    def extension(self):
##        data = self._descripted
##        offset = self._offset1
##        
##        if len(data)>offset:
##            return memoryview(descripted)[offset:]
##
##    def report_get(self,index):
##        offset = (index*24)+20
##        obj = _RPReport(self._descripted, offset)
##        
##        return obj
##
##    def report_iter(self, index):
##        data = self._descripted
##        limit = self._offset1
##        offset = 20
##        
##        while True:
##            if offset >= limit:
##                break
##            obj = _RPReport(data, offset)
##            yield obj
##            
##            offset += 24
##
###http://www.rfcreader.com/#rfc3550_line1879
##class ReceiverReportPacket(RTCPPacket):
##    __slots__ = ('_descripted', '_offset1')
##    type = 201
##    
##    def __init__(self,data,voice_client):
##        data_shard = data[:8]
##        self._data = data_shard
##        
##        nonce = data_shard+b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
##        descripted = voice_client._secret_box.decrypt(data[8:], nonce)
##        self._descripted = descripted
##        
##        report_count = data_shard[0]&0b00011111
##        offset = report_count*24
##        self._offset1 = offset
##
##    def __repr__(self):
##        return (f'<{self.__class__.__name__} timestamp={self.timestamp}, length={self.length}, reports='
##            f'{self.report_count}>')
##
##    @property
##    def descripted(self):
##        return memoryview(self._descripted)
##    
##    def report_get(self,index):
##        offset = index*24
##        obj = _RPReport(self._descripted,offset)
##        
##        return obj
##
##    def report_iter(self,index):
##        data = self._descripted
##        limit = self._offset1
##        offset = 0
##        
##        while True:
##            if offset >= limit:
##                break
##            obj = _RPReport(data, offset)
##            yield obj
##            
##            offset += 24

class AudioStream(AudioSource):
    """
    Represents a received audio stream from Discord.
    
    Attributes
    ----------
    auto_decode : `bool`
        Whether the stream should decode the frames as received.
    buffer : `deque` of `VoicePacket`
        A queue of received voice packets.
    done : `bool`
        Whether the audio stream is stopped.
    client : `WeakReferer`
        Weakreference to the parent ``AudioReader`` to avoid reference loops.
    source : `None` or `int`
        Identificator value of the respective user.
    user : ``User`` or ``Client``
        The user, who's audio is received.
    yield_decoded : `bool`
        Whether the audio stream should yield encoded data.
    
    Class Attributes
    ----------------
    REPEATABLE : `bool` = `False`
        Whether the source can be repeated after it is exhausted once.
    """
    __slots__ = ('auto_decode', 'buffer', 'client', 'done', 'source', 'user', 'yield_decoded')
    
    def __init__(self, voice_client, user, *, auto_decode=False, yield_decoded=False):
        """
        Creates a new audio stream instance.
        
        Parameters
        ----------
        voice_client : ``VoiceClient``
            Parent ``AudioReader`` instance.
        user : ``User`` or ``Client``
            The user, who's audio is received.
        auto_decode : `bool`
            Whether the received packets should be auto decoded.
        yield_decoded : `bool`
            Whether the audio stream should yield decoded data.
        """
        try:
            audio_source = voice_client._audio_sources[user.id]
        except KeyError:
            audio_source = None
        
        self.client = voice_client
        self.buffer = deque()
        self.auto_decode = auto_decode
        self.yield_decoded = yield_decoded
        self.done = False
        self.user = user
        self.source = audio_source
        
    def stop(self):
        """
        Stops the audio stream by marking it as done and unlinks it as well.
        """
        if self.done:
            return
        
        self.done = True
        self.client._unlink_audio_stream(self)
    
    cleanup = stop
    
    @property
    def NEEDS_ENCODE(self):
        """
        Returns whether the audio stream needs encoding when streaming to an audio player.
        
        Returns
        -------
        needs_encode : `bool`
        """
        return self.yield_decoded
    
    def feed(self, packet):
        """
        Adds the given packet to the buffer of the audio stream.
        
        Parameters
        ----------
        packet : ``VoicePacket``
        """
        self.buffer.append(packet)
        
        if self.auto_decode:
            if packet.decoded is None:
                packet.decoded = DECODER.decode(packet.encoded)
    
    def read(self):
        """
        Reads a frame from the audio stream's buffer.
        
        With yielding `None` indicates end of stream.
        
        Returns
        -------
        frame : `None` or `bytes`
        """
        buffer = self.buffer
        if buffer:
            packet = buffer.popleft()
            if self.yield_decoded:
                data = packet.decoded
                if data is None:
                    data = DECODER.decode(packet.encoded)
            else:
                data = packet.encoded
        
        else:
            if self.done:
                data = None
            else:
                if self.yield_decoded:
                    data = EMPTY_VOICE_FRAME_DECODED
                else:
                    data = EMPTY_VOICE_FRAME_ENCODED
        
        return data
    
    @property
    def title(self):
        """
        Returns the title of the audio stream.
        
        Returns
        -------
        title : `str`
        """
        return f'{self.__class__.__name__} from {self.user.full_name!r}'

class AudioReader(Thread):
    """
    Audio reader of a ``VoiceClient``.
    
    Attributes
    ----------
    audio_streams : `dict` of (`int`, (``AudioStream`` or (`list` of ``AudioStream``))) items
        `source` - ``AudioStream`` relation to store the receiving audio streams.
    client : ``VoiceClient``
        The parent voice client.
    done : `bool`
        Whether the audio reader is done receing and should stop.
    """
    __slots__ = ('audio_streams', 'client', 'done', )
    
    def __init__(self, voice_client):
        """
        Creates an ``AudioReader`` instance bound to the given voice client.
        
        Parameters
        ----------
        voice_client : ``VoiceClient``
            The parent voice client.
        """
        Thread.__init__(self, daemon=True)
        self.client = voice_client
        self.done = False
        self.audio_streams = {}
        self.start()
    
    def run(self):
        empty = []
        
        voice_client = self.client
        try:
            if not voice_client.connected.is_set():
                voice_client.connected.wait()
            
            socket=voice_client.socket
            socketlist = [socket]
            while True:
                
                if self.done:
                    break
                
                if not voice_client.connected.is_set():
                    voice_client.connected.wait()
                    socket = voice_client.socket
                    socketlist = [socket]
                
                ready, _, err = select(socketlist, empty, socketlist, 0.01)
                if not ready:
                    continue
                
                try:
                    data = socket.recv(4096)
                except SocketError as err:
                    if err.errno == 10038: #NOT SOCKET, lets do a circle
                        continue
                    raise
                
                try:
                    if data[1] != 120:
                        #not voice data, we dont care
                        continue
                    
                    packet = RTPPacket(data, voice_client)
                    source = packet.source
                    try:
                        audio_stream = self.audio_streams[source]
                    except KeyError:
                        pass
                    else:
                        voice_packet = VoicePacket(bytes(packet.decrypted))
                        if type(audio_stream) is list:
                            for audio_stream in audio_stream:
                                audio_stream.feed(voice_packet)
                        else:
                            audio_stream.feed(voice_packet)
                
                except BaseException as err:
                    extracted=[
                        'Exception occured at decoding voice packet at\n',
                        repr(self),
                        '\n',
                            ]
                    render_exc_to_list(err, extend=extracted)
                    sys.stderr.write(''.join(extracted))
        
        except BaseException as err:
            extracted = [
                'Exception occured at\n',
                repr(self),
                '.run\n',
                    ]
            render_exc_to_list(err, extend=extracted)
            sys.stderr.write(''.join(extracted))
        
        self.stop()
    
    def stop(self):
        """
        Stops the streams of the audio player.
        """
        self.done = True
        
        voice_client = self.client
        if voice_client.reader is self:
            voice_client.reader = None
        
        audio_streams = self.audio_streams
        if audio_streams:
            collected_audio_streams = []
            for audio_stream in audio_streams.values():
                if type(audio_stream) is list:
                    collected_audio_streams.extend(audio_stream)
                else:
                    collected_audio_streams.append(audio_stream)
            
            audio_streams.clear()
            
            while collected_audio_streams:
                audio_stream = collected_audio_streams.pop()
                audio_stream.stop()
    
    __del__ = stop

del opus
del OpusDecoder
