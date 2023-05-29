__all__ = ()

import reprlib
from collections import deque
from datetime import datetime, timedelta
from math import floor
from os.path import split as split_path

from scarletio import to_json
from scarletio.web_common import Formdata

from ...env import API_VERSION

from ..application_command import ApplicationCommand
from ..auto_moderation import AutoModerationRule
from ..bases import maybe_snowflake, maybe_snowflake_pair, maybe_snowflake_token_pair
from ..channel import Channel, ForumTag, PermissionOverwrite
from ..component import Component, ComponentType, create_row
from ..core import (
    APPLICATION_COMMANDS, AUTO_MODERATION_RULES, CHANNELS, FORUM_TAGS, GUILDS, MESSAGES, ROLES, SCHEDULED_EVENTS,
    SOUNDBOARD_SOUNDS, STICKERS, STICKER_PACKS, USERS
)
from ..embed import Embed
from ..emoji import Emoji, parse_reaction
from ..guild import Guild
from ..message import Attachment, Message
from ..oauth2 import Achievement, Oauth2Access, Oauth2User
from ..role import Role
from ..scheduled_event import ScheduledEvent
from ..soundboard import SoundboardSound
from ..stage import Stage
from ..sticker import Sticker, StickerPack
from ..user import ClientUserBase
from ..utils import random_id
from ..webhook import Webhook


def get_components_data(components, is_edit):
    """
    Gets component data from the given components.
    
    Parameters
    ----------
    components : `None`, ``Component``, (`set`, `list`) of (``Component``, (`set`, `list`) of ``Component``)
        Components to be attached to a message.
    is_edit : `bool`
        Whether the processed `components` fields are for message edition. At this case passing `None` will
        remove them.
    
    Returns
    -------
    component_datas : `None`, `list` of (`dict` of (`str`, `Any`) items)
        The generated data if any.
    
    Raises
    ------
    TypeError
        - If `components` was not given neither as `None`, ``Component``, (`list`, `tuple`) of ``Component``
            instances.
    AssertionError
        - If `components` contains a non ``Component`` element.
    """
    
    # Components check order:
    # 1.: None -> None || []
    # 2.: Ellipsis -> None || Ellipsis
    # 2.: Component -> [component.to_data()]
    # 3.: (list, tuple) of Component, (list, tuple) of Component -> [component.to_data(), ...] / None
    # 4.: raise
    
    if components is None:
        if is_edit:
            component_datas = []
        else:
            component_datas = None
    
    elif components is ...:
        if is_edit:
            component_datas = ...
        else:
            component_datas = None
    
    else:
        if isinstance(components, Component):
            if components.type is not ComponentType.row:
                components = create_row(components)
                
            component_datas = [components.to_data()]
        elif isinstance(components, (list, tuple)):
            component_datas = None
            
            for component in components:
                if isinstance(component, Component):
                    if component.type is not ComponentType.row:
                        component = create_row(component)
                
                elif isinstance(component, (list, tuple)):
                    component = create_row(*component)
                
                else:
                    raise TypeError(
                        f'`components` can contain contain `{Component.__name__}`, (`list`, `tuple`) of '
                        f'`{Component.__name__}`, got {components.__class__.__name__}; {components!r}.'
                    )
                
                if component_datas is None:
                    component_datas = []
                
                component_datas.append(component.to_data())
                continue
        
        else:
            raise TypeError(
                f'`components` can be `{Component.__name__}`, (`list`, `tuple`) of '
                f'(`{Component.__name__}`, (`list`, `tuple`) of `{Component.__name__}`), '
                f'got {components.__class__.__name__}; {components!r}.'
            )
    
    return component_datas


def validate_message_to_delete(message):
    """
    Validates a message to delete.
    
    Parameters
    ----------
    message : ``Message``, `tuple` (`int`, `int`)
        The message to validate for deletion.
    
    Returns
    -------
    channel_id : `int`
        The channel's identifier where the message is.
    message_id : `int`
        The message's identifier.
    message : `None`, ``Message``
        The referenced message if found.
    
    Raises
    ------
    TypeError
        If message was not given neither as ``Message``, `tuple` (`int`, `int`).
    """
    if isinstance(message, Message):
        channel_id = message.channel_id
        message_id = message.id
    else:
        snowflake_pair = maybe_snowflake_pair(message)
        if snowflake_pair is None:
            raise TypeError(
                f'`message` can be `{Message.__name__}`, '
                f'`tuple` of (`int`, `int`), got {message.__class__.__name__}; {message!r}.'
            )
        
        channel_id, message_id = snowflake_pair
        
        message = MESSAGES.get(message, None)
    
    return channel_id, message_id, message


