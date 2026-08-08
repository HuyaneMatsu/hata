__all__ = (
    'attachment_request_copy_with_attachment_id', 'attachment_request_create_regular_create',
    'attachment_request_create_video_create', 'attachment_request_create_voice_create',
    'attachment_request_create_keep', 'attachment_request_create_regular_edit', 'attachment_request_create_video_edit',
    'attachment_request_create_voice_edit', 'attachment_request_serialise'
)

from .attachment_request import AttachmentRequest

from .constants import (
    ATTACHMENT_REQUEST_ACTION_CREATE, ATTACHMENT_REQUEST_ACTION_EDIT, ATTACHMENT_REQUEST_FIELD_DESCRIPTION,
    ATTACHMENT_REQUEST_FIELD_SPOILER, ATTACHMENT_REQUEST_MASK_ACTION, ATTACHMENT_REQUEST_MASK_FIELDS,
    ATTACHMENT_REQUEST_MASK_TYPE, ATTACHMENT_REQUEST_SHIFT_ACTION, ATTACHMENT_REQUEST_SHIFT_FIELDS,
    ATTACHMENT_REQUEST_SHIFT_TYPE, ATTACHMENT_REQUEST_TYPE_REGULAR, ATTACHMENT_REQUEST_TYPE_VIDEO,
    ATTACHMENT_REQUEST_TYPE_VOICE, ATTACHMENT_REQUEST_WAVEFORM_OGG_DEFAULT
)
from .fields import (
    put_description, put_duration, put_waveform, validate_description, validate_duration, validate_name,
    validate_waveform, validate_title, validate_spoiler, validate_attachment_id, put_attachment_id,
    put_spoiler, put_title
)


def attachment_request_create_regular_create(name, io, *, description = ..., spoiler = ..., title = ...):
    """
    Creates a new attachment request for regular attachment creation.
    
    Parameters
    ----------
    name : `str`
        The name of the attachment.
    
    io : `object`
        Data or stream to be sent.
    
    description : `None | str`, Optional (Keyword only)
        Description for the attachment.
    
    spoiler : `bool`, Optional (Keyword only)
        Whether the attachment should be spoilered.
    
    title : `None | str`
        The attachment's title. Exclude extension, can contain unicodes, used instead of name when given.
    
    Returns
    -------
    attachment_request : ``AttachmentRequest``
    """
    # name
    name = validate_name(name)
    
    # description
    if description is ...:
        description = None
    else:
        description = validate_description(description)
    
    # spoiler
    if spoiler is ...:
        spoiler = False
    else:
        spoiler = validate_spoiler(spoiler)
    
    # title
    if title is ...:
        title = None
    else:
        title = validate_title(title)
    
    # Construct
    attachment_request = object.__new__(AttachmentRequest)
    attachment_request.attachment_id = 0
    attachment_request.attachment_request_flags = (
        (ATTACHMENT_REQUEST_TYPE_REGULAR << ATTACHMENT_REQUEST_SHIFT_TYPE) |
        (ATTACHMENT_REQUEST_ACTION_CREATE << ATTACHMENT_REQUEST_SHIFT_ACTION)
    )
    attachment_request.attachment_id = 0
    attachment_request.description = description
    attachment_request.duration = 0.0
    attachment_request.io = io
    attachment_request.name = name
    attachment_request.spoiler = spoiler
    attachment_request.title = title
    attachment_request.waveform = None
    return attachment_request


def attachment_request_create_voice_create(name, io, duration, *, description = ..., waveform = ...):
    """
    Creates a new attachment request for voice attachment creation.
    
    Parameters
    ----------
    name : `str`
        The name of the attachment.
    
    io : `object`
        Data or stream to be sent.
    
    duration : `float`
        The attachment's duration in seconds.
    
    description : `None | str`, Optional (Keyword only)
        Description for the attachment.
    
    waveform : `None | bytes`, Optional (Keyword only)
        Represents a sampled waveform of the attached voice data.
    
    Returns
    -------
    attachment_request : ``AttachmentRequest``
    """
    # name
    name = validate_name(name)
    
    # duration
    duration = validate_duration(duration)
    
    # description
    if description is ...:
        description = None
    else:
        description = validate_description(description)
    
    # waveform
    if waveform is ...:
        waveform = None
    else:
        waveform = validate_waveform(waveform)
    
    # Post validate waveform.
    if waveform is None:
        if name.endswith('.ogg'):
            waveform = ATTACHMENT_REQUEST_WAVEFORM_OGG_DEFAULT
        
        else:
            raise ValueError(
                f'Could not interpret default `waveform` from `name` ({name!r}), please pass it manually.'
            )
    
    # Construct
    attachment_request = object.__new__(AttachmentRequest)
    attachment_request.attachment_id = 0
    attachment_request.attachment_request_flags = (
        (ATTACHMENT_REQUEST_TYPE_VOICE << ATTACHMENT_REQUEST_SHIFT_TYPE) |
        (ATTACHMENT_REQUEST_ACTION_CREATE << ATTACHMENT_REQUEST_SHIFT_ACTION)
    )
    attachment_request.attachment_id = 0
    attachment_request.description = description
    attachment_request.duration = duration
    attachment_request.io = io
    attachment_request.name = name
    attachment_request.spoiler = False
    attachment_request.title = None
    attachment_request.waveform = waveform
    return attachment_request


