__all__ = ('ExtensionError', )


class ExtensionError(Exception):
    """
    An exception raised by the ``ExtensionLoader``, if loading, reloading or unloading an extension fails with any
    reason.
    
    Attributes
    ----------
    _message : `str` or `list` of `str`
        The error's message.
    """
    
    def __init__(self, message):
        """
        Creates a new extension error.
        
        Parameters
        ----------
        message : `str` or `list` of `str`
            The error's message.
        """
        self._message = message
    
    @property
    def message(self):
        """
        Returns the extension error's message.
        
        If the extension error contains more message,s connects them.
        
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
        """Returns the amount of messages, what the extension error contains."""
        message = self._message
        if isinstance(message, str):
            return 1
        
        return len(message)
    
    def __repr__(self):
        """Returns the exception error's representation."""
        return f'{self.__class__.__name__} ({len(self)}):\n{self.message}\n'
    
    __str__ = __repr__


class DoNotLoadExtension(BaseException):
    """
    Raised to stop an extension loaded without error.
    """
