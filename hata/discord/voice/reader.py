__all__ = ()

from collections import deque

from scarletio import CancelledError, Task, sleep, write_exception_async

from ..core import KOKORO

from .audio_source import AudioSource
from .opus import OpusDecoder, opus
from .rtp_packet import EMPTY_VOICE_FRAME_DECODED, EMPTY_VOICE_FRAME_ENCODED, RTPPacket, VoicePacket


if opus is None:
    DECODER = None
else:
    DECODER = OpusDecoder()


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
    source : `None`, `int`
        Identifier value of the respective user.
    user : ``ClientUserBase``
        The user, who's audio is received.
    yield_decoded : `bool`
        Whether the audio stream should yield encoded data.
    voice_client : ``VoiceClient``
        Weakreference to the parent ``AudioReader`` to avoid reference loops.
    
    Class Attributes
    ----------------
    REPEATABLE : `bool` = `False`
        Whether the source can be repeated after it is exhausted once.
    """
    __slots__ = ('auto_decode', 'buffer', 'done', 'source', 'user', 'yield_decoded', 'voice_client')
    
    def __init__(self, voice_client, user, *, auto_decode=False, yield_decoded=False):
        """
        Creates a new audio stream instance.
        
        Parameters
        ----------
        voice_client : ``VoiceClient``
            Parent ``AudioReader``.
        user : ``ClientUserBase``
            The user, who's audio is received.
        auto_decode : `bool` = `False`, Optional (Keyword only)
            Whether the received packets should be auto decoded.
        yield_decoded : `bool` = `False`, Optional (Keyword only)
            Whether the audio stream should yield decoded data.
        """
        try:
            audio_source = voice_client._audio_sources[user.id]
        except KeyError:
            audio_source = None
        
        self.voice_client = voice_client
        self.buffer = deque()
        self.auto_decode = auto_decode
        self.yield_decoded = yield_decoded
        self.done = False
        self.user = user
        self.source = audio_source
    
    
    def stop(self):
        """
        Stops the audio stream by marking it as done and un-links it as well.
        """
        if self.done:
            return
        
        self.done = True
        self.voice_client._unlink_audio_stream(self)
    
    
    async def cleanup(self):
        """
        Cleans the audio stream up.
        
        This method is a coroutine.
        """
        self.stop()
    
    __del__ = stop
    
    
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
    
    
    async def read(self):
        """
        Reads a frame from the audio stream's buffer.
        
        With yielding `None` indicates end of stream.
        
        This method is a coroutine.
        
        Returns
        -------
        frame : `None`, `bytes`
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


class AudioReader:
    """
    Audio reader of a ``VoiceClient``.
    
    Attributes
    ----------
    audio_streams : `dict` of (`int`, (``AudioStream`` or (`list` of ``AudioStream``))) items
        `source` - ``AudioStream`` relation to store the receiving audio streams.
    done : `bool`
        Whether the audio reader is done receiving and should stop.
    task : `None`, ``Task``
        Audio reader task. Set as `None` if the reader is stopped.
    voice_client : ``VoiceClient``
        The parent voice client.
    """
    __slots__ = ('audio_streams', 'done', 'task', 'voice_client', )
    
    def __init__(self, voice_client):
        """
        Creates an ``AudioReader`` bound to the given voice client.
        
        Parameters
        ----------
        voice_client : ``VoiceClient``
            The parent voice client.
        """
        self.voice_client = voice_client
        self.done = False
        self.audio_streams = {}
        self.task = Task(self.run(), KOKORO)
    
    
    async def run(self):
        """
        The main runner of the ``AudioReader`` what keeps reading from the voice client's datagram stream and feeding
        them to the receiver ``AudioStream``-s.
        
        This method is a coroutine.
        """
        voice_client = self.voice_client
        audio_streams = self.audio_streams
        
        try:
            if not voice_client.connected.is_set():
                await voice_client.connected
            
            protocol = voice_client._protocol
            while True:
                
                if self.done:
                    break
                
                if not voice_client.connected.is_set():
                    await voice_client.connected
                    protocol = voice_client._protocol
                
                try:
                    data = await protocol.read_once()
                except CancelledError:
                    if self.done:
                        protocol.cancel_current_reader()
                        return
                    
                    # If cancelled, we are probably establishing connection, so wait till that is done.
                    payload_waiter = protocol.payload_waiter
                    if payload_waiter is None:
                        # Wait some?
                        await sleep(0.2, KOKORO)
                        payload_waiter = protocol.payload_waiter
                        if payload_waiter is None:
                            continue
                    
                    await payload_waiter
                    continue
                
                if not audio_streams:
                    continue
            
                try:
                    if data[1] != 120:
                        # not voice data, we don't care
                        continue
                    
                    packet = RTPPacket(data, voice_client)
                    source = packet.source
                    try:
                        audio_stream = audio_streams[source]
                    except KeyError:
                        pass
                    else:
                        voice_packet = VoicePacket(bytes(packet.decrypted))
                        if type(audio_stream) is list:
                            for audio_stream in audio_stream:
                                audio_stream.feed(voice_packet)
                        else:
                            audio_stream.feed(voice_packet)
                
                except GeneratorExit:
                    raise
                
                except BaseException as err:
                    if isinstance(err, CancelledError) and self.done:
                        return
                    
                    await write_exception_async(
                        err,
                         [
                            'Exception occurred at decoding voice packet at\n',
                            repr(self),
                            '\n',
                        ],
                       loop = KOKORO,
                    )
        
        except GeneratorExit:
            self.stop()
            raise
        
        except BaseException as err:
            if isinstance(err, CancelledError) and self.done:
                return
            
            await write_exception_async(
                err,
                [
                    'Exception occurred at\n',
                    repr(self),
                    '\n',
                ],
                loop = KOKORO,
            )
        
        self.stop()
    
    
    def stop(self):
        """
        Stops the streams of the audio player.
        """
        task = self.task
        if task is None:
            return
        
        self.task = None
        self.done = True
        task.cancel()
        
        voice_client = self.voice_client
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
