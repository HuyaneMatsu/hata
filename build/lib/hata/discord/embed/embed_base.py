__all__ = ('EXTRA_EMBED_TYPES', 'EmbedAuthor', 'EmbedBase', 'EmbedField', 'EmbedFooter', 'EmbedImage', 'EmbedProvider',
    'EmbedThumbnail', 'EmbedVideo', )

from datetime import datetime

from ..utils import url_cutter
from ..color import Color

EXTRA_EMBED_TYPES = frozenset(('application_news', 'article', 'gifv', 'image', 'link', 'tweet', 'video'))


class EmbedThumbnail:
    """
    Represents an embed's thumbnail.
    
    Attributes
    ----------
    height : `int`
        The height of the thumbnail. Defaults to `0`.
    proxy_url : `None` or `str`
        A proxied url of the thumbnail.
    url : `None` or `str`
        The url of the thumbnail.
    width : `int`
        The width of the thumbnail. Defaults to `0`.
    """
    __slots__ = ('height', 'proxy_url', 'url', 'width',)
    
    def __init__(self, url):
        """
        Creates an embed thumbnail with the given `url`.
        
        Parameters
        ----------
        url : `str`
            The url of the thumbnail. Can be http(s) or attachment.
        """
        self.url = url
        self.proxy_url = None
        self.height = 0
        self.width = 0
    
    
    def __len__(self):
        """Returns the embed thumbnail's contents' length."""
        return 0
    
    
    def __bool__(self):
        """Returns whether the embed thumbnail is not empty."""
        return (self.url is not None)
    
    
    def __repr__(self):
        """Returns the representation of the embed thumbnail."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' url=',
        ]
        
        url = self.url
        if url is None:
            repr_parts.append('None')
        else:
            repr_parts.append('\'')
            url = url_cutter(url)
            repr_parts.append(url)
            repr_parts.append('\'')
        
        repr_parts.append(', size=')
        repr_parts.append(str(self.width))
        repr_parts.append('x')
        repr_parts.append(str(self.height))
    
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two embed thumbnails are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.url == other.url)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a embed thumbnail object from the data sent by Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embed thumbnail data received from Discord.
        
        Returns
        -------
        embed_thumbnail : ``EmbedThumbnail``
        """
        self = object.__new__(cls)
        self.url = data.get('url', None)
        self.proxy_url = data.get('proxy_url', None)
        self.height = data.get('height', 0)
        self.width = data.get('width', 0)
        
        return self
    
    
    def to_data(self):
        """
        Converts the embed thumbnail to json serializable `dict` representing it.
        
        Returns
        -------
        thumbnail_data : `dict` of (`str`, `Any`) items
        """
        return {
            'url' : self.url,
        }
    
    def copy(self):
        """
        Copies the ``EmbedThumbnail`` returning a new one.
        
        Returns
        -------
        new : ``EmbedThumbnail``
        """
        new = object.__new__(type(self))
        
        new.url = self.url
        new.proxy_url = None
        new.height = 0
        new.width = 0
        
        return self
    
    
    def copy_with(self, *, url=...):
        """
        Copies the ``EmbedThumbnail`` and updates it with the given parameters.
        
        Parameters
        ----------
        url : `str`, Optional (Keyword only)
            The url of the thumbnail. Can be http(s) or attachment.
        
        Returns
        -------
        new : ``EmbedThumbnail``
        """
        if url is ...:
            url = self.url
        
        new = object.__new__(type(self))
        new.url = url
        new.proxy_url = None
        new.height = 0
        new.width = 0
        
        return self


