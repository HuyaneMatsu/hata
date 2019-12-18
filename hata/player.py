# -*- coding: utf-8 -*-
__all__ = ('LocalAudio', )

import os, sys
import subprocess
import audioop
import shlex

from threading import Event, Thread
from time import perf_counter, sleep as blocking_sleep

from .dereaddons_local import alchemy_incendiary
from .opus import FRAME_LENGTH, FRAME_SIZE, SAMPLES_PER_FRAME
from .futures import render_exc_to_list

PLAYER_DELAY=FRAME_LENGTH/1000.0

del FRAME_LENGTH


if os.name=='nt':
    SUBPROCESS_STARTUP_INFO=subprocess.STARTUPINFO()
    SUBPROCESS_STARTUP_INFO.dwFlags|=subprocess.STARTF_USESHOWWINDOW
    SUBPROCESS_STARTUP_INFO.wShowWindow=subprocess.SW_HIDE
else:
    SUBPROCESS_STARTUP_INFO=None
            
class AudioSource(object):
    __slots__=()

    NEEDS_ENCODE=True

    def read(self):
        raise NotImplementedError

    def cleanup(self):
        pass

    def __del__(self):
        self.cleanup()

    def parse_title(self):
        return 'Unknown'
    
class PCMaudio(AudioSource):
    __slots__=('stream',)
    #Represents raw 16-bit 48KHz stereo PCM audio source.

    def __new__(cls,stream):
        self=object.__new__(cls)
        self.stream=stream
        return self

    def read(self):
        result=self.stream.read(FRAME_SIZE)
        if len(result)!=FRAME_SIZE:
            return b''
        return result

class FFmpegPCMaudio(AudioSource):
    #You must have the ffmpeg or avconv executable in your path environment
    #variable in order for this to work.
    __slots__=('process', 'source', 'stdout',)

    #use __new__, so __del__ wont run
    def __new__(cls,source,executable='ffmpeg',pipe=False,stderr=None,before_options=[],options=[]):

        if isinstance(before_options,str):
            before_options=shlex.split(before_options)

        if isinstance(options,str):
            options=shlex.split(options)

        args = [
            'ffmpeg',
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
            'warning',
            *options,
            'pipe:1',
                ]

        if pipe:
            stdin=source
        else:
            stdin=None
            
        try:
            process=subprocess.Popen(args,stdin=stdin,stdout=subprocess.PIPE,stderr=stderr,startupinfo=SUBPROCESS_STARTUP_INFO)
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
        result=self.stdout.read(FRAME_SIZE)
        if len(result)!=FRAME_SIZE:
            return b''
        return result

    def cleanup(self):
        process=self.process
        if process is None:
            return

        process.kill()
        if process.poll() is None:
            process.communicate()

        self.process=None

    def parse_title(self):
        _,name=os.path.split(self.source)
        index=name.rfind('.')
        if index<0:
            return name
        return name[:index]
    
class PCM_volume_transformer(AudioSource):
    downloaded=False
    __slots__=('original', 'title', 'volume',)
    
    def __new__(cls,original):
        if not isinstance(original,AudioSource):
            raise TypeError(f'expected AudioSource not {original.__class__.__name__}.')

        if not original.NEEDS_ENCODE:
            raise ValueError('AudioSource must not be Opus encoded.')


        self=object.__new__(cls)
        
        self.original   = original
        self.volume     = 1.0 #max volume is 2.0
        self.title      = original.parse_title()
        
        return self

    def cleanup(self):
        original=self.original
        if original is None:
            return
        original.cleanup()

    def read(self):
        return audioop.mul(self.original.read(),2,self.volume)
        
class LocalAudio(object):
    __slots__=()
    
    @staticmethod
    def _open(path):
        return FFmpegPCMaudio(path)

    async def __new__(cls,loop,path):
        source = await loop.run_in_executor(alchemy_incendiary(cls._open,(path,)))
        return PCM_volume_transformer(source)

try:
    import youtube_dl
except ImportError:
    youtube_dl=None
else:
    __all__ = (*__all__, 'YTaudio', 'DownloadError', )
    
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
        
    class YTaudio(PCM_volume_transformer):
        downloaded=True
        __slots__=('delete', 'original', 'title', 'url', 'volume',)

        @staticmethod
        def _download(url):
            data = YTdl.extract_info(url,download=True)
            
            if 'entries' in data: #playlist
                data=data['entries'][0]
                
            #if stream:filename=data['url']
            filename    = YTdl.prepare_filename(data)
            original    = FFmpegPCMaudio(filename,options='-vn')

            return original,filename,data
        
        async def __new__(cls,loop,url,executor_id=0,delete_after=True):
            func=alchemy_incendiary(cls._download,(url,))
            if executor_id:
                future=loop.run_in_id_executor(func,executor_id)
            else:
                future=loop.run_in_executor(func)

            original,filename,data = await future
            
            #create self only at the end, so the `__del__` wont pick it up
            self=object.__new__(cls)
            self.original   = original
            self.title      = data.get('title')
            self.url        = data.get('url')
            self.volume     = 1.0
            if delete_after:
                self.delete = filename
            else:
                self.delete = None

            return self

        def cleanup(self):
            self.original.cleanup()
            delete=self.delete
            if delete is None:
                return
            try:
                os.remove(delete)
            except (PermissionError,FileNotFoundError):
                pass
            self.delete=None
    
        
class AudioPlayer(Thread):
    __slots__=('client', 'connected', 'done', 'resumed', 'soure')
    
    def __init__(self,voice_client,source):
        Thread.__init__(self,daemon=True)
        self.source         = source
        self.client         = voice_client

        self.done           = False
        self.resumed        = Event()
        self.resumed.set()    #we are not paused

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

                if self.done or (not data):
                    self.resumed.clear()
                    self.source.cleanup()
                    self.source=None
                    if voice_client.lock.locked():
                        voice_client.lock.acquire()
                    else:
                        with voice_client.lock:
                            stop=voice_client.loop.create_task_threadsafe(voice_client.call_after(voice_client,lock=False)).syncwrap().wait()
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
                self.__repr__(),
                '\n',
                    ]
            render_exc_to_list(err,extend=extracted)
            sys.stderr.write(''.join(extracted))
            
            voice_client.player=None
            self.done=True
            self.resumed.set()
            self.source.cleanup()
