__all__ = ()


import warnings
from collections import deque
from time import time as time_now

from scarletio import Compound, Task, WaitTillAll, WaitTillFirst

from ...allowed_mentions import parse_allowed_mentions
from ...bases import maybe_snowflake, maybe_snowflake_pair
from ...channel import Channel, MessageIterator, message_relative_index
from ...core import CHANNELS, KOKORO, MESSAGES
from ...exceptions import DiscordException, ERROR_CODES
from ...http import DiscordHTTPClient
from ...message import Message, MessageFlag
from ...message.utils import process_message_chunk
from ...permission.permission import PERMISSION_MASK_MANAGE_MESSAGES, PERMISSION_MASK_READ_MESSAGE_HISTORY
from ...sticker import Sticker
from ...utils import DISCORD_EPOCH, log_time_converter

from ..functionality_helpers import (
    MultiClientMessageDeleteSequenceSharder, _message_delete_multiple_private_task, _message_delete_multiple_task
)

from ..request_helpers import (
    add_file_to_message_data, get_channel_and_id, get_channel_id, get_channel_id_and_message_id, get_components_data,
    get_message_and_channel_id_and_message_id, validate_content_and_embed, validate_message_to_delete
)


MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS = MessageFlag().update_by_keys(embeds_suppressed=True)


