__all__ = ('CallableAnalyzer', 'RichAnalyzer')

import sys

from .utils import FunctionType, MethodLike
from .export import include

IS_PYTHON_STULTUS = sys.version_info >= (3, 10, 0)

is_coroutine_function = include('is_coroutine_function')
is_coroutine_generator_function = include('is_coroutine_generator_function')

CO_OPTIMIZED = 1
CO_NEWLOCALS = 2
CO_VARARGS = 4
CO_VARKEYWORDS = 8
CO_NESTED = 16
CO_GENERATOR = 32
CO_NOFREE = 64

CO_COROUTINE = 128
CO_ITERABLE_COROUTINE = 256
CO_ASYNC_GENERATOR = 512
# matches `async def` functions and `@coroutine` functions.
CO_COROUTINE_ALL = CO_COROUTINE|CO_ITERABLE_COROUTINE

INSTANCE_TO_ASYNC_FALSE = 1
INSTANCE_TO_ASYNC_TRUE = 2
INSTANCE_TO_ASYNC_CANNOT = 3
INSTANCE_TO_ASYNC_GENERATOR_FALSE = 4
INSTANCE_TO_ASYNC_GENERATOR_TRUE = 5

PARAMETER_TYPE_POSITIONAL_ONLY = 1
PARAMETER_TYPE_POSITIONAL_AND_KEYWORD = 2
PARAMETER_TYPE_KEYWORD_ONLY = 3
PARAMETER_TYPE_ARGS = 4
PARAMETER_TYPE_KWARGS = 5

PARAMETER_TYPE_NAMES = {
    PARAMETER_TYPE_POSITIONAL_ONLY: 'positional only',
    PARAMETER_TYPE_POSITIONAL_AND_KEYWORD: 'positional',
    PARAMETER_TYPE_KEYWORD_ONLY: 'keyword only',
    PARAMETER_TYPE_ARGS: 'args',
    PARAMETER_TYPE_KWARGS: 'kwargs',
}

class Parameter:
    """
    Represents a callable's parameter.
    
    Attributes
    ----------
    annotation : `Any`
        The parameter's annotation if applicable. Defaults to `None`.
    default : `Any`
        The default value of the parameter if applicable. Defaults to `None`.
    has_annotation : `bool`
        Whether the parameter has annotation.
    has_default : `bool`
        Whether the parameter has default value.
    name : `str`
        The parameter's name.
    positionality : `int`
        Whether the parameter is positional, keyword or such.
        
        Can be set one of the following:
        +----------------------------------------+-----------+
        | Respective Name                        | Value     |
        +========================================+===========+
        | PARAMETER_TYPE_POSITIONAL_ONLY         | 1         |
        +----------------------------------------+-----------+
        | PARAMETER_TYPE_POSITIONAL_AND_KEYWORD  | 2         |
        +----------------------------------------+-----------+
        | PARAMETER_TYPE_KEYWORD_ONLY            | 3         |
        +----------------------------------------+-----------+
        | PARAMETER_TYPE_ARGS                    | 4         |
        +----------------------------------------+-----------+
        | PARAMETER_TYPE_KWARGS                  | 5         |
        +----------------------------------------+-----------+
    reserved : `bool`
        Whether the parameter is reserved.
        
        For example at the case of methods, the first parameter is reserved for the `self` parameter.
    """
    __slots__ = ('annotation', 'default', 'has_annotation', 'has_default', 'name', 'positionality', 'reserved', )
    
    def __repr__(self):
        """Returns the parameter's representation."""
        result = []
        result.append('<')
        result.append(self.__class__.__name__)
        result.append(' ')
        
        if self.reserved:
            result.append('reserved, ')
        
        result.append(PARAMETER_TYPE_NAMES[self.positionality])
        
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
        """
        Returns whether the parameter is positional only.
        
        Returns
        -------
        is_positional_only : `bool`
        """
        positionality = self.positionality
        if positionality == PARAMETER_TYPE_POSITIONAL_ONLY:
            return True
        
        return False
    
    def is_positional(self):
        """
        Returns whether the parameter is positional.
        
        Returns
        -------
        is_positional : `bool`
        """
        positionality = self.positionality
        if positionality == PARAMETER_TYPE_POSITIONAL_ONLY:
            return True
        
        if positionality == PARAMETER_TYPE_POSITIONAL_AND_KEYWORD:
            return True
        
        return False
    
    def is_keyword(self):
        """
        Returns whether the parameter can be used as a keyword parameter.
        
        Returns
        -------
        is_keyword : `bool`
        """
        positionality = self.positionality
        if positionality == PARAMETER_TYPE_POSITIONAL_AND_KEYWORD:
            return True
        
        if positionality == PARAMETER_TYPE_KEYWORD_ONLY:
            return True
        
        return False
    
    def is_keyword_only(self):
        """
        Returns whether they parameter is keyword only.
        
        Returns
        -------
        is_keyword_only : `bool`
        """
        positionality = self.positionality
        if positionality == PARAMETER_TYPE_KEYWORD_ONLY:
            return True
        
        return False
    
    def is_args(self):
        """
        Returns whether the parameter is an `*args` parameter.
        
        Returns
        -------
        is_args : `bool`
        """
        positionality = self.positionality
        if positionality == PARAMETER_TYPE_ARGS:
            return True
        
        return False
    
    def is_kwargs(self):
        """
        Returns whether the parameter is an `**kwargs` parameter.
        
        Returns
        -------
        is_kwargs : `bool`
        """
        positionality = self.positionality
        if positionality == PARAMETER_TYPE_KWARGS:
            return True
        
        return False

