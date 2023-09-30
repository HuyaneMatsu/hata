__all__ = ()

from datetime import datetime as DateTime

from scarletio import Compound

from ...channel import Channel
from ...http import DiscordHTTPClient
from ...oauth2 import Connection
from ...payload_building import add_payload_fields_from_keyword_parameters
from ...user.guild_profile.utils import GUILD_PROFILE_SELF_FIELD_CONVERTERS
from ...user.user.utils import USER_SELF_FIELD_CONVERTERS
from ...utils import datetime_to_timestamp

from ..request_helpers import get_guild_id, get_channel_guild_id_and_id


class ClientCompoundClientEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    
    async def edit(self, **keyword_parameters):
        """
        Edits the client. Only the provided parameters will be changed. Every parameter what refers to a user
        account is not tested.
        
        This method is a coroutine.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Additional keyword parameters representing which field of the client should be edited.
        
        Other Parameters
        ----------------
        avatar : `None`, `bytes-like`, Optional (Keyword only)
            An `'jpg'`, `'png'`, `'webp'` image's raw data. If the client is premium account, then it can be
            `'gif'` as well. By passing `None` you can remove the client's current avatar.
        
        banner : `None`, `bytes-like`, Optional (Keyword only)
            An `'jpg'`, `'png'`, `'webp'`, 'gif'` image's raw data. By passing `None` you can remove the client's
            current avatar.
        
        banner_color : `None`, ``Color``, `int`, Optional (Keyword only)
            The new banner color of the client. By passing it as `None` you can remove the client's current one.
        
        display_name : `None`, `str`, Optional (Keyword only)
            The client's non-unique display name.
        
        name : `str`, Optional (Keyword only)
            The client's new name.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        The method's endpoint has long rate limit reset, so consider using timeout and checking rate limits with
        ``RateLimitProxy``.
        """
        data = {}
        add_payload_fields_from_keyword_parameters(USER_SELF_FIELD_CONVERTERS, keyword_parameters, data, True)
        
        if data:
            await self.http.client_edit(data)
    
    
    async def guild_profile_edit(self, guild, *, reason = None, **keyword_parameters):
        """
        Edits the client guild profile in the given guild. Nick and guild specific avatars can be edited on this way.
        
        An extra `reason` is accepted as well, which will show up at the respective guild's audit logs.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : `None`, `int`, ``Guild``
            The guild where the client's nickname will be changed. If `guild` is given as `None`, then the function
            returns instantly.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters representing which field of the guild profile should be edited.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the respective guild's audit logs.
        
        Other Parameters
        ----------------
        nick : `None`, `str`, Optional (Keyword only)
            The client's new nickname. Pass it as `None` to remove it. Empty strings are interpreted as `None`.
        
        avatar : `None`, `bytes-like`, Optional (Keyword only)
            The client's new guild specific avatar.
            
            Can be a `'jpg'`, `'png'`, `'webp'` image's raw data. If the client is premium account, then it can be
            `'gif'` as well. By passing `None` you can remove the client's current avatar.
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        data = {}
        add_payload_fields_from_keyword_parameters(GUILD_PROFILE_SELF_FIELD_CONVERTERS, keyword_parameters, data, True)
        
        if data:
            await self.http.client_guild_profile_edit(guild_id, data, reason)
    
    
    async def connection_get_all(self):
        """
        Requests the client's connections.
        
        This method is a coroutine.
        
        Returns
        -------
        connections : `list` of ``Connection`` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        For a bot account this request will always return an empty list.
        """
        data = await self.http.client_connection_get_all()
        return [Connection.from_data(connection_data) for connection_data in data]
    
    
    async def guild_leave(self, guild):
        """
        The client leaves the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild from where the client will leave.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        await self.http.guild_leave(guild_id)


    async def join_speakers(self, channel, *, request = False):
        """
        Request to speak or joins the client as a speaker inside of a stage channel. The client must be in the stage
        channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``
            The stage channel to join.
        request : `bool` = `False`, Optional (Keyword only)
            Whether the client should only request to speak.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor as `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_guild_stage)
        
        if request:
            timestamp = datetime_to_timestamp(DateTime.utcnow())
        else:
            timestamp = None
        
        data = {
            'suppress': False,
            'request_to_speak_timestamp': timestamp,
            'channel_id': channel_id
        }
        
        await self.http.voice_state_client_edit(guild_id, data)
    
    
    async def join_audience(self, channel):
        """
        Moves the client to the audience inside of the stage channel. The client must be in the stage channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `tuple` (`int`, `int`)
            The stage channel to join.
        
        Raises
        ------
        RuntimeError
            If `channel` is partial.
        TypeError
            If `channel` was not given neither as ``Channel`` nor as `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_guild_stage)
        
        data = {
            'suppress': True,
            'channel_id': channel_id
        }
        
        await self.http.voice_state_client_edit(guild_id, data)