def attachment_request_create_video_create(name, io, duration, *, description = ...):
    """
    Creates a new attachment request for video attachment creation.
    
    Parameters
    ----------
    name : `str`
        The name of the attachment.
    
    io : `object`
        Data or stream to be sent.
    
    duration : `float`
        The attachment's duration in seconds.
    
    description : `None | str`, Optional (Keyword only)
        Description for the attachment.
    
    Returns
    -------
    attachment_request : ``AttachmentRequest``
    """
    # name
    name = validate_name(name)
    
    # duration
    duration = validate_duration(duration)
    
    # description
    if description is ...:
        description = None
    else:
        description = validate_description(description)
    
    # Construct
    attachment_request = object.__new__(AttachmentRequest)
    attachment_request.attachment_id = 0
    attachment_request.attachment_request_flags = (
        (ATTACHMENT_REQUEST_TYPE_VIDEO << ATTACHMENT_REQUEST_SHIFT_TYPE) |
        (ATTACHMENT_REQUEST_ACTION_CREATE << ATTACHMENT_REQUEST_SHIFT_ACTION)
    )
    attachment_request.attachment_id = 0
    attachment_request.description = description
    attachment_request.duration = duration
    attachment_request.io = io
    attachment_request.name = name
    attachment_request.spoiler = False
    attachment_request.title = None
    attachment_request.waveform = None
    return attachment_request



def attachment_request_create_regular_edit(attachment_id, *, description = ..., spoiler = ...):
    """
    Creates a new attachment request for regular attachment creation.
    
    Parameters
    ----------
    attachment_id : `int`
        The attachment's identifier to be edited.
    
    description : `None | str`, Optional (Keyword only)
        Description for the attachment.
    
    spoiler : `bool`, Optional (Keyword only)
        Whether the attachment should be spoilered.
    
    Returns
    -------
    attachment_request : ``AttachmentRequest``
    """
    field_flags = 0
    
    # attachment_id
    attachment_id = validate_attachment_id(attachment_id)
    
    # description
    if description is ...:
        description = None
    else:
        description = validate_description(description)
        field_flags |= (1 << ATTACHMENT_REQUEST_FIELD_DESCRIPTION)
    
    # spoiler
    if spoiler is ...:
        spoiler = False
    else:
        spoiler = validate_spoiler(spoiler)
        field_flags |= (1 << ATTACHMENT_REQUEST_FIELD_SPOILER)
    
    # Construct
    attachment_request = object.__new__(AttachmentRequest)
    attachment_request.attachment_id = 0
    attachment_request.attachment_request_flags = (
        (ATTACHMENT_REQUEST_TYPE_REGULAR << ATTACHMENT_REQUEST_SHIFT_TYPE) |
        (ATTACHMENT_REQUEST_ACTION_EDIT << ATTACHMENT_REQUEST_SHIFT_ACTION) |
        (field_flags << ATTACHMENT_REQUEST_SHIFT_FIELDS)
    )
    attachment_request.attachment_id = attachment_id
    attachment_request.description = description
    attachment_request.duration = 0.0
    attachment_request.io = None
    attachment_request.name = None
    attachment_request.spoiler = spoiler
    attachment_request.title = None
    attachment_request.waveform = None
    return attachment_request


def attachment_request_create_voice_edit(attachment_id, *, description = ...):
    """
    Creates a new attachment request for voice attachment creation.
    
    Parameters
    ----------
    attachment_id : `int`
        The attachment's identifier to be edited.
    
    description : `None | str`, Optional (Keyword only)
        Description for the attachment.
    
    Returns
    -------
    attachment_request : ``AttachmentRequest``
    """
    field_flags = 0
    
    # attachment_id
    attachment_id = validate_attachment_id(attachment_id)
    
    # description
    if description is ...:
        description = None
    else:
        description = validate_description(description)
        field_flags |= (1 << ATTACHMENT_REQUEST_FIELD_DESCRIPTION)
    
    # Construct
    attachment_request = object.__new__(AttachmentRequest)
    attachment_request.attachment_id = 0
    attachment_request.attachment_request_flags = (
        (ATTACHMENT_REQUEST_TYPE_VOICE << ATTACHMENT_REQUEST_SHIFT_TYPE) |
        (ATTACHMENT_REQUEST_ACTION_EDIT << ATTACHMENT_REQUEST_SHIFT_ACTION) |
        (field_flags << ATTACHMENT_REQUEST_SHIFT_FIELDS)
    )
    attachment_request.attachment_id = attachment_id
    attachment_request.description = description
    attachment_request.duration = 0.0
    attachment_request.io = None
    attachment_request.name = None
    attachment_request.spoiler = False
    attachment_request.title = None
    attachment_request.waveform = None
    return attachment_request


