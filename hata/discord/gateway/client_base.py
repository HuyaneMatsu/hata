__all__ = ()

from .base import DiscordGatewayBase


class DiscordGatewayClientBase(DiscordGatewayBase):
    """
    Base gateway for clients.
    """
    __slots__ = ()
    
    async def change_voice_state(self, guild_id, channel_id, *, self_deaf = False, self_mute = False):
        """
        Sends a `VOICE_STATE` packet to Discord.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild_id : `int`
            The voice client's guild's id.
        channel_id : `int`
            The voice client's channel's id.
        self_deaf : `bool` = `False`, Optional (Keyword only)
            Whether the voice client is deafen.
        self_mute : `bool` = `False`, Optional (Keyword only)
            Whether the voice client is muted.
        """
        pass
    
    
    def get_gateway(self, guild_id):
        """
        Returns the gateway for the given `guild_id`.
        
        Parameters
        ----------
        guild_id : `int`
            The guild's identifier to get the gateway for. Can be `0`.
        
        Returns
        -------
        gateway : ``DiscordGatewayClientBase``
        """
        return self
