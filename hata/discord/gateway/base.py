__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .constants import LATENCY_DEFAULT


class DiscordGatewayBase(RichAttributeErrorBaseType):
    """
    Base type for gateways used by ``Client``-s to communicate with Discord with web socket.
    """
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new gateway
        """
        return object.__new__(cls)
    
    
    def __repr__(self):
        """Returns the gateway's representation."""
        repr_parts = ['<', type(self).__name__]
        self._put_repr_parts_into(repr_parts)
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def _put_repr_parts_into(self, repr_parts):
        """
        Helper method to extend `repr_parts` with type specific fields.
        """
        pass
    
    
    async def run(self):
        """
        Keeps the gateway receiving message and processing it. If the gateway needs to be reconnected, reconnects
        itself. If connecting cannot succeed, because there is no internet returns `True`. If the `.client` is
        stopped, then returns `False`.
        
        If `True` is returned the respective client stops all other gateways as well and tries to reconnect. When
        the internet is back the client will launch back the gateway.
        
        This method is a coroutine.
        
        Returns
        -------
        outcome : `bool<False>`
            Always `False`.
        
        Raises
        ------
        DiscordGatewayException
            The client tries to connect with bad or not acceptable intent or shard value.
        DiscordException
        """
        raise NotImplementedError
    
    
    @property
    def latency(self):
        """
        The latency of the web socket in seconds.
        If no latency is recorded will return the default latency.
        
        Returns
        -------
        latency : `float`
        """
        return LATENCY_DEFAULT

    
    async def terminate(self):
        """
        Terminates the gateway's beating and closes it's web socket with close code of `4000`.
        
        This method is a coroutine.
        """
        pass
    
    
    async def close(self):
        """
        Cancels the gateway's heartbeat and closes it's web socket with close code of `1000`.
        
        This method is a coroutine.
        """
        pass
    
    
    def abort(self):
        """
        Abort the gateway immediately.
        """
        pass
    
    
    async def send_as_json(self, data):
        """
        Sends the data as json to Discord on the gateway's web socket.
        If there is no web socket, or the web socket is closed will not raise.
        
        This method is a coroutine.
        
        Parameters
        ----------
        data : `object`
            The data to send.
        """
        pass
    
    
    async def beat(self):
        """
        Sends a heartbeat packet to Discord.
        
        This method is a coroutine.
        """
        pass
