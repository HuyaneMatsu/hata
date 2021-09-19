__all__ = ()
from os.path import split as split_path
from collections import deque

from ...backend.utils import to_json
from ...backend.export import include
from ...backend.formdata import Formdata

from ..core import MESSAGES, CHANNELS, GUILDS, USERS, STICKERS
from ..message import Message, MessageReference, MessageRepr
from ..user import ClientUserBase
from ..channel import ChannelText, ChannelStage
from ..embed import EmbedBase
from ..utils import random_id
from ..bases import maybe_snowflake_pair, maybe_snowflake, maybe_snowflake_token_pair
from ..guild import Guild, GuildDiscovery
from ..oauth2 import Achievement
from ..role import Role
from ..stage import Stage
from ..webhook import Webhook
from ..emoji import Emoji, parse_reaction
from ..sticker import Sticker


ComponentBase = include('ComponentBase')
ComponentType = include('ComponentType')
ComponentRow = include('ComponentRow')

def get_components_data(components, is_edit):
    """
    Gets component data from the given components.
    
    Parameters
    ----------
    components : `None`, ``ComponentBase``, (`set`, `list`) of \
            (``ComponentBase``, (`set`, `list`) of ``ComponentBase``)
        Components to be attached to a message.
    is_edit : `bool`
        Whether the processed `components` fields are for message edition. At this case passing `None` will
        remove them.
    
    Returns
    -------
    component_datas : `None` ot `list` of (`dict` of (`str`, `Any`) items)
        The generated data if any.
    
    Raises
    ------
    TypeError
        - If `components` was not given neither as `None`, ``ComponentBase``, (`list`, `tuple`) of ``ComponentBase``
            instances.
    AssertionError
        - If `components` contains a non ``ComponentBase`` element.
    """
    
    # Components check order:
    # 1.: None -> None || []
    # 2.: Ellipsis -> None || Ellipsis
    # 2.: ComponentBase -> [component.to_data()]
    # 3.: (list, tuple) of ComponentBase, (list, tuple) of ComponentBase -> [component.to_data(), ...] / None
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
        if isinstance(components, ComponentBase):
            if components.type is not ComponentType.row:
                components = ComponentRow(components)
                
            component_datas = [components.to_data()]
        elif isinstance(components, (list, tuple)):
            component_datas = None
            
            for component in components:
                if isinstance(component, ComponentBase):
                    if component.type is not ComponentType.row:
                        component = ComponentRow(component)
                
                elif isinstance(component, (list, tuple)):
                    component = ComponentRow(*component)
                
                else:
                    raise TypeError(f'`components` contains a non `{ComponentBase.__name__}` or as `list`, `tuple` of '
                        f'`{ComponentBase.__name__}` instances, got {components.__class__.__name__}')
                
                if component_datas is None:
                    component_datas = []
                
                component_datas.append(component.to_data())
                continue
        
        else:
            raise TypeError(f'`components` can be given as `{ComponentBase.__name__}` or as `list`, `tuple` of '
                f'(`{ComponentBase.__name__}` or (`list`, `tuple`) of `{ComponentBase.__name__}`), '
                f'got {components.__class__.__name__}')
    
    return component_datas


def validate_message_to_delete(message):
    """
    Validates a message to delete.
    
    Parameters
    ----------
    message : ``Message``, ``MessageReference``, ``MessageRepr``, `tuple` (`int`, `int`)
        The message to validate for deletion.
    
    Returns
    -------
    channel_id : `int`
        The channel's identifier where the message is.
    message_id : `int`
        The message's identifier.
    message : `None` or ``Message``
        The referenced message if found.
    
    Raises
    ------
    TypeError
        If message was not given neither as ``Message``, ``MessageReference``, ``MessageRepr``, neither as
        `tuple` (`int`, `int`).
    """
    if isinstance(message, Message):
        channel_id = message.channel_id
        message_id = message.id
    else:
        if isinstance(message, MessageRepr):
            channel_id = message.channel_id
            message_id = message.id
        elif isinstance(message, MessageReference):
            channel_id = message.channel_id
            message_id = message.message_id
        else:
            snowflake_pair = maybe_snowflake_pair(message)
            if snowflake_pair is None:
                raise TypeError(f'`message` should have be given as `{Message.__name__}` or as '
                    f'`{MessageRepr.__name__}`, `{MessageReference.__name__}`, or as `tuple` of (`int`, `int`), '
                    f'got {message.__class__.__name__}.')
            
            channel_id, message_id = snowflake_pair
        
        message = MESSAGES.get(message, None)
    
    return channel_id, message_id, message


