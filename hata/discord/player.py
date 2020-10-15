# -*- coding: utf-8 -*-
__all__ = ('DownloadError', 'LocalAudio', 'YTAudio')

import os, sys, subprocess, shlex
from threading import Event, Thread, current_thread
from time import perf_counter, sleep as blocking_sleep
from audioop import mul as audio_mul
from pathlib import Path

from ..backend.dereaddons_local import alchemy_incendiary
from ..backend.futures import render_exc_to_list
from ..backend.eventloop import EventThread

from .client_core import KOKORO
from .opus import FRAME_LENGTH, FRAME_SIZE, SAMPLES_PER_FRAME

PLAYER_DELAY = FRAME_LENGTH/1000.0

del FRAME_LENGTH

DEFAULT_EXECUTABLE = 'ffmpeg'

if os.name == 'nt':
    SUBPROCESS_STARTUP_INFO = subprocess.STARTUPINFO()
    SUBPROCESS_STARTUP_INFO.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    SUBPROCESS_STARTUP_INFO.wShowWindow = subprocess.SW_HIDE
else:
    SUBPROCESS_STARTUP_INFO = None

STREAM_OPTIONS = (
    '-reconnect', '1',
    # '-reconnect_streamed', '1',
    # '-reconnect_delay_max', '3',
        )

