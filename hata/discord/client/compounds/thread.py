__all__ = ()

from scarletio import Compound, set_docs

from ....env import API_VERSION

from ...allowed_mentions import parse_allowed_mentions
from ...bases import maybe_snowflake, maybe_snowflake_pair
from ...channel import CHANNEL_TYPES, Channel, create_partial_channel_from_id
from ...channel.constants import AUTO_ARCHIVE_DEFAULT, AUTO_ARCHIVE_OPTIONS
from ...channel.utils import _maybe_add_channel_slowmode_field_to_data
from ...core import CHANNELS
from ...http import DiscordHTTPClient
from ...message import Message, MessageFlag, MessageReference, MessageRepr
from ...preconverters import preconvert_int_options
from ...sticker import Sticker
from ...user import ClientUserBase, create_partial_user_from_id, thread_user_create

from ..functionality_helpers import request_channel_thread_channels
from ..request_helpers import (
    add_file_to_message_data, get_channel_and_id, get_channel_id, get_components_data, get_guild_id,
    get_channel_guild_id_and_id, get_user_and_id, get_user_id, validate_content_and_embed,
)



MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS = MessageFlag().update_by_keys(embeds_suppressed=True)


class ClientCompoundThreadEndpoints(Compound):
    
    http : DiscordHTTPClient
    id: int
    
    
    async def guild_thread_get_all_active(self, guild):
        """
        Gets all the active threads of the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to get it's threads of.
            
            If the guild is given as `0`, will return an empty list.
        
        Returns
        -------
        threads : `list` of ``Channel``
        
        Raises
        ------
        TypeError
            If `guild` is neither ``Guild`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        if not guild_id:
            return []
        
        data = await self.http.guild_thread_get_all_active(guild_id)
        
        thread_channel_datas = data['threads']
        
        thread_channels = [
            Channel(thread_channel_data, self, guild_id) for thread_channel_data in thread_channel_datas
        ]
        
        thread_user_datas = data['members']
        for thread_user_data in thread_user_datas:
            thread_channel_id = int(thread_user_data['id'])
            try:
                thread_channel = CHANNELS[thread_channel_id]
            except KeyError:
                continue
    
            user_id = int(thread_user_data['user_id'])
            user = create_partial_user_from_id(user_id)
            
            thread_user_create(thread_channel, user, thread_user_data)
        
        return thread_channels
    
    
    async def thread_create(
        self, message_or_channel, name, *, auto_archive_after=None, type_=None, invitable=True, slowmode = None
    ):
        """
        Creates a new thread derived from the given message or channel.
        
        > For private thread channels the guild needs to have level 2 boost level.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message_or_channel : ``Channel``, ``Message``, ``MessageRepr``, ``MessageReference``, `int`, \
                `tuple` (`int`, `int`)
            The channel or message to create thread from.
            
            > If given as a channel instance, will create a private thread, else a public one.
        
        name : `str`
            The created thread's name.
        
        auto_archive_after : `None`, `int` = `None`, Optional (Keyword only)
            The duration in seconds after the thread auto archives. Can be any of `3600`, `86400`, `259200`, `604800`.
        
        type_ : `None`, `int` = `None`, Optional (Keyword only)
            The thread channel's type to create. Can be either `10`,`11`,`12`.
        
        invitable : `bool` = `True`, Optional (Keyword only)
            Whether non-moderators can invite other non-moderators to the threads. Only applicable for private threads.
            
            Applicable for private threads. Defaults to `True`.
        
        slowmode : `int`, Optional (Keyword only)
            Slowmode for the new thread channel.
        
        Returns
        -------
        thread_channel : ``Channel``
            The created thread channel.
        
        Raises
        ------
        TypeError
            If `message`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` is not `str`.
            - If `name`'s length is out of range [2:100].
            - If `auto_archive_after` is neither `int`, nor `bool`.
            - If `auto_archive_after` is not any of the expected ones.
            - If `invitable` is not `bool`.
        """
        # Message check order
        # 1.: Message
        # 2.: MessageRepr
        # 3.: MessageReference
        # 4.: None -> raise
        # 5.: `tuple` (`int`, `int`)
        # 6.: raise
        #
        # Message cannot be detected by id, only cached ones, so ignore that case.
        
        if isinstance(message_or_channel, Channel):
            if message_or_channel.type not in CHANNEL_TYPES.GROUP_CAN_CONTAIN_THREADS:
                raise TypeError(
                    f'{message_or_channel!r} do not supports thread creation.'
                )
            
            message_id = None
            channel = message_or_channel
            channel_id = channel.id
        
        elif isinstance(message_or_channel, Message):
            message_id = message_or_channel.id
            channel_id = message_or_channel.channel_id
            channel = CHANNELS.get(channel_id, None)
        
        else:
            channel_id = maybe_snowflake(message_or_channel)
            if (channel_id is not None):
                message_id = None
                channel = CHANNELS.get(channel_id, None)
            
            elif isinstance(message_or_channel, MessageRepr):
                message_id = message_or_channel.id
                channel_id = message_or_channel.channel_id
                channel = CHANNELS.get(channel_id, None)
            
            elif isinstance(message_or_channel, MessageReference):
                message_id = message_or_channel.message_id
                channel_id = message_or_channel.channel_id
                channel = CHANNELS.get(channel_id, None)
            
            else:
                snowflake_pair = maybe_snowflake_pair(message_or_channel)
                if snowflake_pair is None:
                    raise TypeError(
                        f'`message_or_channel` can be `{Channel.__name__}`, `{Message.__name__}`, '
                        f'`{MessageRepr.__name__}`, `{MessageReference.__name__}`, `int`, `tuple` (`int`, `int`)'
                        f', got {message_or_channel.__class__.__name__}; {message_or_channel!r}.'
                    )
                
                channel_id, message_id = snowflake_pair
                channel = CHANNELS.get(channel_id)
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            
            if (name_length) < 2 or (name_length > 100):
                raise AssertionError(
                    f'`name` length can be in range [2:100], got {name_length}; {name!r}.'
                )
        
        if auto_archive_after is None:
            if channel is None:
                auto_archive_after = AUTO_ARCHIVE_DEFAULT
            else:
                auto_archive_after = channel.default_auto_archive_after
        else:
            if __debug__:
                if not isinstance(auto_archive_after, int):
                    raise AssertionError(
                        f'`auto_archive_after` can be `None`, `datetime`, got '
                        f'{auto_archive_after.__class__.__name__}; {auto_archive_after!r}.'
                    )
                
                if auto_archive_after not in AUTO_ARCHIVE_OPTIONS:
                    raise AssertionError(
                        f'`auto_archive_after` can be any of: {AUTO_ARCHIVE_OPTIONS}, got {auto_archive_after!r}.'
                    )
        
        if type_ is None:
            type_ = CHANNEL_TYPES.guild_thread_public
        else:
            type_ = preconvert_int_options(type_, 'type_', CHANNEL_TYPES.GROUP_THREAD)
        
        if __debug__:
            if not isinstance(invitable, bool):
                raise AssertionError(
                    f'`invitable` can be `bool`, got {invitable.__class__.__name__}; {invitable!r}.'
                )
        
        data = {
            'name': name,
            'auto_archive_duration': auto_archive_after // 60,
            'type': type_,
        }
        
        _maybe_add_channel_slowmode_field_to_data(type_, None, data, slowmode)
        
        
        if (type_ == CHANNEL_TYPES.guild_thread_private) and (not invitable):
            data['invitable'] = invitable
        
        
        if message_id is None:
            coroutine = self.http.thread_create(channel_id, data)
        else:
            coroutine = self.http.thread_create_from_message(channel_id, message_id, data)
        channel_data = await coroutine
        
        if channel is None:
            guild_id = channel_data.get('guild_id', None)
            if (guild_id is not None):
                guild_id = int(guild_id)
        else:
            guild_id = channel.guild_id
        
        return Channel(channel_data, self, guild_id)
    
    
    async def forum_thread_create(
        self, channel_forum, name, content=None, *, allowed_mentions=...,  auto_archive_after=None,
        components=None, embed=None, file=None, nonce=None, slowmode=None, sticker=None,
        suppress_embeds=False, tts=False
    ):
        """
        Creates and thread at the given `channel` with the given message fields. If there is nothing to send will
        return `None` for channel and `None` for message as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel_forum : ``Channel``, `int`
            The forum channel's identifier where the thread will be started.
        
        name : `str`
            The created thread's name.
        
        content : `None`, `str`, ``EmbedBase``, `Any` = `None`, Optional
            The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
            if any other non `str`, ``EmbedBase`` is given, then will be casted to string.
            
            If given as ``EmbedBase``, then is sent as the message's embed.
        
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        
        auto_archive_after : `None`, `int` = `None`, Optional (Keyword only)
            The duration in seconds after the thread auto archives. Can be any of `3600`, `86400`, `259200`, `604800`.
        
        components : `None`, ``ComponentBase``, (`tuple`, `list`) of (``ComponentBase``, (`tuple`, `list`) of
                ``ComponentBase``) = `None`, Optional (Keyword only)
            Components attached to the message.
            
            > `components` do not count towards having any content in the message.
        
        embed : ``EmbedBase``, `list` of ``EmbedBase`` = `None`, Optional (Keyword only)
            The embedded content of the message.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `TypeError` is raised.
        
        file : `None`, `Any` = `None`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        
        nonce : `None`, `str` = `None`, Optional (Keyword only)
            Used for optimistic message sending. Will shop up at the message's data.
        
        slowmode : `int`, Optional (Keyword only)
            Slowmode for the new thread channel.
        
        sticker : `None`, ``Sticker``, `int`, (`list`, `set`, `tuple`) of (``Sticker``, `int`) = `None` \
                , Optional (Keyword only)
            Sticker or stickers to send within the message.
        
        suppress_embeds : `bool` = `False`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech.
        
        Returns
        -------
        thread_channel : `None`, ``Channel``
            The created thread channel. `None` if there was nothing to send.
        message : `None`, ``Message``
            Returns `None` if there is nothing to send.
        
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
        
        See Also
        --------
        ``.message_create`` : Sending a message to a text channel.
        ``.thread_create`` : Create thread in a text channel.
        """
        channel, channel_id = get_channel_and_id(channel_forum, Channel.is_guild_forum)
        
        # name & auto_archive_after
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            
            if (name_length) < 2 or (name_length > 100):
                raise AssertionError(
                    f'`name` length can be in range [2:100], got {name_length}; {name!r}.'
                )
        
        if auto_archive_after is None:
            if channel is None:
                auto_archive_after = AUTO_ARCHIVE_DEFAULT
            else:
                auto_archive_after = channel.default_auto_archive_after
        else:
            if __debug__:
                if not isinstance(auto_archive_after, int):
                    raise AssertionError(
                        f'`auto_archive_after` can be `None`, `datetime`, got '
                        f'{auto_archive_after.__class__.__name__}; {auto_archive_after!r}.'
                    )
                
                if auto_archive_after not in AUTO_ARCHIVE_OPTIONS:
                    raise AssertionError(
                        f'`auto_archive_after` can be any of: {AUTO_ARCHIVE_OPTIONS}, got {auto_archive_after!r}.'
                    )
        
        content, embed = validate_content_and_embed(content, embed, False)
        
        # Sticker check order:
        # 1.: None -> None
        # 2.: Sticker -> [sticker.id]
        # 3.: int (str) -> [sticker]
        # 4.: (list, tuple) of (Sticker, int (str)) -> [sticker.id / sticker, ...] / None
        # 5.: raise
        
        if sticker is None:
            sticker_ids = None
        else:
            sticker_ids = []
            if isinstance(sticker, Sticker):
                sticker_id = sticker.id
                sticker_ids.append(sticker_id)
            else:
                sticker_id = maybe_snowflake(sticker)
                if sticker_id is None:
                    if isinstance(sticker, (list, tuple)):
                        for sticker_element in sticker:
                            if isinstance(sticker_element, Sticker):
                                sticker_id = sticker_element.id
                            else:
                                sticker_id = maybe_snowflake(sticker_element)
                                if sticker_id is None:
                                    raise TypeError(
                                        f'`sticker` can contain only `{Sticker.__name__}`, `int` elements, '
                                        f'got {sticker_element.__class__.__name__}; {sticker_element!r}; '
                                        f'sticker={sticker!r}.'
                                    )
                            
                            sticker_ids.append(sticker_id)
                        
                        if not sticker_ids:
                            sticker_ids = None
                    else:
                        raise TypeError(
                            f'`sticker` can be `None`, `{Sticker.__name__}`, `int`, '
                            f'(`list`, `tuple`) of (`{Sticker.__name__}`, `int`), got '
                            f'{sticker.__class__.__name__}; {sticker!r}.'
                        )
                else:
                    sticker_ids.append(sticker_id)
        
        components = get_components_data(components, False)
        
        if __debug__:
            
            if (nonce is not None) and (not isinstance(nonce, str)):
                raise AssertionError(
                    f'`nonce` can be `None`, `str`, got {nonce.__class__.__name__}; {nonce!r}.'
                )
            
            if not isinstance(suppress_embeds, bool):
                raise AssertionError(
                    f'`suppress_embeds` can be `bool`, got {suppress_embeds.__class__.__name__}; {suppress_embeds!r}.'
                )
        
            if not isinstance(tts, bool):
                raise AssertionError(
                    f'`tts` can be `bool`, got {tts.__class__.__name__}, {tts!r}.'
                )
        
        # Build payload
        message_data = {}
        contains_content = False
        
        if (content is not None):
            message_data['content'] = content
            contains_content = True
        
        if (embed is not None):
            message_data['embeds'] = [embed.to_data() for embed in embed]
            contains_content = True
        
        if (sticker_ids is not None):
            message_data['sticker_ids'] = sticker_ids
            contains_content = True
        
        if (components is not None):
            message_data['components'] = components
        
        if tts:
            message_data['tts'] = True
        
        if (nonce is not None):
            message_data['nonce'] = nonce
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if suppress_embeds:
            message_data['flags'] = MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
        
        message_data = add_file_to_message_data(message_data, file, contains_content, False)
        if message_data is None:
            return None, None
        
        data = {
            'name': name,
            'auto_archive_duration': auto_archive_after // 60,
            'message': message_data,
        }
        
        _maybe_add_channel_slowmode_field_to_data(CHANNEL_TYPES.guild_thread_public, None, data, slowmode)
        
        channel_data = await self.http.thread_create(channel_id, data)
        
        if channel is None:
            guild_id = channel_data.get('guild_id', None)
            if (guild_id is not None):
                guild_id = int(guild_id)
        else:
            guild_id = channel.guild_id
        
        thread_channel = Channel(channel_data, self, guild_id)
        
        message_data = channel_data.get('message', None)
        if (message_data is None):
            message = None
        else:
            message = thread_channel._create_new_message(message_data)
        
        return thread_channel, message
    
    
    async def thread_join(self, thread_channel):
        """
        Joins the client to the given thread channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        thread_channel : ``Channel``, `int`
            The channel to join to, or it's identifier.
        
        Raises
        ------
        TypeError
            If `thread_channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(thread_channel, Channel.is_in_group_thread)
        
        await self.http.thread_join(channel_id)
    
    
    async def thread_leave(self, thread_channel):
        """
        Leaves the client to the given thread channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        thread_channel : ``Channel``, `int`
            The channel to join to, or it's identifier.
        
        Raises
        ------
        TypeError
            If `thread_channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(thread_channel, Channel.is_in_group_thread)
        
        await self.http.thread_leave(channel_id)
    
    
    async def thread_user_get(self, thread_channel, user):
        """
        Gets a user's thread profile inside of a thread channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        thread_channel : ``Channel``, `int`
            The channel to get the user's thread profile of.
        user : ``ClientUserBase``, `int`
            The user to get it's thread profile of.
        
        Returns
        -------
        user : ``ClientUserBase``
            The user, who's thread profile was requested.
        
        Raises
        ------
        TypeError
            - If `thread_channel`'s type is incorrect.
            - If `user`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel, channel_id = get_channel_and_id(thread_channel, Channel.is_in_group_thread)
        user, user_id = get_user_and_id(user)
        
        thread_user_data = await self.http.thread_user_get(channel_id, user_id)
        
        if user is None:
            user = create_partial_user_from_id(user_id)
        
        if channel is None:
            channel = create_partial_channel_from_id(channel_id, 12, 0)
        
        thread_user_create(channel, user, thread_user_data)
        
        return user
    
    
    async def thread_user_add(self, thread_channel, user):
        """
        Adds the user to the thread channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        thread_channel : ``Channel``, `int`
            The channel to add the user to, or it's identifier.
        user : ``ClientUserBase``, `int`
            The user to add to the the thread.
        
        Raises
        ------
        TypeError
            - If `thread_channel`'s type is incorrect.
            - If `user`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(thread_channel, Channel.is_in_group_thread)
        user_id = get_user_id(user)
        
        if user_id == self.id:
            coroutine = self.http.thread_join(channel_id)
        else:
            coroutine = self.http.thread_user_add(channel_id, user_id)
        await coroutine
    
    
    async def thread_user_delete(self, thread_channel, user):
        """
        Deletes the user to the thread channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        thread_channel : ``Channel``, `int`
            The channel to remove the user from, or it's identifier.
        user : ``ClientUserBase``, `int`
            The user to remove from the thread.
        
        Raises
        ------
        TypeError
            - If `thread_channel`'s type is incorrect.
            - If `user`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(thread_channel, Channel.is_in_group_thread)
        user_id = get_user_id(user)
        
        if user_id == self.id:
            coroutine = self.http.thread_leave(channel_id)
        else:
            coroutine = self.http.thread_user_delete(channel_id, user_id)
        await coroutine
    
    
    async def thread_user_get_all(self, thread_channel):
        """
        Gets all the users of a thread channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        thread_channel : ``Channel``, `int`
            The channel to get it's users of.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
            The created users.
        
        Raises
        ------
        TypeError
            If `thread_channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        thread_channel, channel_id = get_channel_and_id(thread_channel, Channel.is_in_group_thread)
        
        thread_user_datas = await self.http.thread_user_get_all(channel_id)
        
        if thread_channel is None:
            thread_channel = create_partial_channel_from_id(channel_id, 12, 0)
        
        users = []
        for thread_user_data in thread_user_datas:
            user_id = int(thread_user_data['user_id'])
            user = create_partial_user_from_id(user_id)
            users.append(user)
            
            thread_user_create(thread_channel, user, thread_user_data)
        
        return users
    
    
    if API_VERSION >= 10:
        async def channel_thread_get_all_active(self, channel):
            guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_in_group_can_contain_threads)
            thread_channels = await self.guild_thread_get_all_active(guild_id)
            return [thread_channel for thread_channel in thread_channels if thread_channel.parent_id == channel_id]
    
    else:
        async def channel_thread_get_all_active(self, channel):
            guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_in_group_can_contain_threads)
            return await request_channel_thread_channels(
                self,
                guild_id,
                channel_id,
                type(self.http).channel_thread_get_chunk_active,
            )
    
    set_docs(
        channel_thread_get_all_active,
        """
        Requests all the active threads of the given channel.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to request the thread of, or it's identifier.
        
        Returns
        -------
        thread_channels : `list` of ``Channel``
        
        Raises
        ------
        TypeError
            If `channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        When using API v10 or later, this endpoint filters from ``.guild_thread_get_all_active`` method's return.
        Consider using that instead.
        
        Active threads can also be extracted from ``Guild.threads``.
        """
    )
    
    async def channel_thread_get_all_archived_private(self, channel):
        """
        Requests all the archived private of the given channel.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to request the thread of, or it's identifier.
        
        Returns
        -------
        thread_channels : `list` of ``Channel``
        
        Raises
        ------
        TypeError
            If `channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_in_group_can_contain_threads)
        return await request_channel_thread_channels(
            self,
            guild_id,
            channel_id,
            type(self.http).channel_thread_get_chunk_archived_private,
        )
    
    
    async def channel_thread_get_all_archived_public(self, channel):
        """
        Requests all the archived public threads of the given channel.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to request the thread of, or it's identifier.
        
        Returns
        -------
        thread_channels : `list` of ``Channel``
        
        Raises
        ------
        TypeError
            If `channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_in_group_can_contain_threads)
        return await request_channel_thread_channels(
            self,
            guild_id,
            channel_id,
            type(self.http).channel_thread_get_chunk_archived_public,
        )
    
    
    async def channel_thread_get_all_self_archived(self, channel):
        """
        Requests all the archived private threads by the client.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel to request the thread of, or it's identifier.
        
        Returns
        -------
        thread_channels : `list` of ``Channel``
        
        Raises
        ------
        TypeError
            If `channel`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_in_group_can_contain_threads)
        return await request_channel_thread_channels(
            self,
            guild_id,
            channel_id,
            type(self.http).channel_thread_get_chunk_self_archived,
    )
    