# -*- coding: utf-8 -*-
__all__ = ('CommandWrapper', 'CommandCheckWrapper', )

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
        *args : Arguments,
            Additional parameters to pass to the `check_type`'s constructor.
        **kwargs : Keyword arguments
            Additional parameters to pass to the `check_type`'s constructor.
        """
        check = check_type(*args, **kwargs)
        
        self = object.__new__(cls)
        self._check = check
        self._wrapped = None
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


def raw_name_to_display(raw_name):
    """
    Converts the given raw command or it's parameter's name to it's display name
    
    Parameters
    ----------
    raw_name : `str`
        The name to convert.
    
    Returns
    -------
    display_name : `str`
        The converted name.
    """
    return '-'.join([w for w in raw_name.strip('_ ').lower().replace(' ', '-').replace('_', '-').split('-') if w])
