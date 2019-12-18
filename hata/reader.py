# -*- coding: utf-8 -*-
from threading import Thread, Lock
from select import select
from socket import error as SocketError
from collections import deque
import sys
from .opus import OpusDecoder, SAMPLES_PER_FRAME
from .futures import render_exc_to_list
#poll is not on windows, but if u want i can add an optimized case for linux
#it is just dumb, how much times i need to copy data instead of slicing it with memoryview

EMPTY_VOICE_DATA=b'\x00'*3840

def insert_packet(buffer,packet):
    timestamp=packet.timestamp
    
    top=len(buffer)
    bot=0
    while True:
        if bot<top:
            half=(bot+top)>>1
            if buffer[half].timestamp>timestamp:
                bot=half+1
            else:
                top=half
            continue
        break

    if bot==len(buffer):
        buffer.append(packet)
        return
    
    other=buffer[bot]
    if other.timestamp==timestamp:
        return

    buffer.insert(bot,packet)
    
class Array_uint_32b(object): #TODO : ask python to implement arrays already
    __slots__=('_data', '_offset', '_limit')
    def __init__(self,data,offset,limit):
        self._data  = data
        self._offset= offset
        self._limit = limit

    def __len__(self):
        limit   = self._limit
        offset  = self._offset
        value   = (limit-offset)>>2

        return value
    
    def __getitem__(self,index):
        index   = index<<2
        offset  = self._offset+index
        value   = int.from_bytes(self._data[offset:offset+4],'big')
        
        return value
    
    def __iter__(self):
        data    = self._data
        offset  = self._offset
        limit   = self._limit
        
        while True:
            if offset==limit:
                break
            value=int.from_bytes(data[offset:offset+4],'big')
            yield value
            
            offset=offset+4
    
class PacketBase(object):
    __slots__=()

    def __gt__(self,other):
        if isinstance(other,PacketBase):
            return self.timestamp<other.timestamp
        return NotImplemented

    def __ge__(self,other):
        if isinstance(other,PacketBase):
            if self.timestamp<other.timestamp:
                return True
            if self.timestamp!=other.timestamp:
                return False
            if type(self) is not type(other):
                return False
            #TODO?
            return True
        return NotImplemented
    
    def __eq__(self,other):
        if isinstance(other,PacketBase):
            if self.timestamp!=other.timestamp:
                return False
            if type(self) is not type(other):
                return False
            #TODO?
            return True
        return NotImplemented

    def __ne__(self,other):
        if isinstance(other,PacketBase):
            if self.timestamp!=other.timestamp:
                return True
            if type(self) is not type(other):
                return True
            #TODO
            return False
        return NotImplemented
    
    def __le__(self,other):
        if isinstance(other,PacketBase):
            if self.timestamp<other.timestamp:
                return True
            if self.timestamp!=other.timestamp:
                return False
            if type(self) is not type(other):
                return False
            #TODO?
            return True
        return NotImplemented
        
    def __lt__(self,other):
        if isinstance(other,PacketBase):
            return self.timestamp<other.timestamp
        return NotImplemented

    @property
    def timestamp(self):
        return 0

class VoicePacket(PacketBase):
    __slots__=('data', 'timestamp')

    def __init__(self,data,timestamp):
        self.data       = data
        self.timestamp  = timestamp
        
    def __repr__(self):
        return f'<{self.__class__.__name__} timestamp={self.timestamp}, size={len(self.data)}>'

class RTPPacket(PacketBase):
    __slots__=('_data', '_offset1', '_offset2', '_decrypted',)

    def __init__(self,data,voice_client):
        self._data=data
        offset=12
        cc=self.cc
        if cc:
            offset=offset+(cc<<2)
        self._offset1=offset
        
        nonce=data[:12]+b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        decrypted=voice_client._secret_box.decrypt(data[offset:],nonce)
        self._decrypted=decrypted
        
        if self.extended:
            extension=int.from_bytes(decrypted[2:4],'big')
            offset=(extension<<2)+4
        else:
            offset=0
        
        self._offset2=offset
        
    @property
    def data(self):
        return memoryview(self._data)[self._offset1:]

    @property
    def decrypted(self):
        return memoryview(self._decrypted)[self._offset2:]
    
    @property
    def csrcs(self):
        return Array_uint_32b(self._data,12,self._offset1)

    @property
    def extension_profile(self):
        if not self.extended:
            return 0
        
        profile=int.from_bytes(self._decrypted[0:2],'big')
        return profile

    @property
    def extension_length(self):
        if not self.extended:
            return 0

        length=int.from_bytes(self._decrypted[2:4],'big')
        return length

    @property
    def extension_values(self):
        limit=self._offset2
        if limit<=4:
            return None
        return Array_uint_32b(self._decrypted,4,limit)
        
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
        return int.from_bytes(self._data[4:8],'big')

    @property
    def ssrc(self):
        return int.from_bytes(self._data[8:12],'big')

    @property
    def sequence(self):
        return int.from_bytes(self._data[2:4],'big')

    @property
    def header(self):
        return memoryview(self._data)[:12]

    def __repr__(self):
        return f'<{self.__class__.__name__} timestamp={self.timestamp}, ssrc={self.ssrc}, sequence={self.sequence}, size={len(self.data)}>'

