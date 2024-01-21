__all__ = ()

from .base import DiscordGatewayBase


class DiscordGatewayVoiceBase(DiscordGatewayBase):
    """
    Base gateway for voice clients.
    """
    __slots__ = ()
    
    async def set_speaking(self, speaking):
        """
        Sends a `speaking` packet.
        
        This method is a coroutine.
        
        Parameters
        ----------
        speaking : `bool`
            Whether the voice voice client should show up as speaking and be able to send voice data or not.
        """
        pass
    
    
    async def run(self, waiter = None):
        """
        Keeps the gateway receiving message and processing it. If the gateway needs to be reconnected, reconnects
        itself. If connecting cannot succeed, because there is no internet returns `False`. If the `.voice_client` is
        disconnected, then returns `False`.
        
        This method is a coroutine.
        
        Parameters
        -----------
        waiter : `None | Future<bool>` = `None`, Optional
            A waiter future what is set, when the gateway finished connecting and started polling events.
            Its result is also set in case the task is finished before connection.
        
        Returns
        -------
        outcome : `bool<False>`
            Always `False`.
        """
        if (waiter is not None):
            waiter.set_result_if_pending(False)
            waiter = None
        
        return False