def create_file_form(data, file):
    """
    Creates a `multipart/form-data` form from the message's data and from the file data. If there is no files to
    send, will return `None` to tell the caller, that nothing is added to the overall data.
    
    Parameters
    ----------
    data : `dict` of `Any`
        The data created by the ``.message_create`` method.
    file : `dict` of (`file-name`, `io`) items, `list` of (`file-name`, `io`) elements, tuple (`file-name`, `io`), `io`
        The files to send.
    
    Returns
    -------
    form : `None` or `Formdata`
        Returns a `Formdata` of the files and from the message's data. If there are no files to send, returns `None`
        instead.
    
    Raises
    ------
    ValueError
        If more than `10` file is registered to be sent.
    
    Notes
    -----
    Accepted `io` types with check order are:
    - ``BodyPartReader`` instance
    - `bytes`, `bytearray`, `memoryview` instance
    - `str` instance
    - `BytesIO` instance
    - `StringIO` instance
    - `TextIOBase` instance
    - `BufferedReader`, `BufferedRandom` instance
    - `IOBase` instance
    - ``AsyncIO`` instance
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
    
    # case 1 dict like
    if hasattr(type(file), 'items'):
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
        form.add_field('file', io, filename=name, content_type='application/octet-stream')
    # case 2, no files -> return None, we should use the already existing data
    elif len(files) == 0:
        return None
    # case 3 maximum 10 files
    elif len(files) < 11:
        for index, (name, io) in enumerate(files):
            form.add_field(f'file{index}s', io, filename=name, content_type='application/octet-stream')
    
    # case 4 more than 10 files
    else:
        raise ValueError('You can send maximum 10 files at once.')
    
    return form


def add_file_to_message_data(message_data, file, contains_content):
    """
    Adds files to the message data creating a form data if applicable.
    
    Parameters
    ----------
    message_data : `dict` of (`str`, `Any`) items
        The message's payload to send.
    file : `None` or `dict` of (`file-name`, `io`) items, `list` of (`file-name`, `io`) elements, \
            tuple (`file-name`, `io`), `io`
        The files to send.
    contains_content : `bool`
        Whether the message already contains any content.
    
    Returns
    -------
    message_data : `None` or `dict`, `Formdata`
        Returns a `Formdata` if the message contains attachments, `dict` if contains any content and `None` if
        not.
    
    Raises
    ------
    ValueError
        If more than `10` file is registered to be sent.
    """
    if (file is None):
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
    content : `str`, ``EmbedBase`` or `Any`, Optional
        The content of the message.
        
        
        If given as ``EmbedBase`` instance, then the message's embeds will be edited with it.
    embed : `None`, ``EmbedBase`` instance or `list` of ``EmbedBase`` instances, Optional (Keyword only)
        The new embedded content of the message. By passing it as `None`, you can remove the old.
        
        > If `embed` and `content` parameters are both given as  ``EmbedBase`` instance, then `AssertionError` is
        raised.
    is_edit : `bool`
        Whether the processed `content` and `embed` fields are for message edition. At this case passing `None` will
        remove them.
    
    Returns
    -------
    content : `Ellipsis`, `None`, `str`
        The message's content.
    embed : `Ellipsis`, `None`, ``EmbedBase``, (`list` or `tuple`) of ``EmbedBase``
        The messages embeds.
    
    Raises
    ------
    TypeError
        If `embed` was not given neither as ``EmbedBase`` nor as `list` or `tuple` of ``EmbedBase`` instances.
    AssertionError
        - If `embed` contains a non ``EmbedBase`` element.
        - If both `content` and `embed` fields are embeds.
    """
    # Embed check order:
    # 1.: None
    # 2.: Ellipsis -> None || Ellipsis
    # 3.: Embed : -> embed || [embed]
    # 4.: list of Embed -> embed[0] || embed[:10] or None
    # 5.: raise
    if embed is None:
        pass
    
    elif embed is ...:
        if not is_edit:
            embed = None
    
    elif isinstance(embed, EmbedBase):
        embed = [embed]
    
    elif isinstance(embed, (list, tuple)):
        if embed:
            if __debug__:
                for embed_element in embed:
                    if not isinstance(embed_element, EmbedBase):
                        raise AssertionError(f'`embed` was given as a `list` or `tuple`, but it\'s it contains a non '
                            f'`{EmbedBase.__name__}` instance element, got {embed_element.__class__.__name__}.')
            
            embed = embed[:10]
        else:
            embed = None
    
    else:
        raise TypeError(f'`embed` was not given as `{EmbedBase.__name__}` instance, neither as a `list`  or `tuple` of '
            f'{EmbedBase.__name__} instances, got {embed.__class__.__name__}.')
    
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
    
    elif isinstance(content, EmbedBase):
        if __debug__:
            if (embed is not (... if is_edit else None)):
                raise AssertionError(f'Multiple embeds were given, got content={content!r}, embed={embed!r}.')
        
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
                    if isinstance(element, EmbedBase):
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
                    raise AssertionError(f'Multiple embeds were given, got content={content!r}, embed={embed!r}.')
            
            embed = content[:10]
            
            if is_edit:
                content = ...
            else:
                content = None
        else:
            content = str(content)
    
    return content, embed


