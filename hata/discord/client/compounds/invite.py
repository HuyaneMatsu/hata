__all__ = ()

from scarletio import Compound

from ...bases import maybe_snowflake
from ...channel import Channel
from ...exceptions import DiscordException, ERROR_CODES
from ...guild import Guild
from ...http import DiscordApiClient
from ...invite import Invite
from ...invite.invite.fields import validate_code
from ...invite.invite.utils import INVITE_GUILD_FIELD_CONVERTERS
from ...payload_building import build_create_payload
from ...permission.permission import PERMISSION_MASK_CREATE_INSTANT_INVITE

from ..request_helpers import get_channel_id, get_guild_and_id, get_guild_id


def _iter_channels_in_preference_order(guild):
    """
    Iterates over a guild's channel in order of preference.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to iterate its channels of.
    
    Yields
    ------
    channel : ``Channel``
    """
    channel = guild.rules_channel
    if (channel is not None):
        yield channel 
    
    channel = guild.system_channel
    if (channel is not None):
        yield channel
    
    channel = guild.widget_channel
    if (channel is not None):
        yield channel
    
    for channel in guild.channel_list_flattened:
        if channel.is_in_group_invitable():
            yield channel


def _get_preferred_channel_for_invite(client, guild):
    """
    Gets the preferred channel to create invite for.
    
    Parameters
    ----------
    client : ``Client``
        The client who is getting the channel.
    guild : ``Guild``
        The guild to get the channel of.
    
    Returns
    -------
    channel : `None`, ``Channel``
    """
    for channel in _iter_channels_in_preference_order(guild):
        if channel.cached_permissions_for(client) & PERMISSION_MASK_CREATE_INSTANT_INVITE:
            return channel


