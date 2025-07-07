__all__ = ()

from scarletio import Compound, set_docs
from scarletio.web_common import FormData

from ....env import API_VERSION

from ...bases import maybe_snowflake, maybe_snowflake_pair
from ...builder.serialization import create_serializer
from ...builder.serialization_configuration import SerializationConfiguration
from ...channel import Channel, ChannelType, create_partial_channel_from_id
from ...channel.channel.utils import CHANNEL_GUILD_THREAD_FIELD_CONVERTERS
from ...core import CHANNELS
from ...http import DiscordApiClient
from ...message import Message
from ...message.message_builder import MessageBuilderForumThreadCreate
from ...payload_building import add_payload_fields_from_keyword_parameters, build_create_payload
from ...user import ClientUserBase, create_partial_user_from_id, create_user_from_thread_user_data, thread_user_create

from ..functionality_helpers import request_channel_thread_channels
from ..request_helpers import (
    get_channel_and_id, get_channel_id, get_guild_id, get_channel_guild_id_and_id, get_user_id,
)


MESSAGE_SERIALIZER_FORUM_THREAD_CREATE = create_serializer(
    MessageBuilderForumThreadCreate,
    SerializationConfiguration(
        [
            MessageBuilderForumThreadCreate.allowed_mentions,
            MessageBuilderForumThreadCreate.attachments,
            MessageBuilderForumThreadCreate.components,
            MessageBuilderForumThreadCreate.content,
            MessageBuilderForumThreadCreate.embeds,
            MessageBuilderForumThreadCreate.flags,
            MessageBuilderForumThreadCreate.nonce,
            MessageBuilderForumThreadCreate.sticker_ids,
            MessageBuilderForumThreadCreate.tts,
        ],
        False,
    )
)