def get_channel_id(channel, channel_type):
    """
    Gets the channel's identifier from the given channel or of it's identifier.
    
    Parameters
    ----------
    channel : `channel_type`, `int`
        The channel, or it's identifier.
    channel_type : `type`
        The expected channel type of `channel`.
    
    Returns
    -------
    channel_id : `int`
        The channel's identifier.
    
    Raises
    ------
    TypeError
        If `channel`'s type is incorrect.
    """
    if isinstance(channel, channel_type):
        channel_id = channel.id
    
    else:
        channel_id = maybe_snowflake(channel)
        if channel_id is None:
            raise TypeError(f'`channel` can be either given as `{channel_type.__name__}` or as `int` instance, '
                f'got {channel.__class__.__name__}.')
    
    return channel_id


def get_guild_and_guild_text_channel_id(channel):
    """
    Gets guild text channel identifier and it's guild from the given text channel or of it's identifier.
    
    Parameters
    ----------
    channel : ``ChannelText``, `int`
        The channel, or it's identifier.
    
    Returns
    -------
    guild : ``Guild`` or `None`
        The respective guild if any found.
    channel_id : `int`
        The channel's identifier.
    
    Raises
    ------
    TypeError
        If `channel`'s type is incorrect.
    """
    while True:
        if isinstance(channel, ChannelText):
            channel_id = channel.id
            guild = channel.guild
            break
        
        channel_id = maybe_snowflake(channel)
        if (channel_id is not None):
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                guild = None
                break
            
            if isinstance(channel, ChannelText):
                guild = channel.guild
                break
        
        raise TypeError(f'`channel` can be either given as `{ChannelText.__name__}` or as `int` instance, '
            f'got {channel.__class__.__name__}.')
    
    return guild, channel_id