class EmbedVideo:
    """
    Represents an embed's video.
    
    Embed videos cannot be sent, they are receive only.
    
    Attributes
    ----------
    height : `int`
        The height of the video. Defaults to `0`.
    proxy_url : `None` or `str`
        A proxied url of the video.
    url : `None` or `str`
        The url of the video.
    width : `int`
        The width of the video. Defaults to `0`.
    """
    __slots__ = ('height', 'proxy_url', 'url', 'width',)
    
    def __init__(self):
        """
        Creates a new embed video object. Because embed videos cannot be sent, it accepts no parameters and just creates
        an empty embed video object with default attributes.
        """
        self.url = None
        self.proxy_url = None
        self.height = 0
        self.width = 0
    
    
    def __len__(self):
        """Returns the embed video's contents' length."""
        return 0
    
    
    def __bool__(self):
        """Returns whether the embed video is not empty."""
        return (self.url is not None)
    
    
    def __repr__(self):
        """Returns the representation of the embed video."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' url=',
        ]
        
        url = self.url
        if url is None:
            repr_parts.append('None')
        else:
            repr_parts.append('\'')
            url = url_cutter(url)
            repr_parts.append(url)
            repr_parts.append('\'')
        
        repr_parts.append(', size=')
        repr_parts.append(str(self.width))
        repr_parts.append('x')
        repr_parts.append(str(self.height))
    
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two embed videos are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.url == other.url)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates an embed video object from the data sent by Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embed video data received from Discord.
        
        Returns
        -------
        embed_video : ``EmbedVideo``
        """
        self = object.__new__(cls)
        self.url = data.get('url', None)
        self.proxy_url = data.get('proxy_url', None)
        self.height = data.get('height', 0)
        self.width = data.get('width', 0)
        
        return self
    
    
    def to_data(self):
        """
        Converts the embed video to json serializable `dict` representing it.
        
        Because embed videos cannot be sent, it always returns an empty `dict`.
        
        Returns
        -------
        video_data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def copy(self):
        """
        Copies the ``EmbedVideo`` returning a new one.
        
        > Since embed videos are receive only, the method will return the instance itself.
        
        Returns
        -------
        new : ``EmbedVideo``
        """
        return self
    
    
    def copy_with(self):
        """
        Copies the ``EmbedVideo`` and updates it with the given parameters.
        
        > Since embed videos are receive only, the method will return the instance itself.
        
        Returns
        -------
        new : ``EmbedVideo``
        """
        return self


class EmbedImage:
    """
    Represents an embed's image.
    
    Attributes
    ----------
    height : `int`
        The height of the image. Defaults to `0`.
    proxy_url : `None` or `str`
        A proxied url of the image.
    url : `None` or `str`
        The url of the image.
    width : `int`
        The width of the image. Defaults to `0`.
    """
    __slots__ = ('height', 'proxy_url', 'url', 'width',)
    
    def __init__(self, url):
        """
        Creates an embed image with the given `url`.
        
        Parameters
        ----------
        url : `str`
            The url of the image. Can be http(s) or attachment.
        """
        self.url = url
        self.proxy_url = None
        self.height = 0
        self.width = 0
    
    
    def __len__(self):
        """Returns the embed image's contents' length."""
        return 0
    
    
    def __bool__(self):
        """Returns whether the embed image is not empty."""
        return (self.url is not None)
    
    
    def __repr__(self):
        """Returns the representation of the embed image."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' url=',
        ]
        
        url = self.url
        if url is None:
            repr_parts.append('None')
        else:
            repr_parts.append('\'')
            url = url_cutter(url)
            repr_parts.append(url)
            repr_parts.append('\'')
            
        repr_parts.append(', size=')
        repr_parts.append(str(self.width))
        repr_parts.append('x')
        repr_parts.append(str(self.height))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two embed images are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.url == other.url)
    
    
    @classmethod
    def from_data(cls,data):
        """
        Creates an embed image object from the data sent by Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embed image data received from Discord.
        
        Returns
        -------
        embed_image : ``EmbedImage``
        """
        self = object.__new__(cls)
        self.url = data.get('url', None)
        self.proxy_url = data.get('proxy_url', None)
        self.height = data.get('height', 0)
        self.width = data.get('width', 0)
        
        return self
    
    
    def to_data(self):
        """
        Converts the embed image to json serializable `dict` representing it.
        
        Returns
        -------
        image_data : `dict` of (`str`, `Any`) items
        """
        return {
            'url' : self.url,
        }
    

    def copy(self):
        """
        Copies the ``EmbedImage`` returning a new one.
        
        Returns
        -------
        new : ``EmbedImage``
        """
        new = object.__new__(type(self))
        
        new.url = self.url
        new.proxy_url = None
        new.height = 0
        new.width = 0
        
        return self
    
    
    def copy_with(self, *, url=...):
        """
        Copies the ``EmbedImage`` and updates it with the given parameters.
        
        Parameters
        ----------
        url : `str`, Optional (Keyword only)
            The url of the image. Can be http(s) or attachment.
        
        Returns
        -------
        new : ``EmbedImage``
        """
        if url is ...:
            url = self.url
        
        new = object.__new__(type(self))
        new.url = url
        new.proxy_url = None
        new.height = 0
        new.width = 0
        
        return self


