__all__ = ('AudioSource', 'DownloadError', 'LocalAudio', 'YTAudio')


import os, sys, subprocess, shlex
from pathlib import Path

from ...backend.utils import alchemy_incendiary
from ...backend.futures import Task, CancelledError

from ..core import KOKORO
from .opus import FRAME_LENGTH, FRAME_SIZE

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

class AudioSource:
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
        Parameters and the stdin used to open the postprocess when postprocess happens.
    _stdout : `_io.BufferedReader`
        Stdout of `.process`.
    path : `None` or `str`
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
            Extra parameters passed before the `-i` flag.
        options : `str` or (`iterable` of `str`)
            Extra parameters passed after the `-i` flag.
        
        Returns
        -------
        executable : `str`
            The executable's name.
        args : `list` of `str`
            Subprocess parameters.
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
            Extra parameters passed before the `-i` flag.
        options : `str` or (`iterable` of `str`), Optional
            Extra parameters passed after the `-i` flag.
        
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
            Parameters and the stdin used to open the postprocess when postprocess happens.
        _stdout : `_io.BufferedReader`
            Stdout of `.process`.
        path : `None` or `str`
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
                Subprocess parameters.
            
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
            self.title = data.get('title', None)
            self.url = data.get('url', None)
            
            return self
