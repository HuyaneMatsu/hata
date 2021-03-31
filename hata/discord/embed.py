# -*- coding: utf-8 -*-
__all__ = ('EXTRA_EMBED_TYPES', 'Embed', 'EmbedAuthor', 'EmbedBase', 'EmbedCore', 'EmbedField', 'EmbedFooter',
    'EmbedImage', 'EmbedProvider', 'EmbedThumbnail', 'EmbedVideo', )

from typing import Union, List
from datetime import datetime

from ..backend.utils import DOCS_ENABLED

from .utils import parse_time, url_cutter, sanitize_mentions
from .color import Color

EXTRA_EMBED_TYPES = ('application_news', 'article', 'gifv', 'image', 'link', 'video')

class EmbedThumbnail:
    """
    Represents an embed's thumbnail.
    
    Attributes
    ----------
    height : `int`
        The height of the thumbnail. Defaults to `0`.
    proxy_url : `str` or `None`
        A proxied url of the thumbnail.
    url : `str` or `None`
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
    
    def __len__(self):
        """Returns the embed thumbnail's contents' length."""
        return 0
    
    def __repr__(self):
        """Returns the representation of the embed thumbnail."""
        text = [
            '<',
            self.__class__.__name__,
            ' url=',
                ]
        
        url = self.url
        if url is None:
            text.append('None')
        else:
            text.append('\'')
            url = url_cutter(url)
            text.append(url)
            text.append('\'')
        
        text.append(', size=')
        text.append(str(self.width))
        text.append('x')
        text.append(str(self.height))
    
        text.append('>')
        
        return ''.join(text)
    
    def __eq__(self, other):
        """Returns whether the two embed thumbnails are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.url == other.url)
    
class EmbedVideo:
    """
    Represents an embed's video.
    
    Embed videos cannot be sent, they are receive only.
    
    Attributes
    ----------
    height : `int`
        The height of the video. Defaults to `0`.
    proxy_url : `str` or `None`
        A proxied url of the video.
    url : `str` or `None`
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
    
    def __len__(self):
        """Returns the embed video's contents' length."""
        return 0
    
    def __repr__(self):
        """Returns the representation of the embed video."""
        text = [
            '<',
            self.__class__.__name__,
            ' url=',
                ]
        
        url = self.url
        if url is None:
            text.append('None')
        else:
            text.append('\'')
            url = url_cutter(url)
            text.append(url)
            text.append('\'')
        
        text.append(', size=')
        text.append(str(self.width))
        text.append('x')
        text.append(str(self.height))
    
        text.append('>')
        
        return ''.join(text)
    
    def __eq__(self, other):
        """Returns whether the two embed videos are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.url == other.url)

class EmbedImage:
    """
    Represents an embed's image.
    
    Attributes
    ----------
    height : `int`
        The height of the image. Defaults to `0`.
    proxy_url : `str` or `None`
        A proxied url of the image.
    url : `str` or `None`
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
    
    def __len__(self):
        """Returns the embed image's contents' length."""
        return 0
    
    def __repr__(self):
        """Returns the representation of the embed image."""
        text = [
            '<',
            self.__class__.__name__,
            ' url=',
                ]
        
        url = self.url
        if url is None:
            text.append('None')
        else:
            text.append('\'')
            url = url_cutter(url)
            text.append(url)
            text.append('\'')
            
        text.append(', size=')
        text.append(str(self.width))
        text.append('x')
        text.append(str(self.height))
        
        text.append('>')
        
        return ''.join(text)
    
    def __eq__(self, other):
        """Returns whether the two embed images are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.url == other.url)
    
class EmbedProvider:
    """
    Represents an embed's provider.
    
    Embed providers cannot be sent, they are receive only.
    
    Attributes
    ----------
    name : `str` or `None`
        The name of the provider.
    url : `str` or `None`
        The url of the provider.
    """
    __slots__ = ('name', 'url',)
    
    def __init__(self):
        self.name = None
        self.url = None
        
    @classmethod
    def from_data(cls, data):
        """
        Creates a new embed provider object. Because embed providers cannot be sent, it accepts no parameters and just
        creates an empty embed provider object with default attributes.
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
    
    def __len__(self):
        """Returns the embed provider's contents' length."""
        name = self.name
        if name is None:
            return 0
        return len(name)
    
    def __repr__(self):
        """Returns the representation of the embed provider."""
        text = [
            '<',
            self.__class__.__name__,
            ' length=',
            str(len(self)),
            ', url='
                ]
        
        url = self.url
        if url is None:
            text.append('None')
        else:
            text.append('\'')
            url = url_cutter(url)
            text.append(url)
            text.append('\'')
        
        text.append('>')
        
        return ''.join(text)
    
    def __eq__(self, other):
        """Returns whether the two embed providers are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.name != other.name:
            return False
        
        if self.url != other.url:
            return False
        
        return True
    
