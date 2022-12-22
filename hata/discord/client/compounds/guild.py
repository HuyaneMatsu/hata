__all__ = ()

import reprlib

from scarletio import Compound

from ...bases import maybe_snowflake
from ...channel import Channel, VoiceRegion
from ...exceptions import DiscordException
from ...guild import (
    AuditLog, AuditLogEvent, AuditLogIterator, ContentFilterLevel, Guild, GuildFeature,
    GuildPreview, GuildWidget, MessageNotificationLevel, SystemChannelFlag, VerificationLevel, VerificationScreen,
    WelcomeChannel, WelcomeScreen, create_partial_guild_from_data, create_partial_guild_from_id
)
from ...guild.verification_screen.utils import VERIFICATION_SCREEN_FIELD_CONVERTERS
from ...http import DiscordHTTPClient, VALID_ICON_MEDIA_TYPES, VALID_ICON_MEDIA_TYPES_EXTENDED
from ...localization.utils import Locale
from ...payload_building import build_create_payload, build_edit_payload
from ...role import Role
from ...user import ClientUserBase, GuildProfile, PremiumType, User, UserBase, UserFlag
from ...utils import get_image_media_type, image_to_base64, log_time_converter

from ..request_helpers import get_guild_and_id, get_guild_id, get_role_id, get_user_id


class ClientCompoundGuildEndpoints(Compound):
    
    flags : UserFlag
    guild_profiles : dict
    guilds : set
    http : DiscordHTTPClient
    id : int
    bot : bool
    premium_type : PremiumType
    
    
    async def guild_preview_get(self, guild):
        """
        Requests the preview of a public guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The id of the guild, what's preview will be requested
        
        Returns
        -------
        preview : ``GuildPreview``
        
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
        
        data = await self.http.guild_preview_get(guild_id)
        return GuildPreview(data)
    
    
    async def guild_user_delete(self, guild, user, *, reason = None):
        """
        Removes the given user from the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild from where the user will be removed.
        user : ``ClientUserBase``, `int`
            The user to delete from the guild.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor `int`.
            - If `user` was not given neither as ``ClientUserBase``, nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        user_id = get_user_id(user)
        
        await self.http.guild_user_delete(guild_id, user_id, reason)
    
    
    async def welcome_screen_get(self, guild):
        """
        Requests the given guild's welcome screen.
        
        You need to have `manage guild` permission to request the welcome screen if the guild has it disabled.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's welcome screen will be requested.
        
        Returns
        -------
        welcome_screen : `None`, ``WelcomeScreen``
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If the guild has no welcome screen enabled, will not do any request.
        """
        guild_id = get_guild_id(guild)
        
        welcome_screen_data = await self.http.welcome_screen_get(guild_id)
        if welcome_screen_data is None:
            welcome_screen = None
        else:
            welcome_screen = WelcomeScreen.from_data(welcome_screen_data)
        
        return welcome_screen
    
    
    async def welcome_screen_edit(self, guild, *, enabled=..., description = ..., welcome_channels=...):
        """
        Edits the given guild's welcome screen.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's welcome screen will be edited.
        enabled : `bool`, Optional (Keyword only)
            Whether the guild's welcome screen should be enabled.
        description : `None`, `str`, Optional (Keyword only)
            The welcome screen's new description. It's length can be in range [0:140].
        welcome_channels : `None`, ``WelcomeChannel`` or  (`tuple`, `list`) of ``WelcomeChannel``
                , Optional (Keyword only)
            The channels mentioned on the welcome screen.
        
        Returns
        -------
        welcome_screen : `None or ``WelcomeScreen``
            The updated welcome screen. Always returns `None` if no change was propagated.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor `int`.
            - If `welcome_channels` was not given neither as `None`, ``WelcomeChannel`` nor as (`tuple`, `list`) of
                ``WelcomeChannel``-s.
            - If `welcome_channels` contains a non ``WelcomeChannel``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `enabled` was not given as `bool`.
            - If `description` was not given neither as `None`, `str`.
            - If `description`'s length is out of range [0:140].
            - If `welcome_channels`'s length is out of range [0:5].
        """
        guild_id = get_guild_id(guild)
        
        data = {}
        
        if (enabled is not ...):
            if __debug__:
                if not isinstance(enabled, bool):
                    raise AssertionError(
                        f'`enabled` can be `bool`, got {enabled.__class__.__name__}; {enabled!r}.'
                    )
            
            data['enabled'] = enabled
        
        if (description is not ...):
            if __debug__:
                if (description is not None):
                    if not isinstance(description, str):
                        raise AssertionError(
                            f'`description` can be `None`, `str`, got {description.__class__.__name__}; '
                            f'{description!r}.'
                        )
                
                    description_length = len(description)
                    if description_length > 300:
                        raise AssertionError(
                            f'`description` length can be in range [0:140], got {description_length!r}; '
                            f'{description!r}.'
                        )
                
            if (description is not None) and (not description):
                description = None
            
            data['description'] = description
        
        if (welcome_channels is not ...):
            welcome_channel_datas = []
            if welcome_channel_datas is None:
                pass
            elif isinstance(welcome_channels, WelcomeChannel):
                welcome_channel_datas.append(welcome_channels.to_data())
            elif isinstance(welcome_channels, (list, tuple)):
                if __debug__:
                    welcome_channels_length = len(welcome_channels)
                    if welcome_channels > 5:
                        raise AssertionError(
                            f'`welcome_channels` length can be in range [0:5], got '
                            f'{welcome_channels_length!r}; {welcome_channels!r}.'
                        )
                
                for index, welcome_channel in enumerate(welcome_channels):
                    if not isinstance(welcome_channel, WelcomeChannel):
                        raise TypeError(
                            f'`welcome_channels[{index}]` is not `{WelcomeChannel.__name__}` , got '
                            f'{welcome_channel.__class__.__name__}; {welcome_channel!r}; '
                            f'welcome_channels={welcome_channels!r}.'
                        )
                    
                    welcome_channel_datas.append(welcome_channel.to_data())
            else:
                raise TypeError(
                    f'`welcome_channels` can be `None`, `{WelcomeChannel.__name__}`, '
                    f'(`list`, `tuple`) of `{WelcomeChannel.__name__}, got '
                    f'{welcome_channels.__class__.__name__}; {welcome_channels!r}.'
                )
            
            data['welcome_channels'] = welcome_channel_datas
        
        if data:
            data = await self.http.welcome_screen_edit(guild_id, data)
            if data:
                welcome_screen = WelcomeScreen.from_data(data)
            else:
                welcome_screen = None
        else:
            welcome_screen = None
        
        return welcome_screen
    
    
    async def verification_screen_get(self, guild):
        """
        Requests the given guild's verification screen.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's verification screen will be requested.

        Returns
        -------
        verification_screen : `None`, ``VerificationScreen``
        
        Raises
        ------
        TypeError
            - If `guild` was not ``Guild``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If the guild has no verification screen enabled, will not do any request.
        """
        guild_id = get_guild_id(guild)
        
        verification_screen_data = await self.http.verification_screen_get(guild_id)
        return VerificationScreen.from_data(verification_screen_data)
    
    
    async def verification_screen_edit(self, guild, verification_screen_template = None, **keyword_parameters):
        """
        Requests the given guild's verification screen.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild what's verification screen will be edited.
        
        verification_screen_template : `None`, ``VerificationScreen``` = `None`, Optional
            Verification screen to use as a template.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to edit the verification screen with.
        
        
        Other Parameters
        ----------------
        description  : `None`, `str`, Optional (Keyword only)
            The guild's description shown in the verification screen.
        
        edited_at : `None`, `datetime`, Optional (Keyword only)
            When the last version of the screen was created.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the verification screen should be enabled.
        
        steps : `None`, `tuple` of ``VerificationScreenStep``, Optional (Keyword only)
            The step in the verification screen.
        
        Returns
        -------
        verification_screen : ``VerificationScreen``
        
        Raises
        ------
        TypeError
            - If `guild` was not ``Guild``, `int`.
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        When editing steps, `DiscordException Internal Server Error (500)` will be dropped.
        """
        guild_id = get_guild_id(guild)
        
        data = build_edit_payload(
            None, verification_screen_template, VERIFICATION_SCREEN_FIELD_CONVERTERS, keyword_parameters
        )
        verification_screen_data = await self.http.verification_screen_edit(guild_id, data)
        
        return VerificationScreen.from_data(verification_screen_data)
    
    
    async def guild_get(self, guild):
        """
        Gets or updates the guild.
        
        > The client must be in the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to request.
        
        Returns
        -------
        guild : ``Guild``
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        data = await self.http.guild_get(guild_id, {'with_counts': True})
        
        if guild is None:
            channel_datas = await self.http.guild_channel_get_all(guild_id)
            data['channels'] = channel_datas
            user_data = await self.http.guild_user_get(guild_id, self.id)
            data['members'] = [user_data]
            guild = Guild.from_data(data, self)
        else:
            guild._sync(data)
        
        return guild
    
    
    async def guild_sync(self, guild):
        """
        Syncs a guild by it's id with the wrapper. Used internally if de-sync is detected when parsing dispatch events.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to sync.

        Returns
        -------
        guild : ``Guild``
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        # sadly guild_get does not returns channel and voice state data at least we can request the channels
        guild, guild_id = get_guild_and_id(guild)
        
        if guild is None:
            data = await self.http.guild_get(guild_id, None)
            channel_datas = await self.http.guild_channel_get_all(guild_id)
            data['channels'] = channel_datas
            user_data = await self.http.guild_user_get(guild_id, self.id)
            data['members'] = [user_data]
            guild = Guild.from_data(data, self)
        else:
            data = await self.http.guild_get(guild_id, None)
            guild._sync(data)
            channel_datas = await self.http.guild_channel_get_all(guild_id)
            guild._sync_channels(channel_datas)
            
            user_data = await self.http.guild_user_get(guild_id, self.id)
            try:
                profile = self.guild_profiles[guild.id]
            except KeyError:
                self.guild_profiles[guild.id] = GuildProfile.from_data(user_data)
                if guild not in guild.clients:
                    guild.clients.append(self)
            else:
                profile._update_attributes(user_data)
        
        return guild

