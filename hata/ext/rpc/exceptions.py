__all__ = ('DiscordRPCError', )

class DiscordRPCError(BaseException):
    """
    Discord RPC error code.
    
    Attributes
    ----------
    code : `int`
        Discord RPC error code.
    message : `str`
        Discord RPC error message.
    """
    def __init__(self, code, message):
        """
        Creates a new Discord RPC error instance with the given parameters.
        
        Parameters
        ----------
        code : `int`
            Discord RPC error code.
        message : `str`
            Discord RPC error message.
            
        """
        self.code = code
        self.message = message
        BaseException.__init__(self, code, message)
    
    def __repr__(self):
        """Returns the representation of the error code."""
        return f'{self.__class__.__name__}: [{self.code}] {self.message!r}'
