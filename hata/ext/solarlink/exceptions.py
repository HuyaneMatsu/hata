__all__ = ('SolarAuthenticationError', 'SolarException', )

class SolarException(Exception):
    """
    Base class for solar client exceptions.
    """

class SolarAuthenticationError(SolarException):
    """
    Raises when the client could not authorize itself a lavalink node.
    
    Attributes
    ----------
    node : ``SolarNode``
        The node we tried to connect to.
    response : ``ClientResponse``
        The http response received from the node.
    """
    def __init__(self, node, response):
        self.node = node
        self.response = response
        Exception.__init__(self, node, response)
    
    def __repr__(self):
        """Returns the exception's representation."""
        return f'<{self.__class__.__name__} node={self.node!r}, response={self.response!r}>'