class ClientCompoundMessageEndpoints(Compound):
    
    http : DiscordHTTPClient
    id : int
    
    
    async def message_get_chunk(self, channel, limit=100, *, after=None, around=None, before=None):
        """
        Requests messages from the given text channel. The `after`, `around` and the `before` parameters are mutually
        exclusive and they can be `int`, or as a ``DiscordEntity`` or as a `datetime` object.
        If there is at least 1 message overlap between the received and the loaded messages, the wrapper will chain
        the channel's message history up. If this happens the channel will get on a queue to have it's messages again
        limited to the default one, but requesting old messages more times, will cause it to extend.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel from where we want to request the messages.
        limit : `int` = `100`, Optional
            The amount of messages to request. Can be between 1 and 100.
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the requested messages were created.
        around : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp around the requested messages were created.
        before : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp before the requested messages were created.
        
        Returns
        -------
        messages : `list` of ``Message``
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``Channel`` nor `int`.
            - If `after`, `around`, `before` was passed with an unexpected type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `limit` was not given as `int`.
            - If `limit` is out of range [1:100].
        
        See Also
        --------
        - ``.message_get_chunk_from_zero`` : Familiar to this method, but it requests only the newest messages of the
            channel and makes sure they are chained up with the channel's message history.
        - ``.message_get_at_index`` : A top-level method to get a message at the specified index at the given channel.
            Usually used to load the channel's message history to that point.
        - ``.message_get_all_in_range`` : A top-level method to get all the messages till the specified index at the
            given channel.
        - ``.message_iterator`` : An iterator over a channel's message history.
        """
        channel, channel_id = get_channel_and_id(channel, Channel.is_in_group_textual)
        
        if __debug__:
            if not isinstance(limit, int):
                raise AssertionError(
                    f'`limit` can be `int`, got {limit.__class__.__name__}; {limit!r}.'
                )
            
            if (limit < 1) or (limit > 100):
                raise AssertionError(
                    f'`limit` is out from the expected [1:100] range, got {limit!r}.'
                )
        
        data = {'limit': limit}
        
        if (after is not None):
            data['after'] = log_time_converter(after)
        
        if (around is not None):
            data['around'] = log_time_converter(around)
        
        if (before is not None):
            data['before'] = log_time_converter(before)
        
        # Set some collection delay.
        if (channel is not None):
            channel._add_message_collection_delay(60.0)
        
        message_datas = await self.http.message_get_chunk(channel_id, data)
        return process_message_chunk(message_datas, channel)
    
    
    # If you have 0-1 messages at a channel, and you wanna store the messages. The other wont store it, because it
    # wont see anything what allows channeling.
    async def message_get_chunk_from_zero(self, channel, limit=100):
        """
        If the `channel` has `1` or less messages loaded use this method instead of ``.message_get_chunk`` to request
        the newest messages there, because this method makes sure, the returned messages will be chained at the
        channel's message history.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``
            The channel from where we want to request the messages.
        limit : `int` = `100`, Optional
            The amount of messages to request. Can be between 1 and 100.
        
        Returns
        -------
        messages : `list` of ``Message`` objects
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `limit` was not given as `int`.
            - If `limit` is out of range [1:100].
        """
        channel, channel_id = get_channel_and_id(channel, Channel.is_in_group_textual)
        
        if __debug__:
            if not isinstance(limit, int):
                raise AssertionError(
                    f'`limit` can be `int`, got {limit.__class__.__name__}; {limit!r}.'
                )
            
            if (limit < 1) or (limit > 100):
                raise AssertionError(
                    f'`limit` is out from the expected [1:100] range, got {limit!r}.'
                )
        
        # Set some collection delay.
        if (channel is not None):
            channel._add_message_collection_delay(60.0)
        
        data = {'limit': limit, 'before': 9223372036854775807}
        data = await self.http.message_get_chunk(channel_id, data)
        if data:
            if (channel is not None):
                # Call this method first, so the channel's messages will be set even if message caching is at 0
                channel._maybe_increase_queue_size()
                
                channel._create_new_message(data[0])
            
            messages = process_message_chunk(data, channel)
        else:
            messages = []
        
        return messages
    
    
    async def message_get(self, message, *positional_parameters, force_update=False):
        """
        Requests a specific message by it's id at the given `channel`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message to get, or a `channel-id`, `message-id` tuple representing it.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the scheduled event should be requested even if it supposed to be up to date.
        
        Returns
        -------
        message : ``Message``
        
        Raises
        ------
        TypeError
            - If `message`'s type is neither ``Message``, nor `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if positional_parameters:
            warnings.warn(
                f'`{self.__class__.__name__}.message_get` parameters are modified from `channel + message_id` to '
                f'`Message` / `(channel_id, message_id`). The old usage is deprecated and will be removed in 2022 '
                f'December.'
            )
            
            channel, message_id = message, *positional_parameters
                
            channel_id = get_channel_id(channel, Channel.is_in_group_textual)
            
            message_id_value = maybe_snowflake(message_id)
            if message_id_value is None:
                raise TypeError(
                    f'`message_id` can be `int`, got {message_id.__class__.__name__}; {message_id!r}.'
                )
            
            message_id = message_id_value
        
        else:
            if isinstance(message, Message):
                message_id = message.id
                channel_id = message.channel_id
            
            else:
                snowflake_pair = maybe_snowflake_pair(message)
                if (snowflake_pair is not None):
                    channel_id, message_id = snowflake_pair
                    message = None
                
                else:
                    raise TypeError(
                        f'`message` can be `{Message.__name__}`, `tuple` (`int`, `int`), '
                        f'got {message.__class__.__name__}; {message!r}.'
                    )
        
        message_data = await self.http.message_get(channel_id, message_id)
        
        if (message is None) or message.partial or force_update:
            if message is None:
                message = MESSAGES.get(message_id, None)
            
            if (message is None):
                message = Message.from_data(message_data)
            
            else:
                message._set_attributes(message_data)
        
        else:
            message = Message.from_data(message_data)
        
        return message
    
    
    async def message_create(
        self, channel, content=None, *, allowed_mentions = ...,  components = None, embed = None, file=None, nonce=None,
        reply_fail_fallback=False,  sticker=None, suppress_embeds=False, tts=False
    ):
        """
        Creates and returns a message at the given `channel`. If there is nothing to send, then returns `None`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`, ``Message``, `tuple` (`int`, `int`)
            The text channel where the message will be sent, or the message on what you want to reply.
        
        content : `None`, `str`, ``EmbedBase``, `Any` = `None`, Optional
            The message's content if given. If given as `str` or empty string, then no content will be sent, meanwhile
            if any other non `str`, ``EmbedBase`` is given, then will be casted to string.
            
            If given as ``EmbedBase``, then is sent as the message's embed.
        
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions`` for details.
        
        components : `None`, ``Component``, (`tuple`, `list`) of (``Component``, (`tuple`, `list`) of
                ``Component``) = `None`, Optional (Keyword only)
            Components attached to the message.
            
            > `components` do not count towards having any content in the message.
        
        embed : ``EmbedBase``, `list` of ``EmbedBase`` = `None`, Optional (Keyword only)
            The embedded content of the message.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `TypeError` is raised.
        
        file : `None`, `Any` = `None`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        
        reply_fail_fallback : `bool` = `False`, Optional (Keyword only)
            Whether normal message should be sent if the referenced message is deleted. Defaults to `False`.
        
        nonce : `None`, `str` = `None`, Optional (Keyword only)
            Used for optimistic message sending. Will shop up at the message's data.
        
        sticker : `None`, ``Sticker``, `int`, (`list`, `set`, `tuple`) of (``Sticker``, `int`) = `None` \
                , Optional (Keyword only)
            Sticker or stickers to send within the message.
        
        suppress_embeds : `bool` = `False`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech.
        
        Returns
        -------
        message : `None`, ``Message``
            Returns `None` if there is nothing to send.
        
        Raises
        ------
        TypeError
            - If `embed` was not given neither as ``EmbedBase``, (`list`, `tuple`) of ``EmbedBase``-s.
            - If `allowed_mentions` contains an element of invalid type.
            - `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
            - If invalid file type would be sent.
            - If `channel`'s type is incorrect.
            - If `sticker` was not given neither as `None`, ``Sticker``, `int`, (`list`, `tuple`) of \
                (``Sticker``, `int).
            - If `components` type is incorrect.
        ValueError
            - If `allowed_mentions`'s elements' type is correct, but one of their value is invalid.
            - If more than `10` files would be sent.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `tts` was not given as `bool`.
            - If `nonce` was not given neither as `None`, `str`.
            - If `reply_fail_fallback` was not given as `bool`.
            - If `embed` contains a non ``EmbedBase`` element.
            - If `suppress_embeds` is not `bool`.
            - If both `content` and `embed` fields are embeds.
        
        See Also
        --------
        ``.webhook_message_create`` : Sending a message with a ``Webhook``.
        """
        
        # Channel check order:
        # 1.: Channel -> channel
        # 2.: Message -> channel + reply
        # 3.: int (str) -> channel
        # 6.: `tuple` (`int`, `int`) -> channel + reply
        # 7.: raise
        
        while True:
            if isinstance(channel, Channel):
                if channel.is_in_group_textual() or channel.partial:
                    message_id = None
                    channel_id = channel.id
                    break
            
            elif isinstance(channel, Message):
                message_id = channel.id
                channel_id = channel.channel_id
                channel = CHANNELS.get(channel_id, None)
                break
            
            else:
                channel_id = maybe_snowflake(channel)
                if (channel_id is not None):
                    message_id = None
                    channel = CHANNELS.get(channel_id, None)
                    break
                
                else:
                    snowflake_pair = maybe_snowflake_pair(channel)
                    if snowflake_pair is not None:
                        channel_id, message_id = snowflake_pair
                        channel = CHANNELS.get(channel_id, None)
                        break
            
            raise TypeError(
                f'`channel` can be a messageable channel, `{Message.__name__}`, `int`, `tuple` (`int`, `int`), '
                f'got {channel.__class__.__name__}; {channel!r}.'
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
            
            if not isinstance(reply_fail_fallback, bool):
                raise AssertionError(
                    f'`reply_fail_fallback` can be `bool`, got {reply_fail_fallback.__class__.__name__}; '
                    f'{reply_fail_fallback!r}.')
            
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
            contains_content = True
        
        if tts:
            message_data['tts'] = True
        
        if (nonce is not None):
            message_data['nonce'] = nonce
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (message_id is not None):
            message_reference_data = {'message_id': message_id}
            
            if reply_fail_fallback:
                message_reference_data['fail_if_not_exists'] = False
            
            message_data['message_reference'] = message_reference_data
        
        if suppress_embeds:
            message_data['flags'] = MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
        
        message_data = add_file_to_message_data(message_data, file, contains_content, False)
        if message_data is None:
            return
        
        message_data = await self.http.message_create(channel_id, message_data)
        if (channel is not None):
            return channel._create_new_message(message_data)
    

    async def message_edit(
        self, message, content=..., *, embed = ..., file=..., allowed_mentions = ..., components = ..., suppress=...,
        suppress_embeds=...
    ):
        """
        Edits the given `message`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message to edit.
        content : `None`, `str`, ``EmbedBase``, `Any`, Optional
            The new content of the message.
            
            If given as `str` then the message's content will be edited with it. If given as any non ``EmbedBase``
            instance, then it will be cased to string first.
            
            If given as ``EmbedBase``, then the message's embeds will be edited with it.
        embed : `None`, ``EmbedBase``, `list` of ``EmbedBase``, Optional (Keyword only)
            The new embedded content of the message. By passing it as `None`, you can remove the old.
            
            If `embed` and `content` parameters are both given as  ``EmbedBase``, then `AssertionError` is
            raised.
        
        file : `None`, `Any`, Optional (Keyword only)
            A file or files to send. Check ``create_file_form`` for details.
        
        allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, `list` of (`str`, ``UserBase``, ``Role`` )
                , Optional (Keyword only)
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        components : `None`, ``Component``, (`tuple`, `list`) of (``Component``, (`tuple`, `list`) of
                ``Component``), Optional (Keyword only)
            Components attached to the message.
            
            Pass it as `None` remove the actual ones.
        
        suppress : `bool`, Optional (Keyword only)
            Whether the message's embeds should be suppressed or unsuppressed.
            
            Deprecated, please use `suppress_embeds` parameter instead.
        
        suppress_embeds : `bool`, Optional (Keyword only)
            Whether the message's embeds should be suppressed or unsuppressed.
        
        Raises
        ------
        TypeError
            - If `embed` was not given neither as ``EmbedBase``, (`list`, `tuple`) of ``EmbedBase``-s.
            - If `allowed_mentions` contains an element of invalid type.
            - `content` parameter was given as ``EmbedBase``, meanwhile `embed` parameter was given as well.
            - If `message`'s type is incorrect.
            - If `components` type is incorrect.
        ValueError
            - If `allowed_mentions` contains an element of invalid type.
            - If more than `10` files would be sent.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `suppress_embeds` was not given as `bool`.
            - If `embed` contains a non ``EmbedBase`` element.
            - If both `content` and `embed` fields are embeds.
        
        See Also
        --------
        - ``.message_suppress_embeds`` : For suppressing only the embeds of the message.
        - ``.webhook_message_edit`` : Editing messages sent by webhooks.
        
        Notes
        -----
        Do not updates he given message object, so dispatch event events can still calculate differences when received.
        """
        message, channel_id, message_id = get_message_and_channel_id_and_message_id(message)
        
        content, embed = validate_content_and_embed(content, embed, True)
        
        components = get_components_data(components, True)
        
        if (suppress is not ...):
            warnings.warn(
                (
                    f'`{self.__class__.__name__}.message_edit`\'s `suppress` parameter is deprecated, and '
                    f'will be removed in 2022 May. Please use `suppress_embeds` instead.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            suppress_embeds = suppress
        
        if __debug__:
            if (suppress_embeds is not ...) and (not isinstance(suppress_embeds, bool)):
                raise AssertionError(
                    f'`suppress_embeds` can be `bool`, got {suppress_embeds.__class__.__name__}; {suppress_embeds!r}.'
                )
        
        # Build payload
        message_data = {}
        
        if (content is not ...):
            message_data['content'] = content
        
        if (embed is not ...):
            if (embed is not None):
                embed = [embed.to_data() for embed in embed]
            
            message_data['embeds'] = embed
        
        if (allowed_mentions is not ...):
            message_data['allowed_mentions'] = parse_allowed_mentions(allowed_mentions)
        
        if (components is not ...):
            message_data['components'] = components
        
        if (suppress is not ...):
            if message is None:
                flags = 0
            else:
                flags = message.flags
            
            if suppress_embeds:
                flags |= MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
            else:
                flags &= ~MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
            
            message_data['flags'] = flags
        
        message_data = add_file_to_message_data(message_data, file, True, True)
        if (message_data is None):
            return
        
        await self.http.message_edit(channel_id, message_id, message_data)
    
    
    async def message_delete(self, message, *, reason = None):
        """
        Deletes the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If message was not given neither as ``Message``, `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        The rate limit group is different for own or for messages newer than 2 weeks than for message's of others,
        which are older than 2 weeks.
        """
        
        channel_id, message_id, message = validate_message_to_delete(message)
        
        if (message is None):
            author = None
        else:
            if not message.is_deletable():
                return
            
            author = message.author
        
        if (author is self) or (message_id > int((time_now() - 1209590.) * 1000.-DISCORD_EPOCH) << 22):
            # own or new
            coroutine = self.http.message_delete(channel_id, message_id, reason)
        else:
            coroutine = self.http.message_delete_b2wo(channel_id, message_id, reason)
        
        await coroutine
        # If the coroutine raises, do not switch `message.deleted` to `True`.
        if (message is not None):
            message.deleted = True
    
    
    async def message_delete_multiple(self, messages, *, reason = None):
        """
        Deletes the given messages. The messages can be from different channels as well.
        
        This method is a coroutine.
        
        Parameters
        ----------
        messages : (`list`, `set`, `tuple`) of \
                (``Message``, `tuple` (`int`, `int`))
            The messages to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If a message was not given neither as ``Message``, `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `messages` was not given neither as `list`, `set`, `tuple`.
        
        Notes
        -----
        This method uses up 3 different rate limit groups parallelly to maximize the deletion speed.
        """
        if __debug__:
            if not isinstance(messages, (list, set, tuple)):
                raise AssertionError(
                    f'`messages` can be `list`, `set`, `tuple`, got {messages.__class__.__name__}; {messages!r}.'
                )
        
        if not messages:
            return
        
        bulk_delete_limit = int((time_now() - 1209600.) * 1000.-DISCORD_EPOCH) << 22 # 2 weeks
        
        by_channel = {}
        
        for message in messages:
            channel_id, message_id, message = validate_message_to_delete(message)
            if (message is not None) and (not message.is_deletable()):
                continue
            
            if message is None:
                own = False
            else:
                if message.author is self:
                    own = True
                else:
                    own = False
            
            try:
                message_group_new, message_group_old, message_group_old_own = by_channel[channel_id]
            except KeyError:
                message_group_new = deque()
                message_group_old = deque()
                message_group_old_own = deque()
                by_channel[channel_id] = (message_group_new, message_group_old, message_group_old_own)
            
            if message_id > bulk_delete_limit:
                message_group_new.append((own, message_id),)
                continue
            
            if own:
                group = message_group_old_own
            else:
                group = message_group_old
            
            group.append(message_id)
            continue
        
        tasks = []
        for channel_id, groups in by_channel.items():
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                is_private = False
            else:
                if channel.partial:
                    is_private = True
                else:
                    is_private = channel.is_in_group_private()
            
            if is_private:
                function = _message_delete_multiple_private_task
            else:
                function = _message_delete_multiple_task
            
            task = Task(function(self, channel_id, groups, reason), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)
        
        last_exception = None
        for task in tasks:
            exception = task.exception()
            if exception is None:
                continue
            
            if last_exception is None:
                last_exception = exception
            else:
                if isinstance(exception, ConnectionError):
                    # This is the lowest priority exception, never overwrite older ones.
                    pass
                elif isinstance(exception, DiscordException):
                    # Do overwrite only `ConnectionError`.
                    if isinstance(last_exception, ConnectionError):
                        last_exception = exception
                else:
                    # Do not overwrite same tier exceptions again, only `ConnectionError` and `DiscordException`
                    if isinstance(last_exception, (ConnectionError, DiscordException)):
                        last_exception = exception
            
            task.cancel()
        
        if (last_exception is not None):
            raise last_exception
    
        
    async def message_delete_sequence(self, channel, *, after=None, before=None, limit=None, filter=None, reason = None):
        """
        Deletes messages between an interval determined by `before` and `after`. They can be `int`, or as
        a ``DiscordEntity`` or as a `datetime` object.
        
        If the client has no `manage_messages` permission at the channel, then returns instantly.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``
            The channel, where the deletion should take place.
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the messages were created, which will be deleted.
        before : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp before the messages were created, which will be deleted.
        limit : `None`, `int` = `None`, Optional (Keyword only)
            The maximal amount of messages to delete.
        filter : `None`, `callable` = `None`, Optional (Keyword only)
            A callable filter, what should accept a message object as parameter and return either `True`, `False`.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `after`, `before` was passed with an unexpected type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `channel` was not given as ``Channel``.
        
        Notes
        -----
        This method uses up 4 different rate limit groups parallelly to maximize the request and the deletion speed.
        """
        if __debug__:
            if not (isinstance(channel, Channel) and (channel.is_in_group_textual() or channel.partial)):
                raise AssertionError(
                    f'`channel` can be a messageable channel, got {channel.__class__.__name__}; {channel!r}.'
                )
        
        # Check permissions
        permissions = channel.cached_permissions_for(self)
        if not permissions & PERMISSION_MASK_MANAGE_MESSAGES:
            return
        
        before = 9223372036854775807 if before is None else log_time_converter(before)
        after = 0 if after is None else log_time_converter(after)
        limit = 9223372036854775807 if limit is None else limit
        
        # Check for reversed intervals
        if before < after:
            return
        
        # Check if we are done already
        if limit <= 0:
            return
        
        message_group_new = deque()
        message_group_old = deque()
        message_group_old_own = deque()
        
        # Check if we can request more messages
        if channel.message_history_reached_end or (not permissions & PERMISSION_MASK_READ_MESSAGE_HISTORY):
            should_request = False
        else:
            should_request = True
        
        last_message_id = before
        
        messages_ = channel.messages
        if (messages_ is not None) and messages_:
            before_index = message_relative_index(messages_, before)
            after_index = message_relative_index(messages_, after)
            if before_index != after_index:
                time_limit = int((time_now() - 1209600.) * 1000.-DISCORD_EPOCH) << 22
                while True:
                    if before_index == after_index:
                        break
                    
                    message_ = messages_[before_index]
                    before_index += 1
                    
                    # Ignore invoking user only messages! Desu!
                    if not message_.is_deletable():
                        continue
                    
                    if (filter is not None):
                        if not filter(message_):
                            continue
                    
                    last_message_id = message_.id
                    own = (message_.author is self)
                    if last_message_id > time_limit:
                        message_group_new.append((own, last_message_id,),)
                    else:
                        if own:
                            group = message_group_old_own
                        else:
                            group = message_group_old
                        group.append(last_message_id)
                    
                    # Check if we reached the limit
                    limit -= 1
                    if limit:
                        continue
                    
                    should_request = False
                    break
        
        tasks = []
        
        get_mass_task = None
        delete_mass_task = None
        delete_new_task = None
        delete_old_task = None
        
        channel_id = channel.id
        
        while True:
            if should_request and (get_mass_task is None):
                request_data = {
                    'limit': 100,
                    'before': last_message_id,
                }
                
                get_mass_task = Task(self.http.message_get_chunk(channel_id, request_data), KOKORO)
                tasks.append(get_mass_task)
            
            if (delete_mass_task is None):
                message_limit = len(message_group_new)
                # If there are more messages, we are waiting for other tasks
                if message_limit:
                    time_limit = int((time_now() - 1209590.) * 1000.-DISCORD_EPOCH) << 22 # 2 weeks -10s
                    collected = 0
                    
                    while True:
                        if collected == message_limit:
                            break
                        
                        if collected == 100:
                            break
                        
                        own, message_id = message_group_new[collected]
                        if message_id < time_limit:
                            break
                        
                        collected += 1
                        continue
                    
                    if collected == 0:
                        pass
                    
                    elif collected == 1:
                        # Delete the message if we don't delete a new message already
                        if (delete_new_task is None):
                            # We collected 1 message -> We cannot use mass delete on this.
                            own, message_id = message_group_new.popleft()
                            delete_new_task = Task(self.http.message_delete(channel_id, message_id, reason),
                                KOKORO)
                            tasks.append(delete_new_task)
                    else:
                        message_ids = []
                        while collected:
                            collected -= 1
                            own, message_id = message_group_new.popleft()
                            message_ids.append(message_id)
                        
                        delete_mass_task = Task(self.http.message_delete_multiple(channel_id, {'messages': message_ids},
                            reason), KOKORO)
                        tasks.append(delete_mass_task)
                    
                    # After we checked what is at this group, lets move the others from it's end, if needed ofc
                    message_limit = len(message_group_new)
                    if message_limit:
                        # time limit -> 2 week
                        time_limit = time_limit - 20971520000
                        
                        while True:
                            # Cannot start at index = len(...), so we instantly do -1
                            message_limit -= 1
                            
                            own, message_id = message_group_new[message_limit]
                            # Check if we should not move -> leave
                            if message_id > time_limit:
                                break
                            
                            del message_group_new[message_limit]
                            if own:
                                group = message_group_old_own
                            else:
                                group = message_group_old
                                
                            group.appendleft(message_id)
                            
                            if message_limit:
                                continue
                            
                            break
            
            if (delete_new_task is None):
                # Check old own messages only, mass delete speed is pretty good by itself.
                if message_group_old_own:
                    message_id = message_group_old_own.popleft()
                    delete_new_task = Task(self.http.message_delete(channel_id, message_id, reason), KOKORO)
                    tasks.append(delete_new_task)
            
            if (delete_old_task is None):
                if message_group_old:
                    message_id = message_group_old.popleft()
                    delete_old_task = Task(self.http.message_delete_b2wo(channel_id, message_id, reason), KOKORO)
                    tasks.append(delete_old_task)
            
            if not tasks:
                # It can happen, that there are no more tasks left, at that case we check if there is more message
                # left. Only at `message_group_new` can be anymore message, because there is a time interval of
                # 10 seconds, what we do not move between categories.
                if not message_group_new:
                    break
                
                # We really have at least 1 message at that interval.
                own, message_id = message_group_new.popleft()
                # We will delete that message with old endpoint if not own, to make sure it will not block the other
                # endpoint for 2 minutes with any chance.
                if own:
                    delete_new_task = Task(self.http.message_delete(channel_id, message_id, reason), KOKORO)
                    task = delete_new_task
                else:
                    delete_old_task = Task(self.http.message_delete_b2wo(channel_id, message_id, reason), KOKORO)
                    task = delete_old_task
                
                tasks.append(task)
            
            done, pending = await WaitTillFirst(tasks, KOKORO)
            
            for task in done:
                tasks.remove(task)
                try:
                    result = task.result()
                except:
                    for task in tasks:
                        task.cancel()
                    raise
                
                if task is get_mass_task:
                    get_mass_task = None
                    
                    received_count = len(result)
                    if received_count < 100:
                        should_request = False
                        
                        # We got 0 messages, move on the next task
                        if received_count == 0:
                            continue
                    
                    # We don't really care about the limit, because we check message id when we delete too.
                    time_limit = int((time_now() - 1209600.) * 1000.-DISCORD_EPOCH) << 22 # 2 weeks
                    
                    for message_data in result:
                        if (filter is None):
                            last_message_id = int(message_data['id'])
    
                            # Did we reach the after limit?
                            if last_message_id < after:
                                should_request = False
                                break
                            
                            # If filter is `None`, we just have to decide, if we were the author or nope.
                            
                            # Try to get user id, first start it with trying to get author data. The default author_id
                            # will be 0, because that's sure not the id of the client.
                            try:
                                author_data = message_data['author']
                            except KeyError:
                                author_id = 0
                            else:
                                # If we have author data, lets select the user's data from it
                                try:
                                    user_data = author_data['user']
                                except KeyError:
                                    user_data = author_data
                                
                                try:
                                    author_id = user_data['id']
                                except KeyError:
                                    author_id = 0
                                else:
                                    author_id = int(author_id)
                        else:
                            message_ = Message.from_data(message_data)
                            last_message_id = message_.id
                            
                            # Did we reach the after limit?
                            if last_message_id < after:
                                should_request = False
                                break
                            
                            if not filter(message_):
                                continue
                            
                            author_id = message_.author.id
                        
                        own = (author_id == self.id)
                        
                        if last_message_id > time_limit:
                            message_group_new.append((own, last_message_id,),)
                        else:
                            if own:
                                group = message_group_old_own
                            else:
                                group = message_group_old
                            
                            group.append(last_message_id)
                        
                        # Did we reach the amount limit?
                        limit -= 1
                        if limit:
                            continue
                        
                        should_request = False
                        break
                
                if task is delete_mass_task:
                    delete_mass_task = None
                    continue
                
                if task is delete_new_task:
                    delete_new_task = None
                    continue
                
                if task is delete_old_task:
                    delete_old_task = None
                    continue
                 
                # Should not happen
                continue
    
    
    async def multi_client_message_delete_sequence(
        self, channel, *, after=None, before=None, limit=None, filter=None, reason = None
    ):
        """
        Deletes messages between an interval determined by `before` and `after`. They can be `int`, or as
        a ``DiscordEntity`` or as a `datetime` object.
        
        Not like ``.message_delete_sequence``, this method uses up all he clients at the respective channel to delete
        messages an not only the one from what it was called from.
        
        If non of the clients have `manage_messages` permission, then returns instantly.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``
            The channel, where the deletion should take place.
        after : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp after the messages were created, which will be deleted.
        before : `None`, `int`, ``DiscordEntity``, `datetime` = `None`, Optional (Keyword only)
            The timestamp before the messages were created, which will be deleted.
        limit : `None`, `int` = `None`, Optional (Keyword only)
            The maximal amount of messages to delete.
        filter : `None`, `callable` = `None`, Optional (Keyword only)
            A callable filter, what should accept a message object as parameter and return either `True`, `False`.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `after`, `before` was passed with an unexpected type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `channel` is not ``Channel``.
        
        Notes
        -----
        This method uses up to 4 different endpoint groups too as ``.message_delete_sequence``, but tries to
        parallelize the them between more clients as well.
        """
        if __debug__:
            if not (isinstance(channel, Channel) and (channel.is_in_group_textual() or channel.partial)):
                raise AssertionError(
                    f'`channel` can be a messageable channel, got {channel.__class__.__name__}; {channel!r}.'
                )
        
        # Check permissions
        sharders = []
        
        for client in channel.clients:
            sharder = MultiClientMessageDeleteSequenceSharder(client, channel)
            if sharder is None:
                continue
            
            sharders.append(sharder)
        
        if not sharders:
            return
        
        for sharder in sharders:
            if sharder.can_manage_messages:
                break
        else:
            return
        
        before = 9223372036854775807 if before is None else log_time_converter(before)
        after = 0 if after is None else log_time_converter(after)
        limit = 9223372036854775807 if limit is None else limit
        
        # Check for reversed intervals
        if before < after:
            return
        
        # Check if we are done already
        if limit <= 0:
            return
        
        message_group_new = deque()
        message_group_old = deque()
        message_group_old_own = deque()
        
        # Check if we can request more messages
        if channel.message_history_reached_end:
            should_request = False
        else:
            for sharder in sharders:
                if sharder.can_read_message_history:
                    should_request = True
                    break
            else:
                should_request = False
        
        last_message_id = before
        
        is_own_getter = {}
        for index in range(len(sharders)):
            is_own_getter[sharders[index].client.id] = index
        
        messages_ = channel.messages
        if (messages_ is not None) and messages_:
            before_index = message_relative_index(messages_, before)
            after_index = message_relative_index(messages_, after)
            if before_index != after_index:
                time_limit = int((time_now() - 1209600.) * 1000.-DISCORD_EPOCH) << 22
                while True:
                    if before_index == after_index:
                        break
                    
                    message_ = messages_[before_index]
                    before_index += 1
                    
                    if not message_.is_deletable():
                        continue
                    
                    if (filter is not None):
                        if not filter(message_):
                            continue
                    
                    last_message_id = message_.id
                    who_s = is_own_getter.get(message_.author.id, -1)
                    if last_message_id > time_limit:
                        message_group_new.append((who_s, last_message_id,),)
                    else:
                        if who_s == -1:
                            message_group_old.append(last_message_id)
                        else:
                            message_group_old_own.append((who_s, last_message_id,),)
                    
                    # Check if we reached the limit
                    limit -= 1
                    if limit:
                        continue
                    
                    should_request = False
                    break
        
        tasks = []
        # Handle requesting together, since we need to know, till where the last request yielded.
        get_mass_task = None
        # Loop the sharders when requesting, so rate limits are used up.
        get_mass_task_next = 0
        
        channel_id = channel.id
        
        while True:
            if should_request and (get_mass_task is None):
                # Will break since `should_request` is set to `True` only if at least of the sharders have
                # `read_message_history` permission
                while True:
                    if get_mass_task_next >= len(sharders):
                        get_mass_task_next = 0
                    
                    sharder = sharders[get_mass_task_next]
                    if sharder.can_read_message_history:
                        break
                    
                    get_mass_task_next += 1
                    continue
                
                request_data = {
                    'limit': 100,
                    'before': last_message_id,
                }
                
                get_mass_task = Task(sharder.client.http.message_get_chunk(channel_id, request_data), KOKORO)
                tasks.append(get_mass_task)
            
            for sharder in sharders:
                if (sharder.can_manage_messages) and (sharder.delete_mass_task is None):
                    message_limit = len(message_group_new)
                    # If there are more messages, we are waiting for other tasks
                    if message_limit:
                        time_limit = int((time_now() - 1209590.) * 1000.-DISCORD_EPOCH) << 22 # 2 weeks -10s
                        collected = 0
                        
                        while True:
                            if collected == message_limit:
                                break
                            
                            if collected == 100:
                                break
                            
                            who_s, message_id = message_group_new[collected]
                            if message_id < time_limit:
                                break
                            
                            collected += 1
                            continue
                        
                        if collected == 0:
                            pass
                        
                        elif collected == 1:
                            # Delete the message if we don't delete a new message already
                            for sub_sharder in sharders:
                                if (sub_sharder.can_manage_messages) and (sharder.delete_new_task is None):
                                    # We collected 1 message -> We cannot use mass delete on this.
                                    who_s, message_id = message_group_new.popleft()
                                    delete_new_task = Task(sub_sharder.client.http.message_delete(channel_id,
                                        message_id, reason = reason), KOKORO)
                                    sub_sharder.delete_new_task = delete_new_task
                                    tasks.append(delete_new_task)
                                    break
                        else:
                            message_ids = []
                            while collected:
                                collected -= 1
                                who_s, message_id = message_group_new.popleft()
                                message_ids.append(message_id)
                            
                            delete_mass_task = Task(sharder.client.http.message_delete_multiple(channel_id,
                                {'messages': message_ids}, reason), KOKORO)
                            sharder.delete_mass_task = delete_mass_task
                            tasks.append(delete_mass_task)
                        
                        # After we checked what is at this group, lets move the others from it's end, if needed ofc
                        message_limit = len(message_group_new)
                        if message_limit:
                            # time limit -> 2 week
                            time_limit = time_limit - 20971520000
                            
                            while True:
                                # Cannot start at index = len(...), so we instantly do -1
                                message_limit -= 1
                                
                                who_s, message_id = message_group_new[message_limit]
                                # Check if we should not move -> leave
                                if message_id > time_limit:
                                    break
                                
                                del message_group_new[message_limit]
                                if who_s == -1:
                                    message_group_old.appendleft(message_id)
                                else:
                                    message_group_old_own.appendleft((who_s, message_group_old,),)
                                
                                if message_limit:
                                    continue
                                
                                break
            
            # Check old own messages only, mass delete speed is pretty good by itself.
            if message_group_old_own:
                # Check who's is the last message. And delete with it. These speed is pretty fast.
                # I doubt it needs further speedup, since deleting not own messages are the bottleneck of message
                # deletions.
                who_s, message_id = message_group_old_own[0]
                sharder = sharders[who_s]
                if sharder.delete_new_task is None:
                    del message_group_old_own[0]
                    delete_new_task = Task(sharder.client.http.message_delete(channel_id, message_id, reason), KOKORO)
                    sharder.delete_new_task = delete_new_task
                    tasks.append(delete_new_task)
            
            if message_group_old:
                for sharder in sharders:
                    if (sharder.delete_old_task is None):
                        message_id = message_group_old.popleft()
                        delete_old_task = Task(
                            sharder.client.http.message_delete_b2wo(channel_id, message_id, reason), KOKORO
                        )
                        sharder.delete_old_task = delete_old_task
                        tasks.append(delete_old_task)
                        
                        if not message_group_old:
                            break
            
            if not tasks:
                # It can happen, that there are no more tasks left, at that case we check if there is more message
                # left. Only at `message_group_new` can be anymore message, because there is a time interval of
                # 10 seconds, what we do not move between categories.
                if not message_group_new:
                    break
                
                # We really have at least 1 message at that interval.
                who_s, message_id = message_group_new.popleft()
                # We will delete that message with old endpoint if not own, to make sure it will not block the other
                # endpoint for 2 minutes with any chance.
                if who_s == -1:
                    for sharder in sharders:
                        if sharder.can_manage_messages:
                            task = Task(sharder.client.http.message_delete_b2wo(channel_id, message_id, reason), KOKORO)
                            tasks.append(task)
                            sharder.delete_old_task = task
                            break
                else:
                    sharder = sharders[who_s]
                    task = Task(sharder.client.http.message_delete(channel_id, message_id, reason), KOKORO)
                    tasks.append(task)
                    sharder.delete_new_task = task
            
            
            done, pending = await WaitTillFirst(tasks, KOKORO)
            
            for task in done:
                tasks.remove(task)
                try:
                    result = task.result()
                except:
                    for task in tasks:
                        task.cancel()
                    raise
                
                if task is get_mass_task:
                    get_mass_task = None
                    
                    received_count = len(result)
                    if received_count < 100:
                        should_request = False
                        
                        # We got 0 messages, move on the next task
                        if received_count == 0:
                            continue
                    
                    # We don't really care about the limit, because we check message id when we delete too.
                    time_limit = int((time_now() - 1209600.) * 1000.-DISCORD_EPOCH) << 22 # 2 weeks
                    
                    for message_data in result:
                        if (filter is None):
                            last_message_id = int(message_data['id'])
                            
                            # Did we reach the after limit?
                            if last_message_id < after:
                                should_request = False
                                break
                            
                            # If filter is `None`, we just have to decide, if we were the author or nope.
                            
                            # Try to get user id, first start it with trying to get author data. The default author_id
                            # will be 0, because that's sure not the id of the client.
                            try:
                                author_data = message_data['author']
                            except KeyError:
                                author_id = 0
                            else:
                                # If we have author data, lets select the user's data from it
                                try:
                                    user_data = author_data['user']
                                except KeyError:
                                    user_data = author_data
                                
                                try:
                                    author_id = user_data['id']
                                except KeyError:
                                    author_id = 0
                                else:
                                    author_id = int(author_id)
                        else:
                            message_ = Message.from_data(message_data)
                            last_message_id = message_.id
                            
                            # Did we reach the after limit?
                            if last_message_id < after:
                                should_request = False
                                break
                            
                            if not filter(message_):
                                continue
                            
                            author_id = message_.author.id
                        
                        who_s = is_own_getter.get(author_id, -1)
                        
                        if last_message_id > time_limit:
                            message_group_new.append((who_s, last_message_id,),)
                        else:
                            if who_s == -1:
                                message_group_old.append(last_message_id)
                            else:
                                message_group_old_own.append((who_s, last_message_id,),)
                        
                        # Did we reach the amount limit?
                        limit -= 1
                        if limit:
                            continue
                        
                        should_request = False
                        break
                
                for sharder in sharders:
                    if task is sharder.delete_mass_task:
                        sharder.delete_mass_task = None
                        break
                    
                    if task is sharder.delete_new_task:
                        sharder.delete_new_task = None
                        break
                    
                    if task is sharder.delete_old_task:
                        sharder.delete_old_task = None
                        break
                
                # Else case should happen.
                continue
    
    
    async def message_suppress_embeds(self, message, suppress_embeds=True):
        """
        Suppresses or unsuppressed the given message's embeds.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message, what's embeds will be (un)suppressed.
        suppress_embeds : `bool` = `True`, Optional
            Whether the message's embeds would be suppressed or unsuppressed.
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `suppress` was not given as `bool`.
        """
        message, channel_id, message_id = get_message_and_channel_id_and_message_id(message)
        
        if __debug__:
            if not isinstance(suppress_embeds, bool):
                raise AssertionError(
                    f'`suppress_embeds` can be `bool`, got {suppress_embeds.__class__.__name__}; {suppress_embeds!r}.'
                )
        
        if message is None:
            flags = 0
        else:
            flags = message.flags
        
        if suppress_embeds:
            flags |= MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
        else:
            flags &= ~MESSAGE_FLAG_VALUE_SUPPRESS_EMBEDS
        
        await self.http.message_edit(channel_id, message_id, {'flags': flags})
    
    
    async def message_crosspost(self, message):
        """
        Crossposts the given message. The message's channel must be an announcements (type 5) channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message to crosspost.
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        
        await self.http.message_crosspost(channel_id, message_id)
    
    
    async def message_pin(self, message):
        """
        Pins the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message to pin.
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        
        await self.http.message_pin(channel_id, message_id)
    
    
    async def message_unpin(self, message):
        """
        Unpins the given message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        message : ``Message``, `tuple` (`int`, `int`)
            The message to unpin.
        
        Raises
        ------
        TypeError
            If `message` was not given neither as ``Message``, `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id, message_id = get_channel_id_and_message_id(message)
        
        await self.http.message_unpin(channel_id, message_id)
    
    
    async def channel_pin_get_all(self, channel):
        """
        Returns the pinned messages at the given channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel from were the pinned messages will be requested.
        
        Returns
        -------
        messages : `list` of ``Message`` objects
            The pinned messages at the given channel.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_textual)
        
        data = await self.http.channel_pin_get_all(channel_id)
        
        return [Message.from_data(message_data) for message_data in data]
    
    
    async def _load_messages_till(self, channel, index):
        """
        An internal function to load the messages at the given channel till the given index. Should not be called if
        the channel reached it's message history's end.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``
            The channel from where the messages will be requested.
        index : `int`
            Till which index the messages should be requested at the given channel.
        
        Returns
        -------
        result_state : `int`
            can return the following variables describing a state:
            
            +-----------+---------------------------------------------------------------------------+
            | Value     | Description                                                               |
            +-----------+---------------------------------------------------------------------------+
            | 0         | Success.                                                                  |
            +-----------+---------------------------------------------------------------------------+
            | 1         | `index` could not be reached, there is no more messages at the channel.   |
            +-----------+---------------------------------------------------------------------------+
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        while True:
            messages = channel.messages
            if messages is None:
                ln = 0
            else:
                ln = len(channel.messages)
            
            load_to = index - ln
            
            # we want to load it till the exact index, so if `load_to` is `0`, that's not enough!
            if load_to < 0:
                result_state = 0
                break
            
            if load_to < 98:
                planned = load_to + 2
            else:
                planned = 100
            
            if ln:
                result = await self.message_get_chunk(channel, planned, before=messages[ln - 1].id + 1)
            else:
                result = await self.message_get_chunk_from_zero(channel, planned)
            
            if len(result) < planned:
                channel.message_history_reached_end = True
                result_state = 1
                break
        
        # Set some collection delay.
        channel._add_message_collection_delay(float(index))
        
        return result_state
    
    
    async def message_get_at_index(self, channel, index):
        """
        Returns the message at the given channel at the specific index. Can be used to load `index` amount of messages
        at the channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`.
            The channel from were the messages will be requested.
        index : `int`
            The index of the target message.
        
        Returns
        -------
        message : ``Message`` object
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `index` was not given as `int`.
            - If `index` is out of range [0:].
        """
        if __debug__:
            if not isinstance(index, int):
                raise AssertionError(
                    f'`index` can be `int`, got {index.__class__.__name__}; {index!r}.'
                )
            
            if index < 0:
                raise AssertionError(
                    f'`index` is out from the expected [0:] range, got {index!r}.'
                )
        
        channel, channel_id = get_channel_and_id(channel, Channel.is_in_group_textual)
        if channel is None:
            messages = await self.message_get_chunk_from_zero(channel_id, min(index + 1, 100))
            
            if messages:
                channel = messages[0].channel
            else:
                raise IndexError(index)
        
        messages = channel.messages
        if (messages is not None) and (index < len(messages)):
            raise IndexError(index)
        
        if channel.message_history_reached_end:
            raise IndexError(index)
        
        if await self._load_messages_till(channel, index):
            raise IndexError(index)
        
        # access it again, because it might be modified
        messages = channel.messages
        if messages is None:
            raise IndexError(index)
        
        return messages[index]
    
    
    async def message_get_all_in_range(self, channel, start=0, end=100):
        """
        Returns a list of the message between the `start` - `end` area. If the client has no permission to request
        messages, or there are no messages at the given area returns an empty list.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel from were the messages will be requested.
        start : `int` = `0`, Optional
            The first message's index at the channel to be requested. Defaults to `0`.
        end : `int` = `100`, Optional
            The last message's index at the channel to be requested. Defaults to `100`.
        
        Returns
        -------
        messages : `list` of ``Message`` objects
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `start` was not given as `int`.
            - If `start` is out of range [0:].
            - If `end` was not given as `int`.
            - If `end` is out of range [0:].
        """
        if __debug__:
            if not isinstance(start, int):
                raise AssertionError(
                    f'`start` can be `int`, got {start.__class__.__name__}; {start!r}.'
                )
            
            if start < 0:
                raise AssertionError(
                    f'`start` is out from the expected [0:] range, got {start!r}.'
                )
        
            if not isinstance(end, int):
                raise AssertionError(
                    f'`end` can be `int`, got {end.__class__.__name__}; {end!r}.'
                )
            
            if end < 0:
                raise AssertionError(
                    f'`end` is out from the expected [0:] range, got {end!r}.'
                )
        
        channel, channel_id = get_channel_and_id(channel, Channel.is_in_group_textual)
        if channel is None:
            messages = await self.message_get_chunk_from_zero(channel_id, min(end + 1, 100))
            
            if messages:
                channel = messages[0].channel
            else:
                return []
        
        if end <= start:
            return []
        
        messages = channel.messages
        if messages is None:
            ln = 0
        else:
            ln = len(messages)
        
        if (end >= ln) and (not channel.message_history_reached_end) and \
               channel.cached_permissions_for(self) & PERMISSION_MASK_READ_MESSAGE_HISTORY:
            
            try:
                await self._load_messages_till(channel, end)
            except DiscordException as err:
                if err.code not in (
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.unknown_channel, # message's channel deleted
                    ERROR_CODES.missing_access, # client removed
                    ERROR_CODES.missing_permissions, # permissions changed meanwhile
                    ERROR_CODES.cannot_message_user, # user has dm-s disallowed
                ):
                    raise
        
        result = []
        messages = channel.messages
        if (messages is not None):
            for index in range(start, min(end, len(messages))):
                result.append(messages[index])
        
        return result
    
    
    async def message_iterator(self, channel, *, chunk_size=99):
        """
        Returns an asynchronous message iterator over the given text channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``  or `int`
            The channel from were the messages will be requested.
        chunk_size : `int` = `99`, Optional (Keyword only)
            The amount of messages to request when the currently loaded history is exhausted. For message chaining
            it is preferably `99`.
        
        Returns
        -------
        message_iterator : ``MessageIterator``
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `chunk_size` was not given as `int`.
            - If `chunk_size` is out of range [1:].
        """
        return await MessageIterator(self, channel, chunk_size)
