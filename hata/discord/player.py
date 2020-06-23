# -*- coding: utf-8 -*-
__all__ = ('DownloadError', 'LocalAudio', 'YTAudio', )

import os, sys, subprocess, audioop, shlex
from threading import Event, Thread, current_thread
from time import perf_counter, sleep as blocking_sleep

from ..backend.dereaddons_local import alchemy_incendiary
from ..backend.futures import render_exc_to_list
from ..backend.eventloop import EventThread

from .client_core import KOKORO
from .opus import FRAME_LENGTH, FRAME_SIZE, SAMPLES_PER_FRAME

PLAYER_DELAY=FRAME_LENGTH/1000.0

del FRAME_LENGTH


if os.name=='nt':
    SUBPROCESS_STARTUP_INFO=subprocess.STARTUPINFO()
    SUBPROCESS_STARTUP_INFO.dwFlags|=subprocess.STARTF_USESHOWWINDOW
    SUBPROCESS_STARTUP_INFO.wShowWindow=subprocess.SW_HIDE
else:
    SUBPROCESS_STARTUP_INFO=None
            
class AudioSource(object):
    """
    Base class for audio sources.
    
    Class Attributes
    ----------------
    NEEDS_ENCODE : `bool` = `True`
        Whether the source is not opus encoded.
    TEMPORARY : `bool` = `False`
        Whether the audio's source is a temporary file.
    """
    __slots__ = ()
    
    NEEDS_ENCODE = True
    
    TEMPORARY = False
    
    def read(self):
        """
        Reads 20ms audio data.
        
        Indicates end of stream by returning `None`.
        
        > Subclasses should implement it.
        
        Returns
        -------
        audio_data : `bytes` or `None`
        """
        return b''

    def cleanup(self):
        """
        Cleans up the allocated resources by the audio source.
        
        > Subclasses should overwrite it.
        """
        pass

    def __del__(self):
        """Cleans up the audio source if ``.cleanup`` was not called for any reason."""
        self.cleanup()

    def parse_title(self):
        """
        Parses and returns the audio source's title.
        
        > Subclasses should overwrite it.
        
        Returns
        -------
        title : `str`
        """
        return 'Unknown'
    
class PCMAudio(AudioSource):
    """
    Represents raw 16-bit 48KHz stereo PCM audio source.
    
    Attributes
    -----------
    stream : `Any`
        PCM (Pulse Code Modulation) output.
    
    Class Attributes
    ----------------
    NEEDS_ENCODE : `bool` = `True`
        Whether the source is not opus encoded.
    TEMPORARY : `bool` = `False`
        Whether the audio's source is a temporary file.
    """
    __slots__=('stream',)

    def __new__(cls, stream):
        """
        Creates a new ``PCMAudio`` source.
        
        Parameters
        ----------
        stream : `Any`
            Opus decoded PCM (Pulse Code Modulation).
        
        Returns
        -------
        self : ``PCMAudio``
        """
        self=object.__new__(cls)
        self.stream=stream
        return self

    def read(self):
        """
        Reads 20ms audio data.
        
        Indicates end of stream by returning `None`
        
        Returns
        -------
        audio_data : `bytes` or `None`
        """
        result=self.stream.read(FRAME_SIZE)
        if len(result)!=FRAME_SIZE:
            return None
        return result

