# -*- coding: utf-8 -*-
__all__ = ('CallableAnalyzer', )

from .dereaddons_local import function, MethodLike
from .futures import iscoroutinefunction as is_coro

CO_OPTIMIZED    = 1
CO_NEWLOCALS    = 2
CO_VARARGS      = 4
CO_VARKEYWORDS  = 8
CO_NESTED       = 16
CO_GENERATOR    = 32
CO_NOFREE       = 64

CO_COROUTINE            = 128
CO_ITERABLE_COROUTINE   = 256
CO_ASYNC_GENERATOR      = 512

INSTANCE_TO_ASYNC_FALSE = 0
INSTANCE_TO_ASYNC_TRUE  = 1
INSTANCE_TO_ASYNC_CANNOT= 2

ARGUMNET_POSITIONAL_ONLY        = 0
ARGUMNET_POSITIONAL_AND_KEYWORD = 1
ARGUMENT_KEYWORD_ONLY           = 2
ARGUMENT_ARGS                   = 3
ARGUMENT_KWARGS                 = 4

class Argument(object):
    __slots__ = ('annotation', 'default', 'has_annotation', 'has_default',
        'name', 'positionality', 'reserved', )
    
    def __repr__(self):
        result=[]
        result.append('<')
        result.append(self.__class__.__name__)
        
        if self.reserved:
            result.append(' reserved ,')
        
        result.append((' positonal only', ' positional', ' keyword only', ' args', ' kwargs')[self.positionality])
        
        result.append(', name=')
        result.append(repr(self.name))
        
        if self.has_default:
            result.append(', default=')
            result.append(repr(self.default))
        
        if self.has_annotation:
            result.append(', annotation=')
            result.append(repr(self.annotation))
        
        result.append('>')
        return ''.join(result)
    
    def is_positional_only(self):
        positionality = self.positionality
        if positionality == ARGUMNET_POSITIONAL_ONLY:
            return True
        
        return False
    
    def is_positional(self):
        positionality = self.positionality
        if positionality == ARGUMNET_POSITIONAL_ONLY:
            return True
        
        if positionality == ARGUMNET_POSITIONAL_AND_KEYWORD:
            return True
        
        return False
    
    def is_keyword(self):
        positionality = self.positionality
        if positionality == ARGUMNET_POSITIONAL_AND_KEYWORD:
            return True
        
        if positionality == ARGUMENT_KEYWORD_ONLY:
            return True
        
        return False
    
    def is_keyword_only(self):
        positionality = self.positionality
        if positionality == ARGUMENT_KEYWORD_ONLY:
            return True
        
        return False
    
    def is_args(self):
        positionality = self.positionality
        if positionality == ARGUMENT_ARGS:
            return True
        
        return False
    
    def is_kwargs(self):
        positionality = self.positionality
        if positionality == ARGUMENT_KWARGS:
            return True
        
        return False

