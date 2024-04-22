__all__ = ()

import reprlib

from scarletio import Compound

from ...application import Application
from ...bases import maybe_snowflake
from ...builder.serialization import create_serializer
from ...builder.serialization_configuration import SerializationConfiguration
from ...channel import Channel, ChannelType, create_partial_channel_from_id
from ...http import DiscordApiClient, VALID_ICON_MEDIA_TYPES_EXTENDED
from ...message import Message
from ...message.message_builder import MessageBuilderWebhookCreate, MessageBuilderWebhookEdit
from ...utils import get_image_media_type, image_to_base64
from ...webhook import Webhook, create_partial_webhook_from_id

from ..request_helpers import (
    get_channel_id, get_guild_id, get_webhook_and_id, get_webhook_and_id_and_token, get_webhook_id,
    get_webhook_id_and_token,
)


MESSAGE_SERIALIZER_WEBHOOK_CREATE = create_serializer(
    MessageBuilderWebhookCreate,
    SerializationConfiguration(
        [
            MessageBuilderWebhookCreate.allowed_mentions,
            MessageBuilderWebhookCreate.attachments,
            MessageBuilderWebhookCreate.applied_tag_ids,
            MessageBuilderWebhookCreate.avatar_url,
            MessageBuilderWebhookCreate.components,
            MessageBuilderWebhookCreate.content,
            MessageBuilderWebhookCreate.embeds,
            MessageBuilderWebhookCreate.flags,
            MessageBuilderWebhookCreate.name,
            MessageBuilderWebhookCreate.poll,
            MessageBuilderWebhookCreate.thread_name,
            MessageBuilderWebhookCreate.tts,
        ],
        False,
    )
)

MESSAGE_SERIALIZER_WEBHOOK_EDIT = create_serializer(
    MessageBuilderWebhookEdit,
    SerializationConfiguration(
        [
            MessageBuilderWebhookEdit.allowed_mentions,
            MessageBuilderWebhookEdit.attachments,
            MessageBuilderWebhookEdit.components,
            MessageBuilderWebhookEdit.content,
            MessageBuilderWebhookEdit.embeds,
            MessageBuilderWebhookEdit.flags,
        ],
        True,
    )
)