class EmbedProvider:
    """
    Represents an embed's provider.
    
    Embed providers cannot be sent, they are receive only.
    
    Attributes
    ----------
    name : `None` or `str`
        The name of the provider.
    url : `None` or `str`
        The url of the provider.
    """
    __slots__ = ('name', 'url',)
    
    def __init__(self):
        self.name = None
        self.url = None
    
    
    def __len__(self):
        """Returns the embed provider's contents' length."""
        name = self.name
        if name is None:
            return 0
        
        return len(name)
    
    
    def __bool__(self):
        """Returns whether the embed provider is not empty."""
        if (self.url is not None):
            return True
        
        name = self.name
        if (name is not None) and name:
            return True
        
        return False
    
    
    def __repr__(self):
        """Returns the representation of the embed provider."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' length=',
            str(len(self)),
            ', url='
        ]
        
        url = self.url
        if url is None:
            repr_parts.append('None')
        else:
            repr_parts.append('\'')
            url = url_cutter(url)
            repr_parts.append(url)
            repr_parts.append('\'')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two embed providers are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.name != other.name:
            return False
        
        if self.url != other.url:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new embed provider object. Because embed providers cannot be sent, it accepts no parameters and just
        creates an empty embed provider object with default attributes.
        
        Returns
        -------
        self : ``EmbedProvider``
        """
        self = object.__new__(cls)
        self.name = data.get('name', None)
        self.url = data.get('url', None)
        
        return self
    
    
    def to_data(self):
        """
        Converts the embed provider to json serializable `dict` representing it.
        
        Because embed provider cannot be sent, it always returns an empty `dict`.
        
        Returns
        -------
        provider_data : `dict` of (`str`, `Any`) items
        """
        return {}


    def copy(self):
        """
        Copies the ``EmbedProvider`` returning a new one.
        
        > Since embed providers are receive only, the method will return the instance itself.
        
        Returns
        -------
        new : ``EmbedProvider``
        """
        return self
    
    
    def copy_with(self):
        """
        Copies the ``EmbedProvider`` and updates it with the given parameters.
        
        > Since embed providers are receive only, the method will return the instance itself.
        
        Returns
        -------
        new : ``EmbedProvider``
        """
        return self


