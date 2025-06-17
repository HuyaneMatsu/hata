__all__ = ('CONVERSION_ATTACHMENTS',)

from collections import deque as Deque
from os.path import split as split_path

from scarletio.web_common import FormData

from .....env import API_VERSION

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion
from ....utils import random_id

from ...attachment import Attachment


def _is_attachments(value):
    """
    Yields the outcome if the `value` is acceptable.
    
    This function is a generator.
    
    Parameters
    ----------
    value : `None`, `(str, object)`, `dict<str, object>, \
            `(list | Deque)<(object,) | (None | str, object) | (None | str, object, None | str)>)`
        The value to check.
    
    Yields
    ------
    attachments : `None | list<(bool<True>, int) | (bool<False>, (str, object, None | str))>`
        The processed attachments:
    """
    # None
    if value is None:
        yield None
        return
    
    # tuple
    if isinstance(value, tuple):
        for attachment in _is_valid_tuple_attachment(value):
            yield [attachment]
        return
    
    # Attachment
    if isinstance(value, Attachment):
        yield [(True, value.id)]
        return
    
    # list | Deque
    if isinstance(value, list) or isinstance(value, Deque):
        attachments = None
        
        for element in value:
            for attachment in _is_single_attachment(element):
                break
            else:
                return
            
            if attachments is None:
                attachments = []
            
            attachments.append(attachment)
            continue
        
        yield attachments
        return
    
    # dict-like
    if hasattr(type(value), 'items'):
        attachments = None
        
        for item in value.items():
            if attachments is None:
                attachments = []
            
            attachments.append((False, (*item, None)))
        
        yield attachments
        return
    
    # rest
    yield [(False, (_get_or_create_io_name(value), value, None))]
    return


def _is_single_attachment(value):
    """
    Yields the outcome if the `value` is acceptable.
    
    This function is a generator.
    
    Parameters
    ----------
    value : `None`, `(str, object)`, `dict<str, object>, \
            `(list | Deque)<(object,) | (None | str, object) | (None | str, object, None | str)>)`
        The value to check
    
    Yields
    ------
    attachments : `(bool<True>, int) | (bool<False>, (str, object, None | str))`
        The processed attachments
    """
    if isinstance(value, tuple):
        yield from _is_valid_tuple_attachment(value)
        return
    
    if isinstance(value, Attachment):
        yield (True, value.id)
        return
    
    yield (False, (_get_or_create_io_name(value), value, None))
    return


def _get_or_create_io_name(io):
    """
    Gets the `io`'s name or creates a new one.
    
    Parameters
    ----------
    io : `object`
        Io to get its name of.
    
    Returns
    -------
    mame : `str`
    """
    name = getattr(io, 'name', None)
    if (name is not None) and name:
        name = split_path(name)[1]
    else:
        name = str(random_id())
    
    return name


def _is_valid_tuple_attachment(value):
    """
    Returns whether the given `tuple` is a valid attachment.
    
    This function is a generator.
    
    Parameters
    ----------
    value : `(None | str, object) | (None | str, object, None | str)`
        The value to check.
    
    Yields
    ------
    attachment : `(bool<False>, (str, object, None | str))`
    """
    length = len(value)
    if length < 1 or length > 3:
        return
        
    if length == 1:
        io, = value
        name = None
        description = None
    elif length == 2:
        name, io = value
        if (name is not None) and (not name):
            name = None
        description = None
    else:
        name, io, description = value
        if (name is not None) and (not name):
            name = None
        if (description is not None) and (not description):
            description = None
    
    if (name is None) or (not name):
        name = _get_or_create_io_name(io)
    
    yield False, (name, io, description)


def _build_partial_attachment_data(attachment_id, description):
    """
    Builds a partial attachment data to be sent to Discord.
    
    Parameters
    ----------
    attachment_id : `int`
        The attachment's identifier.
    description : `None | str`
        Description for the attachment.
    
    Returns
    -------
    data : `dict<str, object>
    """
    data = {'id': str(attachment_id)}
    
    if (description is not None):
        data['description'] = description
    
    return data


class CONVERSION_ATTACHMENTS(Conversion):
    # Generic
    
    name = 'attachments'
    name_aliases = ['files', 'file']
    expected_types_messages = (
        '`None`, `(str, object)`, `dict<str, object>, '
        '`(list | Deque)<(object,) | (None | str, object) | (None | str, object, None | str)>)`'
    )
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = None
    set_type_processor = None
    set_identifier = None
    set_listing_identifier = None
    
    set_validator = _is_attachments
    
    
    # Reading
    
    get_default = None
    get_processor = None
    
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None
    
    
    if API_VERSION >= 9:
        def serializer_putter(data, required, value):
            
            file_attachment_index = 0
            
            if value is None:
                attachment_datas = None
            
            else:
                attachment_datas = []
                
                for is_attachment, details in value:
                    if is_attachment:
                        attachment_id = details
                        description = None
                    else:
                        attachment_id = file_attachment_index
                        file_attachment_index += 1
                        description = details[2]
                    
                    attachment_datas.append(_build_partial_attachment_data(attachment_id, description))
            
            
            if (not required) and (attachment_datas is None):
                return data
            
            if attachment_datas is None:
                data['attachments'] = []
            else:
                data['attachments'] = attachment_datas
            
            if not file_attachment_index:
                return data
            
            form = FormData()
            form.add_json('payload_json', data)
            
            for file_attachment_index, (name, io, description) in enumerate(
                details for is_attachment, details in value if not is_attachment
            ):
                form.add_field(
                    f'files[{file_attachment_index}]', io, file_name = name, content_type = 'application/octet-stream'
                )
            
            return form
    
    else:
        def serializer_putter(data, required, value):
            if value is None:
                return data
            
            file_attachments = [details for is_attachment, details in value if not is_attachment]
            if not file_attachments:
                return data
            
            form = FormData()
            form.add_json('payload_json', data)
            
            if len(file_attachments) == 1:
                name, io, description = file_attachments
                form.add_field('file', io, file_name = name, content_type = 'application/octet-stream')
            else:
                for file_attachment_index, (name, io, description) in enumerate(file_attachments):
                    form.add_field(
                        f'file{file_attachment_index}s', io, file_name = name, content_type = 'application/octet-stream'
                    )
            
            return form
    
    
    # Sorting
    
    sort_priority = 9999
