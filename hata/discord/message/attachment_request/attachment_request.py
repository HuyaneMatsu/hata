__all__ = ('AttachmentRequest',)

from scarletio import RichAttributeErrorBaseType

from .constants import (
    ATTACHMENT_REQUEST_ACTION_CREATE, ATTACHMENT_REQUEST_ACTION_EDIT, ATTACHMENT_REQUEST_FIELD_DESCRIPTION,
    ATTACHMENT_REQUEST_FIELD_SPOILER, ATTACHMENT_REQUEST_MASK_ACTION, ATTACHMENT_REQUEST_MASK_FIELDS,
    ATTACHMENT_REQUEST_MASK_TYPE, ATTACHMENT_REQUEST_SHIFT_ACTION, ATTACHMENT_REQUEST_SHIFT_FIELDS,
    ATTACHMENT_REQUEST_SHIFT_TYPE, ATTACHMENT_REQUEST_TYPE_REGULAR, ATTACHMENT_REQUEST_TYPE_VIDEO,
    ATTACHMENT_REQUEST_TYPE_VOICE
)


class AttachmentRequest(RichAttributeErrorBaseType):
    """
    Voice attachment to be attachable to a message.
    
    Attributes
    ----------
    attachment_id : `int`
        The attachment's identifier at the case of modification.
    
    attachment_request_flags : `int`
        Flags used to store additional information about the request.
    
    description : `None | str`
        Description for the attachment.
    
    duration : `float`
        The attachment's duration in seconds for voice and video attachments.
    
    io : `None | object`
        Data or stream to be sent.
    
    name : `None | str`
        The name of the attachment.
    
    spoiler : `bool`
        Whether the attachment is spoilered.
    
    title : `None | str`
        The attachment's title. Exclude extension, can contain unicodes, used instead of name when given.
    
    waveform : `None | bytes`
        Represents a sampled waveform of the attached voice data.
    """
    __slots__ = (
        'attachment_id', 'attachment_request_flags', 'description', 'duration', 'io', 'name', 'spoiler', 'title',
        'waveform'
    )
    
    def __new__(
        cls, attachment_request_flags, attachment_id, io, name, title, description, spoiler, duration, waveform
    ):
        """
        Creates a new attachment request.
        
        Parameters
        ----------
        attachment_request_flags : `int`
            Flags used to store additional information about the request.
        
        attachment_id : `int`
            The attachment's identifier at the case of modification.
        
        io : `None | object`
            Data or stream to be sent.
        
        name : `None | str`
            The name of the attachment.
        
        title : `None | str`
            The attachment's title. Exclude extension, can contain unicodes, used instead of name when given.
        
        description : `None | str`
            Description for the attachment.
        
        spoiler : `bool`
            Whether the attachment is spoilered.
        
        duration : `float`
            The attachment's duration in seconds for voice and video attachments.
        
        waveform : `None | bytes`
            Represents a sampled waveform of the attached voice data.
        """
        self = object.__new__(cls)
        self.attachment_id = attachment_id
        self.attachment_request_flags = attachment_request_flags
        self.description = description
        self.duration = duration
        self.io = io
        self.name = name
        self.spoiler = spoiler
        self.title = title
        self.waveform = waveform
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # attachment_request_flags
        attachment_request_flags = self.attachment_request_flags
        repr_parts.append(' attachment_request_flags = ')
        repr_parts.append(repr(attachment_request_flags))
        repr_parts.append(' (')
        attachment_request_type = (
            (attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_TYPE) & ATTACHMENT_REQUEST_MASK_TYPE
        )
        if attachment_request_type == ATTACHMENT_REQUEST_TYPE_REGULAR:
            attachment_request_type_name = 'regular'
        elif attachment_request_type == ATTACHMENT_REQUEST_TYPE_VOICE:
            attachment_request_type_name = 'voice'
        elif attachment_request_type == ATTACHMENT_REQUEST_TYPE_VIDEO:
            attachment_request_type_name = 'video'
        else:
            attachment_request_type_name = 'unknown'
        repr_parts.append('type = ')
        repr_parts.append(attachment_request_type_name)
        
        attachment_request_action = (
            (attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_ACTION) & ATTACHMENT_REQUEST_MASK_ACTION
        )
        if attachment_request_action == ATTACHMENT_REQUEST_ACTION_CREATE:
            attachment_request_action_name = 'create'
        elif attachment_request_action == ATTACHMENT_REQUEST_ACTION_EDIT:
            attachment_request_action_name = 'edit'
        else:
            attachment_request_action_name = 'unknown'
        
        repr_parts.append('; action = ')
        repr_parts.append(attachment_request_action_name)
        
        if attachment_request_action == ATTACHMENT_REQUEST_ACTION_EDIT:
            attachment_request_fields = (
                (attachment_request_flags >> ATTACHMENT_REQUEST_SHIFT_FIELDS) & ATTACHMENT_REQUEST_MASK_FIELDS
            )
            if attachment_request_fields:
                repr_parts.append('; fields = ')
                
                if (attachment_request_fields >> ATTACHMENT_REQUEST_FIELD_DESCRIPTION) & 1:
                    repr_parts.append('description')
                    field_added = True
                else:
                    field_added = False
                
                if (attachment_request_fields >> ATTACHMENT_REQUEST_FIELD_SPOILER) & 1:
                    if field_added:
                        repr_parts.append(' + ')
                    repr_parts.append('spoiler')
        
        repr_parts.append(')')
        
        # attachment_id
        attachment_id = self.attachment_id
        if attachment_id:
            repr_parts.append(', attachment_id = ')
            repr_parts.append(repr(attachment_id))
        
        # description
        description = self.description
        if (description is not None):
            repr_parts.append(', description = ')
            repr_parts.append(repr(description))
        
        # duration
        duration = self.duration
        if duration:
            repr_parts.append(', duration = ')
            repr_parts.append(repr(duration))
        
        # io
        io = self.io
        if (io is not None):
            repr_parts.append(', io = ')
            repr_parts.append(repr(io))
        
        # name
        name = self.name
        if (name is not None):
            repr_parts.append(', name = ')
            repr_parts.append(repr(name))
        
        # spoiler
        spoiler = self.spoiler
        if spoiler:
            repr_parts.append(', spoiler = ')
            repr_parts.append(repr(spoiler))
        
        # title
        title = self.title
        if (title is not None):
            repr_parts.append(', title = ')
            repr_parts.append(repr(title))
        
        # waveform
        waveform = self.waveform
        if (waveform is not None):
            repr_parts.append(', waveform = ')
            repr_parts.append(repr(waveform))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)."""
        hash_value = 0
        
        # attachment_id
        hash_value ^= self.attachment_id
        
        # attachment_request_flags
        hash_value ^= self.attachment_request_flags
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # duration
        duration = self.duration
        if duration:
            hash_value ^= hash(duration)
        
        # io
        io = self.io
        if (io is not None):
            hash_value ^= hash(io)
        
        # name
        name = self.name
        if (name is not None):
            hash_value ^= hash(name)
        
        # spoiler
        hash_value ^= self.spoiler << 27
        
        # title
        title = self.title
        if (title is not None):
            hash_value ^= hash(title)
        
        # waveform
        waveform = self.waveform
        if (waveform is not None):
            hash_value ^= hash(waveform)
        
        return waveform
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        # attachment_id
        if self.attachment_id != other.attachment_id:
            return False
        
        # attachment_request_flags
        if self.attachment_request_flags != other.attachment_request_flags:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # duration
        if self.duration != other.duration:
            return False
        
        # io
        if self.io != other.io:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # spoiler
        if self.spoiler != other.spoiler:
            return False
        
        # title
        if self.title != other.title:
            return False
        
        # waveform
        if self.waveform != other.waveform:
            return False
        
        return True