class EmbedAuthor:
    """
    Represents an embed's author.
    
    Attributes
    ----------
    icon_url : `None` or `str`
        Url of the author's icon.
    name : `None` or `str`
        The name of the author.
    proxy_icon_url : `None` or `str`
        A proxied url to the url of the author's icon.
    url : `None` or `str`
        The url of the author.
    """
    __slots__ = ('icon_url', 'name', 'proxy_icon_url', 'url',)
    def __init__(self, icon_url=None, name=None, url=None):
        """
        Creates an embed author with the given parameters.
        
        Parameters
        ----------
        icon_url : `str`, Optional
            An url of the author's icon. Can be http(s) or attachment.
        name : `str`, Optional
            The name of the author.
        url : `str`, Optional
            The url of the author.
        """
        self.icon_url = icon_url
        self.name = name
        self.url = url
        self.proxy_icon_url = None
    
    
    def __len__(self):
        """Returns the embed author's contents' length."""
        name = self.name
        if name is None:
            return 0
        
        return len(name)
    
    
    def __bool__(self):
        """Returns whether the embed author is not empty."""
        name = self.name
        if (name is not None) and name:
            return True
        
        if (self.url is not None):
            return True
        
        if (self.icon_url is not None):
            return True
        
        return False
    
    
    def __repr__(self):
        """Returns the representation of the embed author."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' length=',
            str(len(self)),
            ', url='
        ]
        
        url = self.url
        if url is None:
            repr_parts.append('None')
        else:
            repr_parts.append('\'')
            url = url_cutter(url)
            repr_parts.append(url)
            repr_parts.append('\'')
        
        repr_parts.append(', icon_url=')
        icon_url = self.icon_url
        if icon_url is None:
            repr_parts.append('None')
        else:
            repr_parts.append('\'')
            icon_url = url_cutter(icon_url)
            repr_parts.append(icon_url)
            repr_parts.append('\'')
            
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def __eq__(self, other):
        """Returns whether the two embed authors are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.icon_url != other.icon_url:
            return False
        
        if self.name != other.name:
            return False
        
        if self.url != other.url:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates an embed author object from the data sent by Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embed author data received from Discord.
        
        Returns
        -------
        embed_author : ``EmbedAuthor``
        """
        self = object.__new__(cls)
        self.name = data.get('name', None)
        self.url = data.get('url', None)
        self.icon_url = data.get('icon_url', None)
        self.proxy_icon_url = data.get('proxy_icon_url', None)
        
        return self
    
    
    def to_data(self):
        """
        Converts the embed author to json serializable `dict` representing it.
        
        Returns
        -------
        author_data : `dict` of (`str`, `Any`) items
        """
        author_data = {}
    
        name = self.name
        if (name is not None):
            author_data['name'] = name
        
        url = self.url
        if (url is not None):
            author_data['url'] = url
        
        icon_url = self.icon_url
        if (icon_url is not None):
            author_data['icon_url'] = icon_url
        
        return author_data
    
    
    def copy(self):
        """
        Copies the ``EmbedAuthor`` returning a new one.
        
        Returns
        -------
        new : ``EmbedAuthor``
        """
        new = object.__new__(type(self))
        
        new.icon_url = self.icon_url
        new.name = self.name
        new.url = self.url
        new.proxy_icon_url = None
        
        return self
    
    
    def copy_with(self, *, icon_url=..., name=..., url=...):
        """
        Copies the ``EmbedAuthor`` and updates it with the given parameters.
        
        Parameters
        ----------
        icon_url : `str`, Optional (Keyword only)
            An url of the author's icon. Can be http(s) or attachment.
        name : `str`, Optional (Keyword only)
            The name of the author.
        url : `str`, Optional (Keyword only)
            The url of the author.
        
        Returns
        -------
        new : ``EmbedAuthor``
        """
        if icon_url is ...:
            icon_url = self.icon_url
        
        if name is ...:
            name = self.name
        
        if url is ...:
            url = self.url
        
        new = object.__new__(type(self))
        
        new.icon_url = icon_url
        new.name = name
        new.url = url
        new.proxy_icon_url = None
        
        return self
    

class EmbedFooter:
    """
    Represents an embed's footer.
    
    Attributes
    ----------
    icon_url :`None` or `str`
        Url of the embed footer's icon.
    proxy_icon_url : `None` or `str`
        A proxied url of the embed footer's icon.
    text : `str`
        The embed footer's text.
    """
    __slots__ = ('icon_url', 'proxy_icon_url', 'text',)
    
    
    def __init__(self, text, icon_url=None):
        """
        Creates an embed footer with the given parameters.
        
        Parameters
        ----------
        text : `str`
            The footer's text.
        icon_url : `str`, Optional
            An url of the footer's icon. Can be http(s) or attachment.
        """
        self.text = text
        self.icon_url = icon_url
        self.proxy_icon_url = None
    
    
    def __len__(self):
        """Returns the embed footer's contents' length."""
        return len(self.text)
    
    
    def __bool__(self):
        """Returns whether the embed footer is not empty."""
        if self.text:
            return True
        
        if (self.icon_url is not None):
            return True
        
        return False
    
    
    def __repr__(self):
        """Returns the representation of the embed footer."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' length=',
            str(len(self)),
            ', url='
        ]
        
        icon_url = self.icon_url
        if icon_url is None:
            repr_parts.append('None')
        else:
            repr_parts.append('\'')
            icon_url = url_cutter(icon_url)
            repr_parts.append(icon_url)
            repr_parts.append('\'')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two embed footers are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.icon_url != other.icon_url:
            return False
        
        if self.text != other.text:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates an embed footer object from the data sent by Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embed footer data received from Discord.
        
        Returns
        -------
        embed_footer : ``EmbedFooter``
        """
        self = object.__new__(cls)
        self.text = data['text']
        self.icon_url = data.get('icon_url', None)
        self.proxy_icon_url = data.get('proxy_icon_url', None)
        
        return self
    
    
    def to_data(self):
        """
        Converts the embed footer to json serializable `dict` representing it.
        
        Returns
        -------
        footer_data : `dict` of (`str`, `Any`) items
        """
        footer_data = {
            'text' : self.text,
        }
        
        icon_url = self.icon_url
        if (icon_url is not None):
            footer_data['icon_url'] = icon_url
            
        return footer_data
    
    
    def copy(self):
        """
        Copies the ``EmbedFooter`` returning a new one.
        
        Returns
        -------
        new : ``EmbedFooter``
        """
        new = object.__new__(type(self))
        
        new.text = self.text
        new.icon_url = self.icon_url
        new.proxy_icon_url = None
        
        return self
    
    
    def copy_with(self, *, text=..., icon_url=...):
        """
        Copies the ``EmbedFooter`` and updates it with the given parameters.
        
        Parameters
        ----------
        text : `str`, Optional (Keyword only)
            The footer's text.
        icon_url : `str`, Optional (Keyword only)
            An url of the footer's icon. Can be http(s) or attachment.
        
        Returns
        -------
        new : ``EmbedFooter``
        """
        if text is ...:
            text = self.text
        
        if icon_url is ...:
            icon_url = self.icon_url
        
        new = object.__new__(type(self))
        
        new.text = text
        new.icon_url = icon_url
        new.proxy_icon_url = None
        
        return self


class EmbedField:
    """
    Represents an embed's field.
    
    Attributes
    ----------
    inline : `bool`
        Whether this field should display inline. Defaults to `False`.
    name : `str`
        The name of the field.
    value : `str`
        The value of the field.
    """
    __slots__ = ('inline', 'name', 'value',)
    
    def __init__(self, name, value, inline=False):
        """
        Creates an embed field with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The name of the field.
        value : `str`
            The value of the field.
        inline : `bool`, Optional
            Whether this field should display inline.
        """
        self.name = name
        self.value = value
        self.inline = inline
    
    
    def __len__(self):
        """Returns the embed field's contents' length."""
        return len(self.name)+len(self.value)
    
    
    def __bool__(self):
        """Returns whether the embed field is not empty."""
        if self.name:
            return True
        
        if self.value:
            return True
        
        return False
    
    
    def __repr__(self):
        """Returns the representation of the embed field."""
        return f'<{self.__class__.__name__} length={len(self)}, inline={self.inline}>'
    
    
    def __eq__(self, other):
        """Returns whether the two embed fields are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.name != other.name:
            return False
        
        if self.value != other.value:
            return False
        
        if self.inline != other.inline:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates an embed field object from the data sent by Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embed field data received from Discord.
        
        Returns
        -------
        embed_field : ``EmbedField``
        """
        self = object.__new__(cls)
        
        self.name = data['name']
        self.value = data['value']
        self.inline = data.get('inline',False)
        
        return self
    
    
    def to_data(self):
        """
        Converts the embed field to json serializable `dict` representing it.
        
        Returns
        -------
        field_data : `dict` of (`str`, `Any`) items
        """
        field_data = {
            'name': self.name,
            'value': self.value,
        }
        
        inline = self.inline
        if inline:
            field_data['inline'] = inline
        
        return field_data


    def copy(self):
        """
        Copies the ``EmbedField`` returning a new one.
        
        Returns
        -------
        new : ``EmbedField``
        """
        new = object.__new__(type(self))
        
        new.name = self.name
        new.value = self.value
        new.inline = self.inline
        
        return self
    
    
    def copy_with(self, *, name=..., value=..., inline=...):
        """
        Copies the ``EmbedField`` and updates it with the given parameters.
        
        Parameters
        ----------
        name : `str`, Optional (Keyword only)
            The name of the field.
        value : `str`, Optional (Keyword only)
            The value of the field.
        inline : `bool`, Optional (Keyword only)
            Whether this field should display inline.
        
        Returns
        -------
        new : ``EmbedField``
        """
        if name is ...:
            name = self.name
        
        if value is ...:
            value = self.value
        
        if inline is ...:
            inline = self.inline
        
        new = object.__new__(type(self))
        
        new.name = name
        new.value = value
        new.inline = inline
        
        return self


EMBED_ATTRIBUTES = frozenset((
    'author',
    'color',
    'description',
    'fields',
    'footer',
    'image',
    'provider',
    'thumbnail',
    'timestamp',
    'title',
    'type',
    'url',
    'video',
))

class EmbedBase:
    """
    Base class for Discord embedded contents. Should be taken as a guide for implementing custom embed classes.
    
    Abstract Attributes
    -------------------
    author : `None` or ``EmbedAuthor``
        Author information.
    color : `None`, ``Color`` or `int`
        The color code of the embed. Passing `0` means black, not like at the case of roles.
    description : `None` or `str`
        The main content of the embed.
    fields : `list` of ``EmbedField``
        Fields' information.
    footer : `None` or ``EmbedFooter``
        Footer information.
    image : `None` or ``EmbedImage``
        Image information.
    provider : `None` or ``EmbedProvider``
        Provider information.
    thumbnail : `None` or ``EmbedThumbnail``
        Thumbnail information.
    timestamp : `None` or `datetime`
        Timestamp of the embed's content. Shows up next to the ``.footer`` separated with a `'|'` character.
    title : `None` or `str`
        The title of the embed. Shows at the top with intense white characters.
    type : `None` or `str`
        The type of the embed. Can be one of `EXTRA_EMBED_TYPES`'s elements. Webhook embeds' type must be `'rich'`.
    url : `None` or `str`
        Url of the embed. If defined, the embed's `title` will show up as a hyper link pointing to the `url`.
    video : `None` or `EmbedVideo`
        Video information.
    """
    
    __slots__ = ()
    
    author : {None, EmbedAuthor}
    color : {None, Color, int}
    description : {None, str}
    fields : (list, EmbedField)
    footer : {None, EmbedFooter}
    image : {None, EmbedImage}
    provider : {None, EmbedProvider}
    thumbnail : {None, EmbedThumbnail}
    timestamp : {None, datetime}
    title : {None, str}
    type : {None, str}
    url : {None, str}
    video : {None, EmbedVideo}
    
    
    def __len__(self):
        """Returns the embed's contents' length."""
        result = 0
        
        title = self.title
        if (title is not None):
            result += len(title)
        
        description = self.description
        if (description is not None):
            result += len(description)
        
        title = self.title
        if (title is not None):
            result += len(title)
        
        footer = self.footer
        if (footer is not None):
            result += len(footer.text)
        
        author = self.author
        if (author is not None):
            name = author.name
            if (name is not None):
                result += len(name)
        
        for field in self.fields:
            result += len(field.name)
            result += len(field.value)
        
        return result
    
    
    def __bool__(self):
        """Returns whether the embed is not empty."""
        author = self.author
        if (author is not None) and author:
            return True
        
        if (self.color is not None):
            return True
        
        description = self.description
        if (description is not None) and description:
            return True
        
        if self.fields:
            return True
        
        footer = self.footer
        if (footer is not None) and footer:
            return True
        
        image = self.image
        if (image is not None) and image:
            return True
        
        provider = self.provider
        if (provider is not None) and provider:
            return True
        
        thumbnail = self.thumbnail
        if (thumbnail is not None) and thumbnail:
            return True
        
        if (self.timestamp is not None):
            return True
        
        title = self.title
        if (title is not None) and title:
            return True
        
        if (self.url is not None):
            return True
        
        video = self.video
        if (video is not None) and video:
            return True
        
        return False
    
    
    def __repr__(self):
        """Returns the representation of the embed."""
        return f'<{self.__class__.__name__} length={len(self)}>'
    
    
    def __eq__(self, other):
        """Returns whether the two embeds are equal."""
        if not isinstance(other, EmbedBase):
            return NotImplemented
        
        if self.title != other.title:
            return False
            
        if self.description != other.description:
            return False
        
        if self.color != other.color:
            return False
        
        if self.url != other.url:
            return False
            
        if self.timestamp != other.timestamp:
            return False
            
        if self.type != other.type:
            return False
        
        if self.footer != other.footer:
            return False
            
        if self.image != other.image:
            return False
            
        if self.thumbnail != other.thumbnail:
            return False
        
        if self.video != other.video:
            return False
        
        if self.author != other.author:
            return False
        
        if self.fields != other.fields:
            return False
        
        return True
    
    
    def from_data(self, data):
        """
        Creates a new embed from the given data received from Discord.
        
        > Subclasses should overwrite this method.
        
        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError
    
    
    def to_data(self):
        """
        Converts the embed to json serializable `dict` representing it.
        
        > Subclasses should overwrite this method.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {}
    
    
    def clear(self):
        """
        Clears the embed.
        """
    
    
    @property
    def contents(self):
        """
        Returns the embed's contents.
        
        > Subclasses should overwrite this method.
        
        The embed's contents are the following:
        - `.title`
        - `.description`
        - `.author.name`
        - `.footer.text`
        - `.fields[n].name`
        - `.fields[n].value`
        
        Returns
        -------
        contents : `list` of `str`
        """
        return []
    
    
    def copy(self):
        """
        Copies the embed returning a new one.
        
        Returns
        -------
        new : ``EmbedBase``
        """
        return
    
    
    def copy_with(self, **kwargs):
        """
        Copies the embed and updates it with the given parameters.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
             Keyword parameters referencing attributes.
         
        Other Parameters
        ----------------
        author : `None` or ``EmbedAuthor``, Optional (Keyword only)
            Author information.
        color : `None`, ``Color`` or `int`, Optional (Keyword only)
            The color code of the embed. Passing `0` means black, not like at the case of roles.
        description : `None` or `str`, Optional (Keyword only)
            The main content of the embed.
        fields : `list` of ``EmbedField``, Optional (Keyword only)
            Fields' information.
        footer : `None` or ``EmbedFooter``, Optional (Keyword only)
            Footer information.
        image : `None` or ``EmbedImage``, Optional (Keyword only)
            Image information.
        provider : `None` or ``EmbedProvider``, Optional (Keyword only)
            Provider information.
        thumbnail : `None` or ``EmbedThumbnail``, Optional (Keyword only)
            Thumbnail information.
        timestamp : `None` or `datetime`, Optional (Keyword only)
            Timestamp of the embed's content. Shows up next to the ``.footer`` separated with a `'|'` character.
        title : `None` or `str`, Optional (Keyword only)
            The title of the embed. Shows at the top with intense white characters.
        type : `None` or `str`, Optional (Keyword only)
            The type of the embed. Can be one of `EXTRA_EMBED_TYPES`'s elements. Webhook embeds' type must be `'rich'`.
        url : `None` or `str`, Optional (Keyword only)
            Url of the embed. If defined, the embed's `title` will show up as a hyper link pointing to the `url`.
        video : `None` or `EmbedVideo`, Optional (Keyword only)
            Video information.
        
        Returns
        -------
        new : ``EmbedBase``
        """
        for key in kwargs:
            if key not in EMBED_ATTRIBUTES:
                raise TypeError(f'Unused or unsettable attribute: `{key}`')
        
        return