def attachment_request_create_video_edit(attachment_id, *, description = ...):
    """
    Creates a new attachment request for video attachment creation.
    
    Parameters
    ----------
    attachment_id : `int`
        The attachment's identifier to be edited.
    
    description : `None | str`, Optional (Keyword only)
        Description for the attachment.
    
    Returns
    -------
    attachment_request : ``AttachmentRequest``
    """
    field_flags = 0
    
    # attachment_id
    attachment_id = validate_attachment_id(attachment_id)
    
    # description
    if description is ...:
        description = None
    else:
        description = validate_description(description)
        field_flags |= (1 << ATTACHMENT_REQUEST_FIELD_DESCRIPTION)
    
    # Construct
    attachment_request = object.__new__(AttachmentRequest)
    attachment_request.attachment_id = 0
    attachment_request.attachment_request_flags = (
        (ATTACHMENT_REQUEST_TYPE_VOICE << ATTACHMENT_REQUEST_SHIFT_TYPE) |
        (ATTACHMENT_REQUEST_ACTION_EDIT << ATTACHMENT_REQUEST_SHIFT_ACTION) |
        (field_flags << ATTACHMENT_REQUEST_SHIFT_FIELDS)
    )
    attachment_request.attachment_id = attachment_id
    attachment_request.description = description
    attachment_request.duration = 0.0
    attachment_request.io = None
    attachment_request.name = None
    attachment_request.spoiler = False
    attachment_request.title = None
    attachment_request.waveform = None
    return attachment_request


def attachment_request_create_keep(attachment_id):
    """
    Creates a new attachment request for keeping an attachment.
    
    Parameters
    ----------
    attachment_id : `int`
        The attachment's identifier to be kept.
    
    Returns
    -------
    attachment_request : ``AttachmentRequest``
    """
    # attachment_id
    attachment_id = validate_attachment_id(attachment_id)
    
    # Construct
    attachment_request = object.__new__(AttachmentRequest)
    attachment_request.attachment_id = 0
    attachment_request.attachment_request_flags = (
        (ATTACHMENT_REQUEST_ACTION_EDIT << ATTACHMENT_REQUEST_SHIFT_ACTION)
    )
    attachment_request.attachment_id = attachment_id
    attachment_request.description = None
    attachment_request.duration = 0.0
    attachment_request.io = None
    attachment_request.name = None
    attachment_request.spoiler = False
    attachment_request.title = None
    attachment_request.waveform = None
    return attachment_request


def attachment_request_copy_with_attachment_id(attachment_request, attachment_id):
    """
    Copies the attachment request with the given identifier.
    
    Parameters
    ----------
    attachment_request : ``AttachmentRequest``
        Attachment request to copy.
    
    attachment_id : `int`
        Attachment identifier to use.
    """
    # Construct
    new = object.__new__(AttachmentRequest)
    new.attachment_id = attachment_id
    new.attachment_request_flags = attachment_request.attachment_request_flags
    new.attachment_id = attachment_id
    new.description = attachment_request.description
    new.duration = attachment_request.duration
    new.io = attachment_request.io
    new.name = attachment_request.name
    new.spoiler = attachment_request.spoiler
    new.title = attachment_request.title
    new.waveform = attachment_request.waveform
    return new
    

def attachment_request_serialise(attachment_request):
    """
    Serialises the attachment request.
    
    Parameters
    ----------
    attachment_request : ``AttachmentRequest``
        Instance to serialise.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data = {}
    put_attachment_id(attachment_request.attachment_id, data, False)
    
    attachment_request_flags = attachment_request.attachment_request_flags
    attachment_request_action = (
        (attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_ACTION) & ATTACHMENT_REQUEST_MASK_ACTION
    )
    
    if attachment_request_action == ATTACHMENT_REQUEST_ACTION_CREATE:
        attachment_request_type = (
            (attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_TYPE) & ATTACHMENT_REQUEST_MASK_TYPE
        )
        put_description(attachment_request.description, data, False)
        
        if attachment_request_type == ATTACHMENT_REQUEST_TYPE_REGULAR:
            put_spoiler(attachment_request.spoiler, data, False)
            put_title(attachment_request.title, data, False)
        
        elif attachment_request_type == ATTACHMENT_REQUEST_TYPE_VOICE:
            put_duration(attachment_request.duration, data, False)
            put_waveform(attachment_request.waveform, data, False)
        
        elif attachment_request_type == ATTACHMENT_REQUEST_TYPE_VIDEO:
            put_duration(attachment_request.duration, data, False)
    
        
    elif attachment_request_action == ATTACHMENT_REQUEST_ACTION_EDIT:
        attachment_request_fields = (
            (attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_FIELDS) & ATTACHMENT_REQUEST_MASK_FIELDS
        )
        if (attachment_request_fields >> ATTACHMENT_REQUEST_FIELD_DESCRIPTION) & 1:
            put_description(attachment_request.description, data, True)
        
        if (attachment_request_fields >> ATTACHMENT_REQUEST_FIELD_SPOILER) & 1:
            put_spoiler(attachment_request.spoiler, data, True)
    
    return data
