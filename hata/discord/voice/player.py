__all__ = ()

from audioop import mul as audio_mul
from time import perf_counter

from scarletio import CancelledError, Event, Task, sleep, write_exception_async

from ..core import KOKORO

from .opus import FRAME_LENGTH, SAMPLES_PER_FRAME


PLAYER_DELAY = FRAME_LENGTH / 1000.0

del FRAME_LENGTH

class AudioPlayer:
    """
    Sends voice data through the voice client's socket.
    
    Attributes
    ----------
    done : `bool`
        Whether the audio player finished playing it's source.
    resumed_waiter : `threading.Event`
        Indicates whether the the audio player is not paused.
    source : ``AudioSource``
        The audio source what the player reads each 20 ms.
    should_update : `bool`
        Whether the voice client should update itself.
    task : `None`, ``Task``
        Audio reader task. Set as `None` if the reader is stopped.
    voice_client : ``VoiceClient``
        The voice client of audio player.
    """
    __slots__ = ('done', 'resumed_waiter', 'should_update', 'source', 'task', 'voice_client')
    
    def __init__(self, voice_client, source):
        """
        Creates an starts the audio player.
        
        Parameters
        ----------
        voice_client : ``VoiceClient``
            The voice client of audio player.
        source : ``AudioSource``
            The audio source what the player reads each 20 ms.
        """
        self.source = source
        self.voice_client = voice_client
        
        resumed_waiter = Event(KOKORO)
        resumed_waiter.set()    # we are not paused
        self.resumed_waiter = resumed_waiter
        self.should_update = True
        self.done = False
        
        self.task = Task(self.run(), KOKORO)
    
    async def run(self):
        """
        The main runner of ``AudioPlayer``. Is instantly started inside of a ``Task`` as the player is created.
        
        This method is a coroutine.
        """
        voice_client = self.voice_client
        start = perf_counter()
        loops = 0
        
        source = None
        
        try:
            while True:
                if self.should_update:
                    source = await self.update(source)
                    if source is None:
                        break
                    
                    start = perf_counter()
                    loops = 0
                    continue
                
                # are we disconnected from voice?
                if not voice_client.connected.is_set():
                    await voice_client.connected
                    start = perf_counter()
                    loops = 0
                    continue
                
                loops += 1
                
                data = await source.read()
                
                if data is None:
                    self.source = None
                    await source.cleanup()
                    self.pause()
                    
                    async with voice_client.lock:
                        await voice_client.call_after(voice_client, source)
                    
                    source = None
                    self.should_update = True # safety first
                    continue
                
                sequence = voice_client._sequence
                if sequence == 65535:
                    sequence = 0
                else:
                    sequence += 1
                voice_client._sequence = sequence
                
                if source.NEEDS_ENCODE:
                    pref_volume = voice_client._pref_volume
                    if (pref_volume != 1.0):
                        data = audio_mul(data, 2, pref_volume)
                    
                    data = voice_client._encoder.encode(data)
                
                header = b''.join([
                    b'\x80x',
                    voice_client._sequence.to_bytes(2, 'big'),
                    voice_client._timestamp.to_bytes(4, 'big'),
                    voice_client._audio_source.to_bytes(4, 'big'),
                ])
                
                nonce = header + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                packet = bytearray(header) + voice_client._secret_box.encrypt(bytes(data), nonce).ciphertext
                
                voice_client.send_packet(packet)
                
                timestamp = voice_client._timestamp + SAMPLES_PER_FRAME
                if timestamp > 4294967295:
                    timestamp = 0
                voice_client._timestamp = timestamp
                
                delay = PLAYER_DELAY + ((start + PLAYER_DELAY * loops) - perf_counter())
                if delay < 0.0:
                    continue
                await sleep(delay, KOKORO)
        
        except BaseException as err:
            if voice_client.player is self:
                voice_client.player = None
            
            self.done = True
            
            self.source = None
            if (source is not None):
                await source.cleanup()
                source = None
            
            if isinstance(err, GeneratorExit):
                raise
            
            if isinstance(err, CancelledError):
                return
            
            await write_exception_async(
                err,
                [
                    'Exception occurred at \n',
                    repr(self),
                    '\n',
                ],
                loop = KOKORO
            )
            
        else:
            if voice_client.player is self:
                voice_client.player = None
        
        finally:
            self.task = None
            
            # Force resume if applicable.
            if voice_client.player is None:
                queue = voice_client.queue
                if queue:
                    voice_client.player = type(self)(voice_client, queue.pop(0))
    
    async def update(self, actual_source):
        """
        Updates the player if ``.should_update`` is set as `True`.
        
        Waits for it's resumed waiter to be set if paused. If the voice player's source is updated, then initializes it
        as well and closes the old one too.
        
        This method is a coroutine.
        
        Parameters
        ----------
        actual_source : `None`, ``AudioSource``
            The actual audio source of the player.
        
        Returns
        -------
        new_source : `None`, `AudioSource``
            New source of the player to play.
            
            Can be same as the `actual_source`.
        """
        resumed_waiter = self.resumed_waiter
        if not resumed_waiter.is_set():
            await resumed_waiter
        
        self.should_update = False
        new_source = self.source
        if (new_source is None):
            if (self.voice_client.player is not self):
                self.done = True
                return None
            
            if (actual_source is not None):
                await actual_source.cleanup()
            
            return None
        
        if (new_source is actual_source):
            return actual_source
        
        if (actual_source is not None):
            await actual_source.cleanup()
        
        await new_source.postprocess()
        return new_source
    
    def pause(self):
        """
        Pauses the player.
        """
        self.resumed_waiter.clear()
        self.should_update = True
    
    def resume(self):
        """
        Resumes the player if paused.
        """
        resumed_waiter = self.resumed_waiter
        if not resumed_waiter.is_set():
            resumed_waiter.set()
            self.should_update = True
    
    def stop(self):
        """
        Stops the player if running.
        """
        if self.done:
            return
        
        self.done = True
        task = self.task
        if (task is not None):
            task.cancel()
        
        self.should_update = True
        self.resumed_waiter.set()
    
    def set_source(self, source):
        """
        Sets they player source.
        
        Parameters
        ----------
        source : `None`, ``AudioSource``
            The new source of the player.
        """
        self.source = source
        self.should_update = True
        
        resumed_waiter = self.resumed_waiter
        if not resumed_waiter.is_set():
            resumed_waiter.set()
