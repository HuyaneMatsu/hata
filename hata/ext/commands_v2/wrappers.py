__all__ = ('CommandCooldownWrapper', 'CommandCheckWrapper', 'CommandConverterConfigurerWrapper', 'CommandWrapper', )

from ...backend.utils import copy_docs
from ...backend.export import export

from .content_parser import get_detail_for_value, ConverterFlag
from .cooldown import CooldownHandler

class CommandWrapper:
    """
    Command wrapper to add additional functionality to a command after it is created.
    
    Attributes
    ----------
    _wrapped : `Any`
        The wrapped object.
    """
    __slots__ = ('_wrapped',)
    def __new__(cls):
        """
        Creates a partial function to wrap a command.
        
        Subclasses should overwrite this method.
        """
        self = object.__new__(cls)
        self._wrapped = None
        return self
    
    def __call__(self, wrapped):
        """
        Wraps the given command.
        
        Parameters
        ----------
        wrapped : `Any`
            The slash command or other wrapper to wrap.
        
        Returns
        -------
        self : ``CommandWrapper``
        
        Raises
        ------
        RuntimeError
            The wrapper already wrapped something.
        """
        if (self._wrapped is not None):
            raise RuntimeError('The wrapper already wrapped something.')
        
        self._wrapped = wrapped
        return self
    
    def apply(self, command):
        """
        Applies the wrapper's changes on the respective command.
        
        Parameters
        ----------
        command : ``Command``
        """
        pass
    
    def __repr__(self):
        """Returns the command wrapper's representation."""
        return f'<{self.__class__.__name__} wrapped={self._wrapped!r}>'
    
    def fetch_function_and_wrappers_back(self):
        """
        Fetches back the source function and all the wrappers, the returns them.
        
        Returns
        -------
        function : `Any`
            The wrapped function.
        wrappers : `list` of ``CommandWrapper`` instances
            The fetched back wrappers.
        """
        wrappers = [self]
        maybe_wrapper = self._wrapped
        while True:
            if isinstance(maybe_wrapper, CommandWrapper):
                wrappers.append(maybe_wrapper)
                maybe_wrapper = maybe_wrapper._wrapped
            else:
                function = maybe_wrapper
                break
        
        wrappers.reverse()
        return function, wrappers


class CommandConverterConfigurerWrapper(CommandWrapper):
    """
    Command wrapper to modify parameter parsing settings for a specific command.
    
    Attributes
    ----------
    _wrapped : `Any`
        The wrapped object.
    _detail : ``ContentParserParameterDetail``
        Parsing detail example to match and modify of the source command.
    _flags : `None` or ``ConverterFlag``
        New flag to set to the parameter detail if any.
    _modifiers : `None` or `dict` of (`str`, `bool`) items
        Converter flag modifiers.
    """
    __slots__ = ('_detail', '_flags', '_modifiers', )
    
    def __new__(cls, annotation, flags=None, **modifiers):
        """
        Creates a new command wrapper instance for modifying converter flags.
    
        Raises
        ------
        TypeError
            - Modifier values can be `bool` instances.
            - If `annotation` was not given neither as `type` non as `bool` instance.
        ValueError
            - Invalid modifier name.
            - If `annotation`'s type is correct, but there is specified converter for it.
        """
        detail = get_detail_for_value(annotation)
        if (detail is None):
            raise TypeError(f'`annotation` can be given either as `type` or `str` instance, got '
                f'{annotation.__class__.__name__}.')
        
        if (flags is not None) and not isinstance(flags, ConverterFlag):
            if isinstance(flags, int):
                flags = ConverterFlag(flags)
            else:
                raise TypeError(f'`flag` can be given as `None`, `{ConverterFlag.__name__}` or as other `int` '
                    f'instance, got {flags.__class__.__name__}.')
        
        if modifiers:
            for key in modifiers.keys():
                if key not in ConverterFlag.__keys__:
                    raise ValueError(f'Invalid modifier: `{key!r}.')
            
            for key, value in modifiers.items():
                if not isinstance(value, bool):
                    raise TypeError(f'Modifier value can only be given as `bool` instance, got {key!r}={value!r}.')
            
            if (flags is not None):
                flags = flags.update_by_keys(**modifiers)
                modifiers = None
        else:
            modifiers = None
        
        self = object.__new__(cls)
        self._detail = detail
        self._flags = flags
        self._modifiers = modifiers
        self._wrapped = None
        return self
    
    @copy_docs(CommandWrapper.apply)
    def apply(self, command):
        if (self._flags is None) and (self._modifiers is None):
            return
        
        detail_example = self._detail
        command_function = command._command_function
        if (command_function is None):
            return
            
        content_parser = command_function._content_parser
        for parameter in content_parser._parameters:
            for detail in parameter._iter_details():
                if (detail.type is not detail_example.type):
                    continue
                
                if (detail.converter_setting is detail_example.converter_setting):
                    continue
                
                new_flags = self._flags
                if (new_flags is None):
                    new_flags = detail.flags.update_by_keys(**self._modifiers)
                
                detail.flags = new_flags
                continue


