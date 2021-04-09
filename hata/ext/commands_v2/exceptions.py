# -*- coding: utf-8 -*-
__all__ = ('CommandParameterParsingError', 'CommandProcessingError', )

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