if IS_PYTHON_STULTUS:
    def compile_annotations(real_function, annotations):
        new_annotations = {}
        if not annotations:
            return new_annotations
        
        global_variables = getattr(real_function, '__globals__', None)
        if (global_variables is None):
            # Builtins go brrr
            return new_annotations
        
        for key, value in annotations.items():
            if type(value) is str:
                try:
                    value = eval(value, global_variables, None)
                except:
                    pass
            
            new_annotations[key] = value
        
        return new_annotations


class CallableAnalyzer:
    """
    Analyzer for callable-s.
    
    Can analyze functions, methods, callable objects and types or such.
    
    Attributes
    ----------
    args_parameter : `None` or ``Parameter``
        If the analyzed callable has `*args` parameter, then this attribute is set to it. Defaults to `None`.
    parameters : `list` of ``Parameter``
        The analyzed callable's parameters.
    callable : `callable`
        The analyzed object.
    instance_to_async : `int`
        Whether the analyzed object can be instanced to async.
        
        +---------------------------+-----------+-------------------------------------------+
        | Respective Name           | Value     | Description                               |
        +===========================+===========+===========================================+
        | INSTANCE_TO_ASYNC_FALSE   | 1         | Whether the object is async.              |
        +---------------------------+-----------+-------------------------------------------+
        | INSTANCE_TO_ASYNC_TRUE    | 2         | Whether the object is on async callable,  |
        |                           |           | but after instancing it, returns one.     |
        +---------------------------+-----------+-------------------------------------------+
        | INSTANCE_TO_ASYNC_CANNOT  | 3         | Whether the object is not async.          |
        +---------------------------+-----------+-------------------------------------------+
    kwargs_parameter : `None` or ``Parameter``
        If the analyzed callable has `**kwargs`, then this attribute is set to it. Defaults to `None`.
    method_allocation : `int`
        How much parameter is allocated if the analyzed callable is method if applicable.
    real_function : `callable`
        The function wrapped by the given callable.
    """
    __slots__ = ('args_parameter', 'parameters', 'callable', 'instance_to_async', 'kwargs_parameter',
        'method_allocation', 'real_function', )
    
    def __repr__(self):
        """Returns the callable analyzer's representation."""
        result = []
        result.append('<')
        result.append(self.__class__.__name__)
        
        if self.is_async():
            result.append(' async')
        elif self.is_async_generator():
            result.append(' async generator')
        elif self.can_instance_to_async_callable():
            result.append(' instance async')
        elif self.can_instance_to_async_generator():
            result.append(' instance async generator')
        
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
        
        result.append(', parameters=')
        result.append(repr(self.parameters))
        
        args_parameter = self.args_parameter
        if (args_parameter is not None):
            result.append(', args=')
            result.append(repr(args_parameter))
        
        kwargs_parameter = self.kwargs_parameter
        if (kwargs_parameter is not None):
            result.append(', kwargs=')
            result.append(repr(kwargs_parameter))
        
        result.append('>')
        return ''.join(result)
    
    def __new__(cls, callable_, as_method=False):
        """
        Analyzes the given callable.
        
        Parameters
        ----------
        callable_ : `callable`
            The callable to analyze.
        as_method : `bool`, Optional
            Whether the given `callable` is given as a `function`, but it should be analyzed as a `method`. Defaults
            to `False`.
        
        Raises
        ------
        TypeError
            If the given object is not callable, or could not be used as probably intended.
        """
        while True:
            if isinstance(callable_, FunctionType):
                
                real_function = callable_
                if is_coroutine_function(real_function):
                    instance_to_async = INSTANCE_TO_ASYNC_FALSE
                elif is_coroutine_generator_function(real_function):
                    instance_to_async = INSTANCE_TO_ASYNC_GENERATOR_FALSE
                else:
                    instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                
                method_allocation = 0
                break
            
            if isinstance(callable_, MethodLike):
                real_function = callable_
                
                if is_coroutine_function(real_function):
                    instance_to_async = INSTANCE_TO_ASYNC_FALSE
                elif is_coroutine_generator_function(real_function):
                    instance_to_async = INSTANCE_TO_ASYNC_GENERATOR_FALSE
                else:
                    instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                
                method_allocation = MethodLike.get_reserved_argcount(callable_)
                break
            
            if not isinstance(callable_, type) and hasattr(type(callable_), '__call__'):
                real_function = type(callable_).__call__
                
                if is_coroutine_function(real_function):
                    instance_to_async = INSTANCE_TO_ASYNC_FALSE
                elif is_coroutine_generator_function(real_function):
                    instance_to_async = INSTANCE_TO_ASYNC_GENERATOR_FALSE
                else:
                    instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                    
                if type(real_function) is FunctionType:
                    method_allocation = 1
                else:
                    method_allocation = MethodLike.get_reserved_argcount(real_function)
                
                break
            
            if not issubclass(callable_, type) and isinstance(callable_, type):
                
                while True:
                    real_function = callable_.__new__
                    if not callable(real_function):
                        raise TypeError(f'`{callable_!r}.__new__` should be callable, got `{real_function!r}`')
                    
                    if real_function is not object.__new__:
                        if is_coroutine_function(real_function):
                            instance_to_async = INSTANCE_TO_ASYNC_FALSE
                        elif is_coroutine_generator_function(real_function):
                            instance_to_async = INSTANCE_TO_ASYNC_GENERATOR_FALSE
                        else:
                            if hasattr(callable_, '__call__'):
                                call = callable_.__call__
                                if is_coroutine_function(call):
                                    instance_to_async = INSTANCE_TO_ASYNC_TRUE
                                elif is_coroutine_generator_function(call):
                                    instance_to_async = INSTANCE_TO_ASYNC_GENERATOR_TRUE
                                else:
                                    instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                            else:
                                instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                        
                        if type(real_function) is FunctionType:
                            method_allocation = 1
                        else:
                            method_allocation = MethodLike.get_reserved_argcount(real_function)
                        
                        break
                    
                    real_function = callable_.__init__
                    if not callable(real_function):
                        raise TypeError(f'`{callable_!r}.__init__` should be callable, got `{real_function!r}`')
                    
                    if real_function is not object.__init__:
                        if hasattr(callable_, '__call__'):
                            call = callable_.__call__
                            if is_coroutine_function(call):
                                instance_to_async = INSTANCE_TO_ASYNC_TRUE
                            elif is_coroutine_generator_function(call):
                                instance_to_async = INSTANCE_TO_ASYNC_GENERATOR_TRUE
                            else:
                                instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                        else:
                            instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                        
                        if type(real_function) is FunctionType:
                            method_allocation = 1
                        else:
                            method_allocation = MethodLike.get_reserved_argcount(real_function)
                        
                        break
                    
                    real_function = None
                    method_allocation = 0
                    
                    if hasattr(callable_,'__call__'):
                        call = callable_.__call__
                        if is_coroutine_function(call):
                            instance_to_async = INSTANCE_TO_ASYNC_TRUE
                        elif is_coroutine_generator_function(call):
                            instance_to_async = INSTANCE_TO_ASYNC_GENERATOR_TRUE
                        else:
                            instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                    else:
                        instance_to_async = INSTANCE_TO_ASYNC_CANNOT
                    break
                
                break
            
            raise TypeError(f'Expected function, method or a callable object, got {callable_!r}.')
        
        if as_method and type(callable_) is FunctionType:
            method_allocation += 1
        
        if (real_function is not None) and ( not hasattr(real_function, '__code__')):
            raise TypeError(f'Expected function, got `{real_function!r}`')
        
        parameters = []
        if (real_function is not None):
            parameter_count = real_function.__code__.co_argcount
            accepts_args = real_function.__code__.co_flags&CO_VARARGS
            keyword_only_parameter_count = real_function.__code__.co_kwonlyargcount
            accepts_kwargs = real_function.__code__.co_flags&CO_VARKEYWORDS
            positional_only_argcount = getattr(real_function.__code__, 'co_posonlyargcount', 0)
            default_parameter_values = real_function.__defaults__
            default_keyword_only_parameter_values = real_function.__kwdefaults__
            annotations = getattr(real_function, '__annotations__', None)
            if (annotations is None):
                annotations = {}
            elif IS_PYTHON_STULTUS:
                annotations = compile_annotations(real_function, annotations)
            
            start = 0
            end = parameter_count
            parameter_names = real_function.__code__.co_varnames[start:end]
            
            start = end
            end = start+keyword_only_parameter_count
            keyword_only_parameter_names = real_function.__code__.co_varnames[start:end]
            
            if accepts_args:
                args_name = real_function.__code__.co_varnames[end]
                end += 1
            else:
                args_name= None
            
            if accepts_kwargs:
                kwargs_name = real_function.__code__.co_varnames[end]
            else:
                kwargs_name = None
            
            names_to_defaults = {}
            if (default_parameter_values is not None) and default_parameter_values:
                parameter_index = parameter_count - len(default_parameter_values)
                default_index = 0
                while parameter_index < parameter_count:
                    name = parameter_names[parameter_index]
                    default = default_parameter_values[default_index]
                    
                    names_to_defaults[name] = default
                    
                    parameter_index += 1
                    default_index += 1
            
            if (default_keyword_only_parameter_values is not None) and default_keyword_only_parameter_values:
                parameter_index = keyword_only_parameter_count - len(default_keyword_only_parameter_values)
                while parameter_index < keyword_only_parameter_count:
                    name = keyword_only_parameter_names[parameter_index]
                    default = default_keyword_only_parameter_values[name]
                    
                    names_to_defaults[name] = default
                    
                    parameter_index += 1
            
            if (method_allocation>parameter_count) and (args_name is None):
                raise TypeError(f'The passed object is a method like, but has not enough positional parameters: '
                    f'`{real_function!r}`.')
            
            index = 0
            while index < parameter_count:
                parameter = Parameter()
                name = parameter_names[index]
                parameter.name = name
                
                try:
                    annotation = annotations[name]
                except KeyError:
                    parameter.has_annotation = False
                    parameter.annotation = None
                else:
                    parameter.has_annotation = True
                    parameter.annotation = annotation
                
                try:
                    default = names_to_defaults[name]
                except KeyError:
                    parameter.has_default = False
                    parameter.default = None
                else:
                    parameter.has_default = True
                    parameter.default = default
                
                if index<positional_only_argcount:
                    parameter.positionality = PARAMETER_TYPE_POSITIONAL_ONLY
                else:
                    parameter.positionality = PARAMETER_TYPE_POSITIONAL_AND_KEYWORD
                
                parameter.reserved = (index<method_allocation)
                parameters.append(parameter)
                index = index+1
            
            if args_name is None:
                args_parameter = None
            else:
                args_parameter = Parameter()
                args_parameter.name = args_name
                
                try:
                    annotation = annotations[args_name]
                except KeyError:
                    args_parameter.has_annotation = False
                    args_parameter.annotation = None
                else:
                    args_parameter.has_annotation = True
                    args_parameter.annotation = annotation

                args_parameter.has_default = False
                args_parameter.default = None
                args_parameter.positionality = PARAMETER_TYPE_ARGS
                
                if method_allocation > parameter_count:
                    args_parameter.reserved = True
                else:
                    args_parameter.reserved = False
                parameters.append(args_parameter)
            
            index = 0
            while index < keyword_only_parameter_count:
                parameter = Parameter()
                name = keyword_only_parameter_names[index]
                parameter.name = name
                
                try:
                    annotation = annotations[name]
                except KeyError:
                    parameter.has_annotation = False
                    parameter.annotation = None
                else:
                    parameter.has_annotation = True
                    parameter.annotation = annotation
                
                try:
                    default = names_to_defaults[name]
                except KeyError:
                    parameter.has_default = False
                    parameter.default = None
                else:
                    parameter.has_default = True
                    parameter.default = default
                
                parameter.positionality = PARAMETER_TYPE_KEYWORD_ONLY
                parameter.reserved = False
                parameters.append(parameter)
                index = index+1
            
            if kwargs_name is None:
                kwargs_parameter = None
            else:
                kwargs_parameter = Parameter()
                kwargs_parameter.name = kwargs_name
                try:
                    annotation = annotations[kwargs_name]
                except KeyError:
                    kwargs_parameter.has_annotation = False
                    kwargs_parameter.annotation = None
                else:
                    kwargs_parameter.has_annotation = True
                    kwargs_parameter.annotation = annotation
                
                kwargs_parameter.has_default = False
                kwargs_parameter.default = None
                kwargs_parameter.positionality = PARAMETER_TYPE_KWARGS
                kwargs_parameter.reserved = False
                parameters.append(kwargs_parameter)
        
        else:
            args_parameter = None
            kwargs_parameter = None
        
        self = object.__new__(cls)
        self.parameters = parameters
        self.args_parameter = args_parameter
        self.kwargs_parameter = kwargs_parameter
        self.callable = callable_
        self.method_allocation = method_allocation
        self.real_function = real_function
        self.instance_to_async = instance_to_async
        return self
    
    def is_async(self):
        """
        Returns whether the analyzed callable is async.
        
        Returns
        -------
        is_async : `bool`
        """
        if self.instance_to_async == INSTANCE_TO_ASYNC_FALSE:
            return True
        
        return False
    
    def is_async_generator(self):
        """
        Returns whether the analyzed callable is an async generator.
        
        Returns
        is_async_generator : `bool`
        """
        if self.instance_to_async == INSTANCE_TO_ASYNC_GENERATOR_FALSE:
            return True
        
        return False
    
    def can_instance_to_async_callable(self):
        """
        Returns whether the analyzed callable can be instanced to async.
        
        Returns
        -------
        can_instance_to_async_callable : `bool`
        """
        if self.instance_to_async != INSTANCE_TO_ASYNC_TRUE:
            return False
        
        for parameter in self.parameters:
            if parameter.reserved:
                continue
            
            if parameter.has_default:
                continue
            
            return False
        
        return True
    
    def can_instance_to_async_generator(self):
        """
        Returns whether the analyzed callable can be instanced to async.
        
        Returns
        -------
        can_instance_to_async_callable : `bool`
        """
        if self.instance_to_async != INSTANCE_TO_ASYNC_GENERATOR_TRUE:
            return False
        
        for parameter in self.parameters:
            if parameter.reserved:
                continue
            
            if parameter.has_default:
                continue
            
            return False
        
        return True
    
    # call `.can_instance_async_callable` or `.can_instance_to_async_generator` before
    def instance(self):
        """
        Instances the analyzed callable.
        
        Should be called only after a ``.can_instance_async_callable`` call, if it returned `True`.
        
        Returns
        -------
        instance_to_async_callable : `Any`
        """
        return self.callable()
    
    def get_non_default_keyword_only_parameter_count(self):
        """
        Returns the amount of non default keyword only parameters of the analyzed callable.
        
        Returns
        -------
        non_default_keyword_only_parameter_count : `int`
        """
        count = 0
        for value in self.parameters:
            if not value.is_keyword_only():
                continue
            
            if value.has_default:
                break
            
            count += 1
            continue
        
        return count
    
    def get_non_reserved_positional_parameters(self):
        """
        Returns the non reserved positional parameters of the analyzed callable.
        
        Returns
        -------
        non_reserved_positional_parameters : `list` of ``Parameter``
        """
        result = []
        for parameter in self.parameters:
            if not parameter.is_positional():
                break
            
            if parameter.reserved:
                continue
            
            result.append(parameter)
            continue
        
        return result
    
    def get_non_reserved_positional_parameter_count(self):
        """
        Returns the amount of the non reserved positional parameters of the analyzed callable.
        
        Returns
        -------
        non_reserved_positional_parameters : `int`
        """
        count = 0
        for parameter in self.parameters:
            if not parameter.is_positional():
                break
            
            if parameter.reserved:
                continue
            
            count +=1
            continue
        
        return count
    
    def get_non_reserved_non_default_parameter_count(self):
        """
        Returns the amount of the non reserved non default parameters of the analyzed callable.
        
        Returns
        -------
        non_reserved_non_default_parameter_count : `int`
        """
        count = 0
        for parameter in self.parameters:
            if not parameter.is_positional():
                break
            
            if parameter.reserved:
                continue
            
            if parameter.has_default:
                continue
            
            count +=1
            continue
        
        return count

    def get_non_reserved_positional_parameter_range(self):
        """
        Returns the minimal and the maximal amount how much non reserved positional parameters the analyzed callable
        expects / accepts.
        
        Returns
        -------
        start : `int`
            The minimal amount of non reserved parameters, what the analyzed callable expects.
        end : `int`
            The maximal amount of non reserved parameters, what the analyzed callable accepts.
        
        Notes
        -----
        `*args` parameter is ignored from the calculation.
        """
        iterator = iter(self.parameters)
        start = 0
        for parameter in iterator:
            if not parameter.is_positional():
                return start, start
            
            if parameter.reserved:
                continue
            
            if parameter.has_default:
                break
            
            start += 1
            continue
        
        else:
            return start, start
        
        end = start
        for parameter in iterator:
            if not parameter.is_positional():
                return start, end
            
            if parameter.reserved:
                continue
            
            end += 1
            continue
        
        return start, end
    
    def accepts_args(self):
        """
        Returns whether the analyzed callable accepts `*args` parameter.
        
        Returns
        -------
        accepts_args : `bool`
        """
        return (self.args_parameter is not None)
    
    def accepts_kwargs(self):
        """
        Returns whether the analyzed callable accepts `**kwargs` parameter.
        
        Returns
        -------
        accepts_kwargs : `bool`
        """
        return (self.kwargs_parameter is not None)