if API_VERSION >= 9:
    def _add_file_from_tuple(files, tuple_):
        """
        Processes the given file tuple.
        
        Parameters
        ----------
        files : `None`, `list` of `tuple` (`str`, `Any`, (`None`, `str`))
            The collected files to send.
        tuple_ : `tuple` (?(`None`, `str`), ?`Any`, ?(`None`, `str`))
            A tuple containing the name, io and the description.
        
        Returns
        -------
        files : `None`, `list` of `tuple` (`str`, `Any`, (`None`, `str`))
            The collected files to send.
        
        Raises
        ------
        ValueError
            If a `tuple_`'s length is out of the expected [0:3] range.
        """
        tuple_length = len(tuple_)
        if tuple_length:
            if tuple_length > 3:
                raise ValueError(
                    f'`tuple` length can be in range [0:3], got {tuple_length!r}; {tuple_!r}.'
                )
            
            if tuple_length == 1:
                io = tuple_[0]
                name = None
                description = None
            elif tuple_length == 2:
                name, io = tuple_
                if (name is not None) and (not name):
                    name = None
                description = None
            else:
                name, io, description = tuple_
                if (name is not None) and (not name):
                    name = None
                if (description is not None) and (not description):
                    description = None
            
            if name is None:
                name = getattr(io, 'name', None)
                if (name is not None) and name:
                    _, name = split_path(name)
                else:
                    name = str(random_id())
            
            if files is None:
                files = []
            
            files.append((name, io, description))
        
        return files
    
    
    def _build_partial_attachment_data(attachment_id, description):
        """
        Builds a partial attachment payload to be sent to Discord.
        
        Parameters
        ----------
        attachment_id : `int`
            The attachment's identifier.
        description : `None`, `str`
            Description for the attachment.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`)
        """
        data = {'id': attachment_id}
        
        if (description is not None):
            data['description'] = description
        
        return data
    
    
    def create_file_form(data, file):
        """
        Creates a `multipart/form-data` form from the message's data and from the file data. If there is no files to
        send, will return `None` to tell the caller, that nothing is added to the overall data.
        
        Parameters
        ----------
        data : `dict` of `Any`
            The data created by the ``.message_create`` method.
        file : `dict` of (`file-name`, `io`) items, `list` of (``Attachment``, `tuple` (`file-name`, `io`)) elements,
                `tuple` (`file-name`, `io`, ), `io`, ``Attachment``
            The files to send.
        
        Returns
        -------
        form : `None`, `Formdata`
            Returns a `Formdata` of the files and from the message's data. If there are no files to send, returns
            `None` instead.
        contains_attachments : `bool`
            Whether the message payload contains attachments.
        
        Raises
        ------
        ValueError
            - If more than `10` file is registered to be sent.
            - If a `tuple`'s length is out of the expected [0:3] range.
        
        Notes
        -----
        Accepted `io` types with check order are:
        - ``BodyPartReader``
        - `bytes`, `bytearray`, `memoryview`
        - `str`
        - `BytesIO`
        - `StringIO`
        - `TextIOBase`
        - `BufferedReader`, `BufferedRandom`
        - `IOBase`
        - ``AsyncIO``
        - `async-iterable`
        
        Raises `TypeError` at the case of invalid `io` type.
        
        There are two predefined data types specialized to send files:
        - ``ReuBytesIO``
        - ``ReuAsyncIO``
        
        If a buffer is sent, then when the request is done, it is closed. So if the request fails, we would not be
        able to resend the file, except if we have a data type, what instead of closing on `.close()` just seeks to
        `0` (or later if needed) on close, instead of really closing instantly. These data types implement a
        `.real_close()` method, but they do `real_close` on `__exit__` as well.
        """
        files = None
        attachments = None
        
        # checking structure
        
        # case 0 None
        if file is None:
            pass
        
        # case 1 dict like
        elif hasattr(type(file), 'items'):
            for name, io in file.items():
                if files is None:
                    files = []
                
                files.append((name, io, None))
        
        # case 2 tuple => file, filename pair | file, filename, description pairs
        elif isinstance(file, tuple):
            files = _add_file_from_tuple(files, file)
        
        # case 3 list like
        elif isinstance(file, (list, deque)):
            for element in file:
                if isinstance(element, Attachment):
                    if attachments is None:
                        attachments = []
                    
                    attachments.append(element.id)
                
                else:
                    files = _add_file_from_tuple(files, element)
        
        elif isinstance(file, Attachment):
            if attachments is None:
                attachments = []
            
            attachments.append(file.id)
        
        # case 4 file itself
        else:
            name = getattr(file, 'name', None)
            if (name is not None) and name:
                _, name = split_path(name)
            else:
                name = str(random_id())
            
            if files is None:
                files = []
            
            files.append((name, file, None),)
        
        attachment_fields = None
        
        if (files is not None):
            for index, (name, io, description) in enumerate(files):
                if attachment_fields is None:
                    attachment_fields = []
                
                attachment_fields.append(_build_partial_attachment_data(index, description))
        
        if (attachments is not None):
            for attachment_id in attachments:
                if attachment_fields is None:
                    attachment_fields = []
                
                attachment_fields.append(_build_partial_attachment_data(attachment_id, None))
        
        if (attachment_fields is None):
            contains_attachments = False
            
            form = None
        else:
            contains_attachments = True
            data['attachments'] = attachment_fields
            
            if (files is None):
                form = None
            
            else:
                form = Formdata()
                form.add_field('payload_json', to_json(data))
                
                for index, (name, io, description) in enumerate(files):
                    form.add_field(f'files[{index}]', io, filename = name, content_type = 'application/octet-stream')
        
        
        return form, contains_attachments
    
    
    def add_file_to_message_data(message_data, file, contains_content, is_edit):
        """
        Adds files to the message data creating a form data if applicable.
        
        Parameters
        ----------
        message_data : `dict` of (`str`, `Any`) items
            The message's payload to send.
        file : `None`, `dict` of (`file-name`, `io`) items, `list` of (`file-name`, `io`) elements, \
                tuple (`file-name`, `io`), `io`
            The files to send.
        contains_content : `bool`
            Whether the message already contains any content.
        is_edit : `bool`
            Whether we are creating edit file form.
        
        Returns
        -------
        message_data : `None`, `dict`, ``Formdata``
            Returns a ``Formdata`` if the message contains attachments, `dict` if contains any content and `None` if
            not.
        
        Raises
        ------
        ValueError
            If more than `10` file is registered to be sent.
        """
        if (file is (... if is_edit else None)):
            if not contains_content:
                message_data = None
        else:
            form, contains_attachments = create_file_form(message_data, file)
            if (form is None):
                if (not contains_content) and (not contains_attachments):
                    message_data = None
            else:
                message_data = form
        
        return message_data

else:
    def create_file_form(data, file):
        """
        Creates a `multipart/form-data` form from the message's data and from the file data. If there is no files to
        send, will return `None` to tell the caller, that nothing is added to the overall data.
        
        Parameters
        ----------
        data : `dict` of `Any`
            The data created by the ``.message_create`` method.
        file : `dict` of (`file-name`, `io`) items, `list` of (`file-name`, `io`) elements, tuple (`file-name`, `io`),
                `io`
            The files to send.
        
        Returns
        -------
        form : `None`, `Formdata`
            Returns a `Formdata` of the files and from the message's data. If there are no files to send, returns `None`
            instead.
        
        Raises
        ------
        ValueError
            If more than `10` file is registered to be sent.
        
        Notes
        -----
        Accepted `io` types with check order are:
        - ``BodyPartReader``
        - `bytes`, `bytearray`, `memoryview`
        - `str`
        - `BytesIO`
        - `StringIO`
        - `TextIOBase`
        - `BufferedReader`, `BufferedRandom`
        - `IOBase`
        - ``AsyncIO``
        - `async-iterable`
        
        Raises `TypeError` at the case of invalid `io` type.
        
        There are two predefined data types specialized to send files:
        - ``ReuBytesIO``
        - ``ReuAsyncIO``
        
        If a buffer is sent, then when the request is done, it is closed. So if the request fails, we would not be
        able to resend the file, except if we have a data type, what instead of closing on `.close()` just seeks to
        `0` (or later if needed) on close, instead of really closing instantly. These data types implement a
        `.real_close()` method, but they do `real_close` on `__exit__` as well.
        """
        form = Formdata()
        form.add_field('payload_json', to_json(data))
        files = []
        
        # checking structure
        
        # case 0 none
        if file is None:
            pass
        
        # case 1 dict like
        elif hasattr(type(file), 'items'):
            files.extend(file.items())
        
        # case 2 tuple => file, filename pair
        elif isinstance(file, tuple):
            files.append(file)
        
        # case 3 list like
        elif isinstance(file, (list, deque)):
            for element in file:
                if type(element) is tuple:
                    name, io = element
                else:
                    io = element
                    name = ''
                
                if not name:
                    #guessing name
                    name = getattr(io, 'name', '')
                    if name:
                        _, name = split_path(name)
                    else:
                        name = str(random_id())
                
                files.append((name, io),)
        
        #case 4 file itself
        else:
            name = getattr(file, 'name', '')
            #guessing name
            if name:
                _, name = split_path(name)
            else:
                name = str(random_id())
            
            files.append((name, file),)
        
        # checking the amount of files
        # case 1 one file
        if len(files) == 1:
            name, io = files[0]
            form.add_field('file', io, filename = name, content_type = 'application/octet-stream')
        # case 2, no files -> return None, we should use the already existing data
        elif len(files) == 0:
            return None
        # case 3 maximum 10 files
        elif len(files) < 11:
            for index, (name, io) in enumerate(files):
                form.add_field(f'file{index}s', io, filename = name, content_type = 'application/octet-stream')
        
        # case 4 more than 10 files
        else:
            raise ValueError(
                f'Can send up to 10 files at once, got {len(files)!r}; {reprlib.repr(files)}.'
            )
        
        return form
    
    
    def add_file_to_message_data(message_data, file, contains_content, is_edit):
        """
        Adds files to the message data creating a form data if applicable.
        
        Parameters
        ----------
        message_data : `dict` of (`str`, `Any`) items
            The message's payload to send.
        file : `None`, `dict` of (`file-name`, `io`) items, `list` of (`file-name`, `io`) elements, \
                tuple (`file-name`, `io`), `io`
            The files to send.
        contains_content : `bool`
            Whether the message already contains any content.
        is_edit : `bool`
            Whether we are creating edit file form.
        
        Returns
        -------
        message_data : `None`, `dict`, ``Formdata``
            Returns a ``Formdata`` if the message contains attachments, `dict` if contains any content and `None` if
            not.
        
        Raises
        ------
        ValueError
            If more than `10` file is registered to be sent.
        """
        if (file is (... if is_edit else None)):
            if not contains_content:
                message_data = None
        else:
            form = create_file_form(message_data, file)
            if (form is None) and (not contains_content):
                message_data = None
            else:
                message_data = form
        
        return message_data