class CallableAnalyzer(object):
    __slots__ = ('args_argument', 'arguments', 'callable', 'instance_to_async', 'kwargs_argument', 'method_allocation',
        'real_function', )
    
    def __repr__(self):
        result=[]
        result.append('<')
        result.append(self.__class__.__name__)
        
        if self.is_async():
            result.append(' async')
        elif self.can_instance_to_async_callable():
            result.append(' instance async')
        
        method_allocation = self.method_allocation
        if method_allocation:
            result.append(' method')
            if method_allocation!=1:
                result.append(' (')
                result.append(repr(method_allocation))
                result.append(')')
        
        result.append(' ')
        callable_ = self.callable
        result.append(repr(callable_))
        real_function = self.real_function
        if (callable_ is not real_function):
            result.append(' (')
            result.append(repr(real_function))
            result.append(')')
        
        result.append(', arguments=')
        result.append(repr(self.arguments))
        
        args_argument = self.args_argument
        if (args_argument is not None):
            result.append(', args=')
            result.append(repr(args_argument))
        
        kwargs_argument = self.kwargs_argument
        if (kwargs_argument is not None):
            result.append(', kwargs=')
            result.append(repr(kwargs_argument))
        
        result.append('>')
        return ''.join(result)
    
    def __new__(cls, callable_, as_method=False):
        while True:
            if isinstance(callable_, function):
                
                real_function=callable_
                if is_coro(real_function):
                    instance_to_async=INSTANCE_TO_ASYNC_FALSE
                else:
                    instance_to_async=INSTANCE_TO_ASYNC_CANNOT
                
                method_allocation=0
                break
            
            if isinstance(callable_,MethodLike):
                real_function=callable_
                
                if is_coro(real_function):
                    instance_to_async=INSTANCE_TO_ASYNC_FALSE
                else:
                    instance_to_async=INSTANCE_TO_ASYNC_CANNOT
                
                method_allocation=MethodLike.get_reserved_argcount(callable_)
                break
            
            if not isinstance(callable_, type) and hasattr(type(callable_),'__call__'):
                real_function=type(callable_).__call__
                
                if is_coro(real_function) or getattr(type(callable_),'__async_call__',0)==1:
                    instance_to_async = INSTANCE_TO_ASYNC_FALSE
                else:
                    instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                    
                if type(real_function) is function:
                    method_allocation = 1
                else:
                    method_allocation=MethodLike.get_reserved_argcount(real_function)
                
                break
            
            if not issubclass(callable_, type) and isinstance(callable_, type):
                
                while True:
                    real_function = callable_.__new__
                    if not callable(real_function):
                        raise TypeError(f'`{callable_!r}.__new__` should be callable, got `{real_function!r}`')
                    
                    if real_function is not object.__new__:
                        if is_coro(real_function):
                            instance_to_async = INSTANCE_TO_ASYNC_FALSE
                        else:
                            if hasattr(callable_,'__call__'):
                                call=callable_.__call__
                                if is_coro(call) or getattr(callable_,'__async_call__',0)==1:
                                    instance_to_async = INSTANCE_TO_ASYNC_TRUE
                                else:
                                    instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                            else:
                                instance_to_async = INSTANCE_TO_ASYNC_CANNOT

                        if type(real_function) is function:
                            method_allocation = 1
                        else:
                            method_allocation = MethodLike.get_reserved_argcount(real_function)
                    
                        break
                    
                    real_function = callable_.__init__
                    if not callable(real_function):
                        raise TypeError(f'`{callable_!r}.__init__` should be callable, got `{real_function!r}`')
                    
                    if real_function is not object.__init__:
                        if hasattr(callable_,'__call__'):
                            call=callable_.__call__
                            if is_coro(call) or getattr(callable_,'__async_call__',0)==1:
                                instance_to_async = INSTANCE_TO_ASYNC_TRUE
                            else:
                                instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                        else:
                            instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                        
                        if type(real_function) is function:
                            method_allocation = 1
                        else:
                            method_allocation = MethodLike.get_reserved_argcount(real_function)
                        
                        break
                    
                    real_function = None
                    method_allocation = 0
                    
                    if hasattr(callable_,'__call__'):
                        call=callable_.__call__
                        if is_coro(call) or getattr(callable_,'__async_call__',0)==1:
                            instance_to_async = INSTANCE_TO_ASYNC_TRUE
                        else:
                            instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                    else:
                        instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                    break
                
                break
            
            raise TypeError(f'Expected function, method or a callable object, got {callable_!r}')
        
        if as_method and type(callable_) is function:
            method_allocation +=1
        
        if (real_function is not None) and ( not hasattr(real_function, '__code__')):
            raise TypeError(f'Expected function, got `{real_function!r}`')
        
        arguments = []
        if (real_function is not None):
            argument_count = real_function.__code__.co_argcount
            accepts_args = real_function.__code__.co_flags&CO_VARARGS
            keyword_only_argument_count = real_function.__code__.co_kwonlyargcount
            accepts_kwargs = real_function.__code__.co_flags&CO_VARKEYWORDS
            positional_only_argcount = getattr(real_function.__code__,'co_posonlyargcount',0)
            default_argument_values=real_function.__defaults__
            default_keyword_only_argument_values = real_function.__kwdefaults__
            annotations = getattr(real_function,'__annotations__',None)
            if (annotations is None):
                annotations = {}
            
            start=0
            end=argument_count
            argument_names = real_function.__code__.co_varnames[start:end]
            
            start=end
            end=start+keyword_only_argument_count
            keyword_only_argument_names = real_function.__code__.co_varnames[start:end]
            
            if accepts_args:
                args_name = real_function.__code__.co_varnames[end]
                end = end+1
            else:
                args_name= None
            
            if accepts_kwargs:
                kwargs_name = real_function.__code__.co_varnames[end]
            else:
                kwargs_name = None
            
            names_to_defaults={}
            if (default_argument_values is not None) and default_argument_values:
                argument_index = argument_count - len(default_argument_values)
                default_index = 0
                while argument_index < argument_count:
                    name = argument_names[argument_index]
                    default = default_argument_values[default_index]
                    
                    names_to_defaults[name]=default
                    
                    argument_index+=1
                    default_index+=1
            
            if (default_keyword_only_argument_values is not None) and default_keyword_only_argument_values:
                argument_index = keyword_only_argument_count - len(default_keyword_only_argument_values)
                while argument_index < keyword_only_argument_count:
                    name = keyword_only_argument_names[argument_index]
                    default = default_keyword_only_argument_values[name]
                    
                    names_to_defaults[name]=default
                    
                    argument_index+=1
            
            if (method_allocation>argument_count) and (args_name is None):
                raise TypeError(f'The passed object is a method like, but has not enought positional arguments: `{real_function!r}`')
            
            index = 0
            while index < argument_count:
                argument = Argument()
                name = argument_names[index]
                argument.name = name
                
                try:
                    annotation = annotations[name]
                except KeyError:
                    argument.has_annotation = False
                    argument.annotation = None
                else:
                    argument.has_annotation = True
                    argument.annotation = annotation
                
                try:
                    default = names_to_defaults[name]
                except KeyError:
                    argument.has_default = False
                    argument.default = None
                else:
                    argument.has_default = True
                    argument.default = default
                
                if index<positional_only_argcount:
                    argument.positionality = ARGUMNET_POSITIONAL_ONLY
                else:
                    argument.positionality = ARGUMNET_POSITIONAL_AND_KEYWORD
                
                argument.reserved = (index<method_allocation)
                arguments.append(argument)
                index = index+1
            
            index = 0
            while index < keyword_only_argument_count:
                argument = Argument()
                name = keyword_only_argument_names[index]
                argument.name = name
                
                try:
                    annotation = annotations[name]
                except KeyError:
                    argument.has_annotation = False
                    argument.annotation = None
                else:
                    argument.has_annotation = True
                    argument.annotation = annotation
                
                try:
                    default = names_to_defaults[name]
                except KeyError:
                    argument.has_default = False
                    argument.default = None
                else:
                    argument.has_default = True
                    argument.default = default
                
                argument.positionality = ARGUMENT_KEYWORD_ONLY
                argument.reserved = False
                arguments.append(argument)
                index = index+1
            
            if args_name is None:
                args_argument = None
            else:
                args_argument = Argument()
                args_argument.name = args_name
                
                try:
                    annotation = annotations[args_name]
                except KeyError:
                    args_argument.has_annotation = False
                    args_argument.annotation = None
                else:
                    args_argument.has_annotation = True
                    args_argument.annotation = annotation

                args_argument.has_default = False
                args_argument.default = None
                args_argument.positionality = ARGUMENT_ARGS
                
                if method_allocation>argument_count:
                    args_argument.reserved = True
                else:
                    args_argument.reserved = False
                
            
            if kwargs_name is None:
                kwargs_argument = None
            else:
                kwargs_argument = Argument()
                kwargs_argument.name = kwargs_name
                try:
                    annotation = annotations[kwargs_name]
                except KeyError:
                    kwargs_argument.has_annotation = False
                    kwargs_argument.annotation = None
                else:
                    kwargs_argument.has_annotation = True
                    kwargs_argument.annotation = annotation
                
                kwargs_argument.has_default = False
                kwargs_argument.default = None
                kwargs_argument.positionality = ARGUMENT_KWARGS
                kwargs_argument.reserved = False
            
        else:
            args_argument = None
            kwargs_argument = None
        
        self = object.__new__(cls)
        self.arguments = arguments
        self.args_argument = args_argument
        self.kwargs_argument = kwargs_argument
        self.callable = callable_
        self.method_allocation = method_allocation
        self.real_function = real_function
        self.instance_to_async = instance_to_async
        return self
    
    def is_async(self):
        if self.instance_to_async == INSTANCE_TO_ASYNC_FALSE:
            return True
        
        return False
    
    def can_instance_to_async_callable(self):
        if self.instance_to_async != INSTANCE_TO_ASYNC_TRUE:
            return False
        
        for argument in self.arguments:
            if argument.reserved:
                continue
            
            if argument.has_default:
                continue
            
            return False
        
        return True
    
    # call `.can_instance_async_callable` before
    def instance_to_async_callable(self):
        return self.callable()
    
    def get_non_default_keyword_only_argument_count(self):
        count = 0
        for value in self.arguments:
            if not value.is_keyword_only():
                continue
            
            if value.has_default:
                break
            
            count = count+1
            continue
        
        return count
    
    def get_non_reserved_positional_arguments(self):
        result = []
        for argument in self.arguments:
            if not argument.is_positional():
                break
            
            if argument.reserved:
                continue
            
            result.append(argument)
            continue
        
        return result
    
    def get_non_reserved_positional_argument_count(self):
        count = 0
        for argument in self.arguments:
            if not argument.is_positional():
                break
            
            if argument.reserved:
                continue
            
            count = count+1
            continue
        
        return count
    
    def get_non_reserved_non_default_argument_count(self):
        count = 0
        for argument in self.arguments:
            if not argument.is_positional():
                break
            
            if argument.reserved:
                continue
            
            if argument.has_default:
                continue
            
            count = count+1
            continue
        
        return count

    def get_non_reserved_positional_argument_range(self):
        iterator = iter(self.arguments)
        start = 0
        for argument in iterator:
            if not argument.is_positional():
                return start, start
            
            if argument.reserved:
                continue
            
            if argument.has_default:
                break
            
            start = start+1
            continue
        
        else:
            return start, start
        
        end=start
        for argument in iterator:
            if not argument.is_positional():
                return start, end
            
            if argument.reserved:
                continue
            
            end = end+1
            continue
        
        return start, end
    
    def accepts_args(self):
        return (self.args_argument is not None)
    
    def accepts_kwargs(self):
        return (self.kwargs_argument is not None)
    