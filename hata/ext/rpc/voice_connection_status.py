__all__ = ('VoiceConnectionStatus',)

from .preinstanced import VoiceConnectionState


class VoiceConnectionStatus:
    """
    Called when the client's voice connection status changes.
    
    Attributes
    ----------
    average_ping : `float`
        Average ping in seconds.
    hostname : `str`
        The hostname of the connected voice server.
    last_ping : `float`
        Lats ping in seconds.
    pings : `tuple` of `float`
        The last up to 20 pings in seconds
    state : ``VoiceConnectionState``
        THe voice connections state.
    """
    __slots__ = ('average_ping', 'hostname', 'last_ping', 'pings', 'state')
    
    def __repr__(self):
        """Returns the voice connection state's representation."""
        return f'<{self.__class__.__name__} state={self.state.name}>'
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a nw voice connection status instance from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Voice connections status data.
        
        Returns
        -------
        self : ``VoiceConnectionStatus``
        """
        self = object.__new__(cls)
        self.state = VoiceConnectionState.get(data['state'])
        self.hostname = data['hostname']
        self.pings = tuple(ping * 0.001 for ping in data['pings'])
        self.average_ping = data['average_ping']*0.001
        self.last_ping = data['last_ping']*0.001
        return self
