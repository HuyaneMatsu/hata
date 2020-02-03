# -*- coding: utf-8 -*-
__all__ = ('ExtensionError', 'ExtensionLoader', )

import sys
from io import StringIO
from weakref import ref as WeakReferer, WeakValueDictionary
from importlib.util import find_spec, module_from_spec
from importlib import reload as reload_module
from threading import current_thread

from .eventloop import EventThread
from .dereaddons_local import alchemy_incendiary, _spaceholder
from .futures import iscoroutinefunction as is_coro, Task

from .client_core import KOKORO

EXTENSIONS = WeakValueDictionary()

EXTENSION_STATE_UNDEFINED   = 0
EXTENSION_STATE_LOADED      = 1
EXTENSION_STATE_UNLOADED    = 2

class ExtensionError(Exception):
    """Loading an extension failed."""
    
    # message can be `str` or `list of str`-s
    def __init__(self, message):
        self._message=message
        
    @property
    def message(self):
        message=self._message
        if type(message) is str:
            return message
        
        return '\n\n'.join(message)
    
    @property
    def messages(self):
        message=self._message
        if type(message) is str:
           return [message]
        
        return message
    
    def __len__(self):
        message=self._message
        if type(message) is str:
            return 1
        
        return len(message)
        
    def __repr__(self):
        return f'{self.__class__.__name__} ({len(self)}):\n{self.message}\n'
    
    __str__=__repr__
    
class Extension(object):
    __slots__=('__weakref__', 'spec', 'state', 'lib', 'entry_point', 'exit_point', )
    
    def __new__(cls, name, entry_point, exit_point):
        try:
            return EXTENSIONS[name]
        except KeyError:
            pass
        
        spec=find_spec(name)
        if spec is None:
            raise ModuleNotFoundError(name)
        
        self=object.__new__(cls)
        self.state      = EXTENSION_STATE_UNDEFINED
        self.spec       = spec
        self.lib        = None
        self.entry_point= entry_point
        self.exit_point = exit_point
        EXTENSIONS[name]= self
        
        return self
        
    def __hash__(self):
        return hash(self.spec.origin)
    
    def load(self):
        state=self.state
        if state==EXTENSION_STATE_UNDEFINED:
            
            spec = self.spec
            try:
                # the lib is imported, return it
                lib = sys.modules[spec.name]
            except KeyError:
                # lib is not imported yet, nice
                lib = module_from_spec(spec)
                spec.loader.exec_module(lib)
                sys.modules[spec.name] = lib
            
            self.lib = lib
            
            self.state=EXTENSION_STATE_LOADED
            return lib
        
        if state==EXTENSION_STATE_LOADED:
            # return None -> already loaded
            return None
        
        if state==EXTENSION_STATE_UNLOADED:
            # reload
            lib = self.lib
            reload_module(lib)
            
            self.state=EXTENSION_STATE_LOADED
            return lib
        
        # no more cases
    
    def unload(self):
        state=self.state
        if state==EXTENSION_STATE_UNDEFINED:
            return None
        
        if state==EXTENSION_STATE_LOADED:
            self.state=EXTENSION_STATE_UNLOADED
            return self.lib
        
        if state==EXTENSION_STATE_UNLOADED:
            return None
        
        # no more cases
    
    @property
    def name(self):
        return self.spec.name
    
    def unlink(self):
        state=self.state
        if state==EXTENSION_STATE_UNDEFINED:
            return
        
        if state==EXTENSION_STATE_LOADED:
            self.state=EXTENSION_STATE_UNLOADED
            del sys.modules[self.spec.name]
            return
        
        if state==EXTENSION_STATE_UNLOADED:
            del sys.modules[self.spec.name]
            return
        
        # no more cases
        
        