class RichAnalyzerParameterAccess:
    """
    Parameter access of a ``RichAnalyzer``.
    
    Attributes
    ----------
    _analyzer : ``CallableAnalyzer``
        Analyzer analyzing the respective function.
    """
    def __new__(cls, analyzer):
        self = object.__new__(cls)
        self._analyzer = analyzer
        return self
    
    def __getattr__(self, attribute_name):
        """
        Tries to find the specified attribute of the respective function.
        
        Returns
        -------
        parameter : ``Parameter``
        
        Raises
        ------
        AttributeError
            - If the parameter by the specified name is nto found.
        """
        for parameter in self.parameters:
            if parameter.name == attribute_name:
                return parameter
        
        raise AttributeError(attribute_name)


class RichAnalyzer:
    """
    Analyzer supporting rich access.
    
    Attributes
    ----------
    _analyzer : ``CallableAnalyzer``
        Analyzer analyzing the respective function.
    """
    def __new__(cls, callable_, as_method=False):
        """
        Analyzes the given callable.
        
        Parameters
        ----------
        callable_ : `callable`
            The callable to analyze.
        as_method : `bool`, Optional
            Whether the given `callable` is given as a `function`, but it should be analyzed as a `method`. Defaults
            to `False`.
        
        Raises
        ------
        TypeError
            If the given object is not callable, or could not be used as probably intended.
        """
        analyzer = CallableAnalyzer(callable_, as_method=as_method)
        
        self = object.__new__(cls)
        self._analyzer = analyzer
        return self
    
    
    @property
    def name(self):
        """
        Returns the name of the analyzed callable.
        
        Returns
        -------
        name : `str`
        """
        return self._analyzer.__name__
    
    
    @property
    def parameters(self):
        """
        Returns parameter access to the 
        Returns
        -------
        parameter_access : RichAnalyzerParameterAccess
        """
        return RichAnalyzerParameterAccess(self._analyzer)
