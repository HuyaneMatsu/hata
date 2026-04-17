__all__ = ('Attachment', )

from ...bases import DiscordEntity
from ...precreate_helpers import process_precreate_parameters_and_raise_extra

from .constants import DURATION_DEFAULT
from .fields import (
    parse_application, parse_clip_created_at, parse_clip_users, parse_content_type, parse_description, parse_duration,
    parse_flags, parse_height, parse_id, parse_name, parse_proxy_url, parse_size, parse_temporary, parse_title,
    parse_url, parse_waveform, parse_width, put_application, put_clip_created_at, put_clip_users,
    put_content_type, put_description, put_duration, put_flags, put_height, put_id,
    put_name, put_proxy_url, put_size, put_temporary, put_title, put_url,
    put_waveform, put_width, validate_application, validate_clip_created_at, validate_clip_users,
    validate_content_type, validate_description, validate_duration, validate_flags, validate_height, validate_id,
    validate_name, validate_proxy_url, validate_size, validate_temporary, validate_title, validate_url,
    validate_waveform, validate_width
)
from .flags import AttachmentFlag


PRECREATE_FIELDS = {
    'application': ('application', validate_application),
    'clip_created_at': ('clip_created_at', validate_clip_created_at),
    'clip_users': ('clip_users', validate_clip_users),
    'content_type': ('content_type', validate_content_type),
    'description': ('description', validate_description),
    'duration': ('duration', validate_duration),
    'flags': ('flags', validate_flags),
    'height': ('height', validate_height),
    'name': ('name', validate_name),
    'proxy_url': ('proxy_url', validate_proxy_url),
    'size': ('size', validate_size),
    'temporary': ('temporary', validate_temporary),
    'title': ('title', validate_title),
    'url': ('url', validate_url),
    'waveform': ('waveform', validate_waveform),
    'width': ('width', validate_width),
}