class ClientCompoundWebhookEndpoints(Compound):
    
    application : Application
    api : DiscordApiClient
    
    
    async def webhook_create(self, channel, name, *, avatar = None):
        """
        Creates a webhook at the given channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel of the created webhook.
        name : `str`
            The name of the new webhook. It's length can be in range [1:80].
        avatar : `None`, `bytes-like` = `None`, Optional (Keyword only)
            The webhook's avatar. Can be `'jpg'`, `'png'`, `'webp'`, `'gif'` image's raw data. However if set as
            `'gif'`, it will not have any animation.
            
        Returns
        -------
        webhook : ``Webhook``
            The created webhook.
        
        Raises
        ------
        TypeError
            - If `channel` was not given neither as ``Channel`` nor as `int`.
            - If `avatar` was not given neither as `None`, `bytes-like`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was not given as `str`.
            - If `name` range is out of the expected range [1:80].
            - If `avatar`'s type is not any of the expected ones: `'jpg'`, `'png'`, `'webp'`, `'gif'`.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_system)
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            name_length = len(name)
            if name_length < 1 or name_length > 80:
                raise AssertionError(
                    f'`name` length can be in range [1:80], got {name_length!r}; {name!r}.'
                )
        
        data = {'name': name}
        
        if (avatar is not None):
            if not isinstance(avatar, (bytes, bytearray, memoryview)):
                raise TypeError(
                    f'`avatar` can `None`, `bytes-like`, got {avatar.__name__}; {reprlib.repr(avatar)}.'
                )
            
            if __debug__:
                media_type = get_image_media_type(avatar)
                if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                    raise AssertionError(
                        f'Invalid `avatar` media type: {media_type}; got {reprlib.repr(avatar)}.'
                    )
            
            data['avatar'] = image_to_base64(avatar)
        
        data = await self.api.webhook_create(channel_id, data)
        return Webhook.from_data(data)
    
    
    async def webhook_get(self, webhook):
        """
        Requests the webhook by it's id.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `int`
            The webhook to update or the webhook's id to get.
        
        Returns
        -------
        webhook : ``Webhook``
        
        Raises
        ------
        TypeError
            If `webhook` was not given neither as ``Webhook`` neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        See Also
        --------
        ``.webhook_get_token`` : Getting webhook with Discord's webhook API.
        
        Notes
        -----
        If the webhook already loaded and if it's guild's webhooks are up to date, no request is done.
        """
        webhook, webhook_id = get_webhook_and_id(webhook)
        
        data = await self.api.webhook_get(webhook_id)
        if webhook is None:
            webhook = Webhook.from_data(data)
        else:
            webhook._update_attributes(data)
        
        return webhook
    
    
    async def webhook_get_token(self, webhook):
        """
        Requests the webhook through Discord's webhook API. The client do not needs to be in the guild of the webhook.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook to update or the webhook's id and token.
        
        Returns
        -------
        webhook : ``Webhook``
        
        Raises
        ------
        TypeError
            If `webhook` was not given neither as ``Webhook`` neither as a `tuple` (`int`, `str`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        If the webhook already loaded and if it's guild's webhooks are up to date, no request is done.
        """
        webhook, webhook_id, webhook_token = get_webhook_and_id_and_token(webhook)
        
        if (webhook is None):
            webhook = create_partial_webhook_from_id(webhook_id, webhook_token)
        
        data = await self.api.webhook_get_token(webhook_id, webhook_token)
        webhook._set_attributes(data)
        return webhook
    
    
    async def webhook_get_all_channel(self, channel):
        """
        Requests all the webhooks of the channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel, what's webhooks will be requested.
        
        Returns
        -------
        webhooks : `list` of ``Webhook` objects
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
            
            You may expect the following exceptions:
            
            +---------------+-----------------------+---------------------------------------------------------------+
            | Error code    | Internal name         | Reason                                                        |
            +===============+=======================+===============================================================+
            | 10003         | unknown_channel       | The channel not exists.                                       |
            +---------------+-----------------------+---------------------------------------------------------------+
            | 50013         | missing_permissions   | You need `manage_webhooks` permission. (Or the client has no  |
            |               |                       | access to the channel.)                                       |
            +---------------+-----------------------+---------------------------------------------------------------+
            | 60003         | mfa_required          | You need to have multi-factor authorization to do this        |
            |               |                       | operation (guild setting dependent). For bot accounts it      |
            |               |                       | means their owner needs mfa.                                  |
            +---------------+-----------------------+---------------------------------------------------------------+
            
            > Discord drops `Forbidden (403), code = 50013: Missing Permissions` instead of
            > `Forbidden (403), code = 50001: Missing Access`.
        
        AssertionError
            If `channel` was given as a channel's identifier but it detectably not refers to a ``Channel``.
        
        Notes
        -----
        No request is done, if the passed channel is partial, or if the channel's guild's webhooks are up to date.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_guild_system)
        
        data = await self.api.webhook_get_all_channel(channel_id)
        return [Webhook.from_data(webhook_data) for webhook_data in data]
    
    
    async def webhook_get_own_channel(self, channel):
        """
        Requests the webhooks of the given channel and returns the first owned one.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel, what's webhooks will be requested.
        
        Returns
        -------
        webhooks : `list` of ``Webhook` objects
        """
        webhooks = await self.webhook_get_all_channel(channel)
        
        application_id = self.application.id
        for webhook in webhooks:
            if webhook.application_id == application_id:
                return webhook
        
        return None
    
    
    async def webhook_get_all_guild(self, guild):
        """
        Requests the webhooks of the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's webhooks will be requested.
        
        Returns
        -------
        webhooks : `list` of ``Webhook` objects
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        No request is done, if the guild's webhooks are up to date.
        """
        guild_id = get_guild_id(guild)
        
        webhook_datas = await self.api.webhook_get_all_guild(guild_id)
        return [Webhook.from_data(webhook_data) for webhook_data in webhook_datas]
    
    
    async def webhook_delete(self, webhook):
        """
        Deletes the webhook.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `int`
            The webhook to delete.
        
        Raises
        ------
        TypeError
            If `webhook` was not given neither as ``Webhook``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        See Also
        --------
        ``.webhook_delete_token`` : Deleting webhook with Discord's webhook API.
        """
        webhook_id = get_webhook_id(webhook)
        
        await self.api.webhook_delete(webhook_id)
    
    
    async def webhook_delete_token(self, webhook):
        """
        Deletes the webhook through Discord's webhook API.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook to delete.

        Parameters
        ----------
        webhook : ``Webhook``
            The webhook to delete.
        
        Raises
        ------
        TypeError
            If `webhook` was not given neither as ``Webhook`` neither as a `tuple` (`int`, `str`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        webhook_id, webhook_token = get_webhook_id_and_token(webhook)
        
        await self.api.webhook_delete_token(webhook_id, webhook_token)
    
    # later there gonna be more stuff that's why 2 different
    async def webhook_edit(self, webhook, *, name = ..., avatar = ..., channel = ...):
        """
        Edits and updates the given webhook.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `int`
            The webhook to edit.
        name : `str`, Optional (Keyword only)
            The webhook's new name. It's length can be in range [1:80].
        avatar : `None`, `bytes-like`, Optional (Keyword only)
            The webhook's new avatar. Can be `'jpg'`, `'png'`, `'webp'`, `'gif'` image's raw data. However if set as
            `'gif'`, it will not have any animation. If passed as `None`, will remove the webhook's current avatar.
        channel : ``Channel``, `int`, Optional (Keyword only)
            The webhook's channel.
        
        Raises
        ------
        TypeError
            - If `webhook` was not given neither as ``Webhook`` neither as `int`.
            - If `avatar` was not given neither as `None` nor as `bytes-like`.
            - If `channel` was not given neither as ``Channel`` neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was given but not as `str`.
            - If `name`'s length is out of range [1:80].
            - If `avatar`'s type is not any of the expected ones: `'jpg'`, `'png'`, `'webp'`, `'gif'`.
        
        See Also
        --------
        ``.webhook_edit_token`` : Editing webhook with Discord's webhook API.
        """
        webhook_id = get_webhook_id(webhook)
        
        data = {}
        
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                if name_length < 1 or name_length > 80:
                    raise AssertionError(
                        f'The length of the name can be in range [1:80], got {name_length}; {name!r}.'
                    )
            
            data['name'] = name
        
        if (avatar is not ...):
            if avatar is None:
                avatar_data = None
            else:
                if not isinstance(avatar, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`avatar` can be `None`, `bytes-like`, got {avatar.__class__.__name__}; '
                        f'{reprlib.repr(avatar)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(avatar)
                    if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                        raise AssertionError(
                            f'Invalid `avatar` type for the client: {media_type}; got {reprlib.repr(avatar)}.'
                        )
                
                avatar_data = image_to_base64(avatar)
            
            data['avatar'] = avatar_data
        
        if (channel is not ...):
            while True:
                if isinstance(channel, Channel):
                    if channel.is_in_group_guild_system() or channel.partial:
                        channel_id = channel.id
                        break
                
                else:
                    channel_id = maybe_snowflake(channel)
                    if channel_id is not None:
                        break
                
                raise TypeError(
                    f'`channel` can be gild text channel, `int`, got {channel.__class__.__name__}; '
                    f'{channel!r}.'
                )
            
            data['channel_id'] = channel_id
        
        if not data:
            return # Save 1 request
        
        data = await self.api.webhook_edit(webhook_id, data)
        webhook._set_attributes(data)
    
    
    async def webhook_edit_token(self, webhook, *, name = ..., avatar = ...):
        """
        Edits and updates the given webhook through Discord's webhook API.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook to edit.
        name : `str`, Optional (Keyword only)
            The webhook's new name. It's length can be between `1` and `80`.
        avatar : `None`, `bytes-like`, Optional (Keyword only)
            The webhook's new avatar. Can be `'jpg'`, `'png'`, `'webp'`, `'gif'` image's raw data. However if set as
            `'gif'`, it will not have any animation. If passed as `None`, will remove the webhook's current avatar.
        
        Returns
        -------
        webhook : ``Webhook``
            The updated webhook.
        
        Raises
        ------
        TypeError
            - If `webhook` was not given neither as ``Webhook`` neither as a `tuple` (`int`, `str`).
            - If `avatar` was not given neither as `None` nor as `bytes-like`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was given but not as `str`.
            - If `name`'s length is out of range [1:80].
            - If `avatar`'s type is not any of the expected ones: `'jpg'`, `'png'`, `'webp'`, `'gif'`.
        
        Notes
        -----
        This endpoint cannot edit the webhook's channel, like ``.webhook_edit``.
        """
        webhook, webhook_id, webhook_token = get_webhook_and_id_and_token(webhook)
        
        data = {}
        
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `None`, `str`, got {name.__class__.__name__}; {name!r}.'
                    )
                
                name_length = len(name)
                if name_length < 1 or name_length > 80:
                    raise AssertionError(
                        f'`name`\'s length can be in range [1:80], got {name_length}; {name!r}.'
                    )
            
            data['name'] = name
        
        if (avatar is not ...):
            if avatar is None:
                avatar_data = None
            else:
                if not isinstance(avatar, (bytes, bytearray, memoryview)):
                    raise TypeError(
                        f'`avatar` can be `None`, `bytes-like`, got {avatar.__class__.__name__}; '
                        f'{reprlib.repr(avatar)}.'
                    )
                
                if __debug__:
                    media_type = get_image_media_type(avatar)
                    if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                        raise AssertionError(
                            f'Invalid avatar type for the client: {media_type}; got {reprlib.repr(avatar)}.'
                        )
                
                avatar_data = image_to_base64(avatar)
            
            data['avatar'] = avatar_data
        
        if not data:
            return # Save 1 request
        
        data = await self.api.webhook_edit_token(webhook_id, webhook_token, data)
        
        if webhook is None:
            webhook = Webhook.from_data(data)
        else:
            webhook._set_attributes(data)
        
        return webhook
    
    
    async def webhook_message_create(
        self, webhook, *positional_parameters, thread = None, wait = False, **keyword_parameters,
    ):
        """
        Sends a message with the given webhook. If there is nothing to send, or if `wait` was not passed as `True`
        returns `None`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook through what will the message be sent.
        
        *positional_parameters : Positional parameters
            Additional parameters to create the message with.
        
        thread : `None`, ``Channel``, `int` = `None`, Optional (Keyword only)
            The thread of the webhook's channel where the message should be sent.
        
        wait : `None`, `bool` = `None`, Optional (Keyword only)
            Whether we should wait for the message to send and receive it's data as well.
        
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
             Applicable for threads of a forum-like channels.
        
        applied_tags : `None`, `(list | tuple)<int | ForumTag>`, `int`, `ForumTag`, Optional (Keyword only)
            Alternative for `applied_tag_ids`.
        
        attachments : `None`, `object`, Optional (Keyword only)
            Attachments to send.
        
        avatar_url : `None`, `str` = `None`, Optional (Keyword only)
            The message's author's avatar's url. Defaults to the webhook's avatar' url by Discord.
        
        components : `None`, ``Component``, `(tuple | list)<Component, (tuple | list)<Component>>`
            Components attached to the message.
        
        content : `None`, `str`, Optional
            The message's content if given.
        
        embed : `None`, `Embed`, Optional
            Alternative for `embeds`.
        
        embeds : `None`, `list<Embed>`, Optional
            The new embedded content of the message.
        
        file : `None`, `object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        files : `None`, `object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        flags : `int`, ``MessageFlag`, Optional
            The message's flags.
        
        name : `None`, `str` = `None`, Optional (Keyword only)
            The message's author's new name. Default to the webhook's name by Discord.
        
        poll : `None`, ``Poll``, Optional
            The message's poll.
        
        silent : `bool` = `False`, Optional (Keyword only)
            Whether the message should be delivered silently.
        
        suppress_embeds : `bool` = `False`, Optional (Keyword only)
            Whether the message's embeds should be suppressed initially.
        
        thread_name : `None`, `str`, Optional (Keyword only)
            The thread's name to create. Applicable only in forum-like channels.
        
        tts : `bool` = `False`, Optional (Keyword only)
            Whether the message is text-to-speech.
        
        Returns
        -------
        message : ``Message``, `None`
            Returns `None` if there is nothing to send or if `wait` was given as `False` (so by default).
        
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
        - ``.message_create`` : Create a message with your client.
        - ``.webhook_message_edit`` : Edit a message created by a webhook.
        - ``.webhook_message_delete`` : Delete a message created by a webhook.
        - ``.webhook_message_get`` : Get a message created by a webhook.
        """
        webhook, webhook_id, webhook_token = get_webhook_and_id_and_token(webhook)
        
        while True:
            if thread is None:
                thread_id = 0
                break
                
            elif isinstance(thread, Channel):
                if thread.is_in_group_thread() or thread.partial:
                    thread_id = thread.id
                    break
            
            else:
                thread_id = maybe_snowflake(thread)
                if thread_id is not None:
                    break
            
            raise TypeError(
                f'`thread` can be `None`, thread channel, `int`, '
                f'got {type(thread).__name__}; {thread!r}.'
            )
        
        if not isinstance(wait, bool):
            raise TypeError(
                f'`wait` can be `bool`, got {type(wait).__name__}; {wait!r}.'
            )
        
        message_data = MESSAGE_SERIALIZER_WEBHOOK_CREATE(positional_parameters, keyword_parameters)
        if not message_data:
            return
        
        query_parameters = None
        if wait:
            if query_parameters is None:
                query_parameters = {}
            
            query_parameters['wait'] = wait
        
        if thread_id:
            if query_parameters is None:
                query_parameters = {}
            
            query_parameters['thread_id'] = str(thread_id)
        
        data = await self.api.webhook_message_create(webhook_id, webhook_token, message_data, query_parameters)
        
        if not wait:
            return
        
        # Use goto
        while True:
            # Created into thread
            if thread_id:
                if thread is not None:
                    channel = thread
                    break
                
                channel = create_partial_channel_from_id(thread_id, ChannelType.guild_thread_public, 0)
                break
            
            # Created as thread
            try:
                thread_data = data['thread']
            except KeyError:
                pass
            else:
                channel = create_partial_channel_from_id(
                    int(thread_data['id']),
                    ChannelType.guild_thread_public,
                    0,
                )
                break
            
            # Check webhook.channel
            if (webhook is not None):
                channel = webhook.channel
                if (channel is not None):
                    break
            
            # Create new channel if unknown.
            # Create thread if `thread_name` is present.
            channel = create_partial_channel_from_id(
                int(data['channel_id']),
                ChannelType.guild_text,
                0,
            )
            break
        
        return channel._create_new_message(data)
    
    
    async def webhook_message_edit(self, webhook, message, *positional_parameters, **keyword_parameters):
        """
        Edits the message sent by the given webhook. The message's author must be the webhook itself.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook who created the message.
        
        message : ``Message``, `int`
            The webhook's message to edit.
        
        *positional_parameters : Positional parameters
            Additional parameters to edit the message with.
        
        **keyword_parameters : Keyword parameters
            Additional parameters to edit the message with.
        
        Other Parameters
        ----------------
        allowed_mentions : `None`,  ``AllowedMentionProxy``, `str`, ``UserBase``, ``Role``, `list` of \
                (`str`, ``UserBase``, ``Role`` ) , Optional
            Which user or role can the message ping (or everyone). Check ``parse_allowed_mentions``
            for details.
        
        attachments : `None`, `object`, Optional (Keyword only)
            Attachments to send.
        
        components : `None`, ``Component``, `(tuple | list)<Component, (tuple | list)<Component>>`
            Components attached to the message.
            
            Pass it as `None` remove the actual ones.
        
        content : `None`, `str`, Optional
            The new content of the message.
        
        embed : `None`, `Embed`, Optional
            Alternative for `embeds`.
        
        embeds : `None`, `list<Embed>`, Optional
            The new embedded content of the message.
            
            By passing it as `None`, you can remove the old.
        
        file : `None`, `object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        files : `None`, `object`, Optional (Keyword only)
            Alternative for `attachments`.
        
        flags : `int`, ``MessageFlag`, Optional
            The message's new flags.
        
        suppress_embeds : `bool`, Optional (Keyword only)
            Whether the message's embeds should be suppressed or unsuppressed.
        
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
        - ``.message_edit`` : Edit your own messages.
        - ``.webhook_message_create`` : Create a message with a webhook.
        - ``.webhook_message_delete`` : Delete a message created by a webhook.
        - ``.webhook_message_get`` : Get a message created by a webhook.
        
        Notes
        -----
        Embed messages ignore suppression with their endpoint, not like ``.message_edit`` endpoint.
        
        Editing the message with empty string is broken.
        """
        webhook_id, webhook_token = get_webhook_id_and_token(webhook)
        
        # Detect message id
        # 1.: Message
        # 2.: int (str)
        # 4.: None -> raise
        # 5.: raise
        
        if isinstance(message, Message):
            if message.author.id != webhook_id:
                raise RuntimeError(
                    f'The message was not sent by the webhook, got {message!r}; '
                    f'webhook_id = {webhook_id!r}; message.author.id = {message.author.id!r}.'
                )
                
            message_id = message.id
        
        else:
            message_id = maybe_snowflake(message)
            if (message_id is not None):
                pass
            
            elif message is None:
                raise TypeError(
                    f'`message` was given as `None`. Make sure to use '
                    f'`{self.__class__.__name__}.webhook_message_create` with giving content and by passing '
                    f'`wait` parameter as `True` as well.'
                )
            
            else:
                raise TypeError(
                    f'`message` can be `{Message.__name__}`, int`, got '
                    f'{type(message).__name__}; {message!r}.'
                )
        
        message_data = MESSAGE_SERIALIZER_WEBHOOK_EDIT(positional_parameters, keyword_parameters)
        if not message_data:
            return
        
        # We receive the new message data, but we do not update the message, so dispatch events can get the difference.
        await self.api.webhook_message_edit(webhook_id, webhook_token, message_id, message_data)
    
    
    async def webhook_message_delete(self, webhook, message):
        """
        Deletes the message sent by the webhook.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook who created the message.
        message : ``Message``, `int`
            The webhook's message to delete.
        
        Raises
        ------
        TypeError
            - If `message` was not given neither as ``Message``, `int`.
            - If `webhook` was not given neither as ``Webhook`` neither as a `tuple` (`int`, `str`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `message` was detectably not sent by the `webhook`.
        
        See Also
        --------
        - ``.message_delete`` : Delete a message.
        - ``.webhook_message_create`` : Create a message with a webhook.
        - ``.webhook_message_edit`` : Edit a message created by a webhook.
        - ``.webhook_message_get`` : Get a message created by a webhook.
        """
        webhook_id, webhook_token = get_webhook_id_and_token(webhook)
        
        # Detect message id
        # 1.: Message
        # 2.: int
        # 4.: None -> raise
        # 5.: raise
        
        if isinstance(message, Message):
            if __debug__:
                if message.author.id != webhook_id:
                    raise AssertionError(
                        f'The message was not sent by the webhook, got {message!r}.'
                    )
            
            message_id = message.id
        
        else:
            message_id = maybe_snowflake(message)
            if (message_id is not None):
                pass
            
            elif message is None:
                raise TypeError(
                    f'`message` was given as `None`. Make sure to use '
                    f'`{self.__class__.__name__}.webhook_message_create` with giving content and by passing '
                    f'`wait` parameter as `True` as well.'
                )
            
            else:
                raise TypeError(
                    f'`message` can be `{Message.__name__}`, `int`, got '
                    f'{message.__class__.__name__}; {message!r}.'
                )
        
        await self.api.webhook_message_delete(webhook_id, webhook_token, message_id)
    
    
    async def webhook_message_get(self, webhook, message_id):
        """
        Gets a previously sent message with the webhook.
        
        This method is a coroutine.
        
        Parameters
        ----------
        webhook : ``Webhook``, `tuple` (`int`, `str`)
            The webhook who created the message.
        message_id : `int`
            The webhook's message's identifier to get.
        
        Returns
        -------
        message : ``Message``
        
        Raises
        ------
        TypeError
            - If `webhook` was not given neither as ``Webhook`` neither as a `tuple` (`int`, `str`).
            - If `message_id` was not given as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        See Also
        --------
        - ``.message_get`` : Get a message.
        - ``.webhook_message_create`` : Create a message with a webhook.
        - ``.webhook_message_edit`` : Edit a message created by a webhook.
        - ``.webhook_message_delete`` : Delete a message created by a webhook.
        """
        webhook_id, webhook_token = get_webhook_id_and_token(webhook)
        
        message_id_value = maybe_snowflake(message_id)
        if message_id_value is None:
            raise TypeError(
                f'`message_id` can be `int`, got {message_id.__class__.__name__}; {message_id!r}.'
            )
        
        message_data = await self.api.webhook_message_get(webhook_id, webhook_token, message_id_value)
        return Message.from_data(message_data)