def validate_content_and_embed(content, embed, is_edit):
    """
    Validates the given content and embed fields of a message creation or edition.
    
    Parameters
    ----------
    content : `str`, ``Embed``, `Any`, Optional
        The content of the message.
        
        
        If given as ``Embed``, then the message's embeds will be edited with it.
    embed : `None`, ``Embed``, `list` of ``Embed``, Optional (Keyword only)
        The new embedded content of the message. By passing it as `None`, you can remove the old.
        
        > If `embed` and `content` parameters are both given as  ``Embed``, then `AssertionError` is
        raised.
    is_edit : `bool`
        Whether the processed `content` and `embed` fields are for message edition. At this case passing `None` will
        remove them.
    
    Returns
    -------
    content : `Ellipsis`, `None`, `str`
        The message's content.
    embed : `Ellipsis`, `None`, ``Embed``, (`list`, `tuple`) of ``Embed``
        The messages embeds.
    
    Raises
    ------
    TypeError
        If `embed` was not given neither as ``Embed`` nor as `list`, `tuple` of ``Embed``-s.
    AssertionError
        - If `embed` contains a non ``Embed`` element.
        - If both `content` and `embed` fields are embeds.
    """
    # Embed check order:
    # 1.: None
    # 2.: Ellipsis -> None || Ellipsis
    # 3.: Embed : -> embed || [embed]
    # 4.: list of Embed -> embed[0] || embed[:15] or None
    # 5.: raise
    if embed is None:
        pass
    
    elif embed is ...:
        if not is_edit:
            embed = None
    
    elif isinstance(embed, Embed):
        embed = [embed]
    
    elif isinstance(embed, (list, tuple)):
        if embed:
            if __debug__:
                for embed_element in embed:
                    if not isinstance(embed_element, Embed):
                        raise AssertionError(
                            f'`embed` can contains `{Embed.__name__}` elements, got '
                            f'{embed_element.__class__.__name__}; {embed_element!r}; embed={embed!r}.'
                        )
            
            embed = embed[:15]
        else:
            embed = None
    
    else:
        raise TypeError(
            f'`embed` can be `{Embed.__name__}`, (`list`, `tuple`) of {Embed.__name__}, got '
            f'{embed.__class__.__name__}; {embed!r}.'
        )
    
    # Content check order:
    # 1.: None -> None || ''
    # 2.: Ellipsis -> None || Ellipsis
    # 3.: str
    # 4.: Embed -> embed = content || [content]
    # 5.: list of Embed -> embed = content[0] || content[:10]
    # 6.: object -> str(content)
    
    if content is None:
        if is_edit:
            content = ''
    
    elif content is ...:
        if not is_edit:
            content = None
    
    elif isinstance(content, str):
        pass
    
    elif isinstance(content, Embed):
        if __debug__:
            if (embed is not (... if is_edit else None)):
                raise AssertionError(
                    f'Multiple parameters were given as embed, got content={content!r}, embed={embed!r}.'
                )
        
        embed = [content]
        
        if is_edit:
            content = ...
        else:
            content = None
    
    else:
        # Check for list of embeds as well.
        if isinstance(content, (list, tuple)):
            if content:
                for element in content:
                    if isinstance(element, Embed):
                        continue
                    
                    is_list_of_embeds = False
                    break
                else:
                    is_list_of_embeds = True
            else:
                is_list_of_embeds = False
        else:
            is_list_of_embeds = False
        
        if is_list_of_embeds:
            if __debug__:
                if (embed is not (... if is_edit else None)):
                    raise AssertionError(
                        f'Multiple parameters were given as embed, got content={content!r}, embed={embed!r}.'
                    )
            
            embed = content[:15]
            
            if is_edit:
                content = ...
            else:
                content = None
        else:
            content = str(content)
    
    return content, embed


TIMEOUT_MAX_DURATION = timedelta(days=28)
TIMEOUT_MAX_DURATION_SECONDS_FLOAT = TIMEOUT_MAX_DURATION.total_seconds()
TIMEOUT_MAX_DURATION_SECONDS_INT = floor(TIMEOUT_MAX_DURATION_SECONDS_FLOAT)
ZERO_TIMEDELTA = timedelta(seconds=0)


def validate_timeout_duration(timeout_duration):
    """
    Validates the given `timeout_duration` and returns the processed value which equals to the timeout's end.
    
    Parameters
    ----------
    timeout_duration: `None`, `int`, `float`, `timedelta`, `datetime`, Optional (Keyword only)
        The timeout duration of the user in seconds.
        
        Pass it as `None` or as a non-positive duration to remove it.
        
        The max allowed value equals to 28 days.
    
    Returns
    -------
    timeout_ends_at : `None`, `datetime`
    
    Raises
    ------
    TypeError
        - If `timeout_duration`'s type is incorrect.
    """
    if timeout_duration is None:
        timeout_ends_at = None
    
    elif isinstance(timeout_duration, int):
        if timeout_duration <= 0:
            timeout_ends_at = None
        
        elif timeout_duration >= TIMEOUT_MAX_DURATION_SECONDS_INT:
            timeout_ends_at = datetime.utcnow() + TIMEOUT_MAX_DURATION
        
        else:
            timeout_ends_at = datetime.utcnow() + timedelta(seconds=timeout_duration)
    
    elif isinstance(timeout_duration, float):
        if timeout_duration <= 0.0:
            timeout_ends_at = None
        
        elif timeout_duration >= TIMEOUT_MAX_DURATION_SECONDS_FLOAT:
            timeout_ends_at = datetime.utcnow() + TIMEOUT_MAX_DURATION
        
        else:
            timeout_ends_at = datetime.utcnow() + timedelta(seconds=timeout_duration)
    
    elif isinstance(timeout_duration, timedelta):
        if timeout_duration <= ZERO_TIMEDELTA:
            timeout_ends_at = None
        
        elif timeout_duration >= TIMEOUT_MAX_DURATION:
            timeout_ends_at = datetime.utcnow() + TIMEOUT_MAX_DURATION
        
        else:
            timeout_ends_at = datetime.utcnow() + timeout_duration
    
    elif isinstance(timeout_duration, datetime):
        timeout_ends_at = timeout_duration
    
    else:
        raise TypeError(
            f'`timeout_duration` can be `None`, `int`, `float`, `timedelta`, `datetime`, got '
            f'{timeout_duration.__class__.__name__}; {timeout_duration!r}.'
        )

    return timeout_ends_at


def get_channel_id(channel, type_checker):
    """
    Gets the channel's identifier from the given channel or of it's identifier.
    
    Parameters
    ----------
    channel : ``Channel``, `int`
        The channel, or it's identifier.
    type_checker : `FunctionType`
        Type checker for `channel`.
    
    Returns
    -------
    channel_id : `int`
        The channel's identifier.
    
    Raises
    ------
    TypeError
        If `channel`'s type is incorrect.
    """
    if isinstance(channel, Channel):
        if type_checker(channel) or channel.partial:
            return channel.id
    
    else:
        channel_id = maybe_snowflake(channel)
        if (channel_id is not None):
            return channel_id
        
    raise TypeError(
        f'`channel` can be `{Channel.__name__}`, `int`,  passing the `{type_checker.__name__}` check, '
        f'got {channel.__class__.__name__}; {channel!r}.'
    )


