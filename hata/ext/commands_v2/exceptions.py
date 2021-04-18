# -*- coding: utf-8 -*-
__all__ = ('CommandCheckError', 'CommandParameterParsingError', 'CommandProcessingError', )

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
        Creates a new ``CommandParameterParsingError`` instance.
        
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
        Creates a new ``CommandCheckError`` instance.
        
        Parameters
        ----------
        check : ``ContentParserParameter``
            The failed check.
        """
        self.check = check
        CommandProcessingError.__init__(self, check)


