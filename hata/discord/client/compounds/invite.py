__all__ = ()

import warnings

from scarletio import Compound

from ...application import Application
from ...bases import maybe_snowflake
from ...channel import Channel, ChannelType
from ...exceptions import DiscordException, ERROR_CODES
from ...guild import Guild, create_partial_guild_from_id
from ...http import DiscordHTTPClient
from ...invite import Invite, InviteTargetType
from ...permission.permission import PERMISSION_MASK_CREATE_INSTANT_INVITE
from ...user import ClientUserBase

from ..request_helpers import get_channel_id, get_guild_and_id, get_guild_id


def _assert__vanity_invite_edit__vanity_code(vanity_code):
    """
    Asserts the `vanity_code` parameter of ``Client.vanity_invite_edit`` method.
    
    Parameters
    ----------
    vanity_code : `str`
        The new code of the guild's vanity invite.
    
    Raises
    ------
    AssertionError
        - If `vanity_code` is not `str`.
    """
    if not isinstance(vanity_code, str):
        raise AssertionError(
            f'`vanity_code` can be `str`, got {vanity_code.__class__.__name__}; {vanity_code!r}.'
        )
    
    return True


def _assert__invite_create__max_age(max_age):
    """
    Asserts the `max_age` parameter of ``Client.invite_create`` method.
    
    Parameters
    ----------
    max_age : `int`
        After how much time (in seconds) will the invite expire.
    
    Raises
    ------
    AssertionError
        - If `max_age` is not `int`.
    """
    if not isinstance(max_age, int):
        raise AssertionError(
            f'`max_age` can be `int`, got {max_age.__class__.__name__}; {max_age!r}.'
        )
    
    return True


def _assert__invite_create__max_uses(max_uses):
    """
    Asserts the `max_uses` parameter of ``Client.invite_create`` method.
    
    Parameters
    ----------
    max_uses : `int`
        How much times can the invite be used.
    
    Raises
    ------
    AssertionError
        - If `max_uses` is not `int`.
    """
    if not isinstance(max_uses, int):
        raise AssertionError(
            f'`max_uses` can be `int`, got {max_uses.__class__.__name__}; {max_uses!r}.'
        )
    
    return True


def _assert__invite_create__unique(unique):
    """
    Asserts the `unique` parameter of ``Client.invite_create`` method.
    
    Parameters
    ----------
    unique : `bool`
        Whether the created invite should be unique.
    
    Raises
    ------
    AssertionError
        - If `unique` is not `bool`.
    """
    if not isinstance(unique, bool):
        raise AssertionError(
            f'`unique` can be `bool`, got {unique.__class__.__name__}; {unique!r}.'
        )
    
    return True


def _assert__invite_create__temporary(temporary):
    """
    Asserts the `temporary` parameter of ``Client.invite_create`` method.
    
    Parameters
    ----------
    temporary : `bool`
        Whether the invite should give only temporary membership.
    
    Raises
    ------
    AssertionError
        - If `temporary` is not `bool`.
    """
    if not isinstance(temporary, bool):
        raise AssertionError(
            f'`temporary` can be `bool`, got {temporary.__class__.__name__}; {temporary!r}.'
        )
    
    return True


class ClientCompoundInviteEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    
    async def vanity_invite_get(self, guild):
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
        
        if (guild is None) or guild.partial:
            invite_data = await self.http.vanity_invite_get(guild_id)
            vanity_code = invite_data['code']
        else:
            vanity_code = guild.vanity_code
        
        if vanity_code is None:
            return None
        
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        invite_data = await self.http.invite_get(vanity_code, {})
        return Invite._create_vanity(guild, invite_data)
    
    
    async def vanity_invite_edit(self, guild, vanity_code, *, reason = None):
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
        
        assert _assert__vanity_invite_edit__vanity_code(vanity_code)
        
        await self.http.vanity_invite_edit(guild_id, {'code': vanity_code}, reason)
    
    
    async def invite_create(self, channel, *, max_age=0, max_uses=0, unique=True, temporary=False):
        """
        Creates an invite at the given channel with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel of the created invite.
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
            If `channel` was not given neither as ``Channel``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `max_age` was not given as `int`.
            - If `max_uses` was not given as `int`.
            - If `unique` was not given as `bool`.
            - If `temporary` was not given as `bool`.
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
                f'`channel` can be an invitable channel, `int`'
                f', got {channel.__class__.__name__}; {channel!r}.'
            )
        
        assert _assert__invite_create__max_age(max_age)
        assert _assert__invite_create__max_uses(max_uses)
        assert _assert__invite_create__unique(unique)
        assert _assert__invite_create__temporary(temporary)
        
        data = {
            'max_age': max_age,
            'max_uses': max_uses,
            'temporary': temporary,
            'unique': unique,
        }
        
        data = await self.http.invite_create(channel_id, data)
        return Invite(data, False)
    
    # 'target_user_id' :
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_type.GUILD_INVITE_INVALID_TARGET_USER_TYPE('Invalid target user type')
    # 'target_type', as 0:
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_type.BASE_TYPE_CHOICES('Value must be one of (1,).')
    # 'target_type', as 1:
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_type.GUILD_INVITE_INVALID_TARGET_USER_TYPE('Invalid target user type')
    # 'target_user_id' and 'target_user_type' together:
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_id.GUILD_INVITE_INVALID_STREAMER('The specified user is currently not streaming in this channel')
    # 'target_user_id' and 'target_user_type' with not correct channel:
    #     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
    #     target_user_id.GUILD_INVITE_INVALID_STREAMER('The specified user is currently not streaming in this channel')
    
    async def stream_invite_create(self, guild, user, *, max_age=0, max_uses=0, unique=True, temporary=False):
        """
        Creates an STREAM invite at the given guild for the specific user. The user must be streaming at the guild,
        when the invite is created.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild where the user streams.
        user : ```ClientUserBase``, `int`
            The streaming user.
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
            - If `user` was not given neither as ``ClientUserBase`` neither as `int`.
            - If `guild` is not ``Guild``.
        ValueError
            - If the user is not streaming at the guild.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if not isinstance(guild, Guild):
            raise TypeError(
                f'`guild` can be `{Guild.__name__}`, got {guild.__class__.__name__}; {guild!r}.'
            )
        
        if isinstance(user, ClientUserBase):
            user_id = user.id
        else:
            user_id = maybe_snowflake(user)
            if user_id is None:
                raise TypeError(
                    f'`user` can be `{ClientUserBase.__name__}`, `int`, got {user.__class__.__name__}; {user!r}.'
                )
        
        try:
            voice_state = guild.voice_states[user_id]
        except KeyError:
            raise ValueError(
                f'The user must stream at a voice channel of the guild. Got user = {user!r}; guild = {guild!r}.'
            ) from None
        
        if not voice_state.self_stream:
            raise ValueError(
                f'The user must stream at a voice channel of the guild. Got user = {user!r}; guild = {guild!r}.'
            )
        
        assert _assert__invite_create__max_age(max_age)
        assert _assert__invite_create__max_uses(max_uses)
        assert _assert__invite_create__unique(unique)
        assert _assert__invite_create__temporary(temporary)
        
        data = {
            'max_age': max_age,
            'max_uses': max_uses,
            'temporary': temporary,
            'unique': unique,
            'target_user_id': user_id,
            'target_type': InviteTargetType.stream.value,
        }
        
        data = await self.http.invite_create(voice_state.channel.id, data)
        return Invite(data, False)
    
    # Could not find correct application:
    #    DiscordException Bad Request (400), code=50035: Invalid Form Body
    #    target_application_id.GUILD_INVITE_INVALID_APPLICATION('The specified application is not embedded')
    
    async def application_invite_create(
        self, channel, application, *, max_age=0, max_uses=0, unique=True, temporary=False
    ):
        """
        Creates an EMBEDDED_APPLICATION invite to the specified voice channel. The application must have must have
        `embedded` flag.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int
            The target channel of the invite.
        application : ``Application``, `int`
            The embedded application to open in the voice channel.
            
            > The application must have `EMBEDDED_APPLICATION` flag.
        
        max_age : `int` = `0`, Optional (Keyword only)
            After how much time (in seconds) will the invite expire.
            
            > If given as `0` (so by default) then the created invite will never expire.
        
        max_uses : `int` = `0`, Optional (Keyword only)
            How much times can the invite be used.
            
            > If given as `0` (so by default) then the created invite will have no use limit.
        
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
            - If `channel` was not given neither as ``Channel``, neither as `int`.
            - If `application` was not given neither as ``Application`` nor as`int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, Channel.is_guild_voice)
        
        if isinstance(application, Application):
            application_id = application.id
        else:
            application_id = maybe_snowflake(application)
            if application_id is None:
                raise TypeError(
                    f'`application` can be `{Application.__name__}`, `int`, got '
                    f'{application.__class__.__name__}; {application!r}.'
                )
        
        assert _assert__invite_create__max_age(max_age)
        assert _assert__invite_create__max_uses(max_uses)
        assert _assert__invite_create__unique(unique)
        assert _assert__invite_create__temporary(temporary)
        
        data = {
            'max_age': max_age,
            'max_uses': max_uses,
            'temporary': temporary,
            'unique': unique,
            'target_application_id': application_id,
            'target_type': InviteTargetType.embedded_application.value,
        }
        
        data = await self.http.invite_create(channel_id, data)
        return Invite(data, False)
    
    
    async def invite_create_preferred(self, guild, **kwargs):
        """
        Creates an invite to the guild's preferred channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild . ``Guild``
            The guild to her the invite will be created to.
        **kwargs : Keyword parameters
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
        
        while True:
            if not guild.channels:
                raise ValueError(
                    f'The guild has no channels (yet?), try waiting for dispatch or create a channel. '
                    f'Got guild={guild!r}.'
                )

            channel = guild.system_channel
            if channel is not None:
                break
            
            channel = guild.widget_channel
            if channel is not None:
                break
            
            for channel_type in (ChannelType.guild_text, ChannelType.guild_voice):
                for channel in guild.channels.values():
                    if channel.type == ChannelType.guild_category:
                        for channel in channel.channels:
                            if channel.type == channel_type:
                                break
                    if channel.type == channel_type:
                        break
                if channel.type == channel_type:
                    break
            else:
                raise ValueError(
                    f'The guild has only category channels and cannot create invite from them. '
                    f'Got guild={guild!r}.'
                )
            break
        
        # Check permission, because it can save a lot of time >.>
        if not channel.cached_permissions_for(self) & PERMISSION_MASK_CREATE_INSTANT_INVITE:
            return None
        
        try:
            return (await self.invite_create(channel, **kwargs))
        except DiscordException as err:
            if err.code in (
                ERROR_CODES.unknown_channel, # the channel was deleted meanwhile
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
                ERROR_CODES.missing_access, # client removed
            ):
                return None
            raise
    
    
    async def invite_get(self, invite, *, with_count=...):
        """
        Requests a partial invite with the given code.
        
        This method is a coroutine.
        
        Parameters
        ----------
        invite : ``Invite``, `str`
            The invites code.
        
        with_count : `bool`, Optional (Keyword only)
            Whether the invite should contain the respective guild's user and online user count.
            
            Defaults to `True`.
            
            Deprecated and will be removed in 2023 January.
        
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
        
        if (with_count is not ...):
            warnings.warn(
                (
                    f'`with_count` parameter of `{self.__class__.__name__}` is deprecated and will be removed in '
                    f'2023 January. The parameter is always defaulting to `True`.',
                ),
                FutureWarning,
                stacklevel = 2,
            )
        
        
        invite_data = await self.http.invite_get(invite_code, {'with_counts': True})
        
        if invite is None:
            invite = Invite(invite_data, False)
        else:
            if invite.partial:
                updater = Invite._update_attributes
            else:
                updater = Invite._update_counts_only
            
            updater(invite, invite_data)
        
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
        
        invite_datas = await self.http.invite_get_all_guild(guild_id)
        return [Invite(invite_data, False) for invite_data in invite_datas]
    
    
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
        
        invite_datas = await self.http.invite_get_all_channel(channel_id)
        return [Invite(invite_data, False) for invite_data in invite_datas]
    
    
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
        
        invite_data = await self.http.invite_delete(invite_code, reason)
        
        if invite is None:
            invite = Invite(invite_data, False)
        else:
            invite._update_attributes(invite_data)
        
        return invite