def get_channel_guild_id_and_id(channel, type_checker):
    """
    Gets the channel's and it's guild's identifier from the given channel or of it's identifier.
    
    Parameters
    ----------
    channel : ``Channel``, `tuple` (`int`, `int`)
        The role, or `guild-id`, `role-id` pair.
    type_checker : `FunctionType`
        Type checker for `channel`.
    
    Returns
    -------
    snowflake_pair : `tuple` (`int`, `int`)
        The channel's guild's and it's own identifier if applicable.
    
    Raises
    ------
    TypeError
        If `channel`'s type is incorrect.
    """
    if isinstance(channel, Channel):
        if type_checker(channel) or channel.partial:
            return channel.guild_id, channel.id
    
    else:
        snowflake_pair = maybe_snowflake_pair(channel)
        if (snowflake_pair is not None):
            return snowflake_pair
    
    raise TypeError(
        f'`channel` can be `{Channel.__name__}`, `int`,  passing the `{type_checker.__name__}` check, '
        f'got {channel.__class__.__name__}; {channel!r}.'
    )


def get_channel_and_id(channel, type_checker):
    """
    Gets thread channel and it's identifier from the given thread channel or of it's identifier.
    
    Parameters
    ----------
    channel : ``Channel``, `int`
        The channel, or it's identifier.
    type_checker : `FunctionType`
        Type checker for `channel`.
    
    Returns
    -------
    channel : `None`, ``Channel``
        The channel if found.
    channel_id : `int`
        The channel's identifier.
    
    Raises
    ------
    TypeError
        If `channel`'s type is incorrect.
    """
    while True:
        if isinstance(channel, Channel):
            if type_checker(channel) or channel.partial:
                channel_id = channel.id
                break
        
        else:
            channel_id = maybe_snowflake(channel)
            if (channel_id is not None):
                try:
                    channel = CHANNELS[channel_id]
                except KeyError:
                    channel = None
                    break
                
                if type_checker(channel) or channel.partial:
                    channel_id = channel.id
                    break
        
        raise TypeError(
            f'`channel` can be `{Channel.__name__}`, `int`,  passing the `{type_checker.__name__}` check, '
            f'got {channel.__class__.__name__}; {channel!r}.'
        )
    
    return channel, channel_id


def get_stage_and_channel_id(stage):
    """
    Gets the stage an its channel's identifier.
    
    Parameters
    ----------
    stage : `Stage`, ``Channel``, `int`
        The stage, or it's identifier.
    
    Returns
    -------
    stage : `None`, ``Stage``
        The identified stage if any.
    channel_id : `int`
        The channel's identifier.
    
    Raises
    ------
    TypeError
        If `stage`'s type is incorrect.
    """
    while True:
        if isinstance(stage, Stage):
            channel_id = stage.channel.id
            break
        
        elif isinstance(stage, Channel):
            if stage.is_guild_stage() or stage.partial:
                channel_id = stage.id
                stage = None
                break
        
        else:
            channel_id = maybe_snowflake(stage)
            if (channel_id is not None):
                stage = None
                break
        
        raise TypeError(
            f'`stage` can be `{Stage.__name__}`, `{Channel.__name__}`, `int`, got '
            f'{stage.__class__.__name__}; {stage!r}.'
        )
    
    return stage, channel_id


def get_stage_channel_id(stage):
    """
    Gets stage's channel's identifier from the given stage or of it's identifier.
    
    Parameters
    ----------
    stage : `Stage`, ``Channel``, `int`
        The stage, or it's identifier.
    
    Returns
    -------
    channel_id : `int`
        The channel's identifier.
    
    Raises
    ------
    TypeError
        If `stage`'s type is incorrect.
    """
    while True:
        if isinstance(stage, Stage):
            channel_id = stage.channel.id
            break
        
        elif isinstance(stage, Channel):
            if stage.is_guild_stage() or stage.partial:
                channel_id = stage.id
                break
        
        else:
            channel_id = maybe_snowflake(stage)
            if (channel_id is not None):
                break
        
        raise TypeError(
            f'`stage` can be `{Stage.__name__}`, `{Channel.__name__}`, `int`, got '
            f'{stage.__class__.__name__}; {stage!r}.'
        )
    
    return channel_id


def get_user_id(user):
    """
    Gets user identifier from the given user or of it's identifier.
    
    Parameters
    ----------
    user : ``ClientUserBase``, `int`
        The user, or it's identifier.
    
    Returns
    -------
    user_id : `int`
        The user's identifier.
    
    Raises
    ------
    TypeError
        If `user`'s type is incorrect.
    """
    if isinstance(user, ClientUserBase):
        return user.id
    
    user_id = maybe_snowflake(user)
    if (user_id is not None):
        return user_id
    
    raise TypeError(
        f'`user` can be `{ClientUserBase.__name__}`, `int`, got {user.__class__.__name__}; {user!r}.'
    )


def get_user_and_id(user):
    """
    Gets user and it's identifier from the given user or of it's identifier.
    
    Parameters
    ----------
    user : ``ClientUserBase``, `int`
        The user, or it's identifier.
    
    Returns
    -------
    user : `None`, ``ClientUserBase``
        The user if found.
    user_id : `int`
        The user's identifier.
    
    Raises
    ------
    TypeError
        If `user`'s type is incorrect.
    """
    while True:
        if isinstance(user, ClientUserBase):
            user_id = user.id
            break
        
        user_id = maybe_snowflake(user)
        if (user_id is not None):
            try:
                user = USERS[user_id]
            except KeyError:
                user = None
                break
            
            if isinstance(user, ClientUserBase):
                break
        
        raise TypeError(
            f'`user` can be `{ClientUserBase.__name__}`, `int`, got {user.__class__.__name__}; {user!r}.'
        )
        
    return user, user_id


def get_user_id_nullable(user):
    """
    Gets user identifier from the given user or of it's identifier.
    
    > The user can be `None`. At that case `user_id` will default to `0`.
    
    Parameters
    ----------
    user : `None`, ``ClientUserBase``, `int`
        The user, or it's identifier.
    
    Returns
    -------
    user_id : `int`
        The user's identifier.
    
    Raises
    ------
    TypeError
        If `user`'s type is incorrect.
    """
    if user is None:
        return 0
    
    if isinstance(user, ClientUserBase):
        return user.id
    
    user_id = maybe_snowflake(user)
    if (user_id is not None):
        return user_id
        
    raise TypeError(
        f'`user` can be `{ClientUserBase.__name__}`, `int`, got {user.__class__.__name__}; {user!r}.'
    )


def get_guild_id(guild):
    """
    Gets the guild's identifier from the given guild or of it's identifier.
    
    Parameters
    ----------
    guild : ``Guild``, `int`
        The guild, or it's identifier.
    
    Returns
    -------
    guild_id : `int`
        The guild's identifier.
    
    Raises
    ------
    TypeError
        If `guild`'s type is incorrect.
    """
    if isinstance(guild, Guild):
        return guild.id
    
    guild_id = maybe_snowflake(guild)
    if (guild_id is not None):
        return guild_id
        
    raise TypeError(
        f'`guild` can be `{Guild.__name__}`, `int`, got {guild.__class__.__name__}; {guild!r}.'
    )


def get_guild_and_id(guild):
    """
    Gets the guild and it's identifier from the given guild or of it's identifier.
    
    Parameters
    ----------
    guild : ``Guild``, `int`
        The guild, or it's identifier.
    
    Returns
    -------
    guild : `None`, ``Guild``
        The guild if found.
    guild_id : `int`
        The guild's identifier.
    
    Raises
    ------
    TypeError
        If `guild`'s type is incorrect.
    """
    if isinstance(guild, Guild):
        guild_id = guild.id
    else:
        guild_id = maybe_snowflake(guild)
        if guild_id is None:
            raise TypeError(
                f'`guild` can be `{Guild.__name__}`, `int`, got {guild.__class__.__name__}; {guild!r}.'
            )
        
        guild = GUILDS.get(guild_id, None)
    
    return guild, guild_id


