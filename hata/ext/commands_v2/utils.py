# -*- coding: utf-8 -*-
from functools import partial as partial_func

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
        
        Returns
        -------
        wrapper : `functools.partial` of ``CommandWrapper._decorate``
            Partial function to wrap a command.
        """
        return partial_func(cls._decorate, cls)
    
    def _decorate(cls, wrapped):
        """
        Wraps the given command.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        wrapped : `Any`
            The slash command or other wrapper to wrap.
        
        Returns
        -------
        self : ``CommandWrapper``
            The created instance.
        """
        self = object.__new__(cls)
        self._wrapped = wrapped
        return self
    
    def apply(self, command):
        """
        Applies the wrapper's changes on the respective command.
        
        Subclasses should overwrite this method.
        
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
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        check_type : ``CheckBase`` subclass
            The check's type.
        *args : Arguments, Optional
            Additional parameters to pass to the `check_type`'s constructor.
        **kwargs : Keyword arguments, Optional
            Additional parameters to pass to the `check_type`'s constructor.
        
        Returns
        -------
        wrapper : `functools.partial` of ``CommandWrapper._decorate``
            Partial function to wrap a command.
        """
        check = check_type(*args, **kwargs)
        return partial_func(cls._decorate, cls, check)

    def _decorate(cls, check, wrapped):
        """
        Wraps the given command.
        
        Sub-classes should overwrite this method.
        
        Parameters
        ----------
        check : ``CheckBase`` instance
            The check's type.
        wrapped : `Any`
            The slash command or other wrapper to wrap.
        
        Returns
        -------
        self : ``CommandWrapper``
            The created instance.
        """
        self = object.__new__(cls)
        self._check = check
        self._wrapped = wrapped
        return self
    
    def apply(self, command):
        """
        Applies the wrapper's changes on the respective command.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        command : ``Command``
        """
        command.add_check(self._check)
    
    def __repr__(self):
        """Returns the command wrapper's representation."""
        return f'<{self.__class__.__name__} wrapped={self._wrapped!r} check={self._check!r}>'
