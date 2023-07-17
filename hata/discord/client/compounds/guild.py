__all__ = ()

import warnings

from scarletio import Compound

from ...audit_logs import AuditLog, AuditLogEvent, AuditLogIterator
from ...bases import maybe_snowflake
from ...channel import VoiceRegion
from ...guild import (
    Guild, GuildFeature, GuildPreview, GuildWidget, VerificationScreen, WelcomeScreen, create_partial_guild_from_data
)
from ...guild.guild.utils import GUILD_FIELD_CONVERTERS, create_new_guild_data
from ...guild.verification_screen.utils import VERIFICATION_SCREEN_FIELD_CONVERTERS
from ...guild.welcome_screen.utils import WELCOME_SCREEN_FIELD_CONVERTERS
from ...http import DiscordHTTPClient
from ...payload_building import build_edit_payload
from ...role import Role
from ...onboarding import OnboardingScreen
from ...onboarding.onboarding_screen.utils import ONBOARDING_FIELD_CONVERTERS
from ...user import ClientUserBase, GuildProfile, PremiumType, User, UserFlag
from ...utils import log_time_converter

from ..request_helpers import get_guild_and_id, get_guild_id, get_role_id, get_user_id


def _assert__guild_create__limit(client):
    """
    Asserts in how much guilds the client is in.
    
    Parameters
    ----------
    client : ``Client``
        The client to assert its guild creation limit of.
    """
    if client.bot:
        guild_create_limit = 10
    elif client.flags.staff:
        guild_create_limit = 200
    elif (client.premium_type is PremiumType.nitro):
        guild_create_limit = 200
    else:
        guild_create_limit = 100
    
    guild_count = len(client.guilds)
    if guild_count >= guild_create_limit:
        raise AssertionError(
            f'Guild count over creation limit; limit = {guild_create_limit}; count = {guild_count!r}.'
        )
    
    return True


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
        
        guild_preview_data = await self.http.guild_preview_get(guild_id)
        return GuildPreview.from_data(guild_preview_data)
    
    
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
            The guild what's welcome screen will be requested.
        
        Returns
        -------
        welcome_screen : ``WelcomeScreen``
        
        Raises
        ------
        TypeError
            - If `guild` is not ``Guild``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        welcome_screen_data = await self.http.welcome_screen_get(guild_id)
        return WelcomeScreen.from_data(welcome_screen_data)
    
    
    async def welcome_screen_edit(self, guild, welcome_screen_template = None, **keyword_parameters):
        """
        Edits the given guild's welcome screen.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's welcome screen will be edited.
        
        welcome_screen_template : `None`, ``WelcomeScreen``` = `None`, Optional
            Welcome screen to use as a template.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to edit the welcome screen with.
        
        Other Parameters
        ----------------
        description : `None`, `str`, Optional (Keyword only)
            Description, of what is the server about.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the welcome screen should be enabled.
        
        welcome_channels : `None`, `iterable` of ``WelcomeScreenChannel``, Optional (Keyword only)
            The featured channels by the welcome screen.
        
        Returns
        -------
        welcome_screen : ``WelcomeScreen``
        
        Raises
        ------
        TypeError
            - If `guild` is not ``Guild``, `int`.
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        data = build_edit_payload(None, welcome_screen_template, WELCOME_SCREEN_FIELD_CONVERTERS, keyword_parameters)
        welcome_screen_data = await self.http.welcome_screen_edit(guild_id, data)
        return WelcomeScreen.from_data(welcome_screen_data)
    
    
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
        """
        guild_id = get_guild_id(guild)
        
        data = build_edit_payload(
            None, verification_screen_template, VERIFICATION_SCREEN_FIELD_CONVERTERS, keyword_parameters
        )
        verification_screen_data = await self.http.verification_screen_edit(guild_id, data)
        
        return VerificationScreen.from_data(verification_screen_data)
    
    
    async def onboarding_screen_get(self, guild):
        """
        Requests the given guild's onboarding screen.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild what's onboarding screen will be requested.
        
        Returns
        -------
        onboarding_screen : ``OnboardingScreen``
        
        Raises
        ------
        TypeError
            - If `guild` is not ``Guild``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        onboarding_screen_data = await self.http.onboarding_screen_get(guild_id)
        return OnboardingScreen.from_data(onboarding_screen_data)
    
    
    async def onboarding_screen_edit(
        self, guild, onboarding_screen_template = None, *, reason = None, **keyword_parameters
    ):
        """
        Edits the guild's onboarding screen.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to edit its onboarding screen.
        
        onboarding_screen_template : `None`, ``OnboardingScreen`` = `None`, Optional
            Onboarding screen to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to edit the onboarding screen with.
        
        Returns
        -------
        onboarding_screen : ``OnboardingScreen``
        
        Other parameters
        ----------------
        default_channel_ids : `None`, `iterable` of (`int`, ``Channel``), Optional (Keyword only)
            The channels' identifiers that new members get opted into automatically.
        
        enabled : `bool`, Optional (Keyword only)
            Whether onboarding is enabled.
        
        mode : ``OnboardingMode``, `int`, Optional (Keyword only)
            Onboarding mode.
        
        prompts : `None`, `iterable` of ``OnboardingPrompt``, Optional (Keyword only)
            The prompts shown during onboarding and in customize community.
        
        Raises
        ------
        TypeError
            - If `guild` is not ``Guild``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        data = build_edit_payload(None, onboarding_screen_template, ONBOARDING_FIELD_CONVERTERS, keyword_parameters)
        
        onboarding_screen_data = await self.http.onboarding_screen_edit(guild_id, data, reason)
        return OnboardingScreen.from_data(onboarding_screen_data)
        
        
    
    
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
            guild._update_generic(data)
        
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
            guild._update_generic(data)
            channel_datas = await self.http.guild_channel_get_all(guild_id)
            guild._update_channels(channel_datas)
            
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
    
    
    async def guild_create(self, name, **keyword_parameters):
        """
        Creates a guild with the given parameter. Bot accounts can create guilds only when they have less than 10.
        User account guild limit is 100, meanwhile staff guild limit is 200.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str`
            The name of the new guild.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Additional parameters to create the guild with.
        
        Other Parameters
        ----------------
        afk_channel_id : `None`, `int`, Optional (Keyword only)
            The id of the guild's afk channel. The id should be one of the channel's id from `channels`.
        
        afk_timeout : `None`, `int` = `None`, Optional (Keyword only)
            The afk timeout for the users at the guild's afk channel.
        
        channels : `None`, `list` of (`dict<str, object>`, ``Channel``), Optional (Keyword only)
            A list of channels of the new guild. It should contain channel data objects.
        
        content_filter : ``ContentFilterLevel``, `int`, Optional (Keyword only)
            The content filter level of the guild.
        
        icon : `None`, `bytes-like`, Optional (Keyword only)
            The icon of the new guild.
        
        roles : `None`, `list` of (`dict<str, object>`, ``Role``), Optional (Keyword only)
            A list of roles of the new guild. It should contain role data objects.
        
        message_notification : ``MessageNotificationLevel``, `int`, Optional (Keyword only)
            The message notification level of the new guild.
        
        system_channel_flags : ``SystemChannelFlag``, `int`, Optional (Keyword only)
            Describe which type of messages are sent automatically to the system channel.
        
        system_channel_id: `int`, Optional (Keyword only)
            The id of the guild's system channel. The id should be one of the channel's id from `channels`.
        
        verification_level : ``VerificationLevel``, `int`, Optional (Keyword only)
            The verification level of the new guild.
        
        Returns
        -------
        guild : ``Guild``
            A partial guild made from the received data.
        
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
        assert _assert__guild_create__limit(self)
        
        data = create_new_guild_data(name = name, **keyword_parameters)
        
        data = await self.http.guild_create(data)
        # we can create only partial, because the guild data is not completed usually
        return create_partial_guild_from_data(data)
    
    
    async def guild_prune(self, guild, days, *, roles = None, count = False, reason = None):
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
        
        if count and (guild is not None) and guild.large:
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
    
    
    async def guild_prune_estimate(self, guild, days, *, roles = None):
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
        self,
        guild,
        guild_template = None,
        *,
        add_feature = ...,
        remove_feature = ...,
        reason = None,
        **keyword_parameters,
    ):
        """
        Edits the guild with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to edit.
        
        guild_template : `None`, ``Guild`` = `None`, Optional
            Guild entity to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to edit the guild with.
        
        Other Parameters
        ----------------
        afk_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The afk channel or its identifier.
        
        afk_timeout : `int`, Optional (Keyword only)
            The afk timeout at the `afk_channel`.
        
        banner : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The guild's banner.
        
        boost_progress_bar_enabled : `bool`, Optional (Keyword only)
            Whether the guild has the boost progress bar enabled.
        
        content_filter : ``ContentFilterLevel``, `int`, Optional (Keyword only)
            The explicit content filter level of the guild.
        
        description : `None`, `str`
            Description of the guild. The guild must be a Community guild.
        
        discovery_splash : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The guild's discovery splash.
        
        features : `None`, `iterable` of `(`int`, `GuildFeature``), Optional (Keyword only)
            The guild's features.
        
        hub_type : ``HubType``, `int`, Optional (Keyword only)
            The guild's hub type.
        
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The guild's icon.
        
        invite_splash : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The guild's invite splash.
        
        message_notification : ``MessageNotificationLevel``, `int`, Optional (Keyword only)
            The message notification level of the guild.
        
        mfa : ``MFA``, `int`, Optional (Keyword only)
            The required multi-factor authentication level for the guild.
        
        name : `str`, Optional (Keyword only)
            The guild's name.
        
        nsfw_level : ``NsfwLevel``, `int`, Optional (Keyword only)
            The nsfw level of the guild.
        
        owner_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The guild's owner or their id.
        
        preferred_locale : ``Locale``, `int`, Optional (Keyword only)
            The preferred language of the guild.
        
        public_updates_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel's identifier where the guild's public updates should go.
        
        rules_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where the rules of a public guild's should be.
        
        safety_alerts_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where safety alerts are sent by Discord.
        
        system_channel_flags : ``SystemChannelFlag``, `int`, Optional (Keyword only)
            Describe which type of messages are sent automatically to the system channel.
        
        system_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier where the system messages are sent.
        
        vanity_code : `None`, `str`, Optional (Keyword only)
            The guild's vanity invite's code if it has.
        
        verification_level : ``VerificationLevel``, `int`, Optional (Keyword only)
            The minimal verification needed to join or to interact with guild.
        
        widget_channel_id : `int`, ``Channel``, Optional (Keyword only)
            The channel or its identifier for which the guild's widget is for.
        
        widget_enabled : `bool`, Optional (Keyword only)
            Whether the guild's widget is enabled.
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        data = build_edit_payload(guild, guild_template, GUILD_FIELD_CONVERTERS, keyword_parameters)
        
        if (add_feature is not ...) or (remove_feature is not ...):
            warnings.warn(
                (
                    f'`add_feature` and `remove_feature` parameters are deprecated of '
                    f'`{self.__class__.__name__}.guild_edit` and they will be removed in 2023 December. '
                    f'Please use the `features` parameter accordingly.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
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
        
        if data:
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
        
        data = await self.http.guild_widget_get(guild_id)
        return GuildWidget.from_data(data)
    
    
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
        
        query_parameters = {'limit': 1000, 'after': 0}
        users = []
        while True:
            guild_profile_datas = await self.http.guild_user_get_chunk(guild_id, query_parameters)
            for guild_profile_data in guild_profile_datas:
                user = User.from_data(guild_profile_data['user'], guild_profile_data, guild_id)
                users.append(user)
            
            if len(guild_profile_datas) < 1000:
                break
            
            query_parameters['after'] = user.id
        
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
        
        query_parameters = {'after': 0, 'with_counts': True}
        while True:
            data = await self.http.guild_get_chunk(query_parameters)
            for guild_data in data:
                guild = create_partial_guild_from_data(guild_data)
                guild._update_counts_only(guild_data)
                result.append(guild)
            
            if len(data) < 100:
                break
            
            query_parameters['after'] = result[-1].id
        
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
    
    
    async def audit_log_get_chunk(self, guild, limit = 100, *, before = None, after = None, user = None, event = None):
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
        return AuditLog(data, guild_id)
    
    
    async def audit_log_iterator(self, guild, *, user = None, event = None):
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
        return AuditLogIterator(self, guild, user = user, event = event)