def get_achievement_id(achievement):
    """
    Gets the achievement identifier from the given achievement or of it's identifier.
    
    Parameters
    ----------
    achievement : ``Achievement``, `int`
        The achievement, or it's identifier.
    
    Returns
    -------
    achievement_id : `int`
        The achievement's identifier.
    
    Raises
    ------
    TypeError
        If `achievement`'s type is incorrect.
    """
    if isinstance(achievement, Achievement):
        achievement_id = achievement.id
    else:
        achievement_id = maybe_snowflake(achievement)
        if achievement_id is None:
            raise TypeError(
                f'`achievement` can be `{Achievement.__name__}`, `int`, got '
                f'{achievement.__class__.__name__}; {achievement!r}.'
            )
    
    return achievement_id


def get_achievement_and_id(achievement):
    """
    Gets the achievement and it's identifier from the given achievement or of it's identifier.
    
    Parameters
    ----------
    achievement : ``Achievement``, `int`
        The achievement, or it's identifier.
    
    Returns
    -------
    achievement : ``Achievement``, `None`
        The achievement if found.
    achievement_id : `int`
        The achievement's identifier.
    
    Raises
    ------
    TypeError
        If `achievement`'s type is incorrect.
    """
    if isinstance(achievement, Achievement):
        achievement_id = achievement.id
    else:
        achievement_id = maybe_snowflake(achievement)
        if achievement_id is None:
            raise TypeError(
                f'`achievement` can be `{Achievement.__name__}`, `int`, got '
                f'{achievement.__class__.__name__}; {achievement!r}.'
            )
        
        achievement = None
    
    return achievement, achievement_id


def get_channel_id_and_message_id(message):
    """
    Gets the message's channel's and it's own identifier.
    
    Parameters
    ----------
    message : ``Message``, `tuple` (`int`, `int`)
        The message or it' representation.
    
    Returns
    -------
    channel_id : `int`
        The message's channel's identifier.
    message_id : `int`
        The message's identifier.
    
    Raises
    ------
    TypeError
        If `message`'s type is incorrect.
    """
    # 1.: Message
    # 4.: None -> raise
    # 5.: `tuple` (`int`, `int`)
    # 6.: raise
    if isinstance(message, Message):
        channel_id = message.channel_id
        message_id = message.id
    elif message is None:
        raise TypeError(
            '`message` was given as `None`. Make sure to call message create methods with non-empty content(s).'
        )
    else:
        snowflake_pair = maybe_snowflake_pair(message)
        if snowflake_pair is None:
            raise TypeError(
                f'`message` can be `{Message.__name__}`, '
                f'`tuple` of (`int`, `int`), got {message.__class__.__name__}; {message!r}.'
            )
        
        channel_id, message_id = snowflake_pair
    
    return channel_id, message_id


def get_message_and_channel_id_and_message_id(message):
    """
    Gets the message's channel's and it's own identifier.
    
    Parameters
    ----------
    message : ``Message``, `tuple` (`int`, `int`)
        The message or it' representation.
    
    Returns
    -------
    message : `None`, ``Message``
        The message in context if found.
    channel_id : `int`
        The message's channel's identifier.
    message_id : `int`
        The message's identifier.
    
    Raises
    ------
    TypeError
        If `message`'s type is incorrect.
    """
    # 1.: Message
    # 4.: None -> raise
    # 5.: `tuple` (`int`, `int`)
    # 6.: raise
    if isinstance(message, Message):
        channel_id = message.channel_id
        message_id = message.id
    elif message is None:
        raise TypeError(
            '`message` was given as `None`. Make sure to call message create methods with non-empty content(s).'
        )
    else:
        snowflake_pair = maybe_snowflake_pair(message)
        if snowflake_pair is None:
            raise TypeError(
                f'`message` can be `{Message.__name__}`, '
                f'`tuple` of (`int`, `int`), got {message.__class__.__name__}; {message!r}.'
            )
        
        channel_id, message_id = snowflake_pair
        message = MESSAGES.get(message_id, None)
    
    return message, channel_id, message_id


def get_role_id(role):
    """
    Gets the role identifier from the given role or of it's identifier.
    
    Parameters
    ----------
    role : ``Role``, `int`
        The role, or it's identifier.
    
    Returns
    -------
    role_id : `int`
        The role's identifier.
    
    Raises
    ------
    TypeError
        If `role`'s type is incorrect.
    """
    if isinstance(role, Role):
        role_id = role.id
    else:
        role_id = maybe_snowflake(role)
        if role_id is None:
            raise TypeError(
                f'`role` can be `{Role.__name__}`, `int`, got {role.__class__.__name__}; {role!r}.'
            )
    
    return role_id


def get_role_role_guild_id_and_id(role):
    """
    Gets the role identifier from the given role or of it's identifier.
    
    Parameters
    ----------
    role : ``Role``, `tuple` (`int`, `int`)
        The role, or a `guild-id`, `role-id` pair.
    
    Returns
    -------
    role : `None`, ``Role``
        The respective role.
    
    guild_id : `int`
        The role's guild's identifier.
    
    role_id : `int`
        The role's identifier.
    
    Raises
    ------
    TypeError
        If `role`'s type is incorrect.
    """
    if isinstance(role, Role):
        role_id = role.id
        guild_id = role.guild_id
    
    else:
        snowflake_pair = maybe_snowflake_pair(role)
        if snowflake_pair is None:
            raise TypeError(
                f'`role` can be `{Role.__name__}`, `tuple` (`int`, `int`), got {role.__class__.__name__}; {role!r}.'
            )
        
        guild_id, role_id = snowflake_pair
        role = ROLES.get(role_id, None)
    
    return role, guild_id, role_id


def get_role_guild_id_and_id(role):
    """
    Gets the role's and it's guild's identifier from the given role or of a `guild-id`, `role-id` pair.
    
    Parameters
    ----------
    role : ``Role``, `tuple` (`int`, `int`)
        The role, or a `guild-id`, `role-id` pair.
    
    Returns
    -------
    guild_id : `int`
        The role's guild's identifier.
    
    role_id : `int`
        The role's identifier.
    
    Raises
    ------
    TypeError
        If `role`'s type is incorrect.
    """
    if isinstance(role, Role):
        return role.guild_id, role.id
    
    snowflake_pair = maybe_snowflake_pair(role)
    if snowflake_pair is not None:
        return snowflake_pair
    
    raise TypeError(
        f'`role` can be `{Role.__name__}`, `tuple` (`int`, `int`), got {role.__class__.__name__}; {role!r}.'
    )


def get_webhook_id(webhook):
    """
    Gets the webhook's identifier from the given webhook or of it's identifier.
    
    Parameters
    ----------
    webhook : ``Webhook``, `int`
        The webhook, or it's identifier.
    
    Returns
    -------
    webhook_id : `int`
        The webhook's identifier.
    
    Raises
    ------
    TypeError
        If `webhook`'s type is incorrect.
    """
    if isinstance(webhook, Webhook):
        webhook_id = webhook.id
    else:
        webhook_id = maybe_snowflake(webhook)
        if webhook_id is None:
            raise TypeError(
                f'`webhook` can be `{Webhook.__name__}`, `int`, got {webhook.__class__.__name__}; {webhook!r}.'
            )
    
    return webhook_id


def get_webhook_and_id(webhook):
    """
    Gets the webhook and it's identifier from the given webhook or of it's identifier.
    
    Parameters
    ----------
    webhook : ``Webhook``, `int`
        The webhook, or it's identifier.
    
    Returns
    -------
    webhook : ``Webhook``, `None`
        The webhook if any.
    webhook_id : `int`
        The webhook's identifier.
    
    Raises
    ------
    TypeError
        If `webhook`'s type is incorrect.
    """
    while True:
        if isinstance(webhook, Webhook):
            webhook_id = webhook.id
            break
        
        webhook_id = maybe_snowflake(webhook)
        if (webhook_id is not None):
            try:
                webhook = USERS[webhook_id]
            except KeyError:
                webhook = None
                break
            
            if isinstance(webhook, Webhook):
                break
            
            raise TypeError(
                f'`webhook` can be `{Webhook.__name__}`, `int`, got {webhook.__class__.__name__}; {webhook!r}.'
            )
    
    return webhook, webhook_id


