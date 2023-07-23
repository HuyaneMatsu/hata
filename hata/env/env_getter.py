__all__ = ('EnvGetter',)

from warnings import warn

from scarletio import RichAttributeErrorBaseType

from .getters import (
    RETURN_TYPE_EXCEPTION, RETURN_TYPE_VALUE, RETURN_TYPE_WARNING, _get_env, _handle_get_env_generator,
    _process_bool_env, _process_int_env, _process_str_env
)


class EnvGetter(RichAttributeErrorBaseType):
    """
    Env variable getter that can be used to aggregate error messages.
    
    Attributes
    ----------
    _captured : `None, `list<(int, str)>`
        Captured errors.
    _entered : `int`
        Whether the getter is entered as a context manager. If not, it will propagate the errors instantly.
    
    Examples
    --------
    ```py
    with EnvGetter() as env:
        KOISHI_TOKEN = env.get_str('KOISHI_TOKEN')
        SATORI_TOKEN = env.get_str('SATORI_TOKEN')
    """
    __slots__ = ('_captured', '_entered')
    
    def __new__(cls):
        """
        Creates a new env getter instance.
        
        Env getter can be used to aggregate error messages.
        """
        self = object.__new__(cls)
        self._captured = None
        self._entered = 0
        return self
    
    
    def __repr__(self):
        """Returns the env getter's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        if self._entered:
            repr_parts.append(' entered')
            
            field_added = True
        else:
            field_added = False
        
        captured = self._captured
        if (captured is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' captured = ')
            repr_parts.append(repr(captured))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __enter__(self):
        """Enters the context manager."""
        self._entered += 1
        return self
    
    
    def __exit__(self, exception_type, exception, exception_traceback):
        """
        Exits the context manager.
        
        Parameters
        ----------
        exception_type : `None`, `type<BaseException>`
            The occurred exception's type if any.
        exception : `None`, `BaseException`
            The occurred exception if any.
        exception_traceback : `None`, `TracebackType`
            the exception's traceback if any.
        
        Returns
        -------
        captured : `bool`
            Whether the exception was captured.
        """
        entered = self._entered - 1
        self._entered = entered
        
        if entered:
            return False
        
        error_type, error_message = self._get_aggregated_state()
        self._captured = None
        
        if error_type == RETURN_TYPE_WARNING:
            warn(error_message, stacklevel = 2)
        elif error_type == RETURN_TYPE_EXCEPTION:
            raise RuntimeError(error_message)
        
        return False
    
    
    def get_bool(self, name, default = False, *, raise_if_missing_or_empty = False, warn_if_empty = True):
        """
        Gets the given environmental variable.
        
        If the environmental variable is not present or not present as a boolean's representation returns `default`
        instead.
        
        Parameters
        ----------
        name : `str`
            The name of an environmental variable.
        default : `bool` = `False`, Optional
            The default value of the respective variable.
        raise_if_missing_or_empty : `bool` = `False`, Optional (Keyword only)
            Whether exception should be thrown if the environmental variable is missing or empty.
            Has priority over `default` and `warn_if_empty`.
        warn_if_empty : `bool` = `True`, Optional (Keyword only)
            Whether warning should be dropped if empty environmental variable is received.
        
        Returns
        -------
        variable : `bool`
        """
        return self._handle(
            _get_env(name, default, 'bool', _process_bool_env, raise_if_missing_or_empty, warn_if_empty), default
        )

    
    def get_str(self, name, default = False, *, raise_if_missing_or_empty = False, warn_if_empty = True):
        """
        Gets the given environmental variable.
        
        If the environmental variable is not present or present as an empty string returns `default` instead.
        
        Parameters
        ----------
        name : `str`
            The name of an environmental variable.
        default : `None` | `str` = `None`, Optional
            The default value of the respective variable. Defaults to `None`.
        raise_if_missing_or_empty : `bool` = `False`, Optional (Keyword only)
            Whether exception should be thrown if the environmental variable is missing or empty.
            Has priority over `default` and `warn_if_empty`.
        warn_if_empty : `bool` = `True`, Optional (Keyword only)
            Whether warning should be dropped if empty environmental variable is received.
            
        Returns
        -------
        variable : `bool`
        """
        return self._handle(
            _get_env(name, default, 'str', _process_str_env, raise_if_missing_or_empty, warn_if_empty), default
        )
    
    
    def get_int(self, name, default = 0, *, raise_if_missing_or_empty = False, warn_if_empty = True):
        """
        Gets the given environmental variable.
        
        If the environmental variable is not present or present as non `int`, will return `default` instead.
        
        Parameters
        ----------
        name : `str`
            The name of an environmental variable.
        default : `int` = `0`, Optional
            The default value of the respective variable.
        raise_if_missing_or_empty : `bool` = `False`, Optional (Keyword only)
            Whether exception should be thrown if the environmental variable is missing or empty.
            Has priority over `default` and `warn_if_empty`.
        warn_if_empty : `bool` = `True`, Optional (Keyword only)
            Whether warning should be dropped if empty environmental variable is received.
        
        Returns
        -------
        variable : `int`
        """
        return self._handle(
            _get_env(name, default, 'int', _process_int_env, raise_if_missing_or_empty, warn_if_empty), default
        )
    
    
    def _handle(self, generator, default):
        """
        Handles a ``_get_env`` generator.
        
        Parameters
        ----------
        generator : `iterable<(int, object)>`
            Generator to iterate over.
        default : `object`
            Default to return in case we are capturing the errors & warnings.
        
        Returns
        -------
        value : `object`
        
        Raises
        ------
        RuntimeError
        """
        if not self._entered:
            return _handle_get_env_generator(generator)
        
        return self._handle_as_entered(generator, default)
    
    
    def _handle_as_entered(self, generator, default):
        """
        Handles a ``_get_env`` generator as capturing its errors & warnings.
        
        Parameters
        ----------
        generator : `iterable<(int, object)>`
            Generator to iterate over.
        default : `object`
            Default to return in case we are capturing the errors & warnings.
        
        Returns
        -------
        value : `object`
        """
        for return_type, return_value in generator:
            if return_type == RETURN_TYPE_VALUE:
                return return_value
            
            self._capture(return_type, return_value)
        
        return default
    
    
    def _capture(self, return_type, return_value):
        """
        Captures an error / warning output.
        
        Parameters
        ----------
        return_type : `int`
            The type of the error.
        error_message : `str`
            Error message to capture.
        """
        captured = self._captured
        if captured is None:
            captured = []
            self._captured = captured
        
        captured.append((return_type, return_value))
    
    
    def _get_aggregated_state(self):
        """
        Gets the aggregated state of the captured errors.
        
        Returns
        -------
        error_type : `int`
        error_message : `None`, `str`
        """
        captured = self._captured
        if captured is None:
            return RETURN_TYPE_VALUE, None
        
        warning_messages = None
        exception_messages = None
        
        for return_type, return_value in captured:
            if return_type == RETURN_TYPE_WARNING:
                if warning_messages is None:
                    warning_messages = []
                
                warning_messages.append(return_value)
            
            else:
                if exception_messages is None:
                    exception_messages = []
                
                exception_messages.append(return_value)
        
        if warning_messages is None:
            if exception_messages is None:
                # should never happen
                error_type = RETURN_TYPE_VALUE
                error_message = None
            
            else:
                error_type = RETURN_TYPE_EXCEPTION
                if len(exception_messages) == 1:
                    error_message = exception_messages[0]
                
                else:
                    error_message = _build_error_message_single_source(exception_messages, 'exceptions')
        
        else:
            if exception_messages is None:
                error_type = RETURN_TYPE_WARNING
                
                if len(warning_messages) == 1:
                    error_message = warning_messages[0]
                
                else:
                    error_message =  _build_error_message_single_source(warning_messages, 'warnings')
            
            else:
                error_type = RETURN_TYPE_EXCEPTION
                error_message = _build_error_message_all_sources(exception_messages, warning_messages)
                

        return error_type, error_message


def _build_error_message_single_source(messages, source):
    """
    Builds error message for a single source.
    
    Parameters
    ----------
    messages : `list<str>`
        Collection of error messages.
    source : `str`
        The source of the error messages.
    
    Returns
    -------
    message : `str`
    """
    message_parts = ['Occurred ', source, ' while getting environmental variables (', str(len(messages)), '):']
    
    for message in messages:
        message_parts.append('\n')
        message_parts.append(message)
    
    return ''.join(message_parts)


def _build_error_message_all_sources(exception_messages, warning_messages):
    """
    Builds error message for a single source.
    
    Parameters
    ----------
    exception_messages : `list<str>`
        Collection of exception messages.
    warning_messages : `list<str>`
        Collection of warning messages.
    
    Returns
    -------
    message : `str`
    """
    message_parts = ['Occurred exceptions while getting environmental variables (', str(len(exception_messages)), '):']
    
    for message in exception_messages:
        message_parts.append('\n')
        message_parts.append(message)
    
    message_parts.append('\n\nAdditional warnings (')
    message_parts.append(str(len(warning_messages)))
    message_parts.append('):')
    
    for message in warning_messages:
        message_parts.append('\n')
        message_parts.append(message)
    
    return ''.join(message_parts)