class Attachment(DiscordEntity):
    """
    Represents an attachment of a ``Message``.
    
    Attributes
    ----------
    application : ``None | Application``
        The application in the attachment if recognized. (Only for clips for now.)
    
    clip_created_at : `None | DateTime`
        When the clip was created. Applicable if the attachment is a clip.
    
    clip_users : ``None | tuple<ClientUserBase>``
        The users in the clip. Applicable if the attachment is a clip.
    
    content_type : `None | str`
        The attachment's media type.
    
    description : `None | str`
        Description for the attachment.
        
        > Max 1024 characters.
    
    duration : `float`
        The attachment's duration in seconds. Applicable for voice messages only.
        
        > Defaults to `0.0`.
    
    flags : ``AttachmentFlag``
        Flags of the attachment.
    
    height : `int`
        The height of the attachment if applicable.
        
        > Defaults to `0`.
    
    id : `int`
        The unique identifier number of the attachment.
    
    name : `str`
        The name of the attachment.
        Special and unicode characters are excluded from an attachment's name.
    
    proxy_url : `str`
        Proxied url of the attachment.
    
    size : `int`
        The attachment's size in bytes.
    
    temporary : `bool`
        Whether the attachment is temporary and is removed after a set period of time.
        
        Temporary attachments are guaranteed to be available as long as their message itself exists.
        
        > Defaults to `False`.
    
    title : `None | str`
        The attachment's title.
        Present if any characters were excluded from ``.name``.
    
    url : `str`
        The attachment's url.
    
    waveform : `None | bytes`
        Represents a sampled waveform of the attached voice data. Applicable for voice messages only.
        
        > Defaults to `None`.
    
    width : `int`
        The attachment's width if applicable.
        
        > Defaults to `0`.
    """
    __slots__ = (
        'application', 'clip_created_at', 'clip_users', 'content_type', 'description', 'duration', 'flags', 'height',
        'name', 'proxy_url', 'size', 'temporary', 'title', 'url', 'waveform', 'width'
    )
    
    def __new__(
        cls,
        *,
        application = ...,
        clip_created_at = ...,
        clip_users = ...,
        content_type = ...,
        description = ...,
        duration = ...,
        flags = ...,
        height = ...,
        name = ...,
        size = ...,
        temporary = ...,
        title = ...,
        url = ...,
        waveform = ...,
        width = ...,
    ):
        """
        Creates a new partial attachment.
        
        Parameters
        ----------
        application : ``None | Application``, Optional (Keyword only)
            The application in the attachment if recognized.
        
        clip_created_at : `None | DateTime`, Optional (Keyword only)
            When the clip was created. Applicable if the attachment is a clip.
        
        clip_users : `None | iterable<ClientUserBase>`, Optional (Keyword only)
            The users in the clip. Applicable if the attachment is a clip.
        
        content_type : `None | str`, Optional (Keyword only)
            The attachment's media type.
        
        description : `None | str`, Optional (Keyword only)
            Description for the attachment.
        
        duration : `float`, Optional (Keyword only)
            The attachment's duration in seconds.
        
        flags : ``AttachmentFlag``, `int`, Optional (Keyword only)
            The attachment's flags.
        
        height : `int`, Optional (Keyword only)
            The height of the attachment if applicable.
        
        name : `str`, Optional (Keyword only)
            The name of the attachment.
        
        size : `int`, Optional (Keyword only)
            The attachment's size in bytes.
        
        temporary : `bool`, Optional (Keyword only)
            Whether the attachment is temporary and is removed after a set period of time.
        
        title : `None | str`, Optional (Keyword only)
            The attachment's title.
        
        url : `str`, Optional (Keyword only)
            The attachment's url.
        
        waveform : `None | bytes`, Optional (Keyword only)
            Represents a sampled waveform of the attached voice data.
        
        width : `int`, Optional (Keyword only)
            The attachment's width if applicable.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # application
        if application is ...:
            application = None
        else:
            application = validate_application(application)
        
        # clip_created_at
        if clip_created_at is ...:
            clip_created_at = None
        else:
            clip_created_at = validate_clip_created_at(clip_created_at)
        
        # clip_users
        if clip_users is ...:
            clip_users = None
        else:
            clip_users = validate_clip_users(clip_users)
        
        # content_type
        if content_type is ...:
            content_type = None
        else:
            content_type = validate_content_type(content_type)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # duration
        if duration is ...:
            duration = DURATION_DEFAULT
        else:
            duration = validate_duration(duration)
        
        # flags
        if flags is ...:
            flags = AttachmentFlag()
        else:
            flags = validate_flags(flags)
        
        # height
        if height is ...:
            height = 0
        else:
            height = validate_height(height)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # size
        if size is ...:
            size = 0
        else:
            size = validate_size(size)
        
        # temporary
        if temporary is ...:
            temporary = False
        else:
            temporary = validate_temporary(temporary)
        
        # title
        if title is ...:
            title = None
        else:
            title = validate_title(title)
        
        # url
        if url is ...:
            url = ''
        else:
            url = validate_url(url)
        
        # waveform
        if waveform is ...:
            waveform = None
        else:
            waveform = validate_waveform(waveform)
        
        # width
        if width is ...:
            width = 0
        else:
            width = validate_width(width)
        
        # Construct
        
        self = object.__new__(cls)
        self.application = application
        self.clip_created_at = clip_created_at
        self.clip_users = clip_users
        self.content_type = content_type
        self.description = description
        self.duration = duration
        self.flags = flags
        self.height = height
        self.id = 0
        self.name = name
        self.proxy_url = None
        self.size = size
        self.temporary = temporary
        self.title = title
        self.url = url
        self.waveform = waveform
        self.width = width
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates an attachment object from the attachment data included inside of a ``Message`'s.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received attachment data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.application = parse_application(data)
        self.clip_created_at = parse_clip_created_at(data)
        self.clip_users = parse_clip_users(data)
        self.content_type = parse_content_type(data)
        self.description = parse_description(data)
        self.duration = parse_duration(data)
        self.flags = parse_flags(data)
        self.height = parse_height(data)
        self.id = parse_id(data)
        self.name = parse_name(data)
        self.proxy_url = parse_proxy_url(data)
        self.size = parse_size(data)
        self.temporary = parse_temporary(data)
        self.title = parse_title(data)
        self.url = parse_url(data)
        self.waveform = parse_waveform(data)
        self.width = parse_width(data)
        return self
    
    
    def __repr__(self):
        """Returns the representation of the attachment."""
        repr_parts = ['<', type(self).__name__,]
        
        attachment_id = self.id
        if attachment_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(attachment_id))
            
            if self.temporary:
                repr_parts.append(' (temporary)')
            
            repr_parts.append(',')
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        # If has title
        title = self.title
        if (title is not None):
            repr_parts.append(', title = ')
            repr_parts.append(repr(title))
        
        # Extra if audio
        duration = self.duration
        if duration:
            repr_parts.append(', duration = ')
            repr_parts.append(format(duration, '.02f'))
        
        # Extra if image
        width = self.width
        height = self.height
        if width and height:
            repr_parts.append(', size = ')
            repr_parts.append(repr(width))
            repr_parts.append('x')
            repr_parts.append(repr(height))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two attachments are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # shortcut
        if self is other:
            return True
        
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            # Only compare `.id` and `.proxy_url` if both attachment is not partial.
            
            # id
            if self.id != other.id:
                return False
            
            # proxy_url
            if self.proxy_url != other.proxy_url:
                return False
        
        # application
        if self.application != other.application:
            return False
        
        # clip_created_at
        if self.clip_created_at != other.clip_created_at:
            return False
        
        # clip_users
        if self.clip_users != other.clip_users:
            return False
        
        # content_type
        if self.content_type != other.content_type:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # duration
        if self.duration != other.duration:
            return False
        
        # flags
        if self.flags != other.flags:
            return False
        
        # height
        if self.height != other.height:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # size
        if self.size != other.size:
            return False
        
        # temporary
        if self.temporary != other.temporary:
            return False
        
        # title
        if self.title != other.title:
            return False
        
        # url
        if self.url != other.url:
            return False
        
        # waveform
        if self.waveform != other.waveform:
            return False
        
        # width
        if self.width != other.width:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the attachment."""
        hash_value = 0
        
        # application
        application = self.application
        if (application is not None):
            hash_value ^= hash(application)
        
        # clip_created_at
        clip_created_at = self.clip_created_at
        if (clip_created_at is not None):
            hash_value ^= hash(clip_created_at)
        
        # clip_users
        clip_users = self.clip_users
        if (clip_users is not None):
            hash_value ^= len(clip_users) << 16
            for clip_user in clip_users:
                hash_value ^= hash(clip_user)
        
        # content_type
        content_type = self.content_type
        if (content_type is not None):
            hash_value ^= hash(content_type)
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # duration
        duration = self.duration
        if duration:
            hash_value ^= hash(duration)
        
        # flags
        hash_value ^= self.flags << 3
        
        # height
        hash_value ^= self.height
        
        # id
        attachment_id = self.id
        if attachment_id:
            hash_value ^= attachment_id
            
            # proxy_url
            # Add proxy url to hash only if we have attachment id.
            proxy_url = self.proxy_url
            if (proxy_url is not None):
                hash_value ^= hash(proxy_url)
        
        # name
        name = self.name
        if (description is None) or (name != description):
            hash_value ^= hash(name)
        
        # size
        hash_value ^= self.size << 17
        
        # temporary
        hash_value ^= self.temporary << 16
        
        # title
        title = self.title
        if (title is not None):
            hash_value ^= hash(title)
        
        # url
        hash_value ^= hash(self.url)
        
        # waveform
        waveform = self.waveform
        if (waveform is not None):
            hash_value ^= hash(waveform)
        
        # width
        hash_value ^= self.width << 8
        
        return hash_value
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Tries to convert the attachment back to json serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_application(self.application, data, defaults)
        put_clip_created_at(self.clip_created_at, data, defaults)
        put_clip_users(self.clip_users, data, defaults)
        put_content_type(self.content_type, data, defaults)
        put_description(self.description, data, defaults)
        put_duration(self.duration, data, defaults)
        put_flags(self.flags, data, defaults)
        put_height(self.height, data, defaults)
        put_name(self.name, data, defaults)
        put_size(self.size, data, defaults)
        put_temporary(self.temporary, data, defaults)
        put_title(self.title, data, defaults)
        put_url(self.url, data, defaults)
        put_waveform(self.waveform, data, defaults)
        put_width(self.width, data, defaults)
        
        if include_internals:
            put_id(self.id, data, defaults)
            put_proxy_url(self.proxy_url, data, defaults)
        
        return data
    
    
    def copy(self):
        """
        Returns a copy of the attachment.
        
        > The copy will not include the internal fields of it.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.application = self.application
        new.clip_created_at = self.clip_created_at
        
        clip_users = self.clip_users
        if (clip_users is not None):
            clip_users = (*clip_users,)
        new.clip_users = clip_users
        
        new.content_type = self.content_type
        new.description = self.description
        new.duration = self.duration
        new.flags = self.flags
        new.height = self.height
        new.id = 0
        new.name = self.name
        new.proxy_url = None
        new.size = self.size
        new.temporary = self.temporary
        new.title = self.title
        new.url = self.url
        new.waveform = self.waveform
        new.width = self.width
        return new
    
    
    def copy_with(
        self,
        *,
        application = ...,
        clip_created_at = ...,
        clip_users = ...,
        content_type = ...,
        description = ...,
        duration = ...,
        flags = ...,
        height = ...,
        name = ...,
        size = ...,
        temporary = ...,
        title = ...,
        url = ...,
        waveform = ...,
        width = ...,
    ):
        """
        Returns a copy of the attachment. The attributes of the copy are modified based on the given values.
        
        > The copy will not include the internal fields of it.
        
        Parameters
        ----------
        application : ``None | Application``, Optional (Keyword only)
            The application in the attachment if recognized.
        
        clip_created_at : `None | DateTime`, Optional (Keyword only)
            When the clip was created. Applicable if the attachment is a clip.
        
        clip_users : `None | iterable<ClientUserBase>`, Optional (Keyword only)
            The users in the clip. Applicable if the attachment is a clip.
        
        content_type : `None | str`, Optional (Keyword only)
            The attachment's media type.
        
        description : `None | str`, Optional (Keyword only)
            Description for the attachment.
        
        duration : `float`, Optional (Keyword only)
            The attachment's duration in seconds.
        
        flags : ``AttachmentFlag``, `int`, Optional (Keyword only)
            The attachment's flags.
        
        height : `int`, Optional (Keyword only)
            The height of the attachment if applicable.
        
        name : `str`, Optional (Keyword only)
            The name of the attachment.
        
        size : `int`, Optional (Keyword only)
            The attachment's size in bytes.
        
        temporary : `bool`, Optional (Keyword only)
            Whether the attachment is temporary and is removed after a set period of time.
        
        title : `None | str`, Optional (Keyword only)
            The attachment's title.
        
        url : `str`, Optional (Keyword only)
            The attachment's url.
        
        waveform : `None | bytes`, Optional (Keyword only)
            Represents a sampled waveform of the attached voice data.
        
        width : `int`, Optional (Keyword only)
            The attachment's width if applicable.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        # application
        if application is ...:
            application = self.application
        else:
            application = validate_application(application)
        
        # clip_created_at
        if clip_created_at is ...:
            clip_created_at = self.clip_created_at
        else:
            clip_created_at = validate_clip_created_at(clip_created_at)
        
        # clip_users
        if clip_users is ...:
            clip_users = self.clip_users
            if (clip_users is not None):
                clip_users = (*clip_users,)
        else:
            clip_users = validate_clip_users(clip_users)
        
        # content_type
        if content_type is ...:
            content_type = self.content_type
        else:
            content_type = validate_content_type(content_type)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # duration
        if duration is ...:
            duration = self.duration
        else:
            duration = validate_duration(duration)
        
        # flags
        if flags is ...:
            flags = self.flags
        else:
            flags = validate_flags(flags)
        
        # height
        if height is ...:
            height = self.height
        else:
            height = validate_height(height)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # size
        if size is ...:
            size = self.size
        else:
            size = validate_size(size)
        
        # temporary
        if temporary is ...:
            temporary = self.temporary
        else:
            temporary = validate_temporary(temporary)
        
        # title
        if title is ...:
            title = self.title
        else:
            title = validate_title(title)
        
        # url
        if url is ...:
            url = self.url
        else:
            url = validate_url(url)
        
        # waveform
        if waveform is ...:
            waveform = self.waveform
        else:
            waveform = validate_waveform(waveform)
        
        # width
        if width is ...:
            width = self.width
        else:
            width = validate_width(width)
        
        # Construct
        
        new = object.__new__(type(self))
        new.application = application
        new.clip_created_at = clip_created_at
        new.clip_users = clip_users
        new.content_type = content_type
        new.description = description
        new.duration = duration
        new.flags = flags
        new.height = height
        new.id = 0
        new.name = name
        new.proxy_url = None
        new.size = size
        new.temporary = temporary
        new.title = title
        new.url = url
        new.waveform = waveform
        new.width = width
        return new
    
    
    @classmethod
    def precreate(
        cls,
        attachment_id,
        **keyword_parameters,
    ):
        """
        Precreates an attachment. Since attachments are not cached, this method just a ``.__new__`` alternative.
        
        Parameters
        ----------
        attachment_id : `int`
            The attachment's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional parameters defining how the attachment's fields should be set.
        
        Other Parameters
        ----------------
        application : ``None | Application``, Optional (Keyword only)
            The application in the attachment if recognized.
        
        clip_created_at : `None | DateTime`, Optional (Keyword only)
            When the clip was created. Applicable if the attachment is a clip.
        
        clip_users : `None | iterable<ClientUserBase>`, Optional (Keyword only)
            The users in the clip. Applicable if the attachment is a clip.
        
        content_type : `None | str`, Optional (Keyword only)
            The attachment's media type.
        
        description : `None | str`, Optional (Keyword only)
            Description for the attachment.
        
        duration : `float`, Optional (Keyword only)
            The attachment's duration in seconds.
        
        flags : ``AttachmentFlag``, `int`, Optional (Keyword only)
            The attachment's flags.
        
        height : `int`, Optional (Keyword only)
            The height of the attachment if applicable.
        
        name : `str`, Optional (Keyword only)
            The name of the attachment.
        
        size : `int`, Optional (Keyword only)
            The attachment's size in bytes.
        
        proxy_url : `None | str`, Optional (Keyword only)
            Proxied url of the attachment.
        
        temporary : `bool`, Optional (Keyword only)
            Whether the attachment is temporary and is removed after a set period of time.
        
        title : `None | str`, Optional (Keyword only)
            The attachment's title.
            
        url : `str`, Optional (Keyword only)
            The attachment's url.
        
        waveform : `None | bytes`, Optional (Keyword only)
            Represents a sampled waveform of the attached voice data.
        
        width : `int`, Optional (Keyword only)
            The attachment's width if applicable.
        
        Returns
        -------
        self : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        attachment_id = validate_id(attachment_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        
        else:
            processed = None
        
        # Construct
        
        self = object.__new__(cls)
        self.application = None
        self.clip_created_at = None
        self.clip_users = None
        self.content_type = None
        self.description = None
        self.duration = DURATION_DEFAULT
        self.flags = AttachmentFlag()
        self.height = 0
        self.id = attachment_id
        self.name = ''
        self.proxy_url = None
        self.size = 0
        self.temporary = False
        self.title = None
        self.url = ''
        self.waveform = None
        self.width = 0
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    @property
    def display_name(self):
        """
        Returns the displayed name of the attachment.
        
        Displayed name is not the upload name, but something hata tries to construct to imitate it as close as possible.
        `attachment.name` do not include unicodes and `attachment.title` that was added to address this issue is
        not including the extension. So if there are any unicodes in extension they are omitted.
        To make this worse, uploaded attachment through interaction commands do not even have `.title`.
        
        Include a lot of cursing in this section.
        
        Returns
        -------
        display_name : `str`
        """
        title = self.title
        name = self.name
        
        if (title is None):
            return name
        
        extension_dot_index = name.find('.')
        if extension_dot_index == -1:
            return title
        
        return title + name[extension_dot_index:]
    
    
    @property
    def content_created_at(self):
        """
        Returns when the attachment's content was created if known.
        
        Returns
        -------
        modified_at : `DateTime`
        """
        content_created_at = self.clip_created_at
        if (content_created_at is not None):
            return content_created_at
        
        return self.created_at
    
    
    def iter_clip_users(self):
        """
        Iterates over the users in the clip. Applicable if the attachment is a clip.
        
        This method is an iterable generator.
        
        Yields
        ------
        clip_user : ``ClientUserBase``
        """
        clip_users = self.clip_users
        if (clip_users is not None):
            yield from clip_users