def get_webhook_id_and_token(webhook):
    """
    Gets the webhook's identifier and token from the given webhook or it's token, identifier pair.
    
    Parameters
    ----------
    webhook : ``Webhook``, `tuple` (`int`, `str`)
        The webhook or it's id and token.
    
    Returns
    -------
    webhook_id : `int`
        The webhook's identifier.
    webhook_token : `str`
        The webhook's token.
    
    Raises
    ------
    TypeError
        If `webhook`'s type is incorrect.
    """
    if isinstance(webhook, Webhook):
        snowflake_token_pair = webhook.id, webhook.token
    else:
        snowflake_token_pair = maybe_snowflake_token_pair(webhook)
        if (snowflake_token_pair is None):
            raise TypeError(
                f'`webhook` can be `{Webhook.__name__}`, `tuple` (`int`, `str`), got '
                f'{webhook.__class__.__name__}; {webhook!r}.'
            )
    
    return snowflake_token_pair


def get_webhook_and_id_and_token(webhook):
    """
    Gets the webhook, it's identifier and token from the given webhook or it's token, identifier pair.
    
    Parameters
    ----------
    webhook : ``Webhook``, `tuple` (`int`, `str`)
        The webhook or it's id and token.
    
    Returns
    -------
    webhook : ``Webhook``, `None`
        The webhook if any.
    webhook_id : `int`
        The webhook's identifier.
    webhook_token : `str`
        The webhook's token.
    
    Raises
    ------
    TypeError
        If `webhook`'s type is incorrect.
    """
    while True:
        if isinstance(webhook, Webhook):
            webhook_id = webhook.id
            webhook_token = webhook.token
            break
        
        snowflake_token_pair = maybe_snowflake_token_pair(webhook)
        if (snowflake_token_pair is not None):
            webhook_id, webhook_token = snowflake_token_pair
            
            try:
                webhook = USERS[webhook_id]
            except KeyError:
                webhook = None
                break
            
            if isinstance(webhook, Webhook):
                break
        
        raise TypeError(
            f'`webhook` can be `{Webhook.__name__}`, `tuple` (`int`, `str`), got '
            f'{webhook.__class__.__name__}; {webhook!r}.'
        )
    
    return webhook, webhook_id, webhook_token


def get_reaction(emoji):
    """
    Gets the reaction form of the given emoji.
    
    Parameters
    ----------
    emoji : ``Emoji``, `str`
        The emoji to get it's reaction form of.
    
    Returns
    -------
    as_reaction : `str`
        The emoji's reaction form.
    
    Raises
    ------
    TypeError
        If `emoji`'s type is incorrect.
    """
    if isinstance(emoji, Emoji):
        as_reaction = emoji.as_reaction
    elif isinstance(emoji, str):
        as_reaction = emoji
    else:
        raise TypeError(
            f'`emoji` can be `{Emoji.__class__}`, `str`, got {emoji.__class__.__name__}; {emoji!r}.'
        )
    
    return as_reaction


def get_emoji_from_reaction(emoji):
    """
    Gets emoji from the given emoji or reaction string.
    
    Parameters
    ----------
    emoji : ``Emoji``, `str`
        The emoji or reaction to get the emoji from.
    
    Returns
    -------
    emoji : ``Emoji``
        The emoji itself.
    
    Raises
    ------
    TypeError
        If `emoji`'s type is incorrect.
    ValueError
        The given `emoji` is not a valid reaction.
    """
    if isinstance(emoji, Emoji):
        pass
    elif isinstance(emoji, str):
        emoji = parse_reaction(emoji)
        if emoji is None:
            raise ValueError(
                f'The given `emoji` is not a valid reaction, got {emoji!r}.'
            )
    else:
        raise TypeError(
            f'`emoji` can be `{Emoji.__class__}`, `str`, got {emoji.__class__.__name__}; {emoji!r}.'
        )
    
    return emoji


def get_emoji_guild_id_and_id(emoji):
    """
    Gets the emoji's and it's guild's identifier from the given emoji.
    
    Parameters
    ----------
    emoji : ``Emoji``, `tuple` (`int`, `int`)
        The emoji, or `guild-id`, `emoji-id` pair.
    
    Returns
    -------
    snowflake_pair : `tuple` (`int`, `int`)
        The emoji's guild's and it's own identifier if applicable.
    
    Raises
    ------
    TypeError
        If `emoji`'s type is incorrect.
    """
    if isinstance(emoji, Emoji):
        snowflake_pair = emoji.guild_id, emoji.id
    
    else:
        snowflake_pair = maybe_snowflake_pair(emoji)
        if snowflake_pair is None:
            raise TypeError(
                f'`emoji` can be `{Emoji.__name__}`, `tuple` (`int`, `int`), got {emoji.__class__.__name__}; '
                f'{emoji!r}.'
            )
    
    return snowflake_pair


def get_sticker_and_id(sticker):
    """
    Gets sticker and it's identifier from the given sticker or of it's identifier.
    
    Parameters
    ----------
    sticker : ``Sticker``, `int`
        The sticker, or it's identifier.
    
    Returns
    -------
    sticker : ``Sticker``, `None`
        The sticker if found.
    sticker_id : `int`
        The sticker's identifier.
    
    Raises
    ------
    TypeError
        If `sticker`'s type is incorrect.
    """
    while True:
        if isinstance(sticker, Sticker):
            sticker_id = sticker.id
            break
        
        sticker_id = maybe_snowflake(sticker)
        if (sticker_id is not None):
            sticker = STICKERS.get(sticker_id, None)
            break
        
        raise TypeError(
            f'`sticker` can be `{Sticker.__name__}`, `int`, got {sticker.__class__.__name__}; {sticker!r}.'
        )
        
    return sticker, sticker_id


def get_sticker_pack_and_id(sticker_pack):
    """
    Gets sticker pack and it's identifier from the given sticker pack or of it's identifier.
    
    Parameters
    ----------
    sticker_pack : ``StickerPack``, `int`
        The sticker, or it's identifier.
    
    Returns
    -------
    sticker_pack : ``StickerPack``, `None`
        The sticker pack if found.
    sticker_pack_id : `int`
        The sticker pack's identifier.
    
    Raises
    ------
    TypeError
        If `sticker_pack`'s type is incorrect.
    """
    while True:
        if isinstance(sticker_pack, StickerPack):
            sticker_pack_id = sticker_pack.id
            break
        
        sticker_pack_id = maybe_snowflake(sticker_pack)
        if (sticker_pack_id is not None):
            sticker_pack = STICKER_PACKS.get(sticker_pack_id, None)
            break
        
        raise TypeError(
            f'`sticker_pack` can be `{StickerPack.__name__}`, `int`, got {sticker_pack.__class__.__name__}; '
            f'{sticker_pack!r}.'
        )
        
    return sticker_pack, sticker_pack_id


