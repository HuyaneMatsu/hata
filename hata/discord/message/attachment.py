__all__ = ('Attachment', )

from ..bases import DiscordEntity

class Attachment(DiscordEntity):
    """
    Represents an attachment of a ``Message``.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the attachment.
    content_type : `None` or `str`
        The attachment's media type.
    description : `None` or `str`
        Description for the file.
    height : `int`
        The height of the attachment if applicable. Defaults to `0`.
    name : `str`
        The name of the attachment.
    proxy_url : `str`
        Proxied url of the attachment.
    size : `int`
        The attachment's size in bytes.
    temporary : `bool`
        Whether the attachment is temporary and is removed after a set period of time.
        
        Temporary attachments are guaranteed to be available as long as their message itself exists.
        
        Defaults to `False`.
    
    url : `str`
        The attachment's url.
    width : `int`
        The attachment's width if applicable. Defaults to `0`.
    """
    __slots__ = ('content_type', 'description', 'height', 'name', 'proxy_url', 'size', 'temporary', 'url', 'width')
    
    def __init__(self, data):
        """
        Creates an attachment object from the attachment data included inside of a ``Message`'s.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received attachment data.
        """
        self.name = data['filename']
        self.content_type = data.get('content_type', None)
        self.description = data.get('description', None)
        self.id = int(data['id'])
        self.proxy_url = data['proxy_url']
        self.size = data['size']
        self.url = data['url']
        self.height = data.get('height', 0)
        self.width = data.get('width', 0)
        self.temporary = data.get('ephemeral', False)
    
    
    def __repr__(self):
        """Returns the representation of the attachment."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' id=', repr(self.id),
        ]
        
        if self.temporary:
            repr_parts.append(' (temporary)')
        
        repr_parts.append(', name=')
        repr_parts.append(repr(self.name))
        
        width = self.width
        height = self.height
        if width and height:
            repr_parts.append(', size=')
            repr_parts.append(repr(width))
            repr_parts.append('x')
            repr_parts.append(repr(height))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def to_data(self):
        """
        Tries to convert the attachment back to json serializable dictionary.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`)
        """
        data = {}
        
        # id
        data['id'] = str(self.id)
        
        # content_type
        content_type = self.content_type
        if (content_type is not None):
            data['content_type'] = content_type
        
        # description
        description = self.description
        if (description is not None):
            data['description'] = description
        
        # height & width
        height = self.height
        width = self.width
        if width and height:
            data['width'] = width
            data['height'] = height
        
        # name
        data['filename'] = self.name
        
        # proxy_url
        data['proxy_url'] = self.proxy_url
        
        # temporary
        if self.temporary:
            data['ephemeral'] = True
        
        # url
        data['url'] = self.url
        
        return data