@export
class CommandCheckWrapper(CommandWrapper):
    """
    Command wrapper for checks.
    
    Attributes
    ----------
    _wrapped : `Any`
        The wrapped object.
    _check : ``CheckBase`` instance
        Check to add to the respective command.
    """
    __slots__ = ('_check',)
    def __new__(cls, check_type, *args, **kwargs):
        """
        Creates a partial function to wrap a command.
        
        Parameters
        ----------
        check_type : ``CheckBase`` subclass
            The check's type.
        *args : Parameters,
            Additional parameters to pass to the `check_type`'s constructor.
        **kwargs : Keyword parameters
            Additional parameters to pass to the `check_type`'s constructor.
        """
        check = check_type(*args, **kwargs)
        
        self = object.__new__(cls)
        self._check = check
        self._wrapped = None
        return self
    
    @copy_docs(CommandWrapper.apply)
    def apply(self, command):
        command.add_check(self._check)
    
    def __repr__(self):
        """Returns the command wrapper's representation."""
        return f'<{self.__class__.__name__} wrapped={self._wrapped!r} check={self._check!r}>'
    
    def __invert__(self):
        """Inverts the condition of the wrapped checks and returns a new command check wrapper."""
        new = object.__new__(type(self))
        new._check = ~self._check
        new._wrapped = None
        return new
    
    def __or__(self, other):
        """Connects the condition of two wrapped in `or` relation and returns a new command check wrapper."""
        if not isinstance(other, type(self)):
            return NotImplemented
        
        new = object.__new__(type(self))
        new._check = self._check|other._check
        new._wrapped = None
        return new
    
    def __and__(self, other):
        """Connects the condition of two wrapped in `and` relation and returns a new command check wrapper."""
        if not isinstance(other, type(self)):
            return NotImplemented
        
        new = object.__new__(type(self))
        new._check = self._check&other._check
        new._wrapped = None
        return new


class CommandCooldownWrapper(CommandWrapper):
    """
    Command wrapper for checks.
    
    Attributes
    ----------
    _wrapped : `Any`
        The wrapped object.
    _cooldown_handler : ``CooldownHandler``
        Cooldown to add to the respective command.
    """
    __slots__ = ('_cooldown_handler', )
    
    def __new__(cls, *args, **kwargs):
        """
        Creates a partial function to wrap a command.
        
        Parameters
        ----------
        *args : Parameters
            Parameters to pass to the `CooldownHandler`'s constructor.
        **kwargs : Keyword parameters
            Parameters to pass to the `CooldownHandler`'s constructor.
        
        Other Parameters
        ----------------
        for_ : `str`
            By what type of entity the cooldown should limit the command.
            
            Possible values:
             - `'user'`
             - `'channel'`
             - `'guild'`
         
        reset : `float`
            The reset time of the cooldown.
        
        limit : `int`
            The amount of calls after the respective command goes on cooldown.
        
        weight : `int`, Optional
            The weight of one call. Defaults to `1`.
        
        Raises
        ------
        TypeError
            - If `str` is not given as `str` instance.
            - If `weight` is not numeric convertable to `int`.
            - If `reset` is not numeric convertable to `float`.
            - If `limit` is not numeric convertable to `int`.
        ValueError
            - If `for_` is not given as any of the expected value.
        """
        cooldown_handler = CooldownHandler(*args, **kwargs)
        
        self = object.__new__(cls)
        self._cooldown_handler = cooldown_handler
        self._wrapped = None
        
        return self
    
    
    @copy_docs(CommandWrapper.apply)
    def apply(self, command):
        command.add_wrapper(self._cooldown_handler)
