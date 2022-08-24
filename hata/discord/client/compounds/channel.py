__all__ = ()

import reprlib, warnings

from scarletio import Compound

from ...channel import (
    CHANNEL_TYPES, Channel, cr_pg_channel_object, create_partial_channel_from_id, get_channel_type_name
)
from ...channel.utils import (
    _assert_channel_type, _maybe_add_channel_bitrate_field_to_data,
    _maybe_add_channel_default_auto_archive_after_field_to_data, _maybe_add_channel_nsfw_field_to_data,
    _maybe_add_channel_region_field_to_data, _maybe_add_channel_slowmode_field_to_data,
    _maybe_add_channel_topic_field_to_data, _maybe_add_channel_user_limit_field_to_data,
    _maybe_add_channel_video_quality_mode_field_to_data
)
from ...guild import Guild, create_partial_guild_from_id
from ...http import DiscordHTTPClient, VALID_ICON_MEDIA_TYPES
from ...permission import Permission, PermissionOverwrite, PermissionOverwriteTargetType
from ...role import Role
from ...user import ClientUserBase
from ...utils import get_image_media_type, image_to_base64
from ...webhook import Webhook

from ..functionality_helpers import channel_move_sort_key
from ..request_helpers import get_channel_and_id, get_channel_id, get_guild_and_id, get_user_id


def _assert__channel_group_edit__name(name):
    """
    Asserts the the `name` parameter of ``Client.channel_group_edit`.
    
    Parameters
    ----------
    name : `Ellipsis`, `None`, `str`
        The new name of the channel.
    
    Raises
    ------
    AssertionError
        - If `name` was not given neither as `None`, `str`.
        - If `name`'s length is out of range `[1:100]`.
    """
    if (name is not ...) and (name is not None):
        if not isinstance(name, str):
            raise AssertionError(
                f'`name` can be `None`, `str`, got {name.__class__.__name__}; {name!r}.'
            )
            
        name_length = len(name)
        if name_length > 100:
            raise AssertionError(
                f'`name` length can be in range [0:100], got {name_length}; {name!r}.'
            )
    
    return True


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


def _assert__channel_edit__name(name):
    """
    Asserts the the `name` parameter of ``Client.channel_edit`.
    
    Parameters
    ----------
    name : `Ellipsis`, `str`
        The new name of the channel.
    
    Raises
    ------
    AssertionError
        - If `name` was not given neither as `None`, `str`.
        - If `name`'s length is out of range `[1:100]`.
    """
    if (name is not ...) and (name is not None):
        if not isinstance(name, str):
            raise AssertionError(
                f'`name` can be `None`, `str`, got {name.__class__.__name__}; {name!r}.'
            )
            
        name_length = len(name)
        if (name_length < 1) or (name_length > 100):
            raise AssertionError(
                f'`name` length can be in range [1:100], got {name_length}; {name!r}.'
            )
    
    return True


def _assert__channel_edit__type(type_, channel, channel_type):
    """
    Asserts the the `type_` parameter of ``Client.channel_edit`.
    
    Parameters
    ----------
    type_ : `Ellipsis`, `int`
        The `channel`'s new type value.
    channel : `None`, ``Channel``
        The respective channel.
    channel_type : `int`
        The respective channel's type.
    
    Raises
    ------
    AssertionError
        - If `type_` is not `int` instance.
        - If cannot interchange to `type_`.
    """
    if (type_ is not ...):
        if (channel is not None):
            _assert_channel_type(
                channel_type,
                channel,
                (CHANNEL_TYPES.guild_text, CHANNEL_TYPES.guild_announcements),
                'type_',
                type_,
            )
        
        if not isinstance(type_, int):
            raise AssertionError(
                f'`type_` can be `int`, got {type_.__class__.__name__}.; {type_!r}'
            )
        
        if type_ not in (CHANNEL_TYPES.guild_text, CHANNEL_TYPES.guild_announcements):
            raise AssertionError(
                f'`type_` can be interchanged to `{CHANNEL_TYPES.guild_text!r}` '
                f'(`{get_channel_type_name(CHANNEL_TYPES.guild_text)}`) ,'
                f'`{CHANNEL_TYPES.guild_announcements!r}` '
                f'(`{get_channel_type_name(CHANNEL_TYPES.guild_announcements)}`)'
                f', got {type_!r} (`{get_channel_type_name(type_)}`).'
            )
    
    return True