def get_guild_id_and_channel_id(channel, channel_type):
    """
    Gets the channel's and it's guild's identifier from the given channel or of it's identifier.
    
    Parameters
    ----------
    channel : `channel_type` or `tuple` (`int`, `int`)
        The role, or `guild-id`, `role-id` pair.
    channel_type : `type`
        The expected type of `channel`.
    
    Returns
    -------
    snowflake_pair : `None` or `tuple` (`int`, `int`)
        The channel's guild's and it's own identifier if applicable.
    
    Raises
    ------
    TypeError
        If `channel`'s type is incorrect.
    """
    if isinstance(channel, channel_type):
        guild = channel.guild
        if guild is None:
            snowflake_pair = None
        else:
            snowflake_pair = guild.id, channel.id
    else:
        snowflake_pair = maybe_snowflake_pair(channel)
        if snowflake_pair is None:
            raise TypeError(f'`channel` can be given as `{channel_type.__name__}`, or as '
                f'`tuple` (`int`, `int`), got {channel.__class__.__name__}.')
        
    return snowflake_pair


def get_channel_and_id(channel, channel_type):
    """
    Gets thread channel and it's identifier from the given thread channel or of it's identifier.
    
    Parameters
    ----------
    channel : ``ChannelThread``, `int`
        The channel, or it's identifier.
    channel_type : `type`
        The expected type of `channel`.
    
    Returns
    -------
    channel : ``channel_type``, `None`
        The channel if found.
    channel_id : `int`
        The channel's identifier.
    
    Raises
    ------
    TypeError
        If `channel`'s type is incorrect.
    """
    while True:
        if isinstance(channel, channel_type):
            channel_id = channel.id
            break
        
        channel_id = maybe_snowflake(channel)
        if (channel_id is not None):
            try:
                channel = CHANNELS[channel_id]
            except KeyError:
                channel = None
                break
            
            if isinstance(channel, channel_type):
                break
        
        raise TypeError(f'`channel` can be either given as `{channel_type.__name__}` or as `int` instance, '
            f'got {channel.__class__.__name__}.')
    
    return channel, channel_id


def get_stage_channel_id(stage):
    """
    Gets stage's channel's identifier from the given stage or of it's identifier.
    
    Parameters
    ----------
    stage : `Stage`, ``ChannelStage``, `int`
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
    if isinstance(stage, Stage):
        channel_id = stage.channel.id
    elif isinstance(stage, ChannelStage):
        channel_id = stage.id
    else:
        channel_id = maybe_snowflake(stage)
        if channel_id is None:
            raise TypeError(f'`stage` can be given as `{Stage.__name__}`, `{ChannelStage.__name__}`, or as '
                f'int` instance, got {stage.__class__.__name__}.')
    
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
        user_id = user.id
    
    else:
        user_id = maybe_snowflake(user)
        if user_id is None:
            raise TypeError(f'`user` can be either given as `{ClientUserBase.__name__}` or as `int` instance, '
                f'got {user.__class__.__name__}.')
    
    return user_id


def get_user_and_id(user):
    """
    Gets user and it's identifier from the given user or of it's identifier.
    
    Parameters
    ----------
    user : ``ClientUserBase``, `int`
        The user, or it's identifier.
    
    Returns
    -------
    user : ``ClientUserBase`` or `None`
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
        
        raise TypeError(f'`user` can be either given as `{ClientUserBase.__name__}` or as `int` instance, '
            f'got {user.__class__.__name__}.')
        
    return user, user_id


def get_user_id_nullable(user):
    """
    Gets user identifier from the given user or of it's identifier. The user can be given as `None`. At that case
    `user_id` will default to `0`.
    
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
        user_id = 0
    
    elif isinstance(user, ClientUserBase):
        user_id = user.id
    
    else:
        user_id = maybe_snowflake(user)
        if user_id is None:
            raise TypeError(f'`user` can be either given as `{ClientUserBase.__name__}` or as `int` instance, '
                f'got {user.__class__.__name__}.')
    
    return user_id


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
        guild_id = guild.id
    else:
        guild_id = maybe_snowflake(guild)
        if guild_id is None:
            raise TypeError(f'`guild` can be given as `{Guild.__name__}` or `int` instance, got '
                f'{guild.__class__.__name__}.')
    
    return guild_id


def get_guild_and_id(guild):
    """
    Gets the guild and it's identifier from the given guild or of it's identifier.
    
    Parameters
    ----------
    guild : ``Guild``, `int`
        The guild, or it's identifier.
    
    Returns
    -------
    guild : ``Guild`` or `None`
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
            raise TypeError(f'`guild` can be given as `{Guild.__name__}` or `int` instance, got '
                f'{guild.__class__.__name__}.')
        
        guild = GUILDS.get(guild_id, None)
    
    return guild, guild_id