#NOT USED

###http://www.rfcreader.com/#rfc3550_line855
##class RTCPPacket(PacketBase):
##    __slots__=('_data')
##    type=0
##
##    def __init__(self,data):
##        self._data=data
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
##        return int.from_bytes(self._data[2:4],'big')
##
##    @property
##    def report_count(self):
##        return self._data[0]&0b00011111
##
##    @property
##    def ssrc(self):
##        return int.from_bytes(self._data[4:8],'big')
##
##class _RPReport(self):
##    __slots__=('_data','_offset')
##    def __init__(self,data,offset):
##        self._data  = data
##        self._offset= offset
##
##    @property
##    def ssrc(self):
##        offset=self._offset
##        return int.from_bytes(self._data[offset:offset+4],'big')
##
##    @property
##    def loss_percent(self):
##        offset=self._offset
##        return self._data[offset+4]
##
##    @property
##    def loss_total(self):
##        offset=self._offset+5
##        return int.from_bytes(self._data[offset:offset+3],'big')
##
##    @property
##    def last_sequence(self):
##        offset=self._offset+8
##        return int.from_bytes(self._data[offset:offset+4],'big')
##
##    @property
##    def jitter(self):
##        offset=self._offset+12
##        return int.from_bytes(self._data[offset:offset+4],'big')
##
##    @property
##    def lsr(self):
##        offset=self._offset+16
##        return int.from_bytes(self._data[offset:offset+4],'big')
##
##    @property
##    def dlsr(self):
##        offset=self._offset+20
##        return int.from_bytes(self._data[offset:offset+4],'big')
##        
###http://www.rfcreader.com/#rfc3550_line1614
##class SenderReportPacket(RTCPPacket):
##    __slots__ = ('_descripted', '_offset1')
##    type=200
##    
##    def __init__(self,data,voice_client):
##        data_shard=data[:8]
##        self._data=data_shard
##        
##        nonce=data_shard+b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
##        descripted=voice_client._secret_box.decrypt(data[8:],nonce)
##        self._descripted=descripted
##        
##        report_count=data_shard[0]&0b00011111
##        offset=(report_count*24)+20
##        self._offset1=offset
##
##    def __repr__(self):
##        return f'<{self.__class__.__name__} timestamp={self.timestamp}, length={self.length}, reports={self.report_count}>'
##    
##    @property
##    def descripted(self):
##        return memoryview(self._descripted)[24:]
##    
##    @property
##    def info_ntp_ts_msw(self):
##        return int.from_bytes(self._descripted[0:4],'big')
##
##    @property
##    def info_ntp_ts_lsw(self):
##        return int.from_bytes(self._descripted[4:8],'big')
##
##    @property
##    def info_ntp_ts(self):
##        low = int.from_bytes(self._descripted[4:8],'big')
##        low = low/(1<<low.bit_length())
##        
##        high= int.from_bytes(self._descripted[0:4],'big')
##        
##        return high+low
##
##    @property
##    def info_rtp_ts(self):
##        return int.from_bytes(self._descripted[8:12],'big')
##
##    @property
##    def info_sequence(self):
##        return int.from_bytes(self._descripted[12:16],'big')
##
##    @property
##    def info_octet(self):
##        return int.from_bytes(self._descripted[16:20],'big')
##
##    @property
##    def extension(self):
##        data    = self._descripted
##        offset  = self._offset1
##        
##        if len(data)>offset:
##            return memoryview(descripted)[offset:]
##
##    def report_get(self,index):
##        offset  = (index*24)+20
##        obj     = _RPReport(self._descripted,offset)
##        
##        return obj
##
##    def report_iter(self,index):
##        data    = self._descripted
##        limit   = self._offset1
##        offset  = 20
##        
##        while True:
##            if offset>=limit:
##                break
##            obj=_RPReport(data,offset)
##            yield obj
##            
##            offset=offset+24
##
###http://www.rfcreader.com/#rfc3550_line1879
##class ReceiverReportPacket(RTCPPacket):
##    __slots__ = ('_descripted','_offset1')
##    type = 201
##    
##    def __init__(self,data,voice_client):
##        data_shard=data[:8]
##        self._data=data_shard
##        
##        nonce=data_shard+b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
##        descripted=voice_client._secret_box.decrypt(data[8:],nonce)
##        self._descripted=descripted
##        
##        report_count=data_shard[0]&0b00011111
##        offset=report_count*24
##        self._offset1=offset
##
##    def __repr__(self):
##        return f'<{self.__class__.__name__} timestamp={self.timestamp}, length={self.length}, reports={self.report_count}>'
##
##    @property
##    def descripted(self):
##        return memoryview(self._descripted)
##    
##    def report_get(self,index):
##        offset  = index*24
##        obj     = _RPReport(self._descripted,offset)
##        
##        return obj
##
##    def report_iter(self,index):
##        data    = self._descripted
##        limit   = self._offset1
##        offset  = 0
##        
##        while True:
##            if offset>=limit:
##                break
##            obj=_RPReport(data,offset)
##            yield obj
##            
##            offset=offset+24