def _assert__permission_overwrite__type(permission_overwrite):
    """
    Asserts the `permission_overwrite` parameter of ``Client.permission_overwrite_edit`` and of
    ``Client.permission_overwrite_create``.
    
    Parameters
    ----------
    permission_overwrite : ``PermissionOverwrite``
        The permission overwrite to edit.
    
    Raises
    ------
    AssertionError
        - If `permission_overwrite` was not given as ``PermissionOverwrite``.
    """
    if not isinstance(permission_overwrite, PermissionOverwrite):
        raise AssertionError(
            f'`permission_overwrite` can be `{PermissionOverwrite.__name__}`, got '
            f'{permission_overwrite.__class__.__name__}; {permission_overwrite!r}.'
        )
    
    return True


def _assert__permission_overwrite_edit__allow(allow):
    if (allow is not ...):
        if not isinstance(allow, int):
            raise AssertionError(
                f'`allow` can be `None`, `{Permission.__name__}`, `int`, got '
                f'{allow.__class__.__name__}; {allow!r}.'
            )
    
    return True


def _assert__permission_overwrite_edit__deny(deny):
    if (deny is not ...):
        if not isinstance(deny, int):
            raise AssertionError(
                f'`deny` can be `None`, `{Permission.__name__}`, `int`, got '
                f'{deny.__class__.__name__}; {deny!r}.'
            )
    
    return True


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
    
    
    async def channel_group_edit(self, channel, *, name=..., icon=...):
        """
        Edits the given group channel. Only the provided parameters will be edited.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to edit.
        name : `None`, `str`, Optional (Keyword only)
            The new name of the channel. By passing `None` or an empty string you can remove the actual one.
        icon : `None`, `bytes-like`, Optional (Keyword only)
            The new icon of the channel. By passing `None` your can remove the actual one.
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``Channel`` nor `int`.
            - If `name` is neither `None`, `str`.
            - If `icon` is neither `None`, `bytes-like`.
        ValueError
            - If `name` is passed as `str`, but it's length is `1`, or over `100`.
            - If `icon` is passed as `bytes-like`, but it's format is not any of the expected formats.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        Notes
        -----
        No request is done if no optional parameter is provided.
        """
        channel_id = get_channel_id(channel, Channel.is_private_group)
        
        assert _assert__channel_group_edit__name(name)
        
        data = {}
        
        
        if (name is not ...):
            if (name is not None) and (not name):
                name = None
            
            data['name'] = name
        
        if (icon is not ...):
            if icon is None:
                icon_data = None
            
            else:
                if not isinstance(icon, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`icon` can be `None`, `bytes-like`, got {icon.__class__.__name__}; {reprlib.repr(icon)}.'
                    )
            
                media_type = get_image_media_type(icon)
                if media_type not in VALID_ICON_MEDIA_TYPES:
                    raise ValueError(
                        f'Invalid `icon` type: {media_type}; got {reprlib.repr(icon)}.'
                    )
                
                icon_data = image_to_base64(icon)
            
            data['icon'] = icon_data
        
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
        return Channel(data, self, 0)
    
    
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
            channel = Channel(data, self, 0)
        
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
                channel = Channel(channel_data, self, 0)
                channels.append(channel)
        
        return channels
    
    
    async def channel_move(self, channel, visual_position, *, parent=..., lock_permissions=False, reason=None):
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
        if (not channel.is_in_group_guild_movable()) and (not channel.partial):
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
                f'Can not move category channel under category channel. channel={channel!r}; parent={parent!r}'
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
            if (channel.parent is parent) and (parent.channel_list.index(channel) == visual_position):
                return
        
        # Create a display state, where each channel is listed.
        # Categories are inside of a tuple, where they are the first element of it and their channels are the second.
        display_state = guild.channel_list
        
        for index in range(len(display_state)):
            iter_channel = display_state[index]
            if iter_channel.is_guild_category():
                display_state[index] = iter_channel, iter_channel.channel_list
        
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
        move_to.sort(key=channel_move_sort_key)
        
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
        self, channel, *, name=..., topic=..., nsfw=..., slowmode=..., user_limit=..., bitrate=..., region=...,
        video_quality_mode=..., type_=..., default_auto_archive_after=..., reason=None
    ):
        """
        Edits the given guild channel. Different channel types accept different parameters, so make sure to not pass
        out of place parameters. Only the passed parameters will be edited of the channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to edit.
        
        bitrate : `int`, Optional (Keyword only)
            The new bitrate of the `channel`.
        
        default_auto_archive_after : `None`, `int`, Optional (Keyword only)
            The default duration (in seconds) for newly created threads to automatically archive the themselves. Can be
            one of: `3600`, `86400`, `259200`, `604800`.
        
        name : `str`, Optional (Keyword only)
            The `channel`'s new name.
        
        nsfw : `bool`, Optional (Keyword only)
            Whether the `channel` will be nsfw or not.
        
        region : `None`, ``VoiceRegion``, `str`, Optional (Keyword only)
            The channel's new voice region.
            
            > By giving as `None`, you can remove the old value.
        
        slowmode : `int`, Optional (Keyword only)
            The new slowmode value of the `channel`.
        
        topic : `str`, Optional (Keyword only)
            The new topic of the `channel`.
        
        type_ : `int`, Optional (Keyword only)
            The `channel`'s new type value.
        
        user_limit : `int`, Optional (Keyword only)
            The new user limit of the `channel`.
        
        video_quality_mode : ``VideoQualityMode``, `int`, Optional (Keyword only)
            The channel's new video quality mode.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - If the given `channel` is not ``Channel``, `int`.
            - If `region` was not given neither as `None`, `str` nor ``VoiceRegion``.
            - If `video_quality_mode` was not given neither as ``VideoQualityMode` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel, channel_id = get_channel_and_id(channel, Channel.is_in_group_guild)
        
        assert _assert__channel_edit__name(name)
        
        channel_data = {}
        
        if (name is not ...):
            channel_data['name'] = name
        
        if channel is None:
            channel_type = -1
        else:
            channel_type = channel.type
        
        assert _assert__channel_edit__type(type_, channel, channel_type)
        
        if (type_ is not ...):
            channel_data['type'] = type_
        
        
        _maybe_add_channel_topic_field_to_data(channel_type, channel, channel_data, topic)
        _maybe_add_channel_nsfw_field_to_data(channel_type, channel, channel_data, nsfw)
        _maybe_add_channel_slowmode_field_to_data(channel_type, channel, channel_data, slowmode)
        _maybe_add_channel_bitrate_field_to_data(channel_type, channel, channel_data, bitrate)
        _maybe_add_channel_user_limit_field_to_data(channel_type, channel, channel_data, user_limit)
        _maybe_add_channel_region_field_to_data(channel_type, channel, channel_data, region)
        _maybe_add_channel_video_quality_mode_field_to_data(channel_type, channel, channel_data, video_quality_mode)
        _maybe_add_channel_default_auto_archive_after_field_to_data(
            channel_type, channel, channel_data, default_auto_archive_after,
        )
        
        
        await self.http.channel_edit(channel_id, channel_data, reason)
    
    
    async def channel_create(self, guild, name, type_=CHANNEL_TYPES.guild_text, *, reason=None, **kwargs):
        """
        Creates a new channel at the given `guild`. If the channel is successfully created returns it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild where the channel will be created.
        name : `str`
            The created channel's name.
        type_ : `int`, Optional
            The type of the created channel. Defaults to ``Channel``.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the `guild`'s audit logs.
        **kwargs : Keyword parameters
            Additional keyword parameters to describe the created channel.
        
        Other Parameters
        ----------------
        permission_overwrites : `list` of ``cr_p_permission_overwrite_object`` returns, Optional (Keyword only)
            A list of permission overwrites of the channel. The list should contain json serializable permission
            overwrites made by the ``cr_p_permission_overwrite_object`` function.
        topic : `str`, Optional (Keyword only)
            The channel's topic.
        nsfw : `bool`, Optional (Keyword only)
            Whether the channel is marked as nsfw.
        slowmode : `int`, Optional (Keyword only)
            The channel's slowmode value.
        bitrate : `int`, Optional (Keyword only)
            The channel's bitrate.
        user_limit : `int`, Optional (Keyword only)
            The channel's user limit.
        parent : `None`, ``Channel``, `int`, Optional (Keyword only)
            The channel's parent. If the channel is under a guild, leave it empty.
        category : `None`, ``Channel``, ``Guild``, `int`, Optional (Keyword only)
            Deprecated, please use `parent` parameter instead.
        region : `None`, ``VoiceRegion``, `str`, Optional (Keyword only)
            The channel's voice region.
        video_quality_mode : `None`, ``VideoQualityMode``, `int`, Optional (Keyword only)
            The channel's video quality mode.
        default_auto_archive_after : `None`, `int`
            The default duration (in seconds) for newly created threads to automatically archive the themselves. Can be
            one of: `3600`, `86400`, `259200`, `604800`.
        
        Returns
        -------
        channel : `None`, ``Channel``
            The created channel. Returns `None` if the respective `guild` is not cached.
        
        Raises
        ------
        TypeError
            - If `guild` was not given as ``Guild``, `int`.
            - If `type_` was not passed as `int`, ``Channel``.
            - If `parent` was not given as `None`, ``Channel``, `int`.
            - If `region` was not given either as `None`, `str` nor ``VoiceRegion``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        data = cr_pg_channel_object(name, type_, **kwargs, guild=guild)
        data = await self.http.channel_create(guild_id, data, reason)
        
        return Channel(data, self, guild_id)
    
    
    async def channel_delete(self, channel, *, reason=None):
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
            The channel what will be followed. Must be an announcements (type 5) channel.
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
            source_channel = create_partial_channel_from_id(source_channel_id, 5, 0)
        
        target_channel_id = get_channel_id(target_channel, Channel.is_in_group_guild_main_text)
        
        data = {
            'webhook_channel_id': target_channel_id,
        }
        
        data = await self.http.channel_follow(source_channel_id, data)
        webhook = await Webhook._from_follow_data(data, source_channel, target_channel_id, self)
        return webhook
    

    async def permission_overwrite_edit(self, channel, permission_overwrite, *, allow=..., deny=..., reason=None):
        """
        Edits the given permission overwrite.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ˙˙Channel``, `int`
            The channel where the permission overwrite is.
        permission_overwrite : ``PermissionOverwrite``
            The permission overwrite to edit.
        allow : `None`, ``Permission``, `int`, Optional (Keyword only)
            The permission overwrite's new allowed permission's value.
        deny : `None`, ``Permission``, `int`, Optional (Keyword only)
            The permission overwrite's new denied permission's value.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `permission_overwrite` was not given as ``PermissionOverwrite``.
            - If `allow` was not given neither as `None`, ``Permission`` not other `int`.
            - If `deny` was not given neither as `None`, ``Permission`` not other `int`.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_movable)
        
        assert _assert__permission_overwrite__type(permission_overwrite)
        assert _assert__permission_overwrite_edit__allow(allow)
        assert _assert__permission_overwrite_edit__deny(deny)
        
        if allow is ...:
            allow = permission_overwrite.allow
        
        if deny is ...:
            deny = permission_overwrite.deny
        
        data = {
            'allow': allow,
            'deny': deny,
            'type': permission_overwrite.target_type.value
        }
        
        await self.http.permission_overwrite_create(channel_id, permission_overwrite.target_id, data, reason)
    
    
    async def permission_overwrite_delete(self, channel, permission_overwrite, *, reason=None):
        """
        Deletes the given permission overwrite.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ˙˙Channel``
            The channel where the permission overwrite is.
        permission_overwrite : ``PermissionOverwrite``
            The permission overwrite to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.

        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `permission_overwrite` was not given as ``PermissionOverwrite``.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_movable)
        
        assert _assert__permission_overwrite__type(permission_overwrite)
        
        await self.http.permission_overwrite_delete(channel_id, permission_overwrite.target_id, reason)
    
    
    async def permission_overwrite_create(self, channel, target, allow, deny, *, reason=None):
        """
        Creates a permission overwrite at the given channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to what the permission overwrite will be added.
        target : ``Role``, ``ClientUserBase``
            The permission overwrite's target.
        allow : ``Permission``, `int`
            The permission overwrite's allowed permission's value.
        deny : ``Permission``, `int`
            The permission overwrite's denied permission's value.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Returns
        -------
        permission_overwrite : ``PermissionOverwrite``
            A permission overwrite, what estimatedly is same as the one what Discord will create.
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``Channel`` nor as `int`.
            - If `target` was not passed neither as ``Role``,``User``, neither as ``Client``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `allow` was not given neither as ``Permission`` nor as other `int`.
            - If `deny ` was not given neither as ``Permission`` not as other `int`.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_movable)
        
        if isinstance(target, Role):
            permission_overwrite_target_type = PermissionOverwriteTargetType.role
        elif isinstance(target, ClientUserBase):
            permission_overwrite_target_type = PermissionOverwriteTargetType.user
        else:
            raise TypeError(
                f'`target` can be `{Role.__name__}`, `{ClientUserBase.__name__}`, got '
                f'{target.__class__.__name__}; {target!r}.'
            )
        
        if __debug__:
            if not isinstance(allow, int):
                raise AssertionError(
                    f'`allow` can be `{Permission.__name__}`, `int`, got {allow.__class__.__name__}; {allow!r}.'
                )
        
            if not isinstance(deny, int):
                raise AssertionError(
                    f'`deny` can be `{Permission.__name__}`, `int`, got {deny.__class__.__name__}; {deny!r}.'
                )
        
        data = {
            'target': target.id,
            'allow': allow,
            'deny': deny,
            'type': permission_overwrite_target_type.value,
        }
        
        await self.http.permission_overwrite_create(channel_id, target.id, data, reason)
        return PermissionOverwrite.custom(target, allow, deny)
    
    
    async def guild_sync_channels(self, guild):
        """
        Deprecated and will be removed in 2022 Dec. Please use ``.guild_channels_get_all`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.guild_sync_channels` is deprecated and will be '
                f'removed in 2022 Dec. Please use `.guild_channel_get_all` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return await self.guild_channel_get_all(guild)
    
    
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
        
        guild._sync_channels(data)
        
        return [*guild.channels.values()]