def get_scheduled_event_guild_id_and_id(scheduled_event):
    """
    Gets the scheduled event's and it's identifier from the given scheduled event or from a tuple of 2 identifiers.
    
    Parameters
    ----------
    scheduled_event : ``ScheduledEvent``, `tuple` of (`int`, `int`)
        The scheduled event, or a tuple of two identifiers.
    
    Returns
    -------
    guild_id : `int`
        The scheduled event's guild's identifier.
    scheduled_event_id : `int`
        The scheduled event's identifier.
    
    Raises
    ------
    TypeError
        If `scheduled_event`'s type is incorrect.
    """
    if isinstance(scheduled_event, ScheduledEvent):
        return scheduled_event.guild_id, scheduled_event.id
    
    
    snowflake_pair = maybe_snowflake_pair(scheduled_event)
    if snowflake_pair is None:
        raise TypeError(
            f'`scheduled_event` can be `{ScheduledEvent.__name__}`, `tuple` of (`int`, `int`), got '
            f'{scheduled_event.__class__.__name__}; {scheduled_event!r}.'
        )
    
    return snowflake_pair


def get_scheduled_event_and_guild_id_and_id(scheduled_event):
    """
    Gets the scheduled event, it's guild's identifier and it's identifier.
    
    Parameters
    ----------
    scheduled_event : ``ScheduledEvent``, `tuple` (`int`, `int`)
        The scheduled event, or it's identifier.
    
    Returns
    -------
    scheduled_event : `None`, ``ScheduledEvent``
        The scheduled event.
    guild_id : `int`
        The scheduled event's guild's identifier.
    scheduled_event_id : `int`
        The scheduled event's identifier.
    
    Raises
    ------
    TypeError
        If `scheduled_event`'s type is incorrect.
    """
    if isinstance(scheduled_event, ScheduledEvent):
        scheduled_event =  scheduled_event
        scheduled_event_id = scheduled_event.id
        guild_id = scheduled_event.guild_id
    else:
        snowflake_pair = maybe_snowflake_pair(scheduled_event)
        if snowflake_pair is None:
            raise TypeError(
                f'`scheduled_event` can be `{ScheduledEvent.__name__}`, `tuple` of (`int`, `int`), got '
                f'{scheduled_event.__class__.__name__}; {scheduled_event!r}.'
            )
        
        guild_id, scheduled_event_id = snowflake_pair
        
        scheduled_event = SCHEDULED_EVENTS.get(scheduled_event_id, None)
    
    return scheduled_event, guild_id, scheduled_event_id


def get_application_command_id(application_command):
    """
    Gets the application command's identifier.
    
    Parameters
    ----------
    application_command : ``ApplicationCommand``, `int`
        The application command or it's identifier.
    
    Returns
    -------
    application_command_id : `int`
        The application command's identifier.
    
    Raises
    ------
    TypeError
        If `application_command`'s type is incorrect.
    """
    if isinstance(application_command, ApplicationCommand):
        application_command_id = application_command.id
    
    else:
        application_command_id = maybe_snowflake(application_command)
        if application_command_id is None:
            raise TypeError(
                f'`application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                f'{application_command.__class__.__name__}; {application_command!r}.'
            )
    
    return application_command_id


def get_application_command_and_id(application_command):
    """
    Gets the application command's identifier.
    
    Parameters
    ----------
    application_command : ``ApplicationCommand``, `int`
        The application command or it's identifier.
    
    Returns
    -------
    application_command : `None`, ``ApplicationCommand``
        The application command if exists.
    application_command_id : `int`
        The application command's identifier.
    
    Raises
    ------
    TypeError
        If `application_command`'s type is incorrect.
    """
    if isinstance(application_command, ApplicationCommand):
        application_command_id = application_command.id
    
    else:
        application_command_id = maybe_snowflake(application_command)
        if application_command_id is None:
            raise TypeError(
                f'`application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                f'{application_command.__class__.__name__}; {application_command!r}.'
            )
        
        application_command = APPLICATION_COMMANDS.get(application_command_id, None)
    
    return application_command, application_command_id


def get_application_command_id_nullable(application_command):
    """
    Gets the application command's identifier.
    
    > The application command can be `None`. At that case `application_command_id` will default to `0`.
    
    Parameters
    ----------
    application_command : `None`, ``ApplicationCommand``, `int`
        The application command or it's identifier.
    
    Returns
    -------
    application_command_id : `int`
        The application command's identifier.
    
    Raises
    ------
    TypeError
        If `application_command`'s type is incorrect.
    """
    if application_command is None:
        application_command_id = 0
    
    elif isinstance(application_command, ApplicationCommand):
        application_command_id = application_command.id
    
    else:
        application_command_id = maybe_snowflake(application_command)
        if application_command_id is None:
            raise TypeError(
                f'`application_command` can be `{ApplicationCommand.__name__}`, `int`, got '
                f'{application_command.__class__.__name__}; {application_command!r}.'
            )
    
    return application_command_id


def get_auto_moderation_rule_guild_id_and_id(auto_moderation_rule):
    """
    Gets the auto moderation rule's guild's identifier and it's own identifier.
    
    Parameters
    ----------
    auto_moderation_rule : ``AutoModerationRule``, `tuple` (`int`, `int`)
        The auto moderation rule, or it's identifier as a `guild-id`, `rule-id` pair..
    
    Returns
    -------
    guild_id : `int`
        The auto moderation rule's guild's identifier.
    auto_moderation_rule_id : `int`
        The auto moderation rule's identifier.
    
    Raises
    ------
    TypeError
        If `auto_moderation_rule`'s type is incorrect.
    """
    if isinstance(auto_moderation_rule, AutoModerationRule):
        guild_id = auto_moderation_rule.guild_id
        rule_id = auto_moderation_rule.id
    
    else:
        snowflake_pair = maybe_snowflake_pair(auto_moderation_rule)
        if snowflake_pair is None:
            raise TypeError(
                f'`auto_moderation_rule` can be `{AutoModerationRule.__name__}`, `tuple` of (`int`, `int`), got '
                f'{auto_moderation_rule.__class__.__name__}; {auto_moderation_rule!r}.'
            )
        
        guild_id, rule_id = snowflake_pair
    
    return guild_id, rule_id


def get_auto_moderation_rule_and_guild_id_and_id(auto_moderation_rule):
    """
    Gets the auto moderation, its guild's identifier and it's own identifier.
    
    Parameters
    ----------
    auto_moderation_rule : ``AutoModerationRule``, `tuple` (`int`, `int`)
        The auto moderation rule, or it's identifier as a `guild-id`, `rule-id` pair..
    
    Returns
    -------
    auto_moderation_rule : `None`, ``AutoModerationRule``
        The auto moderation rule.
    guild_id : `int`
        The auto moderation rule's guild's identifier.
    auto_moderation_rule_id : `int`
        The auto moderation rule's identifier.
    
    Raises
    ------
    TypeError
        If `auto_moderation_rule`'s type is incorrect.
    """
    if isinstance(auto_moderation_rule, AutoModerationRule):
        guild_id = auto_moderation_rule.guild_id
        rule_id = auto_moderation_rule.id
    
    else:
        snowflake_pair = maybe_snowflake_pair(auto_moderation_rule)
        if snowflake_pair is None:
            raise TypeError(
                f'`auto_moderation_rule` can be `{AutoModerationRule.__name__}`, `tuple` of (`int`, `int`), got '
                f'{auto_moderation_rule.__class__.__name__}; {auto_moderation_rule!r}.'
            )
        
        guild_id, rule_id = snowflake_pair
        auto_moderation_rule = AUTO_MODERATION_RULES.get(rule_id, None)
    
    return auto_moderation_rule, guild_id, rule_id


def get_forum_tag_id(forum_tag):
    """
    Gets the forum tag's identifier.
    
    Parameters
    ----------
    forum_tag : ``ForumTag``, `int`
        The forum tag or its identifier.
    
    Returns
    -------
    forum_tag_id : `int`
        The forum tag's identifier.
    
    Raises
    ------
    TypeError
        - If `forum_tag` type is incorrect.
    """
    if isinstance(forum_tag, ForumTag):
        forum_tag_id = forum_tag.id
    
    else:
        forum_tag_id = maybe_snowflake(forum_tag)
        if (forum_tag_id is None):
            raise TypeError(
                f'`forum_tag` can be `{ForumTag.__name__}, `int`, got {forum_tag.__class__.__name__}; {forum_tag!r}.'
            )
    
    return forum_tag_id