class ClientCompoundInviteEndpoints(Compound):
    
    api : DiscordApiClient
    
    
    async def invite_get_vanity(self, guild):
        """
        Returns the vanity invite of the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's invite will be returned.
        
        Returns
        -------
        invite : `None`, ``Invite``
            The vanity invite of the `guild`, `None` if it has no vanity invite.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        invite_data_vanity = await self.api.invite_get_vanity(guild_id)
        invite_data = await self.api.invite_get(invite_data_vanity['code'], {'with_counts': True})
        invite_data['uses'] = invite_data_vanity.get('uses', None)
        return Invite.from_data(invite_data)
    
    
    async def invite_edit_vanity(self, guild, vanity_code, *, reason = None):
        """
        Edits the given guild's vanity invite's code.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild, what's invite will be edited.
        vanity_code : `str`
            The new code of the guild's vanity invite.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `vanity_code` was not given as `str`.
        """
        guild_id = get_guild_id(guild)
        
        vanity_code = validate_code(vanity_code)
        
        await self.api.invite_edit_vanity(guild_id, {'code': vanity_code}, reason)
    
    
    async def invite_create(self, channel, invite_template = None, **keyword_parameters):
        """
        Creates an invite at the given channel with the given parameters.
        
        To create stream invite pass the `target_type` parameter as `InviteTargetTypes.stream` and use
        either the `target_user` or `target_user_id` to define the streamer.
        
        To create an embedded application invite pass the `target_type` parameter as
        `InviteTargetTypes.embedded_application` and use either the `target_application` or `target_application_id` to
        define the application.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel of the created invite.
        
        invite_template : `None`, ``Invite`` = `None`, Optional
            Invite entity to use as a template.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to create the invite with.
        
        Other Parameters
        ----------------
        max_age : `int`, Optional (Keyword only)
            After how much time (in seconds) will the invite expire. Defaults is never.
        
        max_uses : `int`, Optional (Keyword only)
            How much times can the invite be used. Defaults to unlimited.
        
        target_application : `int`, ``Application``, Optional (Keyword only)
            Alternative for `target_application_id`.
        
        target_application_id : `int`, ``Application``, Optional (Keyword only)
            The invite's target application.
        
        target_type : ``InviteTargetType``, `int`, Optional (Keyword only)
            The invite's target type.
        
        target_user : `int`, ``ClientUserBase``, Optional (Keyword only)
            Alternative for `target_user`.
        
        target_user_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The target of the invite if applicable.
        
        temporary : `bool`, Optional (Keyword only)
            Whether the invite should give only temporary membership.
        
        unique : `bool`, Optional (Keyword only)
            Whether the created invite should be unique.
        
        Returns
        -------
        invite : ``Invite``
        
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
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_invitable)
        data = build_create_payload(invite_template, INVITE_GUILD_FIELD_CONVERTERS, keyword_parameters)
        invite_data = await self.api.invite_create(channel_id, data)
        return Invite.from_data(invite_data)
    
    
    async def invite_create_preferred(self, guild, **keyword_parameters):
        """
        Creates an invite to the guild's preferred channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild . ``Guild``
            The guild the invite will be created to.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to describe the created invite.
        
        Other Parameters
        ----------------
        max_age : `int` = `0`, Optional (Keyword only)
            After how much time (in seconds) will the invite expire. Defaults is never.
        
        max_uses : `int` = `0`, Optional (Keyword only)
            How much times can the invite be used. Defaults to unlimited.
        
        unique : `bool` = `True`, Optional (Keyword only)
            Whether the created invite should be unique.
        
        temporary : `bool` = `False`, Optional (Keyword only)
            Whether the invite should give only temporary membership.
        
        Returns
        -------
        invite : ``Invite``
        
        Raises
        ------
        TypeError
            - if `guild` is not ``Guild`˛
        ValueError
            If the guild has no channel to create invite to.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if not isinstance(guild, Guild):
            raise TypeError(
                f'`guild` can be `{Guild.__name__}`, got {guild.__class__.__name__}; {guild!r}.'
            )
        
        channel = _get_preferred_channel_for_invite(self, guild)
        if channel is None:
            raise ValueError(
                f'The guild has no available channels to create invite for (or lack of permissions).'
                f'Got guild = {guild!r}.'
            )
        
        try:
            return (await self.invite_create(channel, **keyword_parameters))
        except DiscordException as err:
            if err.code in (
                ERROR_CODES.unknown_channel, # the channel was deleted meanwhile
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
                ERROR_CODES.missing_access, # client removed
            ):
                return None
            raise
    
    
    async def invite_get(self, invite):
        """
        Requests a partial invite with the given code.
        
        This method is a coroutine.
        
        Parameters
        ----------
        invite : ``Invite``, `str`
            The invites code.
        
        Returns
        -------
        invite : ``Invite``
        
        Raises
        ------
        TypeError
            If `invite` was not given neither ``Invite`` nor `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `invite_code` was not given as `str`.
        """
        if isinstance(invite, Invite):
            invite_code = invite.code
        
        elif isinstance(invite, str):
            invite_code = invite
            invite = None
        
        else:
            raise TypeError(
                f'`invite`` can be `{Invite.__name__}`, `str`, got {invite.__class__.__name__}; '
                f'{invite!r}.'
            )
        
        invite_data = await self.api.invite_get(invite_code, {'with_counts': True})
        
        if invite is None:
            invite = Invite.from_data(invite_data)
        else:
            invite._update_attributes(invite_data)
        
        return invite
    
    
    async def invite_get_all_guild(self, guild):
        """
        Gets the invites of the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's invites will be requested.
        
        Returns
        -------
        invites : `list` of ``Invite`` objects
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        invite_datas = await self.api.invite_get_all_guild(guild_id)
        return [Invite.from_data(invite_data) for invite_data in invite_datas]
    
    
    async def invite_get_all_channel(self, channel):
        """
        Gets the invites of the given channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel, what's invites will be requested.
        
        Returns
        -------
        invites : `list` of ``Invite`` objects
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        while True:
            if isinstance(channel, Channel):
                if channel.is_in_group_invitable() or channel.partial:
                    channel_id = channel.id
                    break
            
            else:
                channel_id = maybe_snowflake(channel)
                if (channel_id is not None):
                    break
            
            raise TypeError(
                f'`channel` can be an invitable ``Channel``, `int`, got {channel.__class__.__name__}; {channel!r}.'
            )
        
        invite_datas = await self.api.invite_get_all_channel(channel_id)
        return [Invite.from_data(invite_data) for invite_data in invite_datas]
    
    
    async def invite_delete(self, invite, *, reason = None):
        """
        Deletes the given invite.
        
        This method is a coroutine.
        
        Parameters
        ----------
        invite : ``Invite``
            The invite to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `invite` was not given neither ``Invite`` nor `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(invite, Invite):
            invite_code = invite.code
        
        elif isinstance(invite, str):
            invite_code = invite
            invite = None
        
        else:
            raise TypeError(
                f'`invite`` can be `{Invite.__name__}`, `str`, got {invite.__class__.__name__}; {invite!r}.'
            )
        
        invite_data = await self.api.invite_delete(invite_code, reason)
        
        if invite is None:
            invite = Invite.from_data(invite_data)
        else:
            invite._update_attributes(invite_data)
        
        return invite
