__all__ = ('CONVERSION_ATTACHMENTS',)

from collections import deque as Deque
from os.path import split as split_path

from scarletio.web_common import FormData

from .....env import API_VERSION

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion
from ....utils import random_id

from ...attachment import Attachment
from ...attachment_request import (
    ATTACHMENT_REQUEST_ACTION_CREATE, ATTACHMENT_REQUEST_MASK_ACTION, ATTACHMENT_REQUEST_MASK_TYPE,
    ATTACHMENT_REQUEST_SHIFT_ACTION, ATTACHMENT_REQUEST_SHIFT_TYPE, ATTACHMENT_REQUEST_TYPE_VOICE, AttachmentRequest,
    attachment_request_copy_with_attachment_id, attachment_request_create_keep,
    attachment_request_create_regular_create, attachment_request_serialise
)
from ...message import MessageFlag


MESSAGE_FLAG_VOICE_MESSAGE = MessageFlag().update_by_keys(voice_message = True)


def _is_attachments(value):
    """
    Yields the outcome if the `value` is acceptable.
    
    This function is a generator.
    
    Parameters
    ----------
    value : ``None | Attachment | AttachmentRequest | (str, object) | (str, object, None | str), (list | Deque | dict)<...>``
        The value to check.
    
    Yields
    ------
    attachment_requests: ``None | list<AttachmentRequest>``
        The processed attachments.
    """
    # None
    if value is None:
        yield None
        return
    
    # tuple
    if isinstance(value, tuple):
        for attachment_request in _is_valid_tuple_attachment(value):
            yield [attachment_request]
        return
    
    # AttachmentRequest
    if isinstance(value, AttachmentRequest):
        yield [attachment_request_copy_with_attachment_id(value, 0)]
        return
    
    # Attachment
    if isinstance(value, Attachment):
        yield [attachment_request_create_keep(value.id)]
        return
    
    # list | Deque
    if isinstance(value, list) or isinstance(value, Deque):
        attachment_requests = None
        attachment_index = 0
        
        for element in value:
            for attachment_request in _is_single_attachment(element):
                break
            else:
                return
            
            if (
                ((attachment_request.attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_ACTION) & ATTACHMENT_REQUEST_MASK_ACTION)
                == ATTACHMENT_REQUEST_ACTION_CREATE
            ):
                if attachment_request.attachment_id != attachment_index:
                    attachment_request = attachment_request_copy_with_attachment_id(
                        attachment_request, attachment_index
                    )
                attachment_index += 1
            
            if attachment_requests is None:
                attachment_requests = []
            
            attachment_requests.append(attachment_request)
            continue
        
        yield attachment_requests
        return
    
    # dict-like
    if hasattr(type(value), 'items'):
        attachment_requests = None
        attachment_index = 0
        
        for item in value.items():
            attachment_request = attachment_request_create_regular_create(*item)
            
            if (
                ((attachment_request.attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_ACTION) & ATTACHMENT_REQUEST_MASK_ACTION)
                == ATTACHMENT_REQUEST_ACTION_CREATE
            ):
                if attachment_request.attachment_id != attachment_index:
                    attachment_request = attachment_request_copy_with_attachment_id(
                        attachment_request, attachment_index
                    )
                attachment_index += 1
            
            if attachment_requests is None:
                attachment_requests = []
            
            attachment_requests.append(attachment_request)
        
        yield attachment_requests
        return
    
    # rest
    yield [attachment_request_create_regular_create(_get_or_create_io_name(value), value)]
    return


def _is_single_attachment(value):
    """
    Yields the outcome if the `value` is acceptable.
    
    This function is a generator.
    
    Parameters
    ----------
    value : ``Attachment | AttachmentRequest | (str, object) | (str, object, None | str)``
        The value to check.
    
    Yields
    ------
    attachment_request : ``AttachmentRequest``
        The processed attachment.
    """
    if isinstance(value, tuple):
        yield from _is_valid_tuple_attachment(value)
        return
    
    if isinstance(value, AttachmentRequest):
        yield value
        return
    
    if isinstance(value, Attachment):
        yield attachment_request_create_keep(value.id)
        return
    
    yield attachment_request_create_regular_create(_get_or_create_io_name(value), value)
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
    name : `str`
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
    value : `(str, object) | (str, object, None | str)`
        The value to check.
    
    Yields
    ------
    attachment_request : ``AttachmentRequest``
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
    
    yield attachment_request_create_regular_create(name, io, description = description)


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
            if value is None:
                attachment_datas = None
            
            else:
                attachment_datas = [
                    attachment_request_serialise(attachment_request) for attachment_request in value
                ]
            
            if (not required) and (attachment_datas is None):
                return data
            
            if attachment_datas is None:
                data['attachments'] = []
            else:
                data['attachments'] = attachment_datas
            
            if (value is None) or all(
                (
                    (attachment_request.attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_ACTION) & ATTACHMENT_REQUEST_MASK_ACTION
                    != ATTACHMENT_REQUEST_ACTION_CREATE
                )
                for attachment_request in value
            ):
                return data
            
            # Check whether we are creating a voice attachment message.
            while True:
                # It can have only 1 attachment.
                if len(value) != 1:
                    break
                
                # It must be a new attachment.
                attachment_request = value[0]
                if (
                    (attachment_request.attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_ACTION) & ATTACHMENT_REQUEST_MASK_ACTION
                    != ATTACHMENT_REQUEST_ACTION_CREATE
                ):
                    break
                
                # It must be a voice attachment.
                if (
                    (attachment_request.attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_TYPE) & ATTACHMENT_REQUEST_MASK_TYPE
                    != ATTACHMENT_REQUEST_TYPE_VOICE
                ):
                    break
                
                # It must not have content fields.
                if (
                    ('content' in data) or
                    ('embed' in data) or
                    ('components' in data) or
                    ('poll' in data)
                ):
                    break
                
                data['flags'] = data.get('flags', 0) | MESSAGE_FLAG_VOICE_MESSAGE
                break
            
            form = FormData()
            form.add_json('payload_json', data)
            
            for attachment_request in value:
                if (
                    ((attachment_request.attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_ACTION) & ATTACHMENT_REQUEST_MASK_ACTION)
                    != ATTACHMENT_REQUEST_ACTION_CREATE
                ):
                    continue
                
                form.add_field(
                    f'files[{attachment_request.attachment_id}]',
                    attachment_request.io,
                    file_name = attachment_request.name,
                    content_type = 'application/octet-stream',
                )
            
            return form
    
    else:
        def serializer_putter(data, required, value):
            if value is None:
                return data
            
            file_attachments = [
                attachment_request_serialise(attachment_request) for attachment_request in value
                if  (
                    (attachment_request.attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_ACTION) & ATTACHMENT_REQUEST_MASK_ACTION
                    == ATTACHMENT_REQUEST_ACTION_CREATE
                )
            ]
            if not file_attachments:
                return data
            
            form = FormData()
            form.add_json('payload_json', data)
            
            if len(file_attachments) == 1:
                attachment_request = file_attachments[0]
                form.add_field(
                    'file',
                    attachment_request.io,
                    file_name = attachment_request.name,
                    content_type = 'application/octet-stream',
                )
            else:
                for attachment_request in file_attachments:
                    form.add_field(
                        f'file{attachment_request.attachment_id}s',
                        attachment_request.id,
                        file_name = attachment_request.name,
                        content_type = 'application/octet-stream',
                    )
            
            return form
    
    
    # Sorting
    
    sort_priority = 9999