def get_forum_tag_and_id(forum_tag):
    """
    Gets the forum tag and it's identifier.
    
    Parameters
    ----------
    forum_tag : ``ForumTag``, `int`
        The forum tag or its identifier.
    
    Returns
    -------
    forum_tag : `None`, ``ForumTag``
        The forum tag if exists.
    forum_tag_id : `int`
        The forum tag's identifier.
    
    Raises
    ------
    TypeError
        - If `forum_tag` type is incorrect.
    """
    if isinstance(forum_tag, ForumTag):
        forum_tag_id = forum_tag.id
    
    else:
        forum_tag_id = maybe_snowflake(forum_tag)
        if (forum_tag_id is None):
            raise TypeError(
                f'`forum_tag` can be `{ForumTag.__name__}, `int`, got {forum_tag.__class__.__name__}; {forum_tag!r}.'
            )
        
        forum_tag = FORUM_TAGS.get(forum_tag_id, None)
    
    return forum_tag, forum_tag_id


def get_permission_overwrite_target_id(permission_overwrite):
    """
    Returns the given `permission_overwrite`'s target id.
    
    Parameters
    ----------
    permission_overwrite : ``PermissionOverwrite``
        The permission overwrite or it's target id.
    
    Returns
    -------
    target_id : `int`
    
    Raises
    ------
    TypeError
        - If `permission_overwrite` type is incorrect.
    """
    if isinstance(permission_overwrite, PermissionOverwrite):
        target_id = permission_overwrite.target_id
    
    else:
        target_id = maybe_snowflake(permission_overwrite)
        if (target_id is None):
            raise TypeError(
                f'`permission_overwrite` can be `{PermissionOverwrite.__name__}`, `int` got '
                f'{permission_overwrite.__class__.__name__}; {permission_overwrite!r}.'
            )
    
    return target_id


def _check_required_scope(access, required_scope):
    if (required_scope is not None) and (not access.has_scope(required_scope)):
        raise ValueError(
            f'The given `access` not grants {required_scope.name!r} scope, what is required, '
            f'got {access!r}.'
        )


def get_oauth2_access_token(access, required_scope = None):
    """
    Returns the given oauth2 access's access token. Accepts both access and just token as well.
    
    Parameters
    ----------
    access : ``Oauth2Access``, ``Oauth2User``, `str`
        Oauth2 access to the respective user or it's access token.
    required_scope : `None`, ``Oauth2Scope`` = `None`, Optional
        Required scope of the access if any.
    
    Returns
    -------
    access_token : `str`
    
    Raises
    ------
    TypeError
        - If `access` is not ``Oauth2Access``, ``Oauth2User``, `str`.
    ValueError
        - If the given `access` is not providing the required scope.
    """
    if isinstance(access, (Oauth2Access, Oauth2User)):
        _check_required_scope(access, required_scope)
        access_token = access.access_token
    
    elif isinstance(access, str):
        access_token = access
    
    else:
        raise TypeError(
            f'`access` can be `{Oauth2Access.__name__}`, `{Oauth2User.__name__}`, `str`'
            f', got {access.__class__.__name__}; {access!r}.'
        )
    
    return access_token


def get_oauth2_access_token_and_user_id(access, user, required_scope = None):
    """
    Returns the given oauth2 access's access token and the user's identifier.
    
    Parameters
    ----------
    access : ``Oauth2Access``, ``Oauth2User``, `str`
        Oauth2 access to the respective user or it's access token.
    required_scope : `None`, ``Oauth2Scope`` = `None`, Optional
        Required scope of the access if any.
    
    Raises
    ------
    TypeError
        - If `access` is not ``Oauth2Access``, ``Oauth2User``, `str`.
        - If `user` is not `None`, ``ClientUserBase``.
        - If `user.id` could nto be determined.
    ValueError
        - If the given `access` is not providing the required scope.
        - If `user` and `access` refers to a different user.
    """
    user_id = get_user_id_nullable(user)
    
    if isinstance(access, Oauth2Access):
        _check_required_scope(access, required_scope)
        access_token = access.access_token
    
    elif isinstance(access, Oauth2User):
        _check_required_scope(access, required_scope)
        access_token = access.access_token
        
        if user_id and (user_id != access.id):
            raise ValueError(
                f'The given `user` and `access` refers to different users, got user = {user!r}, '
                f'access = {access!r}.'
            )
        
        user_id = access.id
    
    elif isinstance(access, str):
        access_token = access
    
    else:
        raise TypeError(
            f'`access` can be `{Oauth2Access.__name__}`, `{Oauth2User.__name__}`, `str`, got '
            f'{access.__class__.__name__}; {access!r}.'
        )
    
    
    if not user_id:
        raise TypeError(
            f'`user` was not detectable neither from `user` nor from `access` parameters, got '
            f'user = {user!r}, access = {access!r}.'
        )
    
    return access_token, user_id


def get_soundboard_sound_and_guild_id_and_id(soundboard_sound):
    """
    Gets the soundboard sound identifier from the given soundboard sound or of it's identifier.
    
    Parameters
    ----------
    soundboard_sound : ``SoundboardSound``, `tuple` (`int`, `int`)
        The soundboard sound, or a `guild-id`, `soundboard-sound-id` pair.
    
    Returns
    -------
    soundboard_sound : `None`, ``SoundboardSound``
        The respective soundboard sound.
    
    guild_id : `int`
        The soundboard sound's guild's identifier.
    
    soundboard_sound_id : `int`
        The soundboard sound's identifier.
    
    Raises
    ------
    TypeError
        If `soundboard_sound`'s type is incorrect.
    """
    if isinstance(soundboard_sound, SoundboardSound):
        soundboard_sound_id = soundboard_sound.id
        guild_id = soundboard_sound.guild_id
    
    else:
        snowflake_pair = maybe_snowflake_pair(soundboard_sound)
        if snowflake_pair is None:
            raise TypeError(
                f'`soundboard_sound` can be `{SoundboardSound.__name__}`, `tuple` (`int`, `int`), '
                f'got {soundboard_sound.__class__.__name__}; {soundboard_sound!r}.'
            )
        
        guild_id, soundboard_sound_id = snowflake_pair
        soundboard_sound = SOUNDBOARD_SOUNDS.get(soundboard_sound_id, None)
    
    return soundboard_sound, guild_id, soundboard_sound_id


def get_soundboard_sound_guild_id_and_id(soundboard_sound):
    """
    Gets the soundboard_sound's and it's guild's identifier from the given soundboard_sound or of a `guild-id`,
    `soundboard_sound-id` pair.
    
    Parameters
    ----------
    soundboard_sound : ``SoundboardSound``, `tuple` (`int`, `int`)
        The soundboard sound, or a `guild-id`, `soundboard-sound-id` pair.
    
    Returns
    -------
    guild_id : `int`
        The soundboard sound's guild's identifier.
    
    soundboard_sound_id : `int`
        The soundboard sound's identifier.
    
    Raises
    ------
    TypeError
        If `soundboard_sound`'s type is incorrect.
    """
    if isinstance(soundboard_sound, SoundboardSound):
        return soundboard_sound.guild_id, soundboard_sound.id
    
    snowflake_pair = maybe_snowflake_pair(soundboard_sound)
    if snowflake_pair is not None:
        return snowflake_pair
    
    raise TypeError(
        f'`soundboard_sound` can be `{SoundboardSound.__name__}`, `tuple` (`int`, `int`), '
        f'got {soundboard_sound.__class__.__name__}; {soundboard_sound!r}.'
    )
