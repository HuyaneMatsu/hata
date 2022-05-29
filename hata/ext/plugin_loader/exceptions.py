__all__ = ('PluginError', )


class PluginError(Exception):
    """
    An exception raised by the ``PluginLoader``, if loading, reloading or unloading an plugin fails with any
    reason.
    
    Attributes
    ----------
    _message : `str`, `list` of `str`
        The error's message.
    """
    
    def __init__(self, message):
        """
        Creates a new plugin error.
        
        Parameters
        ----------
        message : `str`, `list` of `str`
            The error's message.
        """
        self._message = message
    
    
    @property
    def message(self):
        """
        Returns the plugin error's message.
        
        If the plugin error contains more message,s connects them.
        
        Returns
        -------
        message : ``Message``
        """
        message = self._message
        if isinstance(message, str):
            return message
        
        return '\n\n'.join(message)
    
    
    @property
    def messages(self):
        """
        Returns a list containing the exception error's messages.
        
        Returns
        -------
        messages : `list` of `str`
        """
        message = self._message
        if isinstance(message, str):
           return [message]
        
        return message
    
    
    def __len__(self):
        """Returns the amount of messages, what the plugin error contains."""
        message = self._message
        if isinstance(message, str):
            return 1
        
        return len(message)
    
    
    def __repr__(self):
        """Returns the exception error's representation."""
        return f'{self.__class__.__name__} ({len(self)}):\n{self.message}\n'
    
    
    __str__ = __repr__


class DoNotLoadPlugin(BaseException):
    """
    Raised to stop an plugin loaded without error.
    """