class AudioSource(object):
    """
    Base class for audio sources.
    
    Class Attributes
    ----------------
    NEEDS_ENCODE : `bool` = `True`
        Whether the source is not opus encoded.
    REPEATABLE : `bool` = `False`
        Whether the source can be repeated after it is exhausted once.
    """
    __slots__ = ()
    
    NEEDS_ENCODE = True
    REPEATABLE = False
    
    def read(self):
        """
        Reads 20ms audio data.
        
        Indicates end of stream by returning `None`.
        
        > Subclasses should implement it.
        
        Returns
        -------
        audio_data : `bytes` or `None`
        """
        return None
    
    def cleanup(self):
        """
        Cleans up the allocated resources by the audio source.
        
        > Subclasses should overwrite it.
        """
        pass
    
    def __del__(self):
        """Cleans up the audio source if ``.cleanup`` was not called for any reason."""
        self.cleanup()
    
    @property
    def title(self):
        """
        Spaceholder method for title attribute.
        
        Always returns an empty string.
        
        Returns
        -------
        title : `str`
        """
        return ''
    
    @property
    def path(self):
        """
        Spaceholder method for path attribute.
        
        Always returns `None`.
        
        Returns
        -------
        path : `None`
        """
        return None
    
    def postprocess(self):
        """
        Called before the audio of the source would be played.
        
        This method can be implemented as blocking.
        """
        pass

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
    REPEATABLE : `bool` = `False`
        Whether the source can be repeated after it is exhausted once.
    """
    __slots__ = ('stream',)
    
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
        self = object.__new__(cls)
        self.stream = stream
        return self

    def read(self):
        """
        Reads 20ms audio data.
        
        Indicates end of stream by returning `None`
        
        Returns
        -------
        audio_data : `bytes` or `None`
        """
        result = self.stream.read(FRAME_SIZE)
        if (result is not None) and (len(result) != FRAME_SIZE):
            result = None
        return result

class LocalAudio(AudioSource):
    """
    Represents a ffmpeg pcm audio.
    
    You must have the ffmpeg or avconv executable in your path environment variable in order for this to work.
    
    Attributes
    ----------
    _process_args : `tuple` ((`list` of `str`),  (`None` or `file-like`))
        Arguments and the stdin used to open the postprocess when postprocess happens.
    _stdout : `_io.BufferedReader`
        Stdout of `.process`.
    path : `str` or `None`
        The audio source's path if applicable. Defaults to `None`.
    process : `subprocess.Popen`
        The ffmpeg or the avconv subprocess.
    title : `str`
        The audio source's title if applicable. Defaults to empty string.
    
    Class Attributes
    ----------------
    NEEDS_ENCODE : `bool` = `True`
        Whether the source is not opus encoded.
    REPEATABLE : `bool` = `True`
        Whether the source can be repeated after it is exhausted once.
    """
    REPEATABLE = True
    
    @staticmethod
    def _create_process_preprocess(source, executable, pipe, before_options, options):
        """
        Creates a a subprocess instance to the given source.
        
        Parameters
        ----------
        source : `str`, `Path` or `file-like`
            The source audio file's path or `file-like` if `pipe` is `True`.
        executable : `str`
            The executable's name to use. Defaults to `'ffmpeg'`.
        pipe : `bool`
            Whether the source is passed to stdin.
        before_options : `str` or (`iterable` of `str`)
            Extra arguments passed before the `-i` flag.
        options : `str` or (`iterable` of `str`)
            Extra arguments passed after the `-i` flag.
        
        Returns
        -------
        args : `list` of `str`
            Subprocess arguments.
        stdin : `None or `file-like`
            Input for the postprocess.
        
        Raises
        ------
        TypeError
            - If `pipe` was given as `True` meanwhile `source` was not given as a `file-like` supporting `.fileno()`
                method.
            - If `pipe` was given as `False`, meanwhile `source` was not given as `str` or `Path` instance.
        ValueError
            - Executable as not found.
            - Popen failed.
        """
        if pipe:
            try:
                fileno_function = source.__class__.fileno
            except AttributeError as err:
                raise TypeError('The given `source` not supports `.fileno()` method') from err
            try:
                fileno_function(source)
            except TypeError as err:
                raise TypeError('The given `source` not supports `.fileno()` method') from err
        else:
            source_type = source.__class__
            if source_type is str:
                pass
            elif issubclass(source_type, Path):
                source = str(source)
            elif issubclass(source_type, str):
                source = str(source)
            else:
                raise TypeError('The given `source` should be given as `str` or as `Path` instance, got '
                    f'{source_type}.')
        
        args = [executable]
        
        if (before_options is not None):
            if isinstance(before_options, str):
                before_options = shlex.split(before_options)
            
            args.extend(before_options)
        
        args.append('-i')
        args.append('-' if pipe else source)
        args.append('-f')
        args.append('s16le')
        args.append('-ar')
        args.append('48000')
        args.append('-ac')
        args.append('2')
        args.append('-loglevel')
        args.append('panic')
        
        if (options is not None):
            if isinstance(options, str):
                options = shlex.split(options)
            
            args.extend(options)
        
        args.append('pipe:1')
        
        return args, (source if pipe else None)
    
    @staticmethod
    def _create_process(args, stdin):
        """
        Creates the subprocess of the audio source. This method should never run on an ``EventThread``.
        
        Paremeters
        ----------
        args : `list` of `str`
            Subprocess arguments.
        stdin : `None or `file-like`
            Input for the postprocess.
        
        Returns
        -------
        process : `subprocess.Popen`
        
        Raises
        ------
        ValueError
            - Executable as not found.
            - Popen failed.
        """
        try:
            process = subprocess.Popen(args, stdin=stdin, stdout=subprocess.PIPE,
                startupinfo=SUBPROCESS_STARTUP_INFO)
        except FileNotFoundError:
            raise ValueError(f'{args[0]} was not found.') from None
        except subprocess.SubprocessError as err:
            raise ValueError(f'Popen failed: {err.__class__.__name__}: {err}') from err
        
        return process
    
    def postprocess(self):
        """
        Creates the process of the audio player.
        
        Raises
        ------
        ValueError
            - Executable as not found.
            - Popen failed.
        """
        process = self.process
        if process is None:
            process = self._create_process(*self._process_args)
            self.process = process
            self._stdout = process.stdout
    
    __slots__ = ('_process_args', '_stdout', 'path', 'process', 'title', )
    
    #use __new__, so __del__ wont run
    async def __new__(cls, source, executable=DEFAULT_EXECUTABLE, pipe=False, before_options=None,
            options=None, title=None):
        """
        Creates a new ``LocalAudio`` instance.
        
        Parameters
        ----------
        source : `str` or `file-like`
            The source audio file's path or `file-like` if `pipe` is `True`.
        executable : `str`, Optional
            The executable's name to use. Defaults to `'ffmpeg'`.
        pipe : `bool`, Optional
            Whether the source is passed to stdin. Defaults to `False`
        before_options : `str` or (`iterable` of `str`), Optional
            Extra arguments passed before the `-i` flag.
        options : `str` or (`iterable` of `str`), Optional
            Extra arguments passed after the `-i` flag.
        
        Returns
        -------
        self : ``LocalAudio``
        
        Raises
        ------
        TypeError
            - If `pipe` was given as `True` meanwhile `source` was not given as a `file-like` supporting `.fileno()`
                method.
            - If `pipe` was given as `False`, meanwhile `source` was not given as `str` or `Path` instance.
        """
        args = cls._create_process_preprocess(source, executable, pipe, before_options, options)
        
        self = object.__new__(cls)
        self._process_args = args
        self.process = None
        self._stdout = None
        
        if pipe:
            path = None
            if title is None:
                title = getattr(source, 'name', None)
                if title is None:
                    title = ''
                else:
                    title = os.path.splitext(title)[0].replace('_', ' ')
        else:
            path = source
            if title is None:
                title = os.path.splitext(os.path.basename(path))[0].replace('_', ' ')
        
        self.path = path
        self.title = title
        
        return self
    
    def read(self):
        """
        Reads 20ms audio data.
        
        Indicates end of stream by returning zero `None`.
        
        Returns
        -------
        audio_data : `bytes` or `None`
        """
        stdout = self._stdout
        if stdout is None:
            result = None
        else:
            try:
                result = stdout.read(FRAME_SIZE)
            except ValueError:
                result = None
            else:
                if len(result) != FRAME_SIZE:
                    result = None
        
        return result
    
    def cleanup(self):
        """
        Closes ``.process`.`
        """
        process = self.process
        if process is None:
            return
        
        process.kill()
        if process.poll() is None:
            process.communicate()
        
        self._stdout = None
        self.process = None
 
try:
    import youtube_dl
except ImportError:
    youtube_dl = None
    DownloadError = None
    YTAudio = None
else:
    from youtube_dl.utils import DownloadError
    youtube_dl.utils.bug_reports_message = lambda: ''
    
    YTdl = youtube_dl.YoutubeDL({
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
    
    class YTAudio(LocalAudio):
        """
        Represents an audio sourced downloaded from youtube.
        
        You must have the ffmpeg or avconv executable in your path environment variable in order for this to work.
        
        Attributes
        ----------
        _process_args : `tuple` ((`list` of `str`),  (`None` or `file-like`))
            Arguments and the stdin used to open the postprocess when postprocess happens.
        _stdout : `_io.BufferedReader`
            Stdout of `.process`.
        path : `str` or `None`
            The audio source's path if applicable. Defaults to `None`.
        process : `subprocess.Popen`
            The ffmpeg or the avconv subprocess.
        title : `str`
            The audio source's title if applicable. Defaults to empty string.
        url : `str`
            The source url of the downloaded audio.
        Class Attributes
        ----------------
        NEEDS_ENCODE : `bool` = `True`
            Whether the source is not opus encoded.
        REPEATABLE : `bool` = `True`
            Whether the source can be repeated after it is exhausted once.
        """
        
        __slots__ = ('url', )
        
        @staticmethod
        def _preprocess(cls, url, stream):
            """
            Downloads the audio source by the given url or title.
            
            This function runs inside of an executor thread.
            
            Parameters
            ----------
            url : `str`
            
            Returns
            -------
            path : `str`
                The title of the dowloaded audio.
            data : `dict` of (`str`, `Any`)
                All extracted data by YTDL.
            args : `list` of `str`
                Subprocess arguments.
            
            Raises
            ------
            DownloadError
                Downloading the audio source failed.
            """
            data = YTdl.extract_info(url, download=(not stream))
            
            if 'entries' in data: #playlist
                data = data['entries'][0]
            
            if stream:
                path = data['url']
                before_options = STREAM_OPTIONS
            else:
                path = YTdl.prepare_filename(data)
                before_options = None
            
            args = cls._create_process_preprocess(path, DEFAULT_EXECUTABLE, False, before_options, ('-vn',))
            
            return path, data, args
        
        async def __new__(cls, url, stream=True):
            """
            Creates a new ``YTAudio`` instance.
            
            Parameters
            ----------
            url : `str`
                The url or the title of the video.
            stream : `bool`
                Whether the audio should be streamed.
            
            Returns
            -------
            self : ``YTAudio``
            
            Raises
            ------
            DownloadError
                Downloading the audio source failed.
            PermissionError
                The given file started to be played at the same time by an other player as well.
            TypeError
                - If `pipe` was given as `True` meanwhile `source` was not given as a `file-like` supporting `.fileno()`
                    method.
                - If `pipe` was given as `False`, meanwhile `source` was not given as `str` or `Path` instance.
            """
            loop = current_thread()
            if isinstance(loop, EventThread):
                path, data, args = await loop.run_in_executor(alchemy_incendiary(cls._preprocess,(cls, url, stream)))
            else:
                path, data, args = cls._preprocess(cls, url, stream)
            
            # Create self only at the end, so the `__del__` wont pick it up
            self = object.__new__(cls)
            self._process_args = args
            self.process = None
            self._stdout = None
            self.path = path
            self.title = data.get('title')
            self.url = data.get('url')
            
            return self

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
    __slots__ = ('client', 'done', 'resumed', 'source')
    
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
        self.done = False
        
        resumed = Event()
        resumed.set()    #we are not paused
        self.resumed = resumed
        
        Thread.start(self)
    
    @staticmethod
    async def _run_call_after(voice_client, last_source):
        """
        Called when playing an ``AudioSource`` of the audio player finished.
        
        Parameters
        ----------
        voice_client : ``VoiceClient``
            The parent voice client of the ``AudioPlayer``.
        last_source : ``AudioSource``
            The play played audio.
        
        Returns
        -------
        should_stop : `bool`
            Whether the player should stop.
        """
        lock = voice_client.lock
        if lock.locked():
            await lock
        else:
            async with lock:
                await voice_client.call_after(voice_client, last_source)
    
    def run(self):
        voice_client = self.client
        start = perf_counter()
        loops = 0
        
        source = None
        
        try:
            while True:
                if not self.resumed.is_set():
                    self.resumed.wait()
                    start = perf_counter()
                    loops = 0
                    continue
                
                #are we disconnected from voice?
                if not voice_client.connected.is_set():
                    voice_client.connected.wait()
                    start = perf_counter()
                    loops = 0
                    continue
                
                loops +=1
                
                new_source = self.source
                if (new_source is None):
                    if (voice_client.player is not self):
                        break
                    
                    if (source is not None):
                        source.cleanup()
                        source = None
                    
                    self.resumed.clear()
                    continue
                
                if (new_source is not source):
                    if (source is not None):
                        source.cleanup()
                        source = None
                    
                    source = new_source
                    new_source = None
                    source.postprocess()
                
                data = source.read()
                
                if self.done or (data is None):
                    self.resumed.clear()
                    source.cleanup()
                    self.source = None
                    
                    if (voice_client.player is not self):
                        break
                    
                    KOKORO.create_task_threadsafe(self._run_call_after(voice_client, source)).syncwrap().wait()
                    
                    source = self.source
                    if (source is None):
                        self.done = True
                        self.resumed.set()
                        break
                    
                    source.postprocess()
                    continue
                
                sequence = voice_client._sequence
                if sequence == 65535:
                    sequence = 0
                else:
                    sequence +=1
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
                
                nonce = header+b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                packet = bytearray(header)+voice_client._secret_box.encrypt(bytes(data), nonce).ciphertext
                
                try:
                    voice_client.socket.sendto(packet, (voice_client._endpoint_ip, voice_client._audio_port))
                except BlockingIOError:
                    pass
                
                timestamp = voice_client._timestamp+SAMPLES_PER_FRAME
                if timestamp > 4294967295:
                    timestamp = 0
                voice_client._timestamp = timestamp
                
                delay = PLAYER_DELAY+((start+PLAYER_DELAY*loops)-perf_counter())
                if delay < 0.0:
                    continue
                blocking_sleep(delay)
        except BaseException as err:
            voice_client.player = None
            self.done = True
            self.resumed.set()
            if (source is not None):
                source.cleanup()
                source = None
            
            self.source = None
            
            extracted = [
                'Exception occured at \n',
                repr(self),
                '\n',
                    ]
            render_exc_to_list(err, extend=extracted)
            sys.stderr.write(''.join(extracted))
            
        else:
            voice_client.player = None