##    # Disable user syncing, takes too much time
##    async def _guild_sync_post_process(self, guild):
##        for client in CLIENTS.values():
##            try:
##                user_data = await self.http.guild_user_get(guild.id, client.id)
##           except (DiscordException, ConnectionError):
##                continue
##            try:
##                profile = client.guild_profiles[guild.id]
##            except KeyError:
##                client.guild_profiles[guild.id] = GuildProfile.from_data(user_data)
##                if client not in guild.clients:
##                    guild.clients.append(client)
##            else:
##                profile._update_attributes(user_data)
##
##        if not CACHE_USER:
##            return
##
##        old_ids = set(guild.users)
##        data = {'limit': 1000, 'after': '0'}
##        while True:
##            user_datas = await self.http.guild_users(guild.id, data)
##            for user_data in user_datas:
##                user = User._create_and_update(user_data, guild)
##                try:
##                    old_ids.remove(user.id)
##                except KeyError:
##                    pass
##
##             if len(user_datas)< 1 000:
##                 break
##
##             data['after'] = user_datas[999]['user']['id']
##
##        del data
##
##        for id_ in old_ids:
##            try:
##               user = guild.users.pop(id_)
##           except KeyError:
##               continue #huh?
##           try:
##               del user.guild_profiles[guild.id]
##           except KeyError:
##               pass # huh??


    async def guild_delete(self, guild):
        """
        Deletes the given guild. The client must be the owner of the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to delete.
        
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
        
        await self.http.guild_delete(guild_id)
    
    
    async def guild_create(
        self, name, *, icon=None, roles=None, channels=None, afk_channel_id=None, system_channel_id=None,
        afk_timeout = None, verification_level=VerificationLevel.medium,
        message_notification=MessageNotificationLevel.only_mentions, content_filter=ContentFilterLevel.disabled,
        boost_progress_bar_enabled=None
    ):
        """
        Creates a guild with the given parameter. Bot accounts can create guilds only when they have less than 10.
        User account guild limit is 100, meanwhile staff guild limit is 200.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str`
            The name of the new guild.
        icon : `None`, `bytes-like` = `None`, Optional (Keyword only)
            The icon of the new guild.
        roles : `None`, `list` of `dict` = `None`, Optional (Keyword only)
            A list of roles of the new guild. It should contain role data objects.
        channels : `None`, `list` of `dict` = `None`, Optional (Keyword only)
            A list of channels of the new guild. It should contain channel data objects.
        afk_channel_id : `None`, `int` = `None`, Optional (Keyword only)
            The id of the guild's afk channel. The id should be one of the channel's id from `channels`.
        system_channel_id: `int`, Optional (Keyword only)
            The id of the guild's system channel. The id should be one of the channel's id from `channels`.
        afk_timeout : `None`, `int` = `None`, Optional (Keyword only)
            The afk timeout for the users at the guild's afk channel.
        
        verification_level : ``VerificationLevel``, `int` = `VerificationLevel.medium`, Optional (Keyword only)
            The verification level of the new guild.
        message_notification : ``MessageNotificationLevel``, `int` = `MessageNotificationLevel.only_mentions`
                , Optional (Keyword only)
            The message notification level of the new guild.
        content_filter : ``ContentFilterLevel``, `int` = `ContentFilterLevel.disabled`, Optional (Keyword only)
            The content filter level of the guild.
        boost_progress_bar_enabled : `None`, `bool` = `None`, Optional (Keyword only)
            Whether the guild has the boost progress bar should be enabled.
        
        Returns
        -------
        guild : ``Guild`` object
            A partial guild made from the received data.
        
        Raises
        ------
        TypeError
            - If `icon` is neither `None`, `bytes-like`.
            - If `verification_level` was not given neither as ``VerificationLevel`` not `int`.
            - If `content_filter` was not given neither as ``ContentFilterLevel`` not `int`.
            - If `message_notification` was not given neither as ``MessageNotificationLevel`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the client cannot create more guilds.
            - If `name` was not given as `str`.
            - If the `name`'s length is out of range [2:100].
            - If `icon` is passed as `bytes-like`, but it's format is not a valid image format.
            - If `afk-timeout` was not given as `int`.
            - If `afk_timeout` was passed and not as one of: `60, 300, 900, 1800, 3600`.
            - If `boost_progress_bar_enabled` was not given as `bool`.
        """
        if __debug__:
            if self.bot:
                guild_create_limit = 10
            elif self.flags.staff:
                guild_create_limit = 200
            elif (self.premium_type is PremiumType.nitro):
                guild_create_limit = 200
            else:
                guild_create_limit = 100
            
            if len(self.guilds) >= guild_create_limit:
                raise AssertionError(
                    f'Guild count over creation limit; limit={guild_create_limit}; count={len(self.guilds)!r}.'
                )
        
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            if name_length < 2 or name_length > 100:
                raise AssertionError(
                    f'`name` length can be in range [2:100], got {name_length!r}; {name!r}.'
                )
        
        
        if icon is None:
            icon_data = None
        else:
            icon_type = icon.__class__
            if not issubclass(icon_type, (bytes, bytearray, memoryview)):
                raise TypeError(
                    f'`icon` can be `None`, `bytes-like`, got {icon_type.__name__}; {reprlib.repr(icon)}.'
                )
            
            if __debug__:
                media_type = get_image_media_type(icon)
                if media_type not in VALID_ICON_MEDIA_TYPES:
                    raise AssertionError(
                        f'Invalid `icon` type: {media_type}; {reprlib.repr(icon)}.'
                    )
            
            icon_data = image_to_base64(icon)
        
        if isinstance(verification_level, VerificationLevel):
            verification_level_value = verification_level.value
        elif isinstance(verification_level, int):
            verification_level_value = verification_level
        else:
            raise TypeError(
                f'`verification_level` can be `{VerificationLevel.__name__}`, `int`, got '
                f'{verification_level.__class__.__name__}; {verification_level!r}.'
            )
        
        
        if isinstance(message_notification, MessageNotificationLevel):
            message_notification_value = message_notification.value
        elif isinstance(message_notification, int):
            message_notification_value = message_notification
        else:
            raise TypeError(
                f'`message_notification` can be `{MessageNotificationLevel.__name__}`, `int`, got '
                f'{message_notification.__class__.__name__}; {message_notification!r}.'
            )
        
        
        if isinstance(content_filter, ContentFilterLevel):
            content_filter_value = content_filter.value
        elif isinstance(content_filter, int):
            content_filter_value = content_filter
        else:
            raise TypeError(
                f'`content_filter` can be {ContentFilterLevel.__name__}, `int` , got '
                f'{content_filter.__class__.__name__}; {content_filter!r}.'
            )
        
        if roles is None:
            roles = []
        
        if channels is None:
            channels = []
        
        data = {
            'name': name,
            'icon': icon_data,
            'verification_level': verification_level_value,
            'default_message_notifications': message_notification_value,
            'explicit_content_filter': content_filter_value,
            'roles': roles,
            'channels': channels,
        }
        
        if (afk_channel_id is not None):
            if __debug__:
                if not isinstance(afk_channel_id, int):
                    raise AssertionError(
                        f'`afk_channel_id` can be `int`, got {afk_channel_id.__class__.__name__}; {afk_channel_id!r}.'
                    )
            
            data['afk_channel_id'] = afk_channel_id
        
        if (system_channel_id is not None):
            if __debug__:
                if not isinstance(system_channel_id, int):
                    raise AssertionError(
                        f'`system_channel_id` can be `int`, got {system_channel_id.__class__.__name__}; '
                        f'{system_channel_id!r}.'
                    )
            
            data['system_channel_id'] = system_channel_id
        
        if (afk_timeout is not None):
            if __debug__:
                if not isinstance(afk_timeout, int):
                    raise AssertionError(
                        f'`afk_timeout` can be `int`, got {afk_timeout.__class__.__name__}; {afk_timeout!r}.'
                    )
                
                if afk_timeout not in (60, 300, 900, 1800, 3600):
                    raise AssertionError(
                        f'`afk_timeout` can be 60, 300, 900, 1800, 3600 seconds; got {afk_timeout!r}.'
                    )
            
            data['afk_timeout'] = afk_timeout
        
        if (boost_progress_bar_enabled is not None):
            if __debug__:
                if not isinstance(boost_progress_bar_enabled, bool):
                    raise AssertionError(
                        f'`boost_progress_bar_enabled` can be `bool`, got '
                        f'{boost_progress_bar_enabled.__class__.__name__}; {boost_progress_bar_enabled!r}.'
                    )
            
            data['premium_progress_bar_enabled'] = boost_progress_bar_enabled
        
        
        data = await self.http.guild_create(data)
        # we can create only partial, because the guild data is not completed usually
        return create_partial_guild_from_data(data)
    
    
    async def guild_prune(self, guild, days, *, roles=None, count=False, reason = None):
        """
        Kicks the members of the guild which were inactive since x days.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            Where the pruning will be executed.
        days : `int`
            The amount of days since at least the users need to inactive. Can be in range [1:30].
        roles : `None`, `list` of (``Role``, `int`) = `None`, Optional (Keyword only)
            By default pruning will kick only the users without any roles, but it can defined which roles to include.
        count : `bool` = `False`, Optional (Keyword only)
            Whether the method should return how much user were pruned, but if the guild is large it will be set to
            `False` anyways. Defaults to `False`.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the guild's audit logs.
        
        Returns
        -------
        count : `None`, `int`
            The number of pruned users or `None` if `count` is set to `False`.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor `int`.
            - If `roles` contain not ``Role``, neither `int` element.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `roles` was given neither as `None`, `list`.
            - If `count` was not given as `bool`.
            - If `days` was not given as `int`.
            - If `days` is out of range [1:30].
        
        See Also
        --------
        ``.guild_prune_estimate`` : Returns how much user would be pruned if ``.guild_prune`` would be called.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        if __debug__:
            if not isinstance(count, bool):
                raise AssertionError(
                    f'`count` can be `bool`, got {count.__class__.__name__}; {count!r}.'
                )
        
        if count and (guild is not None) and guild.is_large:
            count = False
        
        if __debug__:
            if not isinstance(days, int):
                raise AssertionError(
                    f'``days` can be `int`, got {days.__class__.__name__}; {days!r}.'
                )
            
            if days < 1 or days > 30:
                raise AssertionError(
                    f'`days can be in range [1:30], got {days!r}.'
                )
        
        data = {
            'days': days,
            'compute_prune_count': count,
        }
        
        if (roles is not None):
            if __debug__:
                if not isinstance(roles, list):
                    raise AssertionError(
                        f'`roles` can be `None`m `list` of (`{Role.__name__}`, `int`)'
                        f', got {roles.__class__.__name__}; {roles!r}.')
            
            role_ids = set()
            for index, role in enumerate(roles):
                if isinstance(role, Role):
                    role_id = role.id
                else:
                    role_id = maybe_snowflake(role)
                    if role_id is None:
                        raise TypeError(
                            f'`roles[{index}]` is not `{Role.__name__}`, `int`,'
                            f' got {role.__class__.__name__}; {role!r}; roles={roles!r}.'
                        )
                
                role_ids.add(role_id)
            
            if role_ids:
                data['include_roles'] = role_ids
        
        data = await self.http.guild_prune(guild_id, data, reason)
        return data.get('pruned', None)
    
    
    async def guild_prune_estimate(self, guild, days, *, roles=None):
        """
        Returns the amount users, who would been pruned, if ``.guild_prune`` would be called.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`.
            Where the counting of prunable users will be done.
        days : `int`
            The amount of days since at least the users need to inactive. Can be in range [1:30].
        roles : `None`, `list` of (``Role``, `int`) = `None`, Optional (Keyword only)
            By default pruning would kick only the users without any roles, but it can be defined which roles to
            include.
        
        Returns
        -------
        count : `int`
            The amount of users who would be pruned.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor `int`.
            - If `roles` contain not ``Role``, neither `int` element.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `roles` was given neither as `None`, `list`.
            - If `days` was not given as `int`.
            - If `days` is out of range [1:30].
        """
        guild_id = get_guild_id(guild)
        
        if __debug__:
            if not isinstance(days, int):
                raise AssertionError(f'`days can be `int`, got {days.__class__.__name__}.')
            
            if days < 1 or days > 30:
                raise AssertionError(f'`days can be in range [1:30], got {days!r}.')
        
        data = {
            'days': days,
        }
        
        if (roles is not None):
            if __debug__:
                if not isinstance(roles, list):
                    raise AssertionError(
                        f'`roles` can be `None`, `list` of (`{Role.__name__}`, `int`)'
                        f', got {roles.__class__.__name__}; {roles!r}.'
                    )
            
            role_ids = set()
            for role in roles:
                role_id = get_role_id(role)
                role_ids.add(role_id)
            
            if role_ids:
                data['include_roles'] = role_ids
        
        data = await self.http.guild_prune_estimate(guild_id, data)
        return data.get('pruned', None)
    
    
    async def guild_edit(
        self, guild, *, name=..., icon=..., invite_splash=..., discovery_splash=..., banner=...,
        afk_channel = ..., system_channel = ..., rules_channel = ..., public_updates_channel = ..., owner=...,
        afk_timeout = ..., verification_level=..., content_filter=..., message_notification=..., description = ...,
        preferred_locale=..., system_channel_flags=..., add_feature=..., remove_feature=...,
        boost_progress_bar_enabled=..., reason = None
    ):
        """
        Edits the guild with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to edit.
        name : `str`, Optional (Keyword only)
            The guild's new name.
        icon : `None`, `bytes-like`, Optional (Keyword only)
            The new icon of the guild. Can be `'jpg'`, `'png'`, `'webp'` image's raw data. If the guild has
            `ANIMATED_ICON` feature, it can be `'gif'` as well. By passing `None` you can remove the current one.
        invite_splash : `None`, `bytes-like`, Optional (Keyword only)
            The new invite splash of the guild. Can be `'jpg'`, `'png'`, `'webp'` image's raw data. The guild must have
            `INVITE_SPLASH` feature. By passing it as `None` you can remove the current one.
        discovery_splash : `None`, `bytes-like`, Optional (Keyword only)
            The new splash of the guild. Can be `'jpg'`, `'png'`, `'webp'` image's raw data. The guild must have
            `DISCOVERABLE` feature. By passing it as `None` you can remove the current one.
        banner : `None`, `bytes-like`, Optional (Keyword only)
            The new banner of the guild. Can be `'jpg'`, `'png'`, `'webp'`, `'gif'` image's raw data. The guild must
            have `BANNER` feature. `ANIMATED_BANNER` for `gif` banner. By passing it as `None` you can remove the
            current one.
        afk_channel : `None`, ``Channel``, `int`, Optional (Keyword only)
            The new afk channel of the guild. You can remove the current one by passing is as `None`.
        system_channel : `None`, ``Channel``, `int`, Optional (Keyword only)
            The new system channel of the guild. You can remove the current one by passing is as `None`.
        rules_channel : `None`, ``Channel``, `int`, Optional (Keyword only)
            The new rules channel of the guild. The guild must be a Community guild. You can remove the current
            one by passing is as `None`.
        public_updates_channel : `None`, ``Channel``, `int`, Optional (Keyword only)
            The new public updates channel of the guild. The guild must be a Community guild. You can remove the
            current one by passing is as `None`.
        owner : ``ClientUserBase``, `int`, Optional (Keyword only)
            The new owner of the guild. You must be the owner of the guild to transfer ownership.
            
        afk_timeout : `int`, Optional (Keyword only)
            The new afk timeout for the users at the guild's afk channel.
            
            Can be one of: `60, 300, 900, 1800, 3600`.
        verification_level : ``VerificationLevel``, `int`, Optional (Keyword only)
            The new verification level of the guild.
        content_filter : ``ContentFilterLevel``, `int`, Optional (Keyword only)
            The new content filter level of the guild.
        message_notification : ``MessageNotificationLevel``, Optional (Keyword only)
            The new message notification level of the guild.
        description : `None`, `str`, Optional (Keyword only)
            The new description of the guild. By passing `None`, or an empty string you can remove the current one.
        preferred_locale : ``Locale``, `str`, Optional (Keyword only)
            The guild's preferred locale. The guild must be a Community guild.
        system_channel_flags : ``SystemChannelFlag``, Optional (Keyword only)
            The guild's system channel's new flags.
        add_feature : (`str`, ``GuildFeature``) or (`iterable` of (`str`, ``GuildFeature``)), Optional (Keyword only)
            Guild feature(s) to add to the guild.
            
            If `guild` is given as an id, then `add_feature` should contain all the features of the guild to set.
        remove_feature : (`str`, ``GuildFeature``) or (`iterable` of (`str`, ``GuildFeature``)), Optional (Keyword only)
            Guild feature(s) to remove from the guild's.
        boost_progress_bar_enabled : `bool`, Optional (Keyword only)
            Whether the guild has the boost progress bar should be enabled.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild``, `str`.
            - If `icon`, `invite_splash`, `discovery_splash`, `banner` is neither `None`, `bytes-like`.
            - If `add_feature`, `remove_feature` was not given neither as `str`, ``GuildFeature``,
                `iterable` of `str`, ``GuildFeature``-s.
            - If `afk_channel` was given, but not as `None`, ``Channel``, neither as `int`.
            - If `system_channel`, `rules_channel`, `public_updates_channel` was given, but not as `None`,
                ``Channel``, neither as `int`.
            - If `owner` was not given neither as ``ClientUserBase``, `int`.
            - If `verification_level` was not given neither as ``VerificationLevel``, `int`.
            - If `content_filter` was not given neither as ``ContentFilterLevel``, `int`.
            - If `description` was not given either as `None`, `str`.
            - If `preferred_locale` was not given as ``Locale``, `str`.
        AssertionError
            - If `icon`, `invite_splash`, `discovery_splash`, `banner` was passed as `bytes-like`, but it's format
                is not any of the expected formats.
            - If `banner` was given meanwhile the guild has no `BANNER` feature.
            - If `rules_channel`, `preferred_locale`, `public_updates_channel` was passed meanwhile
                the guild is not Community guild.
            - If `owner` was passed meanwhile the client is not the owner of the guild.
            - If `afk_timeout` was passed and not as one of: `60, 300, 900, 1800, 3600`.
            - If `name` is shorter than `2` or longer than `100` characters.
            - If `discovery_splash` was given meanwhile the guild is not discoverable.
            - If `invite_splash` was passed meanwhile the guild has no `INVITE_SPLASH` feature.
            - If `name` was not given as `str`.
            - If `afk_timeout` was not given as `int`.
            - If `system_channel_flags` was not given as `SystemChannelFlag`, `int`.
            - If `boost_progress_bar_enabled` was not given as `bool`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        data = {}
        
        guild, guild_id = get_guild_and_id(guild)
        
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                if name_length < 2 or name_length > 100:
                    raise ValueError(
                        f'Guild\'s name\'s length can be between 2-100, got {name_length}: {name!r}.'
                    )
            
            data['name'] = name
        
        
        if (icon is not ...):
            if icon is None:
                icon_data = None
            
            else:
                if not isinstance(icon, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`icon` can be `None`, `bytes-like`, got {icon.__class__.__name__}; {reprlib.repr(icon)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(icon)
                    if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                        raise AssertionError(
                            f'Invalid `icon` type for the guild: {media_type}; got {reprlib.repr(icon)}.'
                        )
                
                icon_data = image_to_base64(icon)
            
            data['icon'] = icon_data
        
        
        if (banner is not ...):
            if banner is None:
                banner_data = None
            else:
                if not isinstance(banner, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`banner` can be `None`, `bytes-like`, got '
                        f'{banner.__class__.__name__}; got {reprlib.repr(banner)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(banner)
                    if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                        raise AssertionError(
                            f'Invalid `banner` type: {media_type}; got {reprlib.repr(banner)}.'
                        )
                
                banner_data = image_to_base64(banner)
            
            data['banner'] = banner_data
        
        
        if (invite_splash is not ...):
            if invite_splash is None:
                invite_splash_data = None
            else:
                if not isinstance(invite_splash, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`invite_splash` can be `None`, `bytes-like`, got '
                        f'{invite_splash.__class__.__name__}; {reprlib.repr(invite_splash)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(invite_splash)
                    if media_type not in VALID_ICON_MEDIA_TYPES:
                        raise AssertionError(
                            f'Invalid `invite_splash` type: {media_type}; got {reprlib.repr(invite_splash)}.'
                        )
                
                invite_splash_data = image_to_base64(invite_splash)
            
            data['splash'] = invite_splash_data
        
        
        if (discovery_splash is not ...):
            if discovery_splash is None:
                discovery_splash_data = None
            else:
                if not isinstance(discovery_splash, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`discovery_splash` can be `None`, `bytes-like`, got '
                        f'{discovery_splash.__class__.__name__}; {reprlib.repr(discovery_splash)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(discovery_splash)
                    if media_type not in VALID_ICON_MEDIA_TYPES:
                        raise AssertionError(
                            f'Invalid `discovery_splash` type: {media_type}; got {reprlib.repr(discovery_splash)}.'
                        )
                
                discovery_splash_data = image_to_base64(discovery_splash)
            
            data['discovery_splash'] = discovery_splash_data
        
        
        if (afk_channel is not ...):
            while True:
                if afk_channel is None:
                    afk_channel_id = None
                    break
                
                elif isinstance(afk_channel, Channel):
                    if afk_channel.is_guild_voice() or afk_channel.partial:
                        afk_channel_id = afk_channel.id
                        break
                
                else:
                    afk_channel_id = maybe_snowflake(afk_channel)
                    if afk_channel_id is not None:
                        break
                
                raise TypeError(
                    f'`afk_channel` can be `None`, guild voice channel, `int` , got '
                    f'{afk_channel.__class__.__name__}; {afk_channel!r}.'
                )
            
            data['afk_channel_id'] = afk_channel_id
        
        
        if (system_channel is not ...):
            while True:
                if system_channel is None:
                    system_channel_id = None
                    break
                
                elif isinstance(system_channel, Channel):
                    if system_channel.is_in_group_guild_system() or system_channel.partial:
                        system_channel_id = system_channel.id
                        break
                
                else:
                    system_channel_id = maybe_snowflake(system_channel)
                    if system_channel_id is not None:
                        break
                
                raise TypeError(
                    f'`system_channel` can be `None`, guild text channel, `int`, got '
                    f'{system_channel.__class__.__name__}; {system_channel!r}.'
                )
            
            data['system_channel_id'] = system_channel_id
        
        
        if (rules_channel is not ...):
            while True:
                if rules_channel is None:
                    rules_channel_id = None
                    break
                
                elif isinstance(rules_channel, Channel):
                    if rules_channel.is_in_group_guild_system() or rules_channel.partial:
                        rules_channel_id = rules_channel.id
                        break
                
                else:
                    rules_channel_id = maybe_snowflake(rules_channel)
                    if rules_channel_id is not None:
                        break
                
                raise TypeError(
                    f'`rules_channel` can be `None`, guild text channel, `int` , got '
                    f'{rules_channel.__class__.__name__}.'
                )
            
            data['rules_channel_id'] = rules_channel_id
        
        
        if (public_updates_channel is not ...):
            while True:
                if public_updates_channel is None:
                    public_updates_channel_id = None
                    break
                
                elif isinstance(public_updates_channel, Channel):
                    if public_updates_channel.is_in_group_guild_system() or public_updates_channel.partial:
                        public_updates_channel_id = public_updates_channel.id
                        break
                    
                else:
                    public_updates_channel_id = maybe_snowflake(public_updates_channel)
                    if public_updates_channel_id is not None:
                        break
                
                raise TypeError(
                    f'`public_updates_channel` can be `None`, guild text channel, `int`, got '
                    f'{public_updates_channel.__class__.__name__}; {public_updates_channel!r}.'
                )
            
            data['public_updates_channel_id'] = public_updates_channel_id
        
        
        if (owner is not ...):
            if __debug__:
                if (guild is not None) and (guild.owner_id != self.id):
                    raise AssertionError(
                        f'You must be owner to transfer ownership; got {owner!r}; actual owner={guild.owner!r}; '
                        f'guild={guild!r}.'
                    )
            
            if isinstance(owner, ClientUserBase):
                owner_id = owner.id
            else:
                owner_id = maybe_snowflake(owner)
                if owner_id is None:
                    raise TypeError(
                        f'`owner` can be `{UserBase.__name__}`, `int`, got {owner.__class__.__name__}; {owner!r}.'
                    )
            
            
            data['owner_id'] = owner_id
        
        if (afk_timeout is not ...):
            if __debug__:
                if not isinstance(afk_timeout, int):
                    raise AssertionError(
                        f'`afk_timeout` can be `int`, got {afk_timeout.__class__.__name__}; {afk_timeout!r}.'
                    )
                
                if afk_timeout not in (60, 300, 900, 1800, 3600):
                    raise AssertionError(
                        f'`afk_timeout` can be one of (60, 300, 900, 1800, 3600) seconds, got {afk_timeout!r}.'
                    )
            
            data['afk_timeout'] = afk_timeout
        
        
        if (verification_level is not ...):
            if isinstance(verification_level, VerificationLevel):
                verification_level_value = verification_level.value
            elif isinstance(verification_level, int):
                verification_level_value = verification_level
            else:
                raise TypeError(
                    f'`verification_level` can be `{VerificationLevel.__name__}`, `int`, got '
                    f'{verification_level.__class__.__name__}; {verification_level!r}.'
                )
            
            data['verification_level'] = verification_level_value
        
        
        if (content_filter is not ...):
            if isinstance(content_filter, ContentFilterLevel):
                content_filter_value = content_filter.value
            elif isinstance(content_filter, int):
                content_filter_value = content_filter
            else:
                raise TypeError(
                    f'`content_filter` can be `{ContentFilterLevel.__name__}`, `int`, got '
                    f'{content_filter.__class__.__name__}; {content_filter!r}.'
                )
            
            data['explicit_content_filter'] = content_filter_value
        
        
        if (message_notification is not ...):
            if isinstance(message_notification, MessageNotificationLevel):
                message_notification_value = message_notification.value
            elif isinstance(message_notification, int):
                message_notification_value = message_notification
            else:
                raise TypeError(
                    f'`message_notification` can be `{MessageNotificationLevel.__name__}`, `int`, got '
                    f'{message_notification.__class__.__name__}; {message_notification!r}.'
                )
            
            data['default_message_notifications'] = message_notification_value
        
        
        if (description is not ...):
            if description is None:
                pass
            elif isinstance(description, str):
                if not description:
                    description = None
            else:
                raise TypeError(
                    f'`description` can be `None`, `str`, got {description.__class__.__name__}; {description!r}.'
                )
            
            data['description'] = description
        
        
        if (preferred_locale is not ...):
            if isinstance(preferred_locale, Locale):
                preferred_locale_value = preferred_locale.value
            
            elif isinstance(preferred_locale, str):
                preferred_locale_value = preferred_locale
            
            else:
                raise TypeError(
                    f'`preferred_locale` can be `{Locale.__name__}`, `str`, got {preferred_locale.__class__.__name__}; '
                    f'{preferred_locale!r}.'
                )
            
            data['preferred_locale'] = preferred_locale_value
        
        
        if (system_channel_flags is not ...):
            if __debug__:
                if not isinstance(system_channel_flags, int):
                    raise AssertionError(
                        f'`system_channel_flags` can be `{SystemChannelFlag.__name__}`, `int`, got '
                        f'{system_channel_flags.__class__.__name__}; {system_channel_flags!r}.'
                    )
            
            data['system_channel_flags'] = system_channel_flags
        
        
        if (add_feature is not ...) or (remove_feature is not ...):
            # Collect actual
            features = set()
            if (guild is not None):
                for feature in guild.iter_features():
                    features.add(feature.value)
            
            # Collect added
            # Use GOTO
            while True:
                if add_feature is ...:
                    break
                
                if isinstance(add_feature, GuildFeature):
                    feature = add_feature.value
                elif isinstance(add_feature, str):
                    feature = add_feature
                else:
                    iter_func = getattr(type(add_feature), '__iter__', None)
                    if iter_func is None:
                        raise TypeError(
                            f'`add_feature` can be `str`, `{GuildFeature.__name__}`, `iterable` of '
                            f'(`str`, `{GuildFeature.__name__}`), got {add_feature.__class__.__name__}; '
                            f'{add_feature!r}.'
                        )
                    
                    for index, feature in enumerate(iter_func(add_feature)):
                        if isinstance(feature, GuildFeature):
                            feature = feature.value
                        elif isinstance(feature, str):
                            pass
                        else:
                            raise TypeError(
                                f'`add_feature` was given as `iterable` so it expected to have '
                                f'`{GuildFeature.__name__}`, `str` elements, but element `{index!r}` is '
                                f'{feature.__class__.__name__}; {feature!r}; add_feature={add_feature!r}.'
                            )
                        
                        features.add(feature)
                        continue
                    
                    break # End GOTO
                
                features.add(feature)
                break # End GOTO
            
            # Collect removed
            
            while True:
                if remove_feature is ...:
                    break
                
                if isinstance(remove_feature, GuildFeature):
                    feature = remove_feature.value
                elif isinstance(remove_feature, str):
                    feature = remove_feature
                else:
                    iter_func = getattr(type(remove_feature), '__iter__', None)
                    if iter_func is None:
                        raise TypeError(
                            f'`remove_feature` can be `str`, `{GuildFeature.__name__}`, `iterable` of '
                            f'(`str`, `{GuildFeature.__name__}`), got {remove_feature.__class__.__name__}; '
                            f'{remove_feature!r}.'
                        )
                    
                    for index, feature in enumerate(iter_func(remove_feature)):
                        if isinstance(feature, GuildFeature):
                            feature = feature.value
                        elif isinstance(feature, str):
                            pass
                        else:
                            raise TypeError(
                                f'`remove_feature` was given as `iterable` so it expected to have '
                                f'`{GuildFeature.__name__}`, `str` elements, but element `{index!r}` is '
                                f'{feature.__class__.__name__}; {feature!r}; remove_feature={remove_feature!r}.'
                            )
                        
                        features.discard(feature)
                        continue
                    
                    break # End GOTO
                
                features.discard(feature)
                break # End GOTO
            
            data['features'] = features
        
        
        if (boost_progress_bar_enabled is not ...):
            if __debug__:
                if not isinstance(boost_progress_bar_enabled, bool):
                    raise AssertionError(
                        f'`boost_progress_bar_enabled` can be `bool`, got '
                        f'{boost_progress_bar_enabled.__class__.__name__}; {boost_progress_bar_enabled!r}.'
                    )
            
            data['premium_progress_bar_enabled'] = boost_progress_bar_enabled
        
        
        await self.http.guild_edit(guild_id, data, reason)
    
    
    async def guild_widget_get(self, guild):
        """
        Returns the guild's widget.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild or the guild's id, what's widget will be requested.
        
        Returns
        -------
        guild_widget : `None`, ``GuildWidget``
            If the guild has it's widget disabled returns `None` instead.
        
        Raises
        ------
        TypeError
            If `guild` was not passed neither as ``Guild``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        try:
            data = await self.http.guild_widget_get(guild_id)
        except DiscordException as err:
            if err.response.status == 403: # Widget Disabled -> return None
                return
            raise
        
        return GuildWidget(data)
    
    
    async def guild_user_get_all(self, guild):
        """
        Requests all the users of the guild and returns them.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild what's users will be requested.
        
        Returns
        -------
        users : `list` of ``ClientUserBase`` objects
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild``, nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If user caching is allowed, these users should be already loaded if the client finished starting up.
        This method takes a long time to finish for huge guilds.
        
        When using it with user account, the client's token will be invalidated.
        """
        guild_id = get_guild_id(guild)
        
        data = {'limit': 1000, 'after': 0}
        users = []
        while True:
            guild_profile_datas = await self.http.guild_user_get_chunk(guild_id, data)
            for guild_profile_data in guild_profile_datas:
                user = User.from_data(guild_profile_data['user'], guild_profile_data, guild_id)
                users.append(user)
            
            if len(guild_profile_datas) > 1000:
                break
            
            data['after'] = user.id
        
        return users
    
    
    async def guild_get_all(self):
        """
        Requests all the guilds of the client.
        
        This method is a coroutine.
        
        Returns
        -------
        guilds : `list` of ``Guild``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If the client finished starting up, all the guilds should be already loaded.
        """
        result = []
        params = {'after': 0}
        while True:
            data = await self.http.guild_get_all(params)
            result.extend(create_partial_guild_from_data(guild_data) for guild_data in data)
            if len(data) < 100:
                break
            
            params['after'] = result[-1].id
        
        return result
    
    
    async def guild_voice_region_get_all(self, guild):
        """
        Requests the available voice regions for the given guild and returns them and the optional ones.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's regions will be requested.
        
        Returns
        -------
        voice_regions : `list` of ``VoiceRegion`` objects
            The available voice regions for the guild.
        optimals : `list` of ``VoiceRegion`` objects
            The optimal voice regions for the guild.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild``, nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        data = await self.http.guild_voice_region_get_all(guild_id)
        voice_regions = []
        optimals = []
        for voice_region_data in data:
            region = VoiceRegion.from_data(voice_region_data)
            voice_regions.append(region)
            if voice_region_data['optimal']:
                optimals.append(region)
        
        return voice_regions, optimals
    
    
    async def voice_region_get_all(self):
        """
        Returns all the voice regions.
        
        This method is a coroutine.
        
        Returns
        -------
        voice_regions : `list` of ``VoiceRegion`` objects
            Received voice regions.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        data = await self.http.voice_region_get_all()
        voice_regions = []
        for voice_region_data in data:
            region = VoiceRegion.from_data(voice_region_data)
            voice_regions.append(region)
        
        return voice_regions
    
    
    async def audit_log_get_chunk(self, guild, limit=100, *, before=None, after=None, user=None, event = None):
        """
        Request a batch of audit logs of the guild and returns them. The `after`, `around` and the `before` parameters
        are mutually exclusive and they can be `int`, or as a ``DiscordEntity`` or as a `datetime`
        object.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's audit logs will be requested.
        limit : `int` = `100`, Optional
            The amount of audit logs to request. Can be between 1 and 100. Defaults to 100.
        before : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp before the audit log entries wer created.
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the audit log entries wer created.
        user : `None`, ``ClientUserBase``, `int` = `None`, Optional (Keyword only)
            Whether the audit logs should be filtered only to those, which were created by the given user.
        event : `None`, ``AuditLogEvent``, `int` = `None`, Optional (Keyword only)
            Whether the audit logs should be filtered only on the given event.
        
        Returns
        -------
        audit_log : ``AuditLog``
            A container what contains the ``AuditLogEntry``-s.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild``, nor as `int`.
            - If `after`, `before` was passed with an unexpected type.
            - If `user` is neither `None`, ``ClientUserBase``, `int`.
            - If `event` is neither `None`, ``AuditLogEvent``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `limit` was not given as `int`.
            - If `limit` is out of the expected range [1:100].
        """
        guild, guild_id = get_guild_and_id(guild)
        
        if __debug__:
            if not isinstance(limit, int):
                raise AssertionError(
                    f'`limit` can be `int`, got {limit.__class__.__name__}; {limit!r}.'
                )
            
            if limit < 1 or limit > 100:
                raise ValueError(
                    f'`limit` out of the expected range [1:100], got {limit!r}.'
                )
        
        data = {'limit': limit}
        
        if (before is not None):
            data['before'] = log_time_converter(before)
        
        if (after is not None):
            data['after'] = log_time_converter(after)
        
        if (user is not None):
            if isinstance(user, ClientUserBase):
                user_id = user.id
            
            else:
                user_id = maybe_snowflake(user)
                if user_id is None:
                    raise TypeError(
                        f'`user` can be `{ClientUserBase.__name__}`, `int`, got {user.__class__.__name__}; {user!r}.'
                    )
            
            data['user_id'] = user_id
        
        if (event is not None):
            if isinstance(event, AuditLogEvent):
                event_value = event.value
            elif isinstance(event, int):
                event_value = event
            else:
                raise TypeError(
                    f'`event` can be `None`, `{AuditLogEvent.__name__}`, `int`, got '
                    f'{event.__class__.__name__}; {event!r}.'
                )
            
            data['action_type'] = event_value
        
        data = await self.http.audit_log_get_chunk(guild_id, data)
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        return AuditLog(data, guild)
    
    
    async def audit_log_iterator(self, guild, *, user=None, event = None):
        """
        Returns an audit log iterator for the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's audit logs will be requested.
        user : `None`, ``ClientUserBase``, `int` = `None`, Optional (Keyword only)
            Whether the audit logs should be filtered only to those, which were created by the given user.
        event : `None`, ``AuditLogEvent``, `int` = `None`, Optional (Keyword only)
            Whether the audit logs should be filtered only on the given event.
        
        Returns
        -------
        audit_log_iterator : ``AuditLogIterator``
        """
        return await AuditLogIterator(self, guild, user=user, event = event)
