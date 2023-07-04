__all__ = ()

import warnings

from scarletio import Compound

from ...channel import Channel, ChannelType, ForumTag, PermissionOverwrite, create_partial_channel_from_id
from ...channel.channel.utils import (
    CHANNEL_GUILD_FIELD_CONVERTERS, CHANNEL_GUILD_MAIN_FIELD_CONVERTERS, CHANNEL_PRIVATE_GROUP_FIELD_CONVERTERS
)
from ...channel.permission_overwrite.utils import (
    PERMISSION_OVERWRITE_FIELD_CONVERTERS, PERMISSION_OVERWRITE_PERMISSION_FIELD_CONVERTERS
)
from ...channel.forum_tag.utils import FORUM_TAG_FIELD_CONVERTERS
from ...guild import Guild, create_partial_guild_from_id
from ...http import DiscordHTTPClient
from ...payload_building import build_create_payload, build_edit_payload
from ...webhook import Webhook

from ..functionality_helpers import channel_move_sort_key
from ..request_helpers import (
    get_channel_and_id, get_channel_id, get_forum_tag_and_id, get_forum_tag_id, get_guild_and_id, get_guild_id,
    get_permission_overwrite_target_id, get_user_id
)

def _assert__channel_group_create__users(users):
    """
    Asserts the `users` parameter of ``Client.channel_group_create`.
    
    Parameters
    ----------
    users : `tuple` of ``ClientUserBase``, `int`
        The users to create the channel with.
    
    Raises
    ------
    AssertionError
        - If the total amount of users is less than `2`.
    """
    if len(users) < 2:
        raise AssertionError(
            f'group channel can be created at least with at least `2` users,  got '
            f'{len(users)}; {users!r}.'
        )
    
    return True


def _forum_tag_data_array_sort_key(forum_tag_data):
    """
    Sort key used to sort forum tag data.
    
    Parameters
    ----------
    forum_tag_data : `dict` of (`str`, `Any`) items
        Forum tag data.
    
    Returns
    -------
    sort_key : `int`
    """
    return int(forum_tag_data['id'])