class EmbedAuthor:
    """
    Represents an embed's author.
    
    Attributes
    ----------
    icon_url : `str` or `None`
        Url of the author's icon.
    name : `str` or `None`
        The name of the author.
    proxy_icon_url : `str` or `None`
        A proxied url to the url of the author's icon.
    url : `str` or `None`
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

    def __len__(self):
        """Returns the embed author's contents' length."""
        name = self.name
        if name is None:
            return 0
        return len(name)
    
    def __repr__(self):
        """Returns the representation of the embed author."""
        text = [
            '<',
            self.__class__.__name__,
            ' length=',
            str(len(self)),
            ', url='
                ]
        
        url = self.url
        if url is None:
            text.append('None')
        else:
            text.append('\'')
            url = url_cutter(url)
            text.append(url)
            text.append('\'')
        
        text.append(', icon_url=')
        icon_url = self.icon_url
        if icon_url is None:
            text.append('None')
        else:
            text.append('\'')
            icon_url = url_cutter(icon_url)
            text.append(icon_url)
            text.append('\'')
            
        text.append('>')
        
        return ''.join(text)
    
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
    
class EmbedFooter:
    """
    Represents an embed's footer.
    
    Attributes
    ----------
    icon_url :`str` or `None`
        Url of the embed footer's icon.
    proxy_icon_url : `str` or `None`
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
    
    def __len__(self):
        """Returns the embed footer's contents' length."""
        return len(self.text)
    
    def __repr__(self):
        """Returns the representation of the embed footer."""
        text = [
            '<',
            self.__class__.__name__,
            ' length=',
            str(len(self)),
            ', url='
                ]
        
        icon_url = self.icon_url
        if icon_url is None:
            text.append('None')
        else:
            text.append('\'')
            icon_url = url_cutter(icon_url)
            text.append(icon_url)
            text.append('\'')
        
        text.append('>')
        
        return ''.join(text)
    
    def __eq__(self,other):
        """Returns whether the two embed footers are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.icon_url != other.icon_url:
            return False
        
        if self.text != other.text:
            return False
        
        return True

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
            'name' : self.name,
            'value' : self.value,
                }
        
        inline = self.inline
        if inline:
            field_data['inline'] = inline
        
        return field_data
    
    def __len__(self):
        """Returns the embed field's contents' length."""
        return len(self.name)+len(self.value)
    
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
    
    author      : Union[None, EmbedAuthor]
    color       : Union[None, Color, int]
    description : Union[None, str]
    fields      : List[EmbedField]
    footer      : Union[None, EmbedFooter]
    image       : Union[None, EmbedImage]
    provider    : Union[None, EmbedProvider]
    thumbnail   : Union[None, EmbedThumbnail]
    timestamp   : Union[None, datetime]
    title       : Union[None, str]
    type        : Union[None, str]
    url         : Union[None, str]
    video       : Union[None, EmbedVideo]
    
    def __len__(self):
        """
        Returns the embed's contents' length.
        
        Notes
        -----
        Subclasses should overwrite it.
        """
        return 0
    
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
    
    def to_data(self):
        """
        Converts the embed core to json serializable `dict` representing it.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        
        Notes
        -----
        Subclasses should overwrite it.
        """
        return {}
    
    @property
    def contents(self):
        """
        Returns the embed's contents.
        
        The embeds contents are the following:
        - `.title`
        - `.description`
        - `.author.name`
        - `.footer.text`
        - `.fields[n].name`
        - `.fields[n].value`
        
        Returns
        -------
        contents : `list` of `str`
        
        Notes
        -----
        Subclasses should overwrite it.
        """
        return []
    
    def _get_colour(self):
        return self.color
    
    def _set_colour(self, color):
        self.color = color
    
    colour = property(_get_colour, _set_colour)
    if DOCS_ENABLED:
        colour.__doc__ = """Alias of ``.color``."""


class EmbedCore(EmbedBase):
    """
    Represents Discord embedded content. There are two defined embed classes, the other one is ``Embed``.
    
    Each embed what is received from Discord is stored as ``EmbedCore`` object for better operation support. This
    embed type is a valid embed type to send, but it is more cumbersome to build up, because it requires extra
    imports and it is slower to serialize.
    
    Attributes
    ----------
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
    __slots__ = ('author', 'color', 'description', 'fields', 'footer', 'image', 'provider', 'thumbnail', 'timestamp',
        'title', 'type', 'url', 'video',)
    
    def __init__(self, title=None, description=None, color=None, url=None, timestamp=None, type_='rich'):
        """
        Creates an embed core instance. Accepts the base parameters of the embed and sets the other ones as `None`.
        
        Parameters
        ----------
        title : `str`, Optional
            The title of the embed. Shows at the top with intense white characters.
        description : `str`, Optional
            The main content of the embed.
        color : ``Color`` or `int`, Optional
            The color code of the embed. Passing `0` means black, not like at the case of roles.
        url : `str`, Optional
            Url of the embed. If defined, the embed's `title` will show up as a hyper link pointing to the `url`.
        timestamp : `datetime`, optional
            Timestamp of the embed's content. Shows up next to the `footer` separated with a `'|'` character.
        type_ : `None` or `str`, Optional
            The type of the embed. Defaults to `'rich'`.
        """
        self.title = title
        self.description = description
        self.color = color
        self.url = url
        self.timestamp = timestamp
        self.type = type_ # must be `rich` for webhook embeds
        self.footer = None
        self.image = None
        self.thumbnail = None
        self.video = None
        self.provider = None
        self.author = None
        self.fields = []
    
    @classmethod
    def from_data(cls, data):
        """
        Creates an embed core object from the data sent by Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embed data received from Discord.
        
        Returns
        -------
        embed : ``EmbedCore``
        """
        self=cls.__new__(cls)
        
        self.title = data.get('title', None)
        self.type = data.get('type', None)
        self.description = data.get('description', None)
        self.url = data.get('url', None)

        try:
            timestamp_data = data['timestamp']
        except KeyError:
            timestamp = None
        else:
           timestamp = parse_time(timestamp_data)
        self.timestamp = timestamp
        
        try:
            color_data = data['color']
        except KeyError:
            color = None
        else:
            color = Color(color_data)
        self.color = color

        try:
            footer_data = data['footer']
        except KeyError:
            footer = None
        else:
            footer = EmbedFooter.from_data(footer_data)
        self.footer = footer
        
        try:
            image_data = data['image']
        except KeyError:
            image = None
        else:
            image = EmbedImage.from_data(image_data)
        self.image = image
        
        try:
            thumbnail_data = data['thumbnail']
        except KeyError:
            thumbnail = None
        else:
            thumbnail = EmbedThumbnail.from_data(thumbnail_data)
        self.thumbnail = thumbnail
        
        try:
            video_data = data['video']
        except KeyError:
            video = None
        else:
            video = EmbedVideo.from_data(video_data)
        self.video = video
        
        try:
            provider_data = data['provider']
        except KeyError:
            provider = None
        else:
            provider = EmbedProvider.from_data(provider_data)
        self.provider = provider
        
        try:
            author_data = data['author']
        except KeyError:
            author = None
        else:
            author = EmbedAuthor.from_data(author_data)
        self.author = author
        
        try:
            field_datas = data['fields']
        except KeyError:
            fields = []
        else:
            fields = [EmbedField.from_data(field_data) for field_data in field_datas]
        self.fields = fields
        
        return self

    def to_data(self):
        """
        Converts the embed core to json serializable `dict` representing it.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        type_ = self.type
        if (type_ is not None):
            data['type'] = type_
        
        title = self.title
        if (title is not None):
            data['title'] = title
        
        description = self.description
        if (description is not None):
            data['description'] = description
            
        color = self.color
        if (color is not None):
            data['color'] = color
        
        url = self.url
        if (url is not None):
            data['url'] = url
        
        timestamp = self.timestamp
        if (timestamp is not None):
            data['timestamp'] = timestamp.isoformat()
        
        footer = self.footer
        if (footer is not None):
            data['footer'] = footer.to_data()
        
        image = self.image
        if (image is not None):
            data['image'] = image.to_data()
        
        thumbnail = self.thumbnail
        if (thumbnail is not None):
            data['thumbnail'] = thumbnail.to_data()
        
        author = self.author
        if (author is not None):
            data['author'] = author.to_data()
        
        fields = self.fields
        if fields:
            data['fields'] = [field.to_data() for field in fields]
        
        return data

    def _update_sizes(self, data):
        """
        Updates the size information of the embed.
        
        Called when a ``Message`` is edited, but no `edited` timestamp is included with the data. Returns `0` if
        received data does not contain images, if does, then `1`.
        
        This method tries to update the embed's `image`, `thumbnail` amd `video` with their sizes. If any of those is
        not set already (for any reason), then it also creates them.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embed data received from Discord.
        
        Returns
        -------
        changed : `int`
        """
        changed = 0
        try:
            image_data = data['image']
        except KeyError:
            pass
        else:
            image = self.image
            if image is None:
                self.image = EmbedImage.from_data(image_data)
            else:
                image.height = image_data.get('height', 0)
                image.width = image_data.get('width', 0)
            changed = 1
        
        try:
            thumbnail_data = data['thumbnail']
        except KeyError:
            pass
        else:
            thumbnail = self.thumbnail
            if thumbnail is None:
                self.thumbnail = EmbedThumbnail.from_data(thumbnail_data)
            else:
                thumbnail.height= thumbnail_data.get('height', 0)
                thumbnail.width = thumbnail_data.get('width', 0)
            changed = 1

        try:
            video_data = data['video']
        except KeyError:
            pass
        else:
            video = self.video
            if video is None:
                self.video = EmbedVideo.from_data(video_data)
            else:
                video.height = video_data.get('height', 0)
                video.width = video_data.get('width', 0)
            changed = 1

        return changed

    def _update_sizes_no_return(self, data):
        """
        Updates the size information of the embed.

        Familiar to ``._update_sizes`` but it not checks whether the embed's images change, just updates them.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embed data received from Discord.
        """
        try:
            image_data = data['image']
        except KeyError:
            pass
        else:
            image = self.image
            if image is None:
                self.image = EmbedImage.from_data(image_data)
            else:
                image.height = image_data.get('height', 0)
                image.width = image_data.get('width', 0)
        
        try:
            thumbnail_data = data['thumbnail']
        except KeyError:
            pass
        else:
            thumbnail = self.thumbnail
            if thumbnail is None:
                self.thumbnail = EmbedThumbnail.from_data(thumbnail_data)
            else:
                thumbnail.height = thumbnail_data.get('height', 0)
                thumbnail.width = thumbnail_data.get('width', 0)
        
        try:
            video_data = data['video']
        except KeyError:
            pass
        else:
            video = self.video
            if video is None:
                self.video = EmbedVideo.from_data(video_data)
            else:
                video.height = video_data.get('height', 0)
                video.width = video_data.get('width', 0)
    
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
    
    @property
    def contents(self):
        """
        Returns the embed's contents.
        
        The embeds contents are the following:
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
        contents = []
        
        title = self.title
        if (title is not None):
            contents.append(title)
            
        description = self.description
        if (description is not None):
            contents.append(description)
            
        author = self.author
        if (author is not None):
            name = author.name
            if (name is not None):
                contents.append(name)

        footer = self.footer
        if (footer is not None):
            contents.append(footer.text)

        for field in self.fields:
            contents.append(field.name)
            contents.append(field.value)

        return contents

    def _clean_copy(self, message):
        """
        Creates a clean copy of the embed by removing the mentions in it's contents.
        
        Called by ``Message.clean_embeds``.
        
        Parameters
        ----------
        message : ``Message``
            The embed's respective message.
        
        Returns
        -------
        embed : ``EmbedCore``
        """
        new = object.__new__(type(self))
        
        new.title = self.title
        description = self.description
        new.description = None if (description is None) else sanitize_mentions(description, message.guild)
        new.color = self.color
        new.url = self.url
        new.timestamp = self.timestamp
        new.type = self.type
        
        new.footer = self.footer
        new.image = self.image
        new.thumbnail = self.thumbnail
        new.video = self.video
        new.provider = self.provider
        new.author = self.author
        new.fields = [
            type(field)(field.name, sanitize_mentions(field. value, message.guild), inline=field.inline) \
                for field in self.fields]
        
        return new

