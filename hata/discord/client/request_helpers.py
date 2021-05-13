__all__ = ()
from os.path import split as split_path
from collections import deque

from ...backend.utils import to_json
from ...backend.export import include
from ...backend.formdata import Formdata

from ..core import MESSAGES
from ..message import Message, MessageReference, MessageRepr
from ..embed import EmbedBase
from ..utils import random_id
from ..bases import maybe_snowflake_pair

ComponentBase = include('ComponentBase')


def get_components_data(components):
    """
    Gets component data from the given components.
    
    parameters
    ----------
    components : `None`, ``ComponentBase``, (`set`, `list`) of ``ComponentBase`
        Components to be attached to a message.
    
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
    # 1.: None -> None
    # 2.: ComponentBase -> [component.to_data()]
    # 3.: (list, tuple) of ComponentBase -> [component.to_data(), ...] / None
    # 4.: raise
    
    if components is None:
        component_datas = None
    else:
        if isinstance(components, ComponentBase):
            component_datas = [components.to_data()]
        elif isinstance(components, (list, tuple)):
            component_datas = None
            
            for component in components:
                if __debug__:
                    if not isinstance(component, ComponentBase):
                        raise AssertionError(f'`components` contains non `{ComponentBase.__name__}` instance, got '
                            f'{component.__class__.__name__}')
                
                if component_datas is None:
                    component_datas = []
                
                component_datas.append(component.to_data())
        
        else:
            raise TypeError(f'`components` can be given as `{ComponentBase.__name__}` or as `list`, `tuple` of '
                f'`{ComponentBase.__name__}` instances, got {components.__class__.__name__}')
    
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
        channel_id = message.channel.id
        message_id = message.id
    else:
        if isinstance(message, MessageRepr):
            channel_id = message.channel.id
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


def validate_content_and_embed(content, embed, is_multiple_embed_allowed, is_edit):
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
    is_multiple_embed_allowed : `bool`
        Whether sending multiple embeds is allowed. If given as `True`, the returned `embed`-s will be a `list` or
        `tuple`.
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
        if is_multiple_embed_allowed:
            embed = [embed]
    
    elif isinstance(embed, (list, tuple)):
        if embed:
            if __debug__:
                for embed_element in embed:
                    if not isinstance(embed_element, EmbedBase):
                        raise AssertionError(f'`embed` was given as a `list` or `tuple`, but it\'s it contains a non '
                            f'`{EmbedBase.__name__}` instance element, got {embed_element.__class__.__name__}.')
            
            if is_multiple_embed_allowed:
                embed = embed[:10]
            else:
                embed = embed[0]
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
        
        if is_multiple_embed_allowed:
            embed = [content]
        else:
            embed = content
        
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
            
            if is_multiple_embed_allowed:
                embed = content[:10]
            else:
                embed = content[0]
            
            if is_edit:
                content = ...
            else:
                content = None
        else:
            content = str(content)
    
    return content, embed