class AudioReader(Thread):
    __slots__=('client', 'done', 'socket', 'decoder', 'decoded', 'buffer_lock')
    def __init__(self,voice_client):
        Thread.__init__(self,daemon=True)
        self.client     = voice_client
        self.done       = False
        self.socket     = NotImplemented
        self.decoded    = {}
        self.buffer_lock= Lock()
        self.decoder    = OpusDecoder()
        self.start()

    def get_audio_frames_for(self,user,flush=True,fill=True):
        user_id=user.id
        result=[]
        try:
            source=self.client.sources[user_id]
        except KeyError:
            return result

        with self.buffer_lock:
            try:
                buffer=self.decoded[source]
            except KeyError:
                return result

            if not buffer:
                return result

            if fill:
                frame=buffer[0]
                result.append(frame.data)
                timestamp=frame.timestamp
                expected_timestamp=timestamp+SAMPLES_PER_FRAME

                index=0
                limit=len(buffer)
                
                while True:
                    if index==limit:
                        break

                    frame=buffer[index]
                    timestamp=frame.timestamp
                    
                    if timestamp<expected_timestamp:
                        
                        while True:
                            result.append(EMPTY_VOICE_DATA)
                            expected_timestamp=expected_timestamp+SAMPLES_PER_FRAME
                            if expected_timestamp<timestamp:
                                continue
                            
                            break

                    result.append(frame.data)
                    expected_timestamp=timestamp+SAMPLES_PER_FRAME

                    index=index+1
                    continue

            else:
                index=0
                limit=len(buffer)
                while True:
                    
                    frame=buffer[index]
                    result.append(frame.data)

                    index=index+1
                    if index==limit:
                        break
                    
                    continue

            if flush:
                buffer.clear()
        
        return result
        
        
    def stop(self):
        self.done=True
        self.client.reader=None
    
    def run(self):
        empty=[]

        voice_client=self.client
        try:
            if not voice_client.connected.is_set():
                voice_client.connected.wait()

            socket=voice_client.socket
            socketlist=[socket]
            while True:

                if self.done:
                    break
                
                if not voice_client.connected.is_set():
                    voice_client.connected.wait()
                    socket=voice_client.socket
                    socketlist=[socket]

                ready,_,err=select(socketlist,empty,socketlist,0.01)
                if not ready:
                    continue
                
                try:
                    data=socket.recv(4096)
                except SocketError as err:
                    if err.errno==10038: #NOT SOCKET, lets do a circle
                        continue
                    raise
                
                try:
                    if data[1]!=120:
                        #not voice data, we dont care
                        continue
                    
                    packet=RTPPacket(data,voice_client)

                    voice_data=self.decoder.decode(bytes(packet.decrypted))
                    voice_packet=VoicePacket(voice_data,packet.timestamp)
                    
                    with self.buffer_lock:
                        source=packet.ssrc
                        try:
                            buffer=self.decoded[source]
                        except KeyError:
                            buffer=deque()
                            self.decoded[source]=buffer

                        insert_packet(buffer,voice_packet)
                        
                except BaseException as err:
                    extracted=[
                        'Exception occured at decoding voice packet at\n',
                        self.__repr__(),
                        '\n',
                            ]
                    render_exc_to_list(err,extend=extracted)
                    sys.stderr.write(''.join(extracted))
                
        except BaseException as err:
            extracted=[
                'Exception occured at\n',
                self.__repr__(),
                '.run\n',
                    ]
            render_exc_to_list(err,extend=extracted)
            sys.stderr.write(''.join(extracted))