class Embed(EmbedBase):
    """
    Represents Discord embedded content. There are two defined embed classes, the other one is ``EmbedCore``.
    
    Embeds are easier to build with this class than with the other, and faster to serialize, because it stores the
    objects as raw serializable data, but it also means it has worse operation support, because it needs to convert
    the raw data back.
    
    Attributes
    ----------
    data : `dict` of (`str`, `Any`) items
        The raw data of the embed. It should not be accessed directly. There are several properties and methods to do
        operations on them.
    
    Examples
    --------
    Example of using local embed file:
        
        ```py
        # Imports
        from hata import Embed, ReuAsyncIO
        
        # Building the embed
        embed = Embed()
        embed.add_image('attachment://image.png')
        
        # Sending the message
        with (await ReuAsyncIO('some_file_path')) as file:
            await client.message_create(channel, embed=embed, file=('image.png', file))
        ```
        
        Note that you should use async io wrappers, but one which do not closes on `.close` either, but it resets
        itself instead, because if the request fails, the io would be closed and the request could not be done the
        second time.
    """
    __slots__ = ('data',)
    def __init__(self, title=None, description=None, color=None, url=None, timestamp=None, type_='rich'):
        """
        Creates an embed instance. Accepts the base parameters of the embed.
        
        Parameters
        ----------
        title : `str`, Optional
            The title of the embed. Shows at the top with intense white characters.
        description : `str`, Optional
            The main content of the embed.
        color : ``Color`` or `int`, Optional
            The color code of the embed. Passing `0` means black, not like at the case of roles.
        url : `str`, Optional
            Url of the embed. If defined, the embed's `title` will show up as a hyper link pointing to the `url`.
        timestamp : `datetime`, optional
            Timestamp of the embed's content. Shows up next to the `footer` separated with a `'|'` character.
        type_ : `None` or `str`, Optional
            The type of the embed. Defaults to `'rich'`.
        """
        self.data = data = {}
        
        if (title is not None):
            data['title'] = title
            
        if (description is not None):
            data['description'] = description
            
        if (color is not None):
            data['color'] = color
            
        if (url is not None):
            data['url'] = url
            
        if (timestamp is not None):
            data['timestamp'] = timestamp.isoformat()
            
        if (type_ is not None):
            data['type'] = type_
    
    def to_data(self):
        """
        Returns the embed's `.data`.
        
        This method is for compatibility with other embed-likes. When sending embed in message this method is called
        for getting it's data.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return self.data
    
    
    # author
    def _get_author(self):
        try:
            author_data = self.data['author']
        except KeyError:
            return None
        
        return EmbedAuthor.from_data(author_data)
    
    def _set_author(self, value):
        self.data['author'] = value.to_data()
    
    def _del_author(self):
        try:
            del self.data['author']
        except KeyError:
            pass
    
    author = property(_get_author, _set_author, _del_author)
    del _get_author, _set_author, _del_author
    if DOCS_ENABLED:
        author.__doc__ = (
        """
        A get-set-del property for accessing the embed's author.
        
        Accepts and returns `None` or an ``EmbedAuthor`` object.
        """)
    
    def add_author(self, icon_url=None, name=None, url=None):
        """
        Adds an ``EmbedAuthor`` to the embed with the given parameters.
        
        Parameters
        ----------
        icon_url : `str`, Optional
            An url of the author's icon. Can be http(s) or attachment.
        name : `str`, Optional
            The name of the author.
        url : `str`, Optional
            The url of the author.
        
        Returns
        -------
        self : ``Embed``
        """
        author_data = {}
        
        if (name is not None):
            author_data['name'] = name
        
        if (url is not None):
            author_data['url'] = url
        
        if (icon_url is not None):
            author_data['icon_url'] = icon_url
        
        self.data['author'] = author_data
        return self
    
    set_author = add_author
    
    # color
    def _get_color(self):
        return self.data.get('color', None)
    
    def _set_color(self, value):
        self.data['color'] = value
    
    def _del_color(self):
        try:
            del self.data['color']
        except KeyError:
            pass
    
    color = property(_get_color, _set_color, _del_color)
    del _get_color, _set_color, _del_color
    if DOCS_ENABLED:
        color.__doc__ = (
        """
        A get-set-del property for accessing the embed's color.
        
        Accepts and returns `None` or a ``Color`` (/ `int`) object.
        """)
    
    
    # description
    def _get_description(self):
        return self.data.get('description', None)
    
    def _set_description(self, value):
        self.data['description'] = value
    
    def _del_description(self):
        try:
            del self.data['description']
        except KeyError:
            pass
    
    description = property(_get_description, _set_description, _del_description)
    del _get_description, _set_description, _del_description
    if DOCS_ENABLED:
        description.__doc__ = (
        """
        A get-set-del property for accessing the embed's description.
        
        Accepts and returns `None` or a `str` instance.
        """)
    
    
    # fields
    def _get_fields(self):
        try:
            field_datas = self.data['fields']
        except KeyError:
            self.data['fields'] = field_datas = []
        
        return _EmbedFieldsReflection(field_datas)
    
    def _set_fields(self, value):
        data = self.data
        try:
            fields_data = data['fields']
        except KeyError:
            fields_data = data['fields'] = []
        
        if type(value) is _EmbedFieldsReflection:
            new_fields_data = value.data
        else:
            new_fields_data = list(field.to_data() for field in value)
        
        fields_data.clear()
        fields_data.extend(new_fields_data)
    
    def _del_fields(self):
        try:
            field_datas = self.data['fields']
        except KeyError:
            pass
        else:
            field_datas.clear()
    
    fields = property(_get_fields, _set_fields, _del_fields)
    del _get_fields, _set_fields, _del_fields
    if DOCS_ENABLED:
        fields.__doc__ = (
        """
        A get-set-del property for accessing the embed's fields.
        
        Accepts an `iterable` of ``EmbedField``objects. Meanwhile returns an ``_EmbedFieldsReflection`` instance,
        through what the respective embed's fields can be modified directly.
        """)
    
    def add_field(self, name, value, inline=False):
        """
        Adds an ``EmbedField`` to the end of the embed's fields.
        
        Parameters
        ----------
        name : `str`
            The name of the field.
        value : `str`
            The value of the field.
        inline : `bool`, Optional
            Whether this field should display inline.
        
        Returns
        -------
        self : ``Embed``
        """
        field_data = {
            'name' : name,
            'value' : value,
                }
        
        if inline:
            field_data['inline'] = inline
        
        try:
            field_datas = self.data['fields']
        except KeyError:
            self.data['fields'] = [field_data]
        else:
            field_datas.append(field_data)
        
        return self
    
    def insert_field(self, index, name, value, inline=False):
        """
        Inserts an ``EmbedField`` to the embed's fields at the specified `index`.
        
        Parameters
        ----------
        index : `int`
            The index before the field should be inserted.
        name : `str`
            The name of the field.
        value : `str`
            The value of the field.
        inline : `bool`, Optional
            Whether this field should display inline.
        """
        field_data = {
            'name' : name,
            'value' : value,
                }
        
        if inline:
            field_data['inline'] = inline
        
        try:
            field_datas = self.data['fields']
        except KeyError:
            self.data['fields'] = [field_data]
        else:
            field_datas.insert(index, field_data)
    
    def get_field(self, index):
        """
        Returns the embed's field at the given `index`.
        
        Parameters
        ----------
        index : `int`
            The index of the field.
        
        Returns
        -------
        embed_field : ``EmbedField``
        
        Raises
        ------
        IndexError
            Index out of the fields' range.
        """
        try:
            field_datas = self.data['fields']
        except KeyError:
            raise IndexError('Index out of the fields\' range.') from None
        
        try:
            field_data = field_datas[index]
        except IndexError as err:
            err.args = ('Index out of the fields\' range.', )
            raise
        
        return EmbedField.from_data(field_data)
    
    def append_field(self, field):
        """
        Appends the embed's fields with the given field.
        
        Parameters
        ----------
        field : ``EmbedField``
            The field to append the embed's field with.
        """
        field_data = field.to_data()
        
        try:
            field_datas = self.data['fields']
        except KeyError:
            self.data['fields'] = [field_data]
        else:
            field_datas.append(field_data)
    
    def set_field(self, index, field):
        """
        Sets the given ``EmbedField`` at the given `index` to the fields of the embed.
        
        Parameters
        ----------
        index : `int`
            The index of the field to set.
        field : ``EmbedField``
            The embed field to set at the given `index`.
        
        Raises
        ------
        IndexError
            Index out of the fields' range.
        """
        try:
            fields = self.data['fields']
        except KeyError:
            raise IndexError('Index out of the fields\' range.') from None
        
        field_data = field.to_data()
        
        try:
            fields[index] = field_data
        except IndexError as err:
            err.args = ('Index out of the fields\' range.',)
            raise
    
    def del_field(self, index):
        """
        Removes the field of the embed on the given index.
        
        Parameters
        ----------
        index : `int`
            The index of the field to remove.
        
        Raises
        ------
        IndexError
            Index out of the fields' range.
        """
        try:
            fields = self.data['fields']
        except KeyError:
            raise IndexError('Index out of the fields\' range.') from None
        
        try:
            del fields[index]
        except IndexError as err:
            err.args = ('Index out of the fields\' range.', )
            raise
    
    remove_field = del_field
    
    
    # footer
    def _get_footer(self):
        try:
            footer_data = self.data['footer']
        except KeyError:
            return None
        
        return EmbedFooter.from_data(footer_data)
    
    def _set_footer(self, value):
        self.data['footer'] = value.to_data()
    
    def _del_footer(self):
        try:
            del self.data['footer']
        except KeyError:
            pass
    
    footer = property(_get_footer, _set_footer, _del_footer)
    del _get_footer, _set_footer, _del_footer
    if DOCS_ENABLED:
        footer.__doc__ = (
        """
        A get-set-del property for accessing the embed's footer.
        
        Accepts and returns `None` or an ``EmbedFooter`` object.
        """)
    
    def add_footer(self, text, icon_url=None):
        """
        Adds an ``EmbedFooter`` to the embed with the given parameters.
        
        Parameters
        ----------
        text : `str`
            The footer's text.
        icon_url : `str`, Optional
            An url of the footer's icon. Can be http(s) or attachment.
        
        Returns
        -------
        self : ``Embed``
        """
        footer_data = {
            'text' : text,
                }
        
        if (icon_url is not None):
            footer_data['icon_url'] = icon_url
        
        self.data['footer'] = footer_data
        return self
    set_footer = add_footer
    
    # image
    def _get_image(self):
        try:
            image_data = self.data['image']
        except KeyError:
            return None
        
        return EmbedImage.from_data(image_data)
    
    def _set_image(self, value):
        self.data['image'] = value.to_data()
    
    def _del_image(self):
        try:
            del self.data['image']
        except KeyError:
            pass
    
    image = property(_get_image, _set_image, _del_image)
    del _get_image, _set_image, _del_image
    if DOCS_ENABLED:
        image.__doc__ = (
        """
        A get-set-del property for accessing the embed's image.
        
        Accepts and returns `None` or an ``EmbedImage`` object.
        """)
    
    def add_image(self, url):
        """
        Adds an ``EmbedImage`` to the embed with the given `url`.
        
        Parameters
        ----------
        url : `str`
            The url of the image. Can be http(s) or attachment.
        
        Returns
        -------
        self : ``Embed``
        """
        image_data = {
            'url' : url,
                }
        
        self.data['image'] = image_data
        return self
    
    set_image = add_image
    
    
    # provider
    def _get_provider(self):
        try:
            provider_data = self.data['provider']
        except KeyError:
            return None
        
        return EmbedProvider.from_data(provider_data)
    
    def _del_provider(self):
        try:
            del self.data['provider']
        except KeyError:
            pass
    
    provider = property(_get_provider, None, _del_provider)
    del _get_provider, _del_provider
    if DOCS_ENABLED:
        provider.__doc__ = (
        """
        A get-del property for accessing the embed's provider.
        
        Returns `None` or an ``EmbedProvider`` object.
        
        Embed providers cannot be set, they are receive only.
        """)
    
    
    # thumbnail
    def _get_thumbnail(self):
        try:
            thumbnail_data = self.data['thumbnail']
        except KeyError:
            return None
        
        return EmbedThumbnail.from_data(thumbnail_data)
    
    def _set_thumbnail(self, value):
        self.data['thumbnail'] = value.to_data()
    
    def _del_thumbnail(self):
        try:
            self.data['thumbnail']
        except KeyError:
            pass
    
    thumbnail = property(_get_thumbnail, _set_thumbnail, _del_thumbnail)
    del _get_thumbnail, _set_thumbnail, _del_thumbnail
    if DOCS_ENABLED:
        thumbnail.__doc__ = (
        """
        A get-set-del property for accessing the embed's thumbnail.
        
        Accepts and returns `None` or an ``EmbedThumbnail`` object.
        """)
    
    
    def add_thumbnail(self, url):
        """
        Adds an ``EmbedThumbnail`` to the embed with the given `url`.
        
        Parameters
        ----------
        url : `str`
            The url of the thumbnail. Can be http(s) or attachment.
        
        Returns
        -------
        self : ``Embed``
        """
        thumbnail_data = {
            'url' : url,
                }

        self.data['thumbnail'] = thumbnail_data
        return self
    
    set_thumbnail = add_thumbnail
    
    
    # timestamp
    def _get_timestamp(self):
        try:
            timestamp_value = self.data['timestamp']
        except KeyError:
            return None
        
        return parse_time(timestamp_value)
    
    def _set_timestamp(self, value):
        self.data['timestamp'] = value.isoformat()
    
    def _del_timestamp(self):
        try:
            del self.data['timestamp']
        except KeyError:
            pass
    
    timestamp = property(_get_timestamp, _set_timestamp, _del_timestamp)
    del _get_timestamp, _set_timestamp, _del_timestamp
    if DOCS_ENABLED:
        timestamp.__doc__ = (
        """
        A get-set-del property for accessing the embed's timestamp.
        
        Accepts and returns `None` or a `datetime` object.
        """)
    
    # title
    def _get_title(self):
        return self.data.get('title', None)
    
    def _set_title(self, value):
        self.data['title'] = value
    
    def _del_title(self):
        try:
            del self.data['title']
        except KeyError:
            pass
    
    title = property(_get_title, _set_title, _del_title)
    
    del _get_title, _set_title, _del_title
    if DOCS_ENABLED:
        title.__doc__ = (
        """
        A get-set-del property for accessing the embed's title.
        
        Accepts and returns `None` or a `str` instance.
        """)
    
    
    # type
    def _get_type(self):
        return self.data.get('type', None)
    
    def _set_type(self, value):
        self.data['type'] = value
    
    def _del_type(self):
        try:
            del self.data['type']
        except KeyError:
            pass
    
    type = property(_get_type, _set_type, _del_type)
    del _get_type, _set_type, _del_type
    if DOCS_ENABLED:
        type.__doc__ = (
        """
        A get-set-del property for accessing the embed's type.
        
        Accepts and returns `None` or a `str` instance.
        """)
    
    
    # url
    def _get_url(self):
        return self.data.get('url', None)
    
    def _set_url(self, value):
        self.data['url'] = value
    
    def _del_url(self):
        try:
            del self.data['url']
        except KeyError:
            pass
    
    url = property(_get_url, _set_url, _del_url)
    del _get_url, _set_url, _del_url
    if DOCS_ENABLED:
        url.__doc__ = (
        """
        A get-set-del property for accessing the embed's url.
        
        Accepts and returns `None` or a `str` instance.
        """)
    
    
    # video
    def _get_video(self):
        try:
            video_data = self.data['video']
        except KeyError:
            return None
        
        return EmbedVideo.from_data(video_data)
    
    def _del_video(self):
        try:
            del self.data['video']
        except KeyError:
            pass
    
    video = property(_get_video, None, _del_video)
    del _get_video, _del_video
    if DOCS_ENABLED:
        video.__doc__ = (
        """
        A get-del property for accessing the embed's video.
        
        Returns `None` or an ``EmbedVideo`` object.
        
        Embed videos cannot be set, they are receive only.
        """)
    
    
    # rest
    def _get_source(self):
        return EmbedCore.from_data(self.data)
    
    def _set_source(self, value):
        if type(value) is type(self):
            data = value.data.copy()
        else:
            data = value.to_data()
        self.data = data
    
    def _del_source(self):
        data = self.data
        fields = data.get('fields')
        data.clear()
        if (fields is not None):
            fields.clear()
            data['fields'] = fields
    
    source = property(_get_source, _set_source, _del_source)
    del _get_source, _set_source, _del_source
    if DOCS_ENABLED:
        source.__doc__ = (
        """
        A get-set-del property for accessing the embed's data.
        
        Returns an `EmbedCore` object and accepts any embed compatible objects.
        """)
    
    
    def __len__(self):
        """Returns the embed's contents' length."""
        data = self.data
        result = 0
        
        try:
            title = data['title']
        except KeyError:
            pass
        else:
            result += len(title)
        
        try:
            description = data['description']
        except KeyError:
            pass
        else:
            result += len(description)
        
        try:
            author_data = data['author']
        except KeyError:
            pass
        else:
            try:
                author_name = author_data['name']
            except KeyError:
                pass
            else:
                result += len(author_name)
        
        try:
            footer_data = data['footer']
        except KeyError:
            pass
        else:
            result += len(footer_data['text'])
        
        try:
            field_datas = data['fields']
        except KeyError:
            pass
        else:
            for field_data in field_datas:
                result += len(field_data['name'])
                result += len(field_data['value'])
        
        return result
    
    @property
    def contents(self):
        """
        Returns the embed's contents.
        
        The embeds contents are the following:
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
        data = self.data
        result = []
        
        try:
            title = data['title']
        except KeyError:
            pass
        else:
            result.append(title)
        
        try:
            description = data['description']
        except KeyError:
            pass
        else:
            result.append(description)
        
        try:
            author_data = data['author']
        except KeyError:
            pass
        else:
            try:
                author_name = author_data['name']
            except KeyError:
                pass
            else:
                result.append(author_name)
        
        try:
            footer_data = data['footer']
        except KeyError:
            pass
        else:
            result.append(footer_data['text'])
        
        try:
            field_datas = data['fields']
        except KeyError:
            pass
        else:
            for field_data in field_datas:
                result.append(field_data['name'])
                result.append(field_data['value'])
        
        return result


