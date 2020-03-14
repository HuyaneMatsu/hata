# -*- coding: utf-8 -*-
__all__ = ('ExtensionError', 'ExtensionLoader', )

import sys
from io import StringIO
from weakref import WeakValueDictionary
from importlib.util import find_spec, module_from_spec
from importlib import reload as reload_module
from threading import current_thread

from .eventloop import EventThread
from .dereaddons_local import alchemy_incendiary, HybridValueDictionary
from .futures import iscoroutinefunction as is_coro, Task
from .analyzer import CallableAnalyzer

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

def _validate_entry_or_exit(point):
    if point is None:
        return False
    
    if isinstance(point,str):
        return False
    
    if callable(point):
        analyzer = CallableAnalyzer(point)
        min_, max_ = analyzer.get_non_reserved_positional_argument_range()
        if min_>1:
            raise ValueError(f'`{point!r}` excepts at least `{min_!r}` non reserved arguments, meanwhile the event expects to pass `1`.')
        
        if min_==1:
            return False
        
        #min<expected
        if max_>=1:
            return False
        
        if analyzer.accepts_args():
            return False
        
        raise ValueError(f'`{point!r}` expects maximum `{max_!r}` non reserved arguments  meanwhile the event expects to pass `1`.')
    
    return True

class Extension(object):
    __slots__ = ('__weakref__', '_added_variable_names', '_default_variables',
        '_entry_point', '_exit_point', '_extend_default_variables', '_lib',
        '_spec', '_state', )
    
    def __new__(cls, name, entry_point, exit_point, extend_default_variables, default_variables):
        try:
            return EXTENSIONS[name]
        except KeyError:
            pass
        
        spec=find_spec(name)
        if spec is None:
            raise ModuleNotFoundError(name)
        
        self=object.__new__(cls)
        self._state      = EXTENSION_STATE_UNDEFINED
        self._spec       = spec
        self._lib        = None
        self._entry_point= entry_point
        self._exit_point = exit_point
        self._extend_default_variables = extend_default_variables
        self._default_variables = default_variables
        self._added_variable_names = []
        EXTENSIONS[name]= self
        
        return self
    
    def __hash__(self):
        return hash(self._spec.origin)
    
    def __repr__(self):
        result = []
        result.append('<')
        result.append(self.__class__.__name__)
        result.append(' name=')
        result.append(repr(self._spec.name))
        
        state=self._state
        result.append(', state=')
        result.append(repr(state))
        result.append(' (')
        result.append(('undefined', 'loaded', 'unloaded')[state])
        result.append(')')
        
        default_variables = self._default_variables
        if self._extend_default_variables:
            if (default_variables is not None):
                result.append(' extends loader\'s defaults with: ')
                result.append(repr(default_variables))
        else:
            if default_variables is None:
                result.append(' clears loader\'s defaults')
            else:
                result.append(' clears loader\'s defaults and uses: ')
                result.append(repr(default_variables))
        
        result.append('>')
        
        return ''.join(result)
    
    def add_default_variables(self, **variables):
        if not variables:
            return
        
        default_variables = self._default_variables
        if default_variables is None:
            default_variables = HybridValueDictionary()
            self._default_variables = default_variables
        
        for key, value in variables.items():
            if key in PROTECTED_NAMES:
                raise ValueError(f'The passed {key!r} is a protected variable name of module type.')
            default_variables[key]=value
    
    def remove_default_variables(self, *names):
        default_variables = self._default_variables
        if default_variables is None:
            return
        
        for name in names:
            try:
                del default_variables[name]
            except KeyError:
                pass
        
        if default_variables:
            return
        
        self._default_variables=None
    
    def clear_default_variables(self):
        self._default_variables=None
        
    def _get_entry_point(self):
        return self._entry_point
    
    def _set_entry_point(self, entry_point):
        if _validate_entry_or_exit(entry_point):
            raise TypeError(f'`{self.__class__.__name__}.entry_point` expected None, str or a callable, got `{entry_point!r}`.')
        
        self._entry_point=entry_point
    
    def _del_entry_point(self):
        self._entry_point=None
    
    entry_point=property(_get_entry_point,_set_entry_point,_del_entry_point)
    del _get_entry_point, _set_entry_point, _del_entry_point
    
    def _get_exit_point(self):
        return self._exit_point
    
    def _set_exit_point(self, exit_point):
        if _validate_entry_or_exit(exit_point):
            raise TypeError(f'`{self.__class__.__name__}.exit_point` expected None, str or a callable, got `{exit_point!r}`.')
    
        self._exit_point=exit_point
    
    def _del_exit_point(self):
        self._exit_point=None
    
    exit_point=property(_get_exit_point,_set_exit_point,_del_exit_point)
    del _get_exit_point, _set_exit_point, _del_exit_point
    
    def _get_extend_default_variables(self):
        return self._extend_default_variables
    
    def _set_extend_default_variables(self, extend_default_variables):
        if not isinstance(extend_default_variables, int):
            raise TypeError(f'`extend_default_variables` should have been passed as `int` instance, got `{extend_default_variables!r}`.')
        
        if type(extend_default_variables) is not bool:
            if extend_default_variables:
                extend_default_variables=True
            else:
                extend_default_variables=False
        
        self._extend_default_variables=extend_default_variables
    
    extend_default_variables=property(_get_extend_default_variables,_set_extend_default_variables)
    del _get_extend_default_variables, _set_extend_default_variables
    
    def _load(self):
        state=self._state
        if state==EXTENSION_STATE_UNDEFINED:
            
            spec = self._spec
            try:
                # the lib is imported, return it
                lib = sys.modules[spec.name]
            except KeyError:
                # lib is not imported yet, nice
                lib = module_from_spec(spec)
                
                added_variable_names = self._added_variable_names
                if self._extend_default_variables:
                    for name, value in EXTENSION_LOADER._default_variables.items():
                        setattr(lib,name,value)
                        added_variable_names.append(name)
                
                default_variables = self._default_variables
                if (default_variables is not None):
                    for name, value in default_variables.items():
                        setattr(lib,name,value)
                        added_variable_names.append(name)
                
                spec.loader.exec_module(lib)
                sys.modules[spec.name] = lib
            
            self._lib = lib
            
            self._state=EXTENSION_STATE_LOADED
            return lib
        
        if state==EXTENSION_STATE_LOADED:
            # return None -> already loaded
            return None
        
        if state==EXTENSION_STATE_UNLOADED:
            # reload
            lib = self._lib
            
            added_variable_names = self._added_variable_names
            if self._extend_default_variables:
                for name, value in EXTENSION_LOADER._default_variables.items():
                    setattr(lib,name,value)
                    added_variable_names.append(name)
            
            default_variables = self._default_variables
            if (default_variables is not None):
                for name, value in default_variables.items():
                    setattr(lib,name,value)
                    added_variable_names.append(name)
            
            reload_module(lib)
            
            self._state=EXTENSION_STATE_LOADED
            return lib
        
        # no more cases
    
    def _unload(self):
        state=self._state
        if state==EXTENSION_STATE_UNDEFINED:
            return None
        
        if state==EXTENSION_STATE_LOADED:
            self._state=EXTENSION_STATE_UNLOADED
            return self._lib
        
        if state==EXTENSION_STATE_UNLOADED:
            return None
        
        # no more cases
    
    def _unasign_variables(self):
        lib = self._lib
        if lib is None:
            return
        
        added_variable_names = self._added_variable_names
        for name in added_variable_names:
            try:
                delattr(lib, name)
            except AttributeError:
                pass
        added_variable_names.clear()
    
    @property
    def name(self):
        return self._spec.name
    
    def _unlink(self):
        state=self._state
        if state==EXTENSION_STATE_UNDEFINED:
            return
        
        if state==EXTENSION_STATE_LOADED:
            self._state=EXTENSION_STATE_UNLOADED
            lib = self._lib
            
            if self._extend_default_variables:
                for name in EXTENSION_LOADER._default_variables:
                    try:
                        delattr(lib,name)
                    except AttributeError:
                        pass
            
            default_variables = self._default_variables
            if (default_variables is not None):
                for name in default_variables:
                    delattr(lib,name)
            
            del sys.modules[self._spec.name]
            return
        
        if state==EXTENSION_STATE_UNLOADED:
            del sys.modules[self._spec.name]
            return
        
        # no more cases