class ClientCompoundThreadEndpoints(Compound):
    
    api : DiscordApiClient
    id: int
    
    
    async def guild_thread_get_all_active(self, guild):
        """
        Gets all the active threads of the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``int | Guild``
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
        
        data = await self.api.guild_thread_get_all_active(guild_id)
        
        thread_channel_datas = data['threads']
        
        thread_channels = [
            Channel.from_data(thread_channel_data, self, guild_id) for thread_channel_data in thread_channel_datas
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
    
    
    async def thread_create(self, message_or_channel, channel_template = None, **keyword_parameters,):
        """
        Creates a new thread derived from the given message or channel.
        
        > For private thread channels the guild needs to have level 2 boost level.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message_or_channel : ``Channel``, ``Message``, `int`, `tuple` (`int`, `int`)
            The channel or message to create thread from.
            
            > If given as a channel instance, will create a private thread, else a public one.
        
        channel_template : ``None | Channel`` = `None`, Optional
            Channel to use as a template.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters either to define the template, or to overwrite specific fields' values.
        
        Other Parameters
        ----------------
        applied_tag_ids : `None`, `(list | tuple)<int | ForumTag>`, `int`, `ForumTag`, Optional (Keyword only)
             The tags' identifier which have been applied to the thread.
        
        applied_tags : `None`, `(list | tuple)<int | ForumTag>`, `int`, `ForumTag`, Optional (Keyword only)
            Alternative for `applied_tag_ids`.
        
        auto_archive_after : `int`, Optional (Keyword only)
            The default duration (in seconds) for newly created threads to automatically archive the themselves.
        
        channel_type : `None`, ``ChannelType``, `int` = `None`, Optional (Keyword only)
            The type of the created (thread) channel.
        
        flags : `int`, ``ChannelFlag``, Optional (Keyword only)
            The channel's flags.
        
        invitable : `bool`, Optional (Keyword only)
            Whether non-moderators can invite other non-moderators to the threads.
        
        name : `str`, Optional (Keyword only)
            The channel's name.
        
        open_ : `bool`, Optional (Keyword only)
            Whether the thread channel is open.
        
        slowmode : `int`, Optional (Keyword only)
            The channel's slowmode.
        
        Returns
        -------
        thread_channel : ``Channel``
            The created thread channel.
        
        Raises
        ------
        TypeError
            If any parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        # Message check order
        # 1.: Message
        # 4.: None -> raise
        # 5.: `tuple` (`int`, `int`)
        # 6.: raise
        #
        # Message cannot be detected by id, only cached ones, so ignore that case.
        
        if isinstance(message_or_channel, Channel):
            if not message_or_channel.is_threadable():
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
            
            else:
                snowflake_pair = maybe_snowflake_pair(message_or_channel)
                if snowflake_pair is None:
                    raise TypeError(
                        f'`message_or_channel` can be `{Channel.__name__}`, `{Message.__name__}`, '
                        f'`int`, `tuple` (`int`, `int`), '
                        f'got {message_or_channel.__class__.__name__}; {message_or_channel!r}.'
                    )
                
                channel_id, message_id = snowflake_pair
                channel = CHANNELS.get(channel_id)
                # Checkout type
        
        if message_id is None:
            channel_type = ChannelType.guild_thread_private
        else:
            channel_type = ChannelType.guild_thread_public
        keyword_parameters.setdefault('channel_type', channel_type)
        
        data = build_create_payload(channel_template, CHANNEL_GUILD_THREAD_FIELD_CONVERTERS, keyword_parameters)
        
        if message_id is None:
            coroutine = self.api.thread_create(channel_id, data)
        else:
            coroutine = self.api.thread_create_from_message(channel_id, message_id, data)
        channel_data = await coroutine
        
        if channel is None:
            guild_id = channel_data.get('guild_id', None)
            if (guild_id is not None):
                guild_id = int(guild_id)
        else:
            guild_id = channel.guild_id
        
        return Channel.from_data(channel_data, self, guild_id)
    
    
    async def forum_thread_create(
        self, channel_forum, channel_template = None, *positional_parameters, **keyword_parameters,
    ):
        """
        Creates and thread at the given `channel` with the given message fields. If there is nothing to send will
        return `None` for channel and `None` for message as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel_forum : ``Channel``, `int`
            The forum channel's identifier where the thread will be started.
        
        channel_template : ``None | Channel`` = `None`, Optional
            (Thread) channel entity to use as a template.
        
        *positional_parameters : Positional parameters
            Additional parameters to create the message with.
        
        **keyword_parameters : Keyword parameters
            Additional parameters to create the message with.
        
        Other Parameters
        ----------------
        allowed_mentions : `None`,  ``AllowedMentionProxy``, `str`, ``UserBase``, ``Role``, `list` of \
                (`str`, ``UserBase``, ``Role`` ) , Optional
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        
        applied_tag_ids : `None`, `(list | tuple)<int | ForumTag>`, `int`, `ForumTag`, Optional (Keyword only)
             The tags' identifier which have been applied to the thread.
        
        applied_tags : `None`, `(list | tuple)<int | ForumTag>`, `int`, `ForumTag`, Optional (Keyword only)
            Alternative for `applied_tag_ids`.
        
        attachments : `None | object`, Optional (Keyword only)
            Attachments to send.
        
        auto_archive_after : `int`, Optional (Keyword only)
            The default duration (in seconds) for newly created threads to automatically archive the themselves.
        
        components : `None`, ``Component``, `(tuple | list)<Component, (tuple | list)<Component>>`
            Components attached to the message.
        
        content : `None`, `str`, Optional
            The message's content if given.
        
        embed : `None`, `Embed`, Optional
            Alternative for `embeds`.
        
        embeds : `None`, `list<Embed>`, Optional
            The new embedded content of the message.
        
        file : `None | object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        files : `None | object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        flags : `int`, ``ChannelFlag``, Optional (Keyword only)
            The channel's flags. Due to name collision, `message.flags` is not directly supported.
        
        invitable : `bool`, Optional (Keyword only)
            Whether non-moderators can invite other non-moderators to the threads.
        
        name : `str`, Optional (Keyword only)
            The channel's name.
        
        nonce : `None`, `str`, Optional (Keyword only)
            Used for optimistic message sending.
        
        open_ : `bool`, Optional (Keyword only)
            Whether the thread is open.
        
        silent : `bool` = `False`, Optional (Keyword only)
            Whether the message should be delivered silently.
        
        slowmode : `int`, Optional (Keyword only)
            The channel's slowmode.
        
        sticker : `None`, ``Sticker``, Optional
            Alternative for `sticker_ids`.
        
        sticker_ids : `None`, `list<int>`, Optional (Keyword only)
            Sticker(s) to send within the message.
        
        stickers : `None`, `list<int | Sticker>`, Optional
            Alternative for `sticker_ids`.
        
        suppress_embeds : `bool` = `False`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech.
        
        Returns
        -------
        thread_channel : ``None | Channel``
            The created thread channel. `None` if there was nothing to send.
        message : `None`, ``Message``
            Returns `None` if there is nothing to send.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        See Also
        --------
        ``.message_create`` : Sending a message to a text channel.
        ``.thread_create`` : Create thread in a text channel.
        """
        channel, channel_id = get_channel_and_id(channel_forum, Channel.is_in_group_forum)
        
        # channel_data
        if (channel_template is None):
            data = {}
        else:
            data = channel_template.to_data(defaults = False)
        
        keyword_parameters = add_payload_fields_from_keyword_parameters(
            CHANNEL_GUILD_THREAD_FIELD_CONVERTERS, keyword_parameters, data, False, raise_unused = False,
        )
        
        if keyword_parameters is None:
            keyword_parameters = {}
        
        message_data = MESSAGE_SERIALIZER_FORUM_THREAD_CREATE(positional_parameters, keyword_parameters)
        if not message_data:
            return None, None
        
        # Nest `message_data` under `data['message']`
        if isinstance(message_data, FormData):
            field = message_data.fields[0]
            data['message'] = field.value
            field.value = data
            data = message_data
        else:
            data['message'] = message_data
        
        channel_data = await self.api.thread_create(channel_id, data)
        
        if channel is None:
            guild_id = channel_data.get('guild_id', None)
            if (guild_id is None):
                guild_id = 0
            else:
                guild_id = int(guild_id)
        else:
            guild_id = channel.guild_id
        
        thread_channel = Channel.from_data(channel_data, self, guild_id)
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
        
        await self.api.thread_join(channel_id)
    
    
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
        
        await self.api.thread_leave(channel_id)
    
    
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
        thread_channel, channel_id = get_channel_and_id(thread_channel, Channel.is_in_group_thread)
        user_id = get_user_id(user)
        
        thread_user_data = await self.api.thread_user_get(channel_id, user_id, {'with_member': True})
        
        if thread_channel is None:
            thread_channel = create_partial_channel_from_id(channel_id, ChannelType.guild_thread_public, 0)
        
        user = create_user_from_thread_user_data(thread_channel, thread_user_data)
        thread_user_create(thread_channel, user, thread_user_data)
        
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
            coroutine = self.api.thread_join(channel_id)
        else:
            coroutine = self.api.thread_user_add(channel_id, user_id)
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
            coroutine = self.api.thread_leave(channel_id)
        else:
            coroutine = self.api.thread_user_delete(channel_id, user_id)
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
        users : ``list<ClientUserBase>``
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
        
        data = {
            'after': 0,
            'limit': 100,
            'with_member': True,
        }
        
        users = []
        
        while True:
            thread_user_datas = await self.api.thread_user_get_chunk(channel_id, data)
            
            if thread_channel is None:
                thread_channel = create_partial_channel_from_id(channel_id, ChannelType.guild_thread_public, 0)
            
            for thread_user_data in thread_user_datas:
                user = create_user_from_thread_user_data(thread_channel, thread_user_data)
                thread_user_create(thread_channel, user, thread_user_data)
                users.append(user)
            
            if len(thread_user_datas) < 100:
                break
            
            data['after'] = users[-1].id
            continue
        
        return users
    
    
    if API_VERSION >= 10:
        async def channel_thread_get_all_active(self, channel):
            guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_in_group_threadable)
            thread_channels = await self.guild_thread_get_all_active(guild_id)
            return [thread_channel for thread_channel in thread_channels if thread_channel.parent_id == channel_id]
    
    else:
        async def channel_thread_get_all_active(self, channel):
            guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_in_group_threadable)
            return await request_channel_thread_channels(
                self, guild_id, channel_id, type(self.api).channel_thread_get_chunk_active,
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
        guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_in_group_threadable)
        return await request_channel_thread_channels(
            self, guild_id, channel_id, type(self.api).channel_thread_get_chunk_archived_private,
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
        guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_in_group_threadable)
        return await request_channel_thread_channels(
            self, guild_id, channel_id, type(self.api).channel_thread_get_chunk_archived_public,
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
        guild_id, channel_id = get_channel_guild_id_and_id(channel, Channel.is_in_group_threadable)
        return await request_channel_thread_channels(
            self, guild_id, channel_id, type(self.api).channel_thread_get_chunk_self_archived,
    )