class ClientCompoundChannelEndpoints(Compound):
    
    http : DiscordHTTPClient
    id : int
    bot : bool
    private_channels : dict
    
    
    async def channel_group_leave(self, channel):
        """
        Leaves the client from the specified group channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to leave from.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, Channel.is_private_group)
        
        await self.http.channel_group_leave(channel_id)
    
    
    async def channel_group_user_add(self, channel, *users):
        """
        Adds the users to the given group channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to add the `users` to.
        *users : ``ClientUserBase``, `int`
            The users to add to the `channel`.
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``Channel`` nor `int`.
            - If `users` contains non ``ClientUserBase``, neither `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, Channel.is_private_group)
        
        user_ids = set()
        for user in users:
            user_id = get_user_id(user)
            user_ids.add(user_id)
        
        for user_id in user_ids:
            await self.http.channel_group_user_add(channel_id, user_id)
    
    
    async def channel_group_user_delete(self, channel, *users):
        """
        Removes the users from the given group channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel from where the `users` will be removed.
        *users : ``ClientUserBase``, `int`
            The users to remove from the `channel`.
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``Channel`` nor `int`.
            - If `users` contains non ``ClientUserBase``, neither `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, Channel.is_private_group)
        
        user_ids = set()
        for user in users:
            user_id = get_user_id(user)
            user_ids.add(user_id)
        
        for user_id in user_ids:
            await self.http.channel_group_user_delete(channel_id, user_id)
    
    
    async def channel_group_edit(self, channel, channel_template = None, **keyword_parameters):
        """
        Edits the given group channel. Only the provided parameters will be edited.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to edit.
        
        channel_template : `None`, ``Channel`` = `None`, Optional
            A channel to use as a template.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to define which fields should be modified.
        
        Other Parameters
        ----------------
        icon : `None`, `bytes-like`, Optional (Keyword only)
            The new icon of the channel. By passing `None` your can remove the actual one.
        
        name : `None`, `str`, Optional (Keyword only)
            The new name of the channel. By passing `None` or an empty string you can remove the actual one.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        Notes
        -----
        No request is done if no optional parameter is provided.
        """
        channel_id = get_channel_id(channel, Channel.is_private_group)
        data = build_edit_payload(channel, channel_template, CHANNEL_PRIVATE_GROUP_FIELD_CONVERTERS, keyword_parameters)

        if data:
            await self.http.channel_group_edit(channel_id, data)
    
    
    async def channel_group_create(self, *users):
        """
        Creates a group channel with the given users.
        
        This method is a coroutine.
        
        Parameters
        ----------
        *users : ``ClientUserBase``, `int`
            The users to create the channel with.
        
        Returns
        -------
        channel : ``Channel``
            The created group channel.
        
        Raises
        ------
        TypeError
            If `users` contain not only ``User`, ``Client``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This endpoint does not support bot accounts.
        """
        assert _assert__channel_group_create__users(users)
        
        user_ids = set()
        for user in users:
            user_id = get_user_id(user)
            user_ids.add(user_id)
        
        user_ids.add(self.id)
        
        data = {'recipients': user_ids}
        data = await self.http.channel_group_create(self.id, data)
        return Channel.from_data(data, self, 0)
    
    
    async def channel_private_create(self, user):
        """
        Creates a private channel with the given user. If there is an already cached private channel with the user,
        returns that.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ``ClientUserBase``, `int`
            The user to create the private with.
        
        Returns
        -------
        channel : ``Channel``
            The created private channel.
        
        Raises
        ------
        TypeError
            If `user` was not given neither as ``ClientUserBase`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        user_id = get_user_id(user)
        
        try:
            channel = self.private_channels[user_id]
        except KeyError:
            data = await self.http.channel_private_create({'recipient_id': user_id})
            channel = Channel.from_data(data, self, 0)
        
        return channel
    
    
    async def channel_private_get_all(self):
        """
        Request the client's private + group channels and returns them in a list. At the case of bot accounts the
        request returns an empty list, so we skip it.
        
        This method is a coroutine.
        
        Returns
        -------
        channels : `list` of (``Channel``, ``Channel``) objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channels = []
        if (not self.bot):
            data = await self.http.channel_private_get_all()
            for channel_data in data:
                channel = Channel.from_data(channel_data, self, 0)
                channels.append(channel)
        
        return channels
    
    
    async def channel_move(self, channel, visual_position, *, parent=..., lock_permissions = False, reason = None):
        """
        Moves a guild channel to the given visual position under it's parent, or guild. If the algorithm can not
        place the channel exactly on that location, it will place it as close, as it can. If there is nothing to
        move, then the request is skipped.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``
            The channel to be moved.
        visual_position : `int`
            The visual position where the channel should go.
        parent : `None`, ``Channel``, Optional (Keyword only)
            If not set, then the channel will keep it's current parent. If the parameter is set ``Guild`` or to
            `None`, then the  channel will be moved under the guild itself, Or if passed as ``Channel``,
            then the channel will be moved under it.
        lock_permissions : `bool` = `False`, Optional (Keyword only)
            If you want to sync the permissions with the new category set it to `True`. Defaults to `False`.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        ValueError
            - If the `channel` would be between guilds.
            - If parent channel would be moved under an other category.
        TypeError
            - If `channel` was isn ot movable.
            - If `parent` was not given as `None`, ``Channel``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This method also fixes the messy channel positions of Discord to an intuitive one.
        """
        # Check channel type
        if (not channel.is_in_group_guild_sortable()) and (not channel.partial):
            raise TypeError(
                f'`channel` can be any movable guild channel, got {channel.__class__.__name__}; {channel!r}.'
            )
        
        # Check whether the channel is partial.
        guild = channel.guild
        if guild is None:
            # Cannot move partial channels, leave
            return
        
        # Check parent
        if parent is ...:
            parent = channel.parent
        elif parent is None:
            parent = None
        elif isinstance(parent, Channel):
            if parent.guild is not guild:
                raise ValueError(
                    f'Can not move channel between guilds! Channel\'s guild: {guild!r}; Category\'s '
                    f'guild: {parent.guild!r}'
                )
        else:
            raise TypeError(
                f'`parent` can be `None` or {Channel.__name__}`, got {parent.__class__.__name__}; {parent!r}.'
            )
        
        # Cannot put category under category
        if isinstance(parent, Channel) and channel.is_guild_category() and (not channel.partial):
            raise ValueError(
                f'Can not move category channel under category channel. channel = {channel!r}; parent = {parent!r}'
            )
        
        if not isinstance(visual_position, int):
            raise TypeError(
                f'`visual_position` can be `int`, got {visual_position.__class__.__name__}; '
                f'{visual_position!r}.'
            )
        
        if not isinstance(lock_permissions, bool):
            raise TypeError(
                f'`lock_permissions` can be `bool`, got {lock_permissions.__class__.__name__}; {lock_permissions!r}.'
            )
        
        # Cap at 0
        if visual_position < 0:
            visual_position = 0
        
        # If the channel is where it should be, we can leave.
        if (parent is not None):
            # Add `parent is not None` check for the linter
            if (channel.parent is parent) and (parent.channels.index(channel) == visual_position):
                return
        
        # Create a display state, where each channel is listed.
        # Categories are inside of a tuple, where they are the first element of it and their channels are the second.
        display_state = guild.channel_list
        
        for index in range(len(display_state)):
            iter_channel = display_state[index]
            if iter_channel.is_guild_category():
                display_state[index] = iter_channel, iter_channel.channels
        
        # Generate a state where the channels are theoretically ordered with tuples
        display_new = []
        for iter_channel in display_state:
            if isinstance(iter_channel, tuple):
                iter_channel, sub_channels = iter_channel
                display_sub_channels = []
                for sub_channel in sub_channels:
                    channel_key = (sub_channel.order_group, sub_channel.position, sub_channel.id, None)
                    display_sub_channels.append(channel_key)
            else:
                display_sub_channels = None
            
            channel_key = (iter_channel.order_group, iter_channel.position, iter_channel.id, display_sub_channels)
            
            display_new.append(channel_key)
        
        # We have 2 display states, we will compare the old to the new one when calculating differences, but we didn't
        # move our channel yet!
        
        # We get from where we will move from.
        old_parent = channel.parent
        if isinstance(old_parent, Guild):
            move_from = display_new
        else:
            old_parent_id = old_parent.id
            for channel_key in display_new:
                if channel_key[2] == old_parent_id:
                    move_from = channel_key[3]
                    break
            
            else:
                # If no breaking was not done, our channel not exists, lol
                return
        
        # We got from which thing we will move from, so we remove first
        
        channel_id = channel.id
        
        for index in range(len(move_from)):
            channel_key = move_from[index]
            
            if channel_key[2] == channel_id:
                channel_key_to_move = channel_key
                del move_from[index]
                break
        
        else:
            # If breaking was not done, our channel not exists, lol
            return
        
        # We get to where we will move to.
        if parent is None:
            move_to = display_new
        else:
            new_parent_id = parent.id
            for channel_key in display_new:
                if channel_key[2] == new_parent_id:
                    move_to = channel_key[3]
                    break
            
            else:
                # If no breaking was not done, our channel not exists, lol
                return
        
        # Move, yayyy
        move_to.insert(visual_position, channel_key_to_move)
        # Reorder
        move_to.sort(key = channel_move_sort_key)
        
        # Now we resort every channel in the guild and categories, mostly for security issues
        to_sort_all = [display_new]
        for channel_key in display_new:
            display_sub_channels = channel_key[3]
            if display_sub_channels is not None:
                to_sort_all.append(display_sub_channels)
        
        ordered = []
        
        for to_sort in to_sort_all:
            expected_channel_order_group = 0
            channel_position = 0
            for sort_key in to_sort:
                channel_order_group = sort_key[0]
                channel_id = sort_key[2]
                
                if channel_order_group != expected_channel_order_group:
                    expected_channel_order_group = channel_order_group
                    channel_position = 0
                
                ordered.append((channel_position, channel_id))
                channel_position += 1
                continue
        
        bonus_data = {'lock_permissions': lock_permissions}
        if parent is None:
            parent_id = None
        else:
            parent_id = parent.id
        bonus_data['parent_id'] = parent_id
        
        data = []
        channels = guild.channels
        for position, channel_id in ordered:
            channel_ = channels[channel_id]
            
            if channel is channel_:
                data.append({'id': channel_id, 'position': position, **bonus_data})
                continue
            
            if channel_.position != position:
                data.append({'id': channel_id, 'position': position})
        
        await self.http.channel_move(guild.id, data, reason)
    
    
    async def channel_edit(
        self, channel, channel_template = None, *, reason = None, **keyword_parameters,
    ):
        """
        Edits the given guild channel. Different channel types accept different fields, so make sure to not pass
        out of place parameters. Only the given fields will be modified of the channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to edit.
        
        channel_template : `None`, ``Channel`` = `None`, Optional
            A channel to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters either to define the template, or to overwrite specific fields' values.
        
        Other Parameters
        ----------------
        bitrate : `int`, Optional (Keyword only)
            The bitrate (in bits) of the voice channel.
        
        default_forum_layout : ``ForumLayout``, `int`, Optional (Keyword only)
            The default layout used to display threads of the forum.
        
        default_sort_order : ``SortOrder``, `int`, Optional (Keyword only)
            The default thread ordering of the forum.
        
        default_thread_auto_archive_after : `int`, Optional (Keyword only)
            The default duration (in seconds) for newly created threads to automatically archive the themselves.
        
        default_thread_reaction : `None`, ``Emoji``, Optional (Keyword only)
            The emoji to show in the add reaction button on a thread of the forum channel.
                
        default_thread_slowmode : `int`, Optional (Keyword only)
            The default slowmode applied to the channel's threads.
        
        flags : `int`, ``ChannelFlag``, Optional (Keyword only)
            The channel's flags.
        
        name : `str`, Optional (Keyword only)
            The channel's name.
        
        nsfw : `bool`, Optional (Keyword only)
            Whether the channel is marked as non safe for work.
        
        parent_id : `None`, `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        
        permission_overwrites : `None`, list` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        
        position : `int`, Optional (Keyword only)
            The channel's position.
        
        region : `None`, ``VoiceRegion``, `str`, Optional (Keyword only)
            The channel's voice region.
        
        slowmode : `int`, Optional (Keyword only)
            The channel's slowmode.
        
        topic : `None`, `str`, Optional (Keyword only)
            The channel's topic.
        
        users : `iterable` of (`int`, ``ClientUserBase``), Optional (Keyword only)
            The users in the channel.
        
        video_quality_mode : ``VideoQualityMode``, Optional (Keyword only)
            The video quality of the voice channel.
        
        Raises
        ------
        TypeError
            - If any parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel, channel_id = get_channel_and_id(channel, Channel.is_in_group_guild)
        data = build_edit_payload(channel, channel_template, CHANNEL_GUILD_FIELD_CONVERTERS, keyword_parameters)
        
        if data:
            await self.http.channel_edit(channel_id, data, reason)
    
    
    async def channel_create(
        self, 
        guild,
        channel_template = None,
        type_ = ...,
        *,
        channel_type = ChannelType.guild_text,
        reason = None,
        **keyword_parameters,
    ):
        """
        Creates a new channel at the given `guild`. If the channel is successfully created returns it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild where the channel will be created.
        
        channel_template : `None`, ``Channel`` = `None`, Optional
            Channel entity to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the `guild`'s audit logs.
        
        channel_type : ``ChannelType``, `int` = ``ChannelType.guild_text``, Optional (Keyword only)
            The type of the created channel.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to create the channel with.
        
        Other Parameters
        ----------------
        bitrate : `int`, Optional (Keyword only)
            The bitrate (in bits) of the voice channel.
        
        default_forum_layout : ``ForumLayout``, `int`, Optional (Keyword only)
            The default layout used to display threads of the forum.
        
        default_sort_order : ``SortOrder``, `int`, Optional (Keyword only)
            The default thread ordering of the forum.
        
        default_thread_auto_archive_after : `int`, Optional (Keyword only)
            The default duration (in seconds) for newly created threads to automatically archive the themselves.
        
        default_thread_reaction : `None`, ``Emoji``, Optional (Keyword only)
            The emoji to show in the add reaction button on a thread of the forum channel.
                
        default_thread_slowmode : `int`, Optional (Keyword only)
            The default slowmode applied to the channel's threads.
        
        flags : `int`, ``ChannelFlag``, Optional (Keyword only)
            The channel's flags.
        
        name : `str`, Optional (Keyword only)
            The channel's name.
        
        nsfw : `bool`, Optional (Keyword only)
            Whether the channel is marked as non safe for work.
        
        parent_id : `None`, `int`, ``Channel``, Optional (Keyword only)
            The channel's parent's identifier.
        
        permission_overwrites : `None`, list` of ``PermissionOverwrite``, Optional (Keyword only)
            The channel's permission overwrites.
        
        position : `int`, Optional (Keyword only)
            The channel's position.
        
        region : `None`, ``VoiceRegion``, `str`, Optional (Keyword only)
            The channel's voice region.
        
        slowmode : `int`, Optional (Keyword only)
            The channel's slowmode.
        
        topic : `None`, `str`, Optional (Keyword only)
            The channel's topic.
        
        users : `iterable` of (`int`, ``ClientUserBase``), Optional (Keyword only)
            The users in the channel.
            
        video_quality_mode : ``VideoQualityMode``, Optional (Keyword only)
            The video quality of the voice channel.
        
        Returns
        -------
        channel : ``Channel``
        
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
        guild_id = get_guild_id(guild)
        
        # Checkout type
        if type_ is not ...:
            warnings.warn(
                (
                    f'`type_` parameter of `{self.__class__.__name__}.channel_create` is deprecated and will be '
                    f'removed in 2023 February. Please use `channel_type` instead.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            channel_type = type_
        
        keyword_parameters['channel_type'] = channel_type
        
        # Checkout name
        if (channel_template is not None) and isinstance(channel_template, str) and ('name' not in keyword_parameters):
            warnings.warn(
                (
                    f'`name` parameter of `{self.__class__.__name__}.channel_create` is moved to be a keyword only '
                    f'parameter and the positional usage is deprecated and will be removed in 2023 February.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            keyword_parameters['name'] = channel_template
            channel_template = None
        
        data = build_create_payload(channel_template, CHANNEL_GUILD_MAIN_FIELD_CONVERTERS, keyword_parameters)
        channel_data = await self.http.channel_create(guild_id, data, reason)
        
        return Channel.from_data(channel_data, self, guild_id)
    
    
    async def channel_delete(self, channel, *, reason = None):
        """
        Deletes the specified guild channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If the given `channel` is not ``Channel``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If a category channel is deleted, it's sub-channels will not be removed, instead they will move under the guild.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild)
        
        await self.http.channel_delete(channel_id, reason)
    
    
    async def channel_follow(self, source_channel, target_channel):
        """
        Follows the `source_channel` with the `target_channel`. Returns the webhook, what will crosspost the published
        messages.
        
        This method is a coroutine.
        
        Parameters
        ----------
        source_channel : ``Channel``, `int`
            The channel what will be followed. Must be an announcements channel.
        target_channel : ``Channel``, `int`instance
            The target channel where the webhook messages will be sent. Can be any guild text channel type.
        
        Returns
        -------
        webhook : ``Webhook``
            The webhook what will crosspost the published messages. This webhook has no `.token` set.
        
        Raises
        ------
        TypeError
            - If the `source_channel` was not given neither as ``Channel`` nor `int`.
            - If the `target_channel` was not given neither as ``Channel`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        source_channel, source_channel_id = get_channel_and_id(source_channel, Channel.is_guild_announcements)
        if source_channel is None:
            source_channel = create_partial_channel_from_id(source_channel_id, ChannelType.guild_announcements, 0)
        
        target_channel_id = get_channel_id(target_channel, Channel.is_in_group_guild_system)
        
        data = {
            'webhook_channel_id': target_channel_id,
        }
        
        data = await self.http.channel_follow(source_channel_id, data)
        webhook = await Webhook._from_follow_data(data, source_channel, target_channel_id, self)
        return webhook
    

    async def permission_overwrite_edit(self, channel, permission_overwrite, *, reason = None, **keyword_parameters):
        """
        Edits the given permission overwrite.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ˙˙Channel``, `int`
            The channel where the permission overwrite is.
        
        permission_overwrite : ``PermissionOverwrite``
            The permission overwrite to edit.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters either to define the template, or to overwrite specific fields' values.
        
        Other Parameters
        ----------------
        allow : `None`, ``Permission``, `int`, Optional (Keyword only)
            The permission overwrite's allowed permission's value.
        
        deny : `None`, ``Permission``, `int`, Optional (Keyword only)
            The permission overwrite's denied permission's value.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_sortable)
        target_id = get_permission_overwrite_target_id(permission_overwrite)
        
        data = build_create_payload(
            permission_overwrite, PERMISSION_OVERWRITE_PERMISSION_FIELD_CONVERTERS, keyword_parameters
        )
        
        await self.http.permission_overwrite_create(channel_id, target_id, data, reason)
    
    
    async def permission_overwrite_delete(self, channel, permission_overwrite, *, reason = None):
        """
        Deletes the given permission overwrite.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ˙˙Channel``
            The channel where the permission overwrite is.
        
        permission_overwrite : ``PermissionOverwrite``, `int`
            The permission overwrite to delete.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.

        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_sortable)
        target_id = get_permission_overwrite_target_id(permission_overwrite)
        
        await self.http.permission_overwrite_delete(channel_id, target_id, reason)
    
    
    async def permission_overwrite_create(
        self, channel, permission_overwrite_template = None, *, reason = None, **keyword_parameters
    ):
        """
        Creates a permission overwrite at the given channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to what the permission overwrite will be added.
        
        permission_overwrite_template : `None`, ``PermissionOverwrite`` = `None`, Optional
            Permission overwrite to be used as a template for creating the new one.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters either to define the template, or to overwrite specific fields' values.
        
        Other Parameters
        ----------------
        allow : `None`, ``Permission``, `int`, Optional (Keyword only)
            The permission overwrite's allowed permission's value.
        
        deny : `None`, ``Permission``, `int`, Optional (Keyword only)
            The permission overwrite's denied permission's value.
        
        target : `int`, ``Role``, ``ClientUserBase``, Optional (Keyword only)
            The permission overwrite's target. Shortcut for defining `target_id` and `target_type` with 1 parameter.
        
        target_id : `int`, Optional (Keyword only)
            The permission overwrite's target's identifier.
        
        target_type : `None`, ``PermissionOverwriteTargetType``, Optional (Keyword only)
            The permission overwrite's target's type. Required if `target_id` is given as a snowflake.
        
        
        Returns
        -------
        permission_overwrite : ``PermissionOverwrite``
            A permission overwrite, what estimatedly is same as the one what Discord will create.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_sortable)
        
        if (
            (permission_overwrite_template is not None) and
            (not isinstance(permission_overwrite_template, PermissionOverwrite)) and
            ('target' not in keyword_parameters)
        ):
            warnings.warn(
                (
                    f'`target` parameter of `{self.__class__.__name__}.permission_overwrite_create` is moved to be '
                    f'a keyword only parameter and the positional usage is deprecated and will be removed in 2023 '
                    f'February.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            keyword_parameters['target'] = permission_overwrite_template
        
        data = build_create_payload(
            permission_overwrite_template, PERMISSION_OVERWRITE_FIELD_CONVERTERS, keyword_parameters
        )
        
        try:
            target_id = data['id']
        except KeyError:
            raise RuntimeError(
                f'Cannot create permission overwrite to unknown target. Parameters are already destructed, no '
                f'additional context is providable.'
            )
        
        await self.http.permission_overwrite_create(channel_id, target_id, data, reason)
        return PermissionOverwrite.from_data(data)
    
    
    async def guild_channel_get_all(self, guild):
        """
        Requests the given guild's channels and if there any de-sync between the wrapper and Discord, applies the
        changes.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's channels will be requested.
        
        Returns
        -------
        channels : `list` of ``Channel``
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild``, nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        data = await self.http.guild_channel_get_all(guild_id)
        if guild is None:
            guild = create_partial_guild_from_id(guild_id)
        
        guild._update_channels(data)
        
        return [*guild.channels.values()]
    
    
    async def forum_tag_create(self, forum_channel, forum_tag = None, *, reason = None, **keyword_parameters):
        """
        Creates a new forum tag in the channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        forum_channel : ``Channel``, `int`
            The channel to create the tag in.
        
        forum_tag : ``ForumTag``, `None` = `None`, Optional
            A forum tag which can be used as a template for the newly created tag.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters either to define the template, or to overwrite specific fields' values.
        
        Other Parameters
        ----------------
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            The tag's emoji.
            
        moderated : `bool`, Optional (Keyword only)
            Whether this tag can only be added or removed by a user with `manage_threads` permission.
        
        name : `str`, Optional (Keyword only)
            The tag's name.
        
        Returns
        -------
        forum_tag : `None`, ``ForumTag``
            The created forum tag.
        
        Raises
        ------
        TypeError
            If a parameter's type is not acceptable.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        A forum channel can have up to 25 tags.
        
        See Also
        --------
        - ``.forum_tag_delete`` : Delete a forum tag.
        - ``.forum_tag_edit`` : Modify a forum tag.
        """
        channel_id = get_channel_id(forum_channel, Channel.is_in_group_forum)
        data = build_create_payload(forum_tag, FORUM_TAG_FIELD_CONVERTERS, keyword_parameters)
        
        channel_data = await self.http.forum_tag_create(channel_id, data, reason)
        
        # Fixing discord bug: Returns channel data instead of forum tag.
        available_tag_data_array = channel_data.get('available_tags', None)
        if (available_tag_data_array is None) or (not available_tag_data_array):
            # Cannot build forum tag from nothing, eww..
            return None
        
        available_tag_data_array = sorted(
            available_tag_data_array, key = _forum_tag_data_array_sort_key, reverse = True
        )
        
        for forum_tag_data in available_tag_data_array:
            for key, value in data.items():
                if forum_tag_data.get(key, None) != value:
                    break
            
            else:
                # All fields matched.
                break
            
            continue
        
        else:
            # If no fields matched, return the newest tag.
            forum_tag_data = available_tag_data_array[0]
        
        return ForumTag.from_data(forum_tag_data)
    
    
    async def forum_tag_edit(
        self, forum_channel, forum_tag, template_forum_tag = None, *, reason = None, **keyword_parameters
    ):
        """
        Edits the given forum tag.
        
        This method is a coroutine.
        
        Parameters
        ----------
        forum_channel : ``Channel``, `int`
            The channel to edit the tag in.
        
        forum_tag : ``ForumTag``, `int`
            The forum tag to edit.
        
        template_forum_tag : ``ForumTag``, `None` = `None`, Optional
            A forum tag which can be used as a template for edition.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters either to define the template, or to overwrite specific fields' values.
        
        Other Parameters
        ----------------
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            The tag's emoji.
            
        moderated : `bool`, Optional (Keyword only)
            Whether this tag can only be added or removed by a user with `manage_threads` permission.
        
        name : `str`, Optional (Keyword only)
            The tag's name.
        
        Raises
        ------
        TypeError
            If a parameter's type is not acceptable.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        See Also
        --------
        - ``.forum_tag_create`` : Create a forum tag.
        - ``.forum_tag_delete`` : Delete a forum tag.
        """
        channel_id = get_channel_id(forum_channel, Channel.is_in_group_forum)
        forum_tag, forum_tag_id = get_forum_tag_and_id(forum_tag)
        data = build_edit_payload(forum_tag, template_forum_tag, FORUM_TAG_FIELD_CONVERTERS, keyword_parameters)
        
        if data:
            # Fixing discord bug: name.BASE_TYPE_REQUIRED('This field is required')
            if (forum_tag is not None) and ('name' not in data):
                data['name'] = forum_tag.name
            
            await self.http.forum_tag_edit(channel_id, forum_tag_id, data, reason)
    
    
    async def forum_tag_delete(self, forum_channel, forum_tag, *, reason = None):
        """
        Deletes the given forum tag.
        
        Parameters
        ----------
        forum_channel : ``Channel``, `int`
            The channel to edit the tag in.
        
        forum_tag : ``ForumTag``, `int`
            The forum tag to delete.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If a parameter's type is not acceptable.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        See Also
        --------
        - ``.forum_tag_create`` : Create a forum tag.
        - ``.forum_tag_edit`` : Modify a forum tag.
        """
        channel_id = get_channel_id(forum_channel, Channel.is_in_group_forum)
        forum_tag_id = get_forum_tag_id(forum_tag)
        await self.http.forum_tag_delete(channel_id, forum_tag_id, reason)
