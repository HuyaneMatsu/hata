__all__ = ('TopGGHttpException', 'TopGGGloballyRateLimited',)

import reprlib

from .constants import JSON_KEY_EXCEPTION_MESSAGE


class TopGGGloballyRateLimited(Exception):
    """
    response : ``ClientResponse``, `None`
        Response from top.gg if received as a response.
    """
    def __init__(self, response):
        """
        Creates a new top.gg http exception instance.
        
        Parameters
        ----------
        response : ``ClientResponse``, `None`
            Response from top.gg if received as a response.
        """
        self.response = response
        Exception.__init__(self, response)


class TopGGHttpException(Exception):
    """
    Http exception raised by Top.gg.
    
    Attributes
    ----------
    response : ``ClientResponse``
        Response from top.gg.
    message : `str`
        Exception message.
    """
    def __init__(self, response, response_data):
        """
        Creates a new top.gg http exception instance.
        
        Parameters
        ----------
        response : ``ClientResponse``
            Response from top.gg.
        response_data : `str`, `dict` of (`str`, `Any`) items
            Response data.
        """
        if isinstance(response_data, str):
            message = response_data
        elif isinstance(response_data, dict):
            message = response_data.get(JSON_KEY_EXCEPTION_MESSAGE, '')
        else:
            message = ''
        
        self.message = message
        self.response = response
        
        Exception.__init__(self, response, response_data)
    
    
    @property
    def status(self):
        """
        Returns the response's status code.
        
        Returns
        -------
        status_code : `int`
        """
        return self.response.status
    
    
    def __repr__(self):
        """Returns the exception's representation."""
        repr_parts = ['<', self.__class__.__name__, ' status=', str(self.response.status)]
        
        
        message = self.message
        if message:
            repr_parts.append(', message=')
            repr_parts.append(reprlib.repr(message))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