class ExtensionLoader(object):
    __slots__=('client', 'extensions', )
    
    def __new__(cls, client):
        self=getattr(client,'extension_loader',None)
        if self is not None:
            if type(self) is cls:
                return self
            raise RuntimeError(f'The {client.full_name} has an extension loader already {self!r}, of a different class.')
            
        self=object.__new__(cls)
        # weakrefer the client, so it can be deleted runtime freely
        self.client=WeakReferer(client)
        self.extensions={}
        client.extension_loader=self
        
        return self
    
    def add(self, name, entry_point=None, exit_point=None):
        if (entry_point is not None) and (not isinstance(entry_point,str)) and (not callable(entry_point)):
            raise TypeError(f'`{self.__class__.__name__}.add` expected None, str or a callable as `entry_point`, got `{entry_point!r}`')

        if (exit_point is not None) and (not isinstance(exit_point,str)) and (not callable(exit_point)):
            raise TypeError(f'`{self.__class__.__name__}.add` expected None, str or a callable as `exit_point`, got `{exit_point!r}`')
        
        if isinstance(name,str):
            # case of 1 element
            self.extensions[name] = Extension(name,entry_point,exit_point)
            return
        
        if hasattr(type(name),'__iter__'):
            values=[]
            for value in name:
                if isinstance(value,str):
                    values.append(value)
                    continue
                
                raise TypeError(
                    f'`{self.__class__.__name__}.add` expected `str` or `iterable of str`-s as `name`, '
                    f'{name!r} is not `str`, but `iterable`, but it has at least 1 non `str` element: {value!r}')
            
            for name in values:
                self.extensions[name] = Extension(name,entry_point,exit_point)
            
            return
        
        #no more good case -> raise
        raise TypeError(f'`{self.__class__.__name__}.add` expected `str` or `iterable of str` as `name`, got `{name!r}`')
    
    def remove(self, name):
        if isinstance(name,str):
            # case of 1 element
            try:
                extension=self.extensions[name]
            except KeyError:
                return
            
            if extension.state==EXTENSION_STATE_LOADED:
                raise RuntimeError(f'Extension `{name}` can not be removed, meanwhile it is loaded.')
            
            extension.unlink()
            
            return
        
        if hasattr(type(name),'__iter__'):
            values=[]
            for value in name:
                if isinstance(value,str):
                    values.append(value)
                    continue
                
                raise TypeError(
                    f'`{self.__class__.__name__}.add` expected `str` or `iterable of str`-s as `name`, '
                    f'{name!r} is not `str`, but `iterable`, but it has at least 1 non `str` element: {value!r}')
            
            collected=[]
            extensions=self.extensions
            for name in values:
                try:
                    extension=extensions[name]
                except KeyError:
                    continue
                
                if extension.state==EXTENSION_STATE_LOADED:
                    raise RuntimeError(f'Extension `{name}` can not be removed, meanwhile it is loaded.')
                
                collected.append(extension)
                
            for extension in collected:
                extension.unlink()
            
            return
        
        #no more good case -> raise
        raise TypeError(f'`{self.__class__.__name__}.add` expected `str` or `iterable of str` as `name`, got `{name!r}`')
    
    def load(self, name):
        task=Task(self._load(name),KOKORO)
        if current_thread() is not KOKORO:
            KOKORO.wakeup()
            
        return task
    
    async def _load(self, name):
        client=self.client()
        if client is None:
            raise RuntimeError('Loading extension of a deleted client.')

        try:
            extension=self.extensions[name]
        except KeyError as err:
            raise ExtensionError(f'No extension was added with name: `{name}`.') from err
        
        await self._load_extension(client,extension)
        
    def unload(self, name):
        task=Task(self._unload(name),KOKORO)
        if current_thread() is not KOKORO:
            KOKORO.wakeup()
        
        return task
       
    async def _unload(self, name):
        client=self.client()
        if client is None:
            raise RuntimeError('Unloading extension of a deleted client.')
        
        try:
            extension=self.extensions[name]
        except KeyError as err:
            raise ExtensionError(f'No extension was added with name: `{name}`.') from err
        
        await self._unload_extension(client,extension)
        
    def reload(self, name):
        task=Task(self._reload(name),KOKORO)
        if current_thread() is not KOKORO:
            KOKORO.wakeup()
        
        return task
        
    async def _reload(self, name):
        client=self.client()
        if client is None:
            raise RuntimeError('Reloading extension of a deleted client.')
        
        try:
            extension=self.extensions[name]
        except KeyError as err:
            raise ExtensionError(f'No extension was added with name: `{name}`.') from err
        
        await self._unload_extension(client, extension)
        await self._load_extension(client, extension)
    
    def load_all(self):
        task=Task(self._load_all(),KOKORO)
        if current_thread() is not KOKORO:
            KOKORO.wakeup()
        
        return task
        
    async def _load_all(self):
        client=self.client()
        if client is None:
            raise RuntimeError('Loading all extension of a deleted client.')
        
        error_messages=[]
        
        for extension in self.extensions.values():
            try:
                await self._load_extension(client,extension)
            except ExtensionError as err:
                error_messages.append(err.message)
            
        if error_messages:
            raise ExtensionError(error_messages)
        
    def unload_all(self):
        task=Task(self._unload_all(),KOKORO)
        if current_thread() is not KOKORO:
            KOKORO.wakeup()
        
        return task
    
    async def _unload_all(self):
        client=self.client()
        if client is None:
            raise RuntimeError('Unloading all extension of a deleted client.')
        
        error_messages=[]
        
        for extension in self.extensions.values():
            try:
                await self._unload_extension(client,extension)
            except ExtensionError as err:
                error_messages.append(err.message)
            
        if error_messages:
            raise ExtensionError(error_messages)
    
    def reload_all(self):
        task=Task(self._reload_all(),KOKORO)
        if current_thread() is not KOKORO:
            KOKORO.wakeup()
        
        return task

    async def _reload_all(self):
        client=self.client()
        if client is None:
            raise RuntimeError('Reloading all extension of a deleted client.')
        
        error_messages=[]
        
        for extension in self.extensions.values():
            try:
                await self._unload_extension(client,extension)
            except ExtensionError as err:
                error_messages.append(err.message)
                continue
            
            try:
                await self._load_extension(client,extension)
            except ExtensionError as err:
                error_messages.append(err.message)
        
        if error_messages:
            raise ExtensionError(error_messages)

    async def _load_extension(self, client, extension):
        try:
            # loading blocks, but unloading does not
            lib = await client.loop.run_in_executor(extension.load)
        except BaseException as err:
            message=self._render_exc(err,[
                'Exception occured meanwhile loading an extension: ',extension.name,'\n',])
            
            raise ExtensionError(message) from None
        
        if lib is None:
            return # already loaded
        
        entry_point=extension.entry_point
        if entry_point is None:
            return
        
        if not isinstance(entry_point,str):
            try:
                
                if is_coro(entry_point):
                    await entry_point(client,lib)
                else:
                    entry_point(client,lib)
                    
            except BaseException as err:
                message = await client.loop.run_in_executor(alchemy_incendiary(
                    self._render_exc,(err,[
                    'Exception occured meanwhile entering an extension: `',extension.name,
                    '`\nAt entry_point:',repr(entry_point),'\n',],
                        )))
                
                raise ExtensionError(message) from None
            
            return
        
        entry_point=getattr(lib,entry_point,_spaceholder)
        if entry_point is _spaceholder:
            raise ExtensionError(f'Entry point: `{entry_point}` not found of extension: `{extension.name}`.')
        
        if entry_point is None:
            return # None is OK
        
        try:
            
            if is_coro(entry_point):
                await entry_point(client)
            else:
                entry_point(client)
                
        except BaseException as err:
            message = await client.loop.run_in_executor(alchemy_incendiary(
                self._render_exc,(err,[
                'Exception occured meanwhile entering an extension: `',extension.name,
                '`\nAt entry_point:',repr(entry_point),'\n',],
                    )))
            
            raise ExtensionError(message) from None

    async def _unload_extension(self, client, extension):
        # loading blocks, but unloading does not
        lib = extension.unload()
        
        if lib is None:
            return # not loaded

        exit_point=extension.exit_point
        if exit_point is None:
            return
        
        if not isinstance(exit_point,str):
            try:
                
                if is_coro(exit_point):
                    await exit_point(client,lib)
                else:
                    exit_point(client,lib)
                        
            except BaseException as err:
                message = await client.loop.run_in_executor(alchemy_incendiary(
                    self._render_exc,(err,[
                    'Exception occured meanwhile exiting an extension: `',extension.name,
                    '`\nAt exit_point:',repr(exit_point),'\n',],
                        )))
                
                raise ExtensionError(message) from None
            
            return
            
        exit_point=getattr(lib,exit_point,_spaceholder)
        if exit_point is _spaceholder:
            raise ExtensionError(f'Exit point: `{exit_point}` not found of extension: `{extension.name}`.')
        
        if exit_point is None:
            return # None is OK
        
        try:
            
            if is_coro(exit_point):
                await exit_point(client)
            else:
                exit_point(client)
            
        except BaseException as err:
            message = await client.loop.run_in_executor(alchemy_incendiary(
                self._render_exc,(err,[
                'Exception occured meanwhile exiting an extension: `',extension.name,
                '`\nAt exit_point:',repr(exit_point),'\n',],
                    )))
            
            raise ExtensionError(message) from None
        
    @staticmethod
    def _render_exc(exception, header):
        file=StringIO()
        EventThread._render_exc_sync(exception, before=header, after=None, file=file)
        message=file.getvalue()
        file.close()
        
        return message
    
    def __repr__(self):
        client=self.client()
        if client is None:
            client_repr='deleted'
        else:
            client_repr=repr(client.full_name)
        
        extension_count=repr(len(self.extensions))
        
        return f'{self.__class__.__name__} client={client_repr}, extension count={extension_count}>'
    
del WeakValueDictionary
