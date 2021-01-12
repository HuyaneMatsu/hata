# -*- coding: utf-8 -*-
__all__ = ('DownloadError', 'LocalAudio', 'YTAudio')

import os, sys, subprocess, shlex
from time import perf_counter
from audioop import mul as audio_mul
from pathlib import Path

from ..backend.utils import alchemy_incendiary
from ..backend.futures import Task, Event, sleep, CancelledError

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
    
    async def read(self):
        """
        Reads 20ms audio data.
        
        Indicates end of stream by returning `None`.
        
        Subclasses should implement it.
        
        This method is a coroutine.
        
        Returns
        -------
        audio_data : `bytes` or `None`
        """
        return None
    
    async def cleanup(self):
        """
        Cleans up the allocated resources by the audio source.
        
        Subclasses should overwrite it.
        
        This method is a coroutine.
        """
        pass
    
    def __del__(self):
        """Cleans up the audio source if ``.cleanup`` was not called for any reason."""
        Task(self.cleanup(), KOKORO)
    
    @property
    def title(self):
        """
        Placeholder method for title attribute.
        
        Always returns an empty string.
        
        Returns
        -------
        title : `str`
        """
        return ''
    
    @property
    def path(self):
        """
        Placeholder method for path attribute.
        
        Always returns `None`.
        
        Returns
        -------
        path : `None`
        """
        return None
    
    async def postprocess(self):
        """
        Called before the audio of the source would be played.
        
        This method is a coroutine.
        """
        pass


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
        Creates a subprocess's args to open.
        
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
        executable : `str`
            The executable's name.
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
        
        args = []
        
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
        
        return executable, args, (source if pipe else None)
    
    async def postprocess(self):
        """
        Creates the process of the audio player.
        
        This method is a coroutine.
        
        Raises
        ------
        ValueError
            - Executable as not found.
            - Popen failed.
        """
        process = self.process
        if process is None:
            executable, args, stdin = self._process_args
            try:
                process = await KOKORO.subprocess_exec(executable, *args, stdin=stdin, stdout=subprocess.PIPE,
                    startup_info=SUBPROCESS_STARTUP_INFO)
            except FileNotFoundError:
                raise ValueError(f'{executable!r} was not found.') from None
            except subprocess.SubprocessError as err:
                raise ValueError(f'Opening subprocess failed: {err.__class__.__name__}: {err}') from err
            
            self.process = process
            self._stdout = process.stdout
    
    __slots__ = ('_process_args', '_stdout', 'path', 'process', 'title', )
    
    # use __new__, so __del__ wont run
    async def __new__(cls, source, executable=DEFAULT_EXECUTABLE, pipe=False, before_options=None,
            options=None, title=None):
        """
        Creates a new ``LocalAudio`` instance.
        
        This method is a coroutine.
        
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
    
    async def read(self):
        """
        Reads 20ms audio data.
        
        Indicates end of stream by returning zero `None`.
        
        This method is a coroutine.
        
        Returns
        -------
        audio_data : `bytes` or `None`
        """
        stdout = self._stdout
        if stdout is None:
            result = None
        else:
            try:
                result = await stdout.read(FRAME_SIZE)
            except (CancelledError, ConnectionError):
                result = None
            else:
                if len(result) != FRAME_SIZE:
                    result = None
        
        return result
    
    async def cleanup(self):
        """
        Closes ``.process``.
        
        This method is a coroutine.
        """
        process = self.process
        if process is None:
            return
        
        await process.kill()
        if process.poll() is None:
            await process.communicate()
        
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
                The title of the downloaded audio.
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
            
            This method is a coroutine.
            
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
            path, data, args = await KOKORO.run_in_executor(alchemy_incendiary(cls._preprocess,(cls, url, stream)))
            
            # Create self only at the end, so the `__del__` wont pick it up
            self = object.__new__(cls)
            self._process_args = args
            self.process = None
            self._stdout = None
            self.path = path
            self.title = data.get('title')
            self.url = data.get('url')
            
            return self


class AudioPlayer(object):
    """
    Sends voice data through the voice client's socket.
    
    Attributes
    ----------
    client : ``VoiceClient``
        The voice client of audio player.
    done : `bool`
        Whether the audio player finished playing it's source.
    resumed_waiter : `threading.Event`
        Indicates whether the the audio player is not paused.
    source : ``AudioSource`` instance
        The audio source what the player reads each 20 ms.
    should_update : `bool`
        Whether the voice client should update itself.
    task : `None` or ``Task``
        Audio reader task. Set as `None` if the reader is stopped.
    """
    __slots__ = ('client', 'done', 'resumed_waiter', 'should_update', 'source', 'task')
    
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
        self.source = source
        self.client = voice_client
        
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
        voice_client = self.client
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
                
                nonce = header+b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                packet = bytearray(header)+voice_client._secret_box.encrypt(bytes(data), nonce).ciphertext
                
                voice_client.send_packet(packet)
                
                timestamp = voice_client._timestamp+SAMPLES_PER_FRAME
                if timestamp > 4294967295:
                    timestamp = 0
                voice_client._timestamp = timestamp
                
                delay = PLAYER_DELAY+((start+PLAYER_DELAY*loops)-perf_counter())
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
            
            if isinstance(err, CancelledError):
                return
            
            await KOKORO.render_exc_async(err, before=[
                'Exception occurred at \n',
                repr(self),
                '\n',
                    ])
            
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
        actual_source : `None` or ``AudioSource`` instance
            The actual audio source of the player.
        
        Returns
        -------
        new_source : `None` or `AudioSource`` instance
            New source of the player to play.
            
            Can be same as the `actual_source`.
        """
        resumed_waiter = self.resumed_waiter
        if not resumed_waiter.is_set():
            await resumed_waiter
        
        self.should_update = False
        new_source = self.source
        if (new_source is None):
            if (self.client.player is not self):
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
        source : `None` or ``AudioSource`` instance
            The new source of the player.
        """
        self.source = source
        self.should_update = True
        
        resumed_waiter = self.resumed_waiter
        if not resumed_waiter.is_set():
            resumed_waiter.set()