def get_guild_discovery_and_id(guild):
    """
    Gets the guild discovery and it's identifier from the given guild or it's identifier.
    
    Parameters
    ----------
    guild : ``Guild``, `int`
        The guild, or it's identifier.
    
    Returns
    -------
    guild : ``GuildDiscovery`` or `None`
        The guild or the
    guild_id : `int`
        The guild's identifier.
    
    Raises
    ------
    TypeError
        If `guild`'s type is incorrect.
    """
    if isinstance(guild, Guild):
        guild_id = guild.id
        guild_discovery = None
    elif isinstance(guild, GuildDiscovery):
        guild_id = guild.guild.id
        guild_discovery = guild
    else:
        guild_id = maybe_snowflake(guild)
        if guild_id is None:
            raise TypeError(f'`guild` can be given as `{Guild.__name__}`, `{GuildDiscovery.__name__}` or `int` '
                f'instance, got {guild.__class__.__name__}.')
        
        guild_discovery = None
    
    return guild_discovery, guild_id


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
            raise TypeError(f'`achievement` can be given as `{Achievement.__name__}` or `int` instance, got '
                f'{achievement.__class__.__name__}.')
    
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
            raise TypeError(f'`achievement` can be given as `{Achievement.__name__}` or `int` instance, got '
                f'{achievement.__class__.__name__}.')
        
        achievement = None
    
    return achievement, achievement_id


def get_channel_id_and_message_id(message):
    """
    Gets the message's channel's and it's own identifier.
    
    Parameters
    ----------
    message : ``Message``, ``MessageRepr``, ``MessageReference``, `tuple` (`int`, `int`)
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
    # 2.: MessageRepr
    # 3.: MessageReference
    # 4.: None -> raise
    # 5.: `tuple` (`int`, `int`)
    # 6.: raise
    if isinstance(message, Message):
        channel_id = message.channel_id
        message_id = message.id
    elif isinstance(message, MessageRepr):
        channel_id = message.channel_id
        message_id = message.id
    elif isinstance(message, MessageReference):
        channel_id = message.channel_id
        message_id = message.message_id
    elif message is None:
        raise TypeError('`message` was given as `None`. Make sure to use `Client.message_create` with giving '
            'content and using a cached channel.')
    else:
        snowflake_pair = maybe_snowflake_pair(message)
        if snowflake_pair is None:
            raise TypeError(f'`message` can be given as `{Message.__name__}` or as '
                f'`{MessageRepr.__name__}`, `{MessageReference.__name__}` or as `tuple` of (`int`, `int`), got '
                f'`{message.__class__.__name__}`.')
        
        channel_id, message_id = snowflake_pair
    
    return channel_id, message_id


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
            raise TypeError(f'`role` can be given as `{Role.__name__}` or `int` instance, got '
                f'{role.__class__.__name__}.')
    
    return role_id


def get_guild_id_and_role_id(role):
    """
    Gets the role's and it's guild's identifier from the given role or of a `guild-id`, `role-id` pair.
    
    Parameters
    ----------
    role : ``Role`` or `tuple` (`int`, `int`)
        The role, or `guild-id`, `role-id` pair.
    
    Returns
    -------
    snowflake_pair : `None` or `tuple` (`int`, `int`)
        The role's guild's and it's own identifier if applicable.
    
    Raises
    ------
    TypeError
        If `role`'s type is incorrect.
    """
    if isinstance(role, Role):
        guild = role.guild
        if guild is None:
            snowflake_pair = None
        else:
            snowflake_pair = guild.id, role.id
    
    else:
        snowflake_pair = maybe_snowflake_pair(role)
        if snowflake_pair is None:
            raise TypeError(f'`role` can be given as `{Role.__name__}`, or as `tuple` (`int`, `int`), got '
                f'{role.__class__.__name__}.')
    
    return snowflake_pair


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
            raise TypeError(f'`webhook` can be given as `{Webhook.__name__}` or `int` instance, got '
                f'{webhook.__class__.__name__}.')
    
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
    webhook : ``Webhook`` or `None`
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
            
            raise TypeError(f'`webhook` can be given as `{Webhook.__name__}` or `int` instance, got '
                f'{webhook.__class__.__name__}.')
    
    return webhook, webhook_id


def get_webhook_id_token(webhook):
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
            raise TypeError(f'`webhook` can be given either as `{Webhook.__name__}` or as `tuple` (`int`, `str`), '
                f'got {webhook.__class__.__name__}.')
    
    return snowflake_token_pair


def get_webhook_and_id_token(webhook):
    """
    Gets the webhook, it's identifier and token from the given webhook or it's token, identifier pair.
    
    Parameters
    ----------
    webhook : ``Webhook``, `tuple` (`int`, `str`)
        The webhook or it's id and token.
    
    Returns
    -------
    webhook : ``Webhook`` or `None`
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
        
        raise TypeError(f'`webhook` can be given either as `{Webhook.__name__}` or as `tuple` (`int`, `str`), '
            f'got {webhook.__class__.__name__}.')
    
    return webhook, webhook_id, webhook_token