PROTECTED_NAMES = {
    '__class__',
    '__delattr__',
    '__dict__',
    '__dir__',
    '__doc__',
    '__eq__',
    '__format__',
    '__ge__',
    '__getattribute__',
    '__gt__',
    '__hash__',
    '__init__',
    '__init_subclass__',
    '__le__',
    '__lt__',
    '__module__',
    '__ne__',
    '__new__',
    '__reduce__',
    '__reduce_ex__',
    '__repr__',
    '__setattr__',
    '__sizeof__',
    '__str__',
    '__subclasshook__',
    '__weakref__',
    '_cached',
    '_set_fileattr',
    'cached',
    'has_location',
    'loader',
    'loader_state',
    'name',
    'origin',
    'parent',
    'submodule_search_locations',
        }

class ExtensionLoader(object):
    __slots__=('extensions', '_default_entry_point', '_default_exit_point', '_default_variables')
    
    _instance = None
    def __new__(cls,):
        self = cls._instance
        if self is None:
            self = object.__new__(cls)
            self._default_entry_point = 'setup'
            self._default_exit_point = 'teardown'
            self.extensions={}
            self._default_variables = HybridValueDictionary()
        
        return self
    
    def _get_default_entry_point(self):
        return self._default_entry_point
    
    def _set_default_entry_point(self, default_entry_point):
        if _validate_entry_or_exit(default_entry_point):
            raise TypeError(f'`{self.__class__.__name__}.default_entry_point` expected None, str or a callable, got `{default_entry_point!r}`.')
        
        self._default_entry_point=default_entry_point
    
    def _del_default_entry_point(self):
        self._default_entry_point=None
    
    default_entry_point=property(_get_default_entry_point,_set_default_entry_point,_del_default_entry_point)
    del _get_default_entry_point, _set_default_entry_point, _del_default_entry_point
    
    def _get_default_exit_point(self):
        return self._default_exit_point
    
    def _set_default_exit_point(self, default_exit_point):
        if _validate_entry_or_exit(default_exit_point):
            raise TypeError(f'`{self.__class__.__name__}.default_exit_point` expected None, str or a callable, got `{default_exit_point!r}`.')
        
        self._default_exit_point=default_exit_point
    
    def _del_default_exit_point(self):
        self._default_exit_point=None
    
    default_exit_point=property(_get_default_exit_point,_set_default_exit_point,_del_default_exit_point)
    del _get_default_exit_point, _set_default_exit_point, _del_default_exit_point
    
    def add_default_variables(self, **variables):
        default_variables = self._default_variables
        for key, value in variables.items():
            if key in PROTECTED_NAMES:
                raise ValueError(f'The passed {key!r} is a protected variable name of module type.')
            default_variables[key]=value
    
    def remove_default_variables(self, *names):
        default_variables = self._default_variables
        for name in names:
            try:
                del default_variables[name]
            except KeyError:
                pass
    
    def clear_default_variables(self):
        self._default_variables.clear()
    
    def add(self, name, entry_point=None, exit_point=None, extend_default_variables=True, **variables):
        if _validate_entry_or_exit(entry_point):
            raise TypeError(f'`{self.__class__.__name__}.add` expected None, str or a callable as `entry_point`, got `{entry_point!r}`.')
        
        if _validate_entry_or_exit(exit_point):
            raise TypeError(f'`{self.__class__.__name__}.add` expected None, str or a callable as `exit_point`, got `{exit_point!r}`.')
        
        if variables:
            default_variables=HybridValueDictionary(variables)
            for key, value in variables.items():
                if key in PROTECTED_NAMES:
                    raise ValueError(f'The passed {key!r} is a protected variable name of module type.')
                default_variables[key]=value
        else:
            default_variables = None
        
        if isinstance(name,str):
            # case of 1 element
            self.extensions[name] = Extension(name, entry_point, exit_point, extend_default_variables, default_variables)
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
                self.extensions[name] = Extension(name, entry_point, exit_point, extend_default_variables, default_variables)
            
            return
        
        #no more good case -> raise
        raise TypeError(f'`{self.__class__.__name__}.add` expected `str` or `iterable of str` as `name`, got `{name!r}`.')
    
    def remove(self, name):
        if isinstance(name,str):
            # case of 1 element
            try:
                extension=self.extensions[name]
            except KeyError:
                return
            
            if extension._state==EXTENSION_STATE_LOADED:
                raise RuntimeError(f'Extension `{name}` can not be removed, meanwhile it is loaded.')
            
            extension._unlink()
            
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
                
                if extension._state==EXTENSION_STATE_LOADED:
                    raise RuntimeError(f'Extension `{name}` can not be removed, meanwhile it is loaded.')
                
                collected.append(extension)
                
            for extension in collected:
                extension._unlink()
            
            return
        
        #no more good case -> raise
        raise TypeError(f'`{self.__class__.__name__}.add` expected `str` or `iterable of str` as `name`, got `{name!r}`.')
   
    def load_extension(self, name, *args, **kwargs):
        self.add(name, *args, **kwargs)
        return self.load(name)
    
    def load(self, name):
        task=Task(self._load(name),KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread,EventThread):
            return task.asyncwrap(current_thread)
        
        KOKORO.wakeup()
        task.syncwrap().wait()
    
    async def _load(self, name):
        try:
            extension=self.extensions[name]
        except KeyError:
            raise ExtensionError(f'No extension was added with name: `{name}`.') from None
        
        await self._load_extension(extension)
        
    def unload(self, name):
        task=Task(self._unload(name),KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread,EventThread):
            return task.asyncwrap(current_thread)
        
        KOKORO.wakeup()
        task.syncwrap().wait()
    
    async def _unload(self, name):
        try:
            extension=self.extensions[name]
        except KeyError:
            raise ExtensionError(f'No extension was added with name: `{name}`.') from None
        
        await self._unload_extension(extension)
        
    def reload(self, name):
        task=Task(self._reload(name),KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread,EventThread):
            return task.asyncwrap(current_thread)
        
        KOKORO.wakeup()
        task.syncwrap().wait()
    
    async def _reload(self, name):
        try:
            extension=self.extensions[name]
        except KeyError:
            raise ExtensionError(f'No extension was added with name: `{name}`.') from None
        
        await self._unload_extension(extension)
        await self._load_extension(extension)
    
    def load_all(self):
        task=Task(self._load_all(),KOKORO)

        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread,EventThread):
            return task.asyncwrap(current_thread)
        
        KOKORO.wakeup()
        task.syncwrap().wait()
        
    async def _load_all(self):
        error_messages=[]
        
        for extension in self.extensions.values():
            try:
                await self._load_extension(extension)
            except ExtensionError as err:
                error_messages.append(err.message)
            
        if error_messages:
            raise ExtensionError(error_messages) from None
        
    def unload_all(self):
        task=Task(self._unload_all(),KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread,EventThread):
            return task.asyncwrap(current_thread)
        
        KOKORO.wakeup()
        task.syncwrap().wait()
    
    async def _unload_all(self):
        error_messages=[]
        
        for extension in self.extensions.values():
            try:
                await self._unload_extension(extension)
            except ExtensionError as err:
                error_messages.append(err.message)
            
        if error_messages:
            raise ExtensionError(error_messages) from None
    
    def reload_all(self):
        task=Task(self._reload_all(),KOKORO)
        
        thread = current_thread()
        if thread is KOKORO:
            return task
        
        if isinstance(current_thread,EventThread):
            return task.asyncwrap(current_thread)
        
        KOKORO.wakeup()
        task.syncwrap().wait()
    
    async def _reload_all(self):
        error_messages=[]
        
        for extension in self.extensions.values():
            try:
                await self._unload_extension(extension)
            except ExtensionError as err:
                error_messages.append(err.message)
                continue
            
            try:
                await self._load_extension(extension)
            except ExtensionError as err:
                error_messages.append(err.message)
        
        if error_messages:
            raise ExtensionError(error_messages) from None
    
    async def _load_extension(self, extension):
        try:
            # loading blocks, but unloading does not
            lib = await KOKORO.run_in_executor(extension._load)
        except BaseException as err:
            message=self._render_exc(err,[
                'Exception occured meanwhile loading an extension: `',extension.name,'`.\n\n',])
            
            raise ExtensionError(message) from None
        
        if lib is None:
            return # already loaded
        
        entry_point=extension._entry_point
        if entry_point is None:
            entry_point=self._default_entry_point
            if entry_point is None:
                return
        
        if not isinstance(entry_point,str):
            try:
                
                if is_coro(entry_point):
                    await entry_point(lib)
                else:
                    entry_point(lib)
            
            except BaseException as err:
                message = await KOKORO.run_in_executor(alchemy_incendiary(
                    self._render_exc,(err,[
                    'Exception occured meanwhile entering an extension: `',extension.name,
                    '`.\nAt entry_point:',repr(entry_point),'\n\n',],
                        )))
                
                raise ExtensionError(message) from None
            
            return
        
        entry_point=getattr(lib,entry_point,None)
        if entry_point is None:
            return # None is OK
        
        try:
            
            if is_coro(entry_point):
                await entry_point(lib)
            else:
                entry_point(lib)
        
        except BaseException as err:
            message = await KOKORO.run_in_executor(alchemy_incendiary(
                self._render_exc,(err,[
                'Exception occured meanwhile entering an extension: `',extension.name,
                '`.\nAt entry_point:',repr(entry_point),'\n\n',],
                    )))
            
            raise ExtensionError(message) from None
    
    async def _unload_extension(self, extension):
        # loading blocks, but unloading does not
        lib = extension._unload()
        
        if lib is None:
            return # not loaded

        exit_point=extension._exit_point
        if exit_point is None:
            exit_point=self._default_exit_point
            if exit_point is None:
                return
        
        if not isinstance(exit_point,str):
            try:
                
                if is_coro(exit_point):
                    await exit_point(lib)
                else:
                    exit_point(lib)
            
            except BaseException as err:
                message = await KOKORO.run_in_executor(alchemy_incendiary(
                    self._render_exc,(err,[
                    'Exception occured meanwhile exiting an extension: `',extension.name,
                    '`.\nAt exit_point:',repr(exit_point),'\n\n',],
                        )))
                
                raise ExtensionError(message) from None
            
        else:
            exit_point=getattr(lib,exit_point,None)
            if (exit_point is not None):
                try:
                    
                    if is_coro(exit_point):
                        await exit_point(lib)
                    else:
                        exit_point(lib)
                    
                except BaseException as err:
                    message = await KOKORO.run_in_executor(alchemy_incendiary(
                        self._render_exc,(err,[
                        'Exception occured meanwhile exiting an extension: `',extension.name,
                        '`.\nAt exit_point:',repr(exit_point),'\n\n',],
                            )))
                    
                    raise ExtensionError(message) from None
        
        extension._unasign_variables()
        
    @staticmethod
    def _render_exc(exception, header):
        file=StringIO()
        EventThread._render_exc_sync(exception, before=header, after=None, file=file)
        message=file.getvalue()
        file.close()
        
        return message
    
    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
            ' extension count=',
            repr(len(self.extensions)),
                ]
        
        entry_point = self._default_entry_point
        if (entry_point is not None):
            result.append(', defualt_entry_point=')
            result.append(repr(entry_point))
        
        exit_point = self._default_exit_point
        if (exit_point is not None):
            result.append(', defualt_exit_point=')
            result.append(repr(exit_point))
        
        default_variables = self._default_variables
        if default_variables:
            result.append(', default_variables=')
            result.append(repr(default_variables))
        
        result.append('>')
        
        return ''.join(result)

EXTENSION_LOADER = ExtensionLoader()

del WeakValueDictionary