class FFmpegPCMAudio(AudioSource):
    """
    Represents an ffmpeg pcm audio.
    
    You must have the ffmpeg or avconv executable in your path environment variable in order for this to work.
    
    Attributes
    ----------
    process : `subprocess.Popen`
        The ffmpeg or the avconv subprocess.
    source : `str`
        The source audio file's path.
    stdout : `_io.BufferedReader`
        Stdout of the `.process`.
    
    Class Attributes
    ----------------
    NEEDS_ENCODE : `bool` = `True`
        Whether the source is not opus encoded.
    TEMPORARY : `bool` = `False`
        Whether the audio's source is a temporary file.
    """
    __slots__ = ('process', 'source', 'stdout',)
    
    #use __new__, so __del__ wont run
    def __new__(cls, source, executable='ffmpeg', pipe=False, stderr=None, before_options=(), options=(),):
        """
        Creates a new ``FFmpegPCMAudio`` instance.
        
        Parameters
        ----------
        source : `str`
            The source audio file's path.
        executable : `str`
            The executable's name to use. Defaults to `'ffmpeg'`.
        pipe : `bool`
            Whether the source is passed to stdin.
        stderr : `file-like`
            Stdout for the
        before_options : `str` or (`iterable` of `str`)
            Extra arguments passed before the `-i` flag.
        options : `str` or (`iterable` of `str`)
            Extra arguments passed after the `-i` flag.
        
        Returns
        -------
        self : ``FFmpegPCMAudio``
        
        Raises
        ------
        ValueError
            - Executable as not found.
            - Popen failed.
        """
        if isinstance(before_options,str):
            before_options=shlex.split(before_options)
        
        if isinstance(options,str):
            options=shlex.split(options)
        
        args = [
            executable,
            *before_options,
            '-i',
            '-' if pipe else source,
            '-f',
            's16le',
            '-ar',
            '48000',
            '-ac',
            '2',
            '-loglevel',
            'panic',
            *options,
            'pipe:1',
                ]
        
        if pipe:
            stdin=source
        else:
            stdin=None
        
        try:
            process = subprocess.Popen(args, stdin=stdin, stdout=subprocess.PIPE, stderr=stderr,
                startupinfo=SUBPROCESS_STARTUP_INFO)
        except FileNotFoundError:
            raise ValueError(f'{executable} was not found.') from None
        except subprocess.SubprocessError as err:
            raise ValueError(f'Popen failed: {err.__class__.__name__}: {err}') from err
        
        self=object.__new__(cls)
        
        self.source     = source
        self.process    = process
        self.stdout     = process.stdout

        return self
        
    def read(self):
        """
        Reads 20ms audio data.
        
        Indicates end of stream by returning zero `None`.
        
        Returns
        -------
        audio_data : `bytes` or `None`
        """
        result=self.stdout.read(FRAME_SIZE)
        if len(result)!=FRAME_SIZE:
            return None
        return result

    def cleanup(self):
        """
        Closes ``.process`.`
        """
        process=self.process
        if process is None:
            return

        process.kill()
        if process.poll() is None:
            process.communicate()

        self.process=None

    def parse_title(self):
        """
        Parses and returns the audio source's title.
        
        Returns
        -------
        title : `str`
        """
        _,name=os.path.split(self.source)
        index=name.rfind('.')
        if index<0:
            return name
        return name[:index]
    
class PCMVolumeTransformer(AudioSource):
    """
    Volume transformer what wraps an other ``AudioSource`` instance.
    
    Attributes
    ----------
    original : ``AudioSource`` instance
        The wrapped audio source.
    volume : `float`
        The volume multiplier.
    
    Class Attributes
    ----------------
    NEEDS_ENCODE : `bool` = `True`
        Whether the source is not opus encoded.
    TEMPORARY : `bool` = `False`
        Whether the audio's source is a temporary file.
    """
    __slots__ = ('original', 'title', 'volume',)
    
    def __new__(cls, original):
        """
        Creates a new `PCMVolumeTransformer` from the given audio source.
        
        Parameters
        ----------
        original : ``AudioSource`` instance.
            The audio source to wrap.
        
        Returns
        -------
        self : ``PCMVolumeTransformer``
        
        Raises
        ------
        TypeError
            `original` is not `AudioSource` instance.
        ValueError
            `original` is opus encoded.
        """
        if not isinstance(original, AudioSource):
            raise TypeError(f'`original` can be `{AudioSource.__name__}` instance, got {original.__class__.__name__}.')
        
        if not original.NEEDS_ENCODE:
            raise ValueError('`original` must not be Opus encoded.')
        
        self = object.__new__(cls)
        
        self.original   = original
        self.volume     = 1.0 #max volume is 2.0
        self.title      = original.parse_title()
        
        return self
    
    def cleanup(self):
        """
        Cleans up ``.original`.
        """
        original = self.original
        if original is None:
            return
        
        original.cleanup()
    
    def read(self):
        """
        Reads ``.original`` and transforms it's volume.
        
        Indicates end of stream by returning zero `None`.
        
        Returns
        -------
        audio_data : `bytes` or `None`
        """
        audio_data = self.original.read()
        if (audio_data is not None):
            audio_data = audioop.mul(audio_data, 2, self.volume)
        
        return audio_data
    
    def parse_title(self):
        """
        Returns the original audio source's title.
        
        Returns
        -------
        title : `str`
        """
        return self.original.parse_title()

