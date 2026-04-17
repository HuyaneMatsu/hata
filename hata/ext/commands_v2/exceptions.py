__all__ = ('CommandCheckError', 'CommandCooldownError', 'CommandParameterParsingError', 'CommandProcessingError', )

class CommandProcessingError(BaseException):
    """
    Exception raised when a command's processing failed.
    
    This is a superclass for various exceptions types raised around the table.
    """


class CommandParameterParsingError(CommandProcessingError):
    """
    Raised when a required parameter could not be parsed.
    
    Attributes
    ----------
    content_parser_parameter : ``ContentParserParameter``
        The unfulfilled parameter.
    """
    def __init__(self, content_parser_parameter):
        """
        Creates a new ``CommandParameterParsingError``.
        
        Parameters
        ----------
        content_parser_parameter : ``ContentParserParameter``
            The unfulfilled parameter.
        """
        self.content_parser_parameter = content_parser_parameter
        CommandProcessingError.__init__(self, content_parser_parameter)


class CommandCheckError(CommandProcessingError):
    """
    Raised when a check fails.
    
    Attributes
    ----------
    check : ``CheckBase``
        The failed check.
    """
    def __init__(self, check):
        """
        Creates a new ``CommandCheckError``.
        
        Parameters
        ----------
        check : ``ContentParserParameter``
            The failed check.
        """
        self.check = check
        CommandProcessingError.__init__(self, check)


class CommandCooldownError(CommandProcessingError):
    """
    Raised when the command is on cooldown.
    
    Attributes
    ----------
    expires_after : `float`
        After how much time the cooldown expires.
        
        If a prerequisite didn't pass, may be `-1.0`.
    
    cooldown_handler : ``CooldownHandler``
        The respective cooldown handler which is on cooldown.
    """
    def __init__(self, cooldown_handler, expires_after):
        """
        Creates a new ``CommandCheckError``.
        
        Parameters
        ----------
        cooldown_handler : ``CooldownHandler``
            The respective cooldown handler which is on cooldown.
        expires_after : `float`
            After how much time the cooldown expires.
            
            If a prerequisite didn't pass, may be `-1.0`.
        """
        self.cooldown_handler = cooldown_handler
        self.expires_after = expires_after
        CommandProcessingError.__init__(self, cooldown_handler, expires_after)