def get_reaction(emoji):
    """
    Gets the reaction form of the given emoji.
    
    Parameters
    ----------
    emoji : ``Emoji`` or `str`
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
        raise TypeError(f'`emoji` can be given as ``{Emoji.__class__}`` or as `str` instance, got '
            f'{emoji.__class__.__name__}.')
    
    return as_reaction


def get_emoji_from_reaction(emoji):
    """
    Gets emoji from the given emoji or reaction string.
    
    Parameters
    ----------
    emoji : ``Emoji`` or `str`
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
            raise ValueError(f'The given `emoji` is not a valid reaction, got {emoji!r}.')
    else:
        raise TypeError(f'`emoji` can be given as ``{Emoji.__class__}`` or as `str` instance, got '
            f'{emoji.__class__.__name__}.')
    
    return emoji


def get_guild_id_and_emoji_id(emoji):
    """
    Gets the emoji's and it's guild's identifier from the given emoji.
    
    Parameters
    ----------
    emoji : ``Emoji`` or `tuple` (`int`, `int`)
        The emoji, or `guild-id`, `emoji-id` pair.
    
    Returns
    -------
    snowflake_pair : `None` or `tuple` (`int`, `int`)
        The emoji's guild's and it's own identifier if applicable.
    
    Raises
    ------
    TypeError
        If `emoji`'s type is incorrect.
    """
    if isinstance(emoji, Emoji):
        guild = emoji.guild
        if guild is None:
            snowflake_pair = None
        else:
            snowflake_pair = guild.id, emoji.id
    
    else:
        snowflake_pair = maybe_snowflake_pair(emoji)
        if snowflake_pair is None:
            raise TypeError(f'`emoji` can be given as `{Emoji.__name__}`, or as `tuple` (`int`, `int`), got '
                f'{emoji.__class__.__name__}.')
    
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
    sticker : ``Sticker`` or `None`
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
            try:
                sticker = STICKERS[sticker_id]
            except KeyError:
                sticker = None
                break
            
            if isinstance(sticker, Sticker):
                break
        
        raise TypeError(f'`sticker` can be either given as `{Sticker.__name__}` or as `int` instance, '
            f'got {sticker.__class__.__name__}.')
        
    return sticker, sticker_id