async def LocalAudio(path):
    """
    Provides an easy async way to open a local audio file.
    
    Parameters
    ----------
    path : `str`
        Path of the audio file.
    
    Returns
    -------
    audio_source : ``PCMVolumeTransformer``
    
    Raises
    ------
    RuntimeError
        Was not called from an `EventThread`.
    ValueError
        - Executable as not found.
        - Popen failed.
    """
    loop = current_thread()
    if not isinstance(loop,EventThread):
        raise RuntimeError(f'LocalAudio({path!r},...) was called from a non {EventThread.__name__}: {loop!r}.')
        
    source = await loop.run_in_executor(alchemy_incendiary(FFmpegPCMAudio,(path,)))
    return PCMVolumeTransformer(source)

try:
    import youtube_dl
except ImportError:
    youtube_dl=None
    DownloadError = None
    YTAudio = None
else:
    from youtube_dl.utils import DownloadError
    youtube_dl.utils.bug_reports_message = lambda: ''
    
    YTdl=youtube_dl.YoutubeDL({
        'format'            : 'bestaudio/best',
        'outtmpl'           : '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames' : True,
        'noplaylist'        : True,
        'nocheckcertificate': True,
        'ignoreerrors'      : False,
        'logtostderr'       : False,
        'quiet'             : True,
        'no_warnings'       : True,
        'default_search'    : 'auto',
        'source_address'    : '0.0.0.0',
            })
        
    class YTAudio(PCMVolumeTransformer):
        """
        Represents an audio sourced downloaded from youtube.
        
        You must have the ffmpeg or avconv executable in your path environment variable in order for this to work.
        
        Attributes
        ----------
        process : `subprocess.Popen`
            The ffmpeg or the avconv subprocess.
        source : `str`
            The source audio file's path.
        stdout : `_io.BufferedReader`
            Stdout of the `.process`.
        
        Class Attributes
        ----------------
        NEEDS_ENCODE : `bool` = `True`
            Whether the source is not opus encoded.
        TEMPORARY : `bool` = `True`
            Whether the audio's source is a temporary file.
        """
        TEMPORARY = True
        
        __slots__=('delete', 'original', 'title', 'url', 'volume',)
        
        @staticmethod
        def _download(url):
            """
            Downloads the audio source by the given url or title.
            
            This function runs inside of an executor thread.
            
            Parameters
            ----------
            url : `str`
            
            Returns
            -------
            original : ``FFmpegPCMAudio``
                Audio stream source.
            filename : `str`
                The title of the dowloaded audio.
            data : `dict` of
            """
            data = YTdl.extract_info(url, download=True)
            
            if 'entries' in data: #playlist
                data=data['entries'][0]
            
            #if stream:filename=data['url']
            filename = YTdl.prepare_filename(data)
            original = FFmpegPCMAudio(filename, options=('-vn',))
            
            return original,filename,data
        
        async def __new__(cls, url, executor_id=None, delete_after=True):
            """
            Creates a new ``YTAudio`` instance.
            
            Parameters
            ----------
            url : `str`
                The url or the title of the video.
            executor_id : `int`, Optional
                Id of an executor to use. Two executor with the same id cannot run and `ReferenceError` is raised.
            delete_after : `bool`
                Whether the temporary file should be deleted after it finished playing.
            
            Returns
            -------
            self : ``YTAudio``
            
            Raises
            ------
            DownloadError
                Downloading the audio source failed.
            PermissionError
                The given file started to be played at the same time by an other player as well.
            ReferenceError
                There is an already running executor with the given id.
            RuntimeError
                Was not called from an `EventThread`.
            ValueError
                - Executable as not found.
                - Popen failed.
            """
            loop = current_thread()
            if not isinstance(loop,EventThread):
                raise RuntimeError(f'{cls.__name__}({url!r},...) was called from a non {EventThread.__name__}: {loop!r}.')
            
            func = alchemy_incendiary(cls._download,(url,))
            
            if (executor_id is None):
                future=loop.run_in_executor(func)
            else:
                future=loop.run_in_id_executor(func,executor_id)
            
            original, filename, data = await future
            
            #create self only at the end, so the `__del__` wont pick it up
            self=object.__new__(cls)
            self.original   = original
            self.title      = data.get('title')
            self.url        = data.get('url')
            self.volume     = 1.0
            if delete_after:
                delete = filename
            else:
                delete = None
            self.delete = delete
            
            return self
        
        def cleanup(self):
            """
            Cleans up ``.original`` and removes the ``YTAudio's file if given.
            """
            self.original.cleanup()
            delete=self.delete
            if delete is None:
                return
            
            self.delete=None
            try:
                os.remove(delete)
            except (PermissionError,FileNotFoundError):
                pass