class _EmbedFieldsReflection:
    """
    A reflection of an `Embed` object's fields. The instances of this type allow direct modifications of their
    respective embed's fields.
    
    Attributes
    ----------
    data : `list` of (`dict` of (`str`, `Any`) items)
        Raw data containing the respective embed's fields.
    """
    __slots__ = ('data',)
    def __init__(self, data):
        """
        Creates a ``_EmbedFieldsReflection`` object.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items)
            Raw data containing the respective embed's fields.
        """
        self.data = data
        
    def clear(self):
        """
        Removes all of the respective embed's fields.
        """
        self.data.clear()

    def __len__(self):
        """Returns how much fields the respective embed has."""
        return len(self.data)
    
    def __repr__(self):
        """Returns the representation of the object."""
        return f'<{self.__class__.__name__} length={len(self.data)}>'
    
    def __getitem__(self, index):
        """Returns the embed field on the given index."""
        return EmbedField.from_data(self.data[index])
    
    def __setitem__(self, index, field):
        """Sets the given embed field object on the given index."""
        self.data[index] = field.to_data()
    
    def __delitem__(self, index):
        """Deletes the field on the given index"""
        del self.data[index]
    
    def append(self, field):
        """
        Appends the respective embed's fields with the given field.
        
        Parameters
        ----------
        field : ``EmbedField``
            The field to append the embed's field with.
        """
        self.data.append(field.to_data())
    
    def insert(self, index, field):
        """
        Inserts the given `field` to the respective embed's fields at the specified `index`.
        
        Parameters
        ----------
        index : `int`
            The index before the field should be inserted.
        field : ``EmbedField``
            The field to insert.
        """
        self.data.insert(index,field.to_data())
    
    def add_field(self, name, value, inline=False):
        """
        Adds an ``EmbedField`` to the end of the respective embed's fields.
        
        Parameters
        ----------
        name : `str`
            The name of the field.
        value : `str`
            The value of the field.
        inline : `bool`, Optional
            Whether this field should display inline.
        """
        field_data = {
            'name' : name,
            'value' : value,
                }
        
        if inline:
            field_data['inline'] = inline
        
        self.data.append(field_data)
    
    def insert_field(self, index, name, value, inline=False):
        """
        Inserts an ``EmbedField`` to the respective embed's fields at the specified `index`.
        
        Parameters
        ----------
        index : `int`
            The index before the field should be inserted.
        name : `str`
            The name of the field.
        value : `str`
            The value of the field.
        inline : `bool`, Optional
            Whether this field should display inline.
        """
        field_data = {
            'name' : name,
            'value' : value,
                }
        
        if inline:
            field_data['inline'] = inline
        
        self.data.insert(index, field_data)
    
    def __iter__(self):
        """
        Iterates over the respective embed's fields.
        
        This method is a generator.
        """
        for field_data in self.data:
            yield EmbedField.from_data(field_data)
    
    def __reversed__(self):
        """
        Reverse iterates over the respective embed's fields.
        
        This method is a generator.
        """
        for field_data in reversed(self.data):
            yield EmbedField.from_data(field_data)
