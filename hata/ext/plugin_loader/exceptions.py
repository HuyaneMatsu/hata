__all__ = ('PluginError', )

from scarletio import CauseGroup


class PluginError(Exception):
    """
    An exception raised by the ``PluginLoader``, if loading, reloading or unloading an plugin fails with any
    reason.
    
    Attributes
    ----------
    _message : `None`, `str`
        The error's message.
    """
    
    def __init__(self, message = None, *, cause = None):
        """
        Creates a new plugin error.
        
        Parameters
        ----------
        message : `None`, `str` = `None`, Optional
            The error's message.
        
        cause : `None`, `BaseException` = `None`, Optional (Keyword only)
            Exception cause to apply manually.
        """
        self._message = message
        
        if message is None:
            Exception.__init__(self)
        else:
            Exception.__init__(self, message)
        
        if (cause is not None):
            self.__cause__ = cause
    
    
    @property
    def message(self):
        """
        Returns the plugin error's message.
        
        If the plugin error contains more messages connects them.
        
        Returns
        -------
        message : ``Message``
        """
        return '\n\n'.join(self.messages)
    
    
    @property
    def messages(self):
        """
        Returns a list containing the exception error's messages.
        
        Returns
        -------
        messages : `list` of `str`
        """
        messages = []
        
        message = self._message
        if (message is not None):
            messages.append(message)
        
        cause = self.__cause__
        if (cause is not None):
            if isinstance(cause, CauseGroup):
                for cause in cause:
                    messages.append(repr(cause))
            
            else:
                messages.append(repr(cause))
        
        return messages
    
    
    def __len__(self):
        """Returns the amount of messages, what the plugin error contains."""
        length = 0
        
        if (self._message is not None):
            length += 1

        cause = self.__cause__
        if (cause is not None):
            if isinstance(cause, CauseGroup):
                length += len(cause)
            
            else:
                length += 1
        
        return length
    
    
    def __repr__(self):
        """Returns the exception error's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        message = self._message
        if (message is not None):
            repr_parts.append(' message=')
            repr_parts.append(repr(message))
        
        cause = self.__cause__
        if (cause is not None):
            if isinstance(cause, CauseGroup):
                cause_count = len(cause)
            
            else:
                cause_count = 1
            
            repr_parts.append(' with ')
            repr_parts.append(repr(cause_count))
            repr_parts.append(' cause')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    __str__ = __repr__


class DoNotLoadPlugin(BaseException):
    """
    Raised to stop an plugin loaded without error.
    """