class AudioPlayer(Thread):
    """
    Sends voice data through the voice client's socket.
    
    Attributes
    ----------
    client : ``VoiceClient``
        The voice client of audio player.
    done : `bool`
        Whether the audio player finished playing it's source.
    resumed : `threading.Event`
        Indicates whether the the audio player is not paused.
    source : ``AudioSource`` instance
        The audio source what the player reads each 20 ms.
    """
    __slots__=('client', 'done', 'resumed', 'source')
    
    def __init__(self, voice_client, source):
        """
        Creates an starts the audio player.
        
        Parameters
        ----------
        voice_client : ``VoiceClient``
            The voice client of audio player.
        source : ``AudioSource`` instance
            The audio source what the player reads each 20 ms.
        """
        Thread.__init__(self, daemon=True)
        self.source = source
        self.client = voice_client
        self.done  = False
        
        resumed = Event()
        resumed.set()    #we are not paused
        self.resumed = resumed
        
        Thread.start(self)
    
    def run(self):
        voice_client=self.client
        start=perf_counter()
        loops=0
        
        try:
            while True:
                if not self.resumed.is_set():
                    self.resumed.wait()
                    start=perf_counter()
                    loops=0
                    continue
                
                #are we disconnected from voice?
                if not voice_client.connected.is_set():
                    voice_client.connected.wait()
                    start=perf_counter()
                    loops=0
                    continue
                
                loops+=1
                data=self.source.read()
                
                if self.done or (data is None):
                    self.resumed.clear()
                    self.source.cleanup()
                    self.source=None
                    if voice_client.lock.locked():
                        voice_client.lock.acquire()
                    else:
                        with voice_client.lock:
                            stop=KOKORO.create_task_threadsafe(voice_client.call_after(voice_client,lock=False)).syncwrap().wait()
                        if stop:
                            self.done=True
                            self.resumed.set()
                            break
                    
                    continue
                
                sequence=voice_client._sequence
                if sequence==65535:
                    sequence=0
                else:
                    sequence=sequence+1
                voice_client._sequence=sequence
                
                if self.source.NEEDS_ENCODE:
                    data=voice_client._encoder.encode(data)
                
                header=b''.join([
                    b'\x80x',
                    voice_client._sequence.to_bytes(2,'big'),
                    voice_client._timestamp.to_bytes(4,'big'),
                    voice_client._source.to_bytes(4,'big'),
                        ])
                
                nonce=header+b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                packet=bytearray(header)+voice_client._secret_box.encrypt(bytes(data),nonce).ciphertext
                
                
                try:
                    voice_client.socket.sendto(packet,(voice_client._endpoint_ip,voice_client._voice_port))
                except BlockingIOError:
                    pass

                timestamp=voice_client._timestamp+SAMPLES_PER_FRAME
                if timestamp>4294967295:
                    timestamp=0
                voice_client._timestamp=timestamp
                
                delay=PLAYER_DELAY+((start+PLAYER_DELAY*loops)-perf_counter())
                if delay<.0:
                    continue
                blocking_sleep(delay)
        except BaseException as err:
            extracted=[
                'Exception occured at \n',
                repr(self),
                '\n',
                    ]
            render_exc_to_list(err,extend=extracted)
            sys.stderr.write(''.join(extracted))
            
            voice_client.player=None
            self.done=True
            self.resumed.set()
            self.source.cleanup()
