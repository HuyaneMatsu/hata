# -*- coding: utf-8 -*-
__all__ = ('EXTRA_EMBED_TYPES', 'Embed', 'EmbedAuthor', 'EmbedBase', 'EmbedCore', 'EmbedField', 'EmbedFooter',
    'EmbedImage', 'EmbedProvider', 'EmbedThumbnail', 'EmbedVideo', )

from datetime import datetime

from ..backend.utils import copy_docs
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
    
    def __eq__(self,other):
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
            'name' : self.name,
            'value' : self.value,
                }
        
        inline = self.inline
        if inline:
            field_data['inline'] = inline
        
        return field_data


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
        Creates an `EmbedCore`` object from the data sent by Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embed data received from Discord.
        
        Returns
        -------
        self : ``EmbedCore``
        """
        self = cls.__new__(cls)
        
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
    
    @copy_docs(EmbedBase.clear)
    def clear(self):
        self.author = None
        self.color = None
        self.description = None
        self.fields.clear()
        self.footer = None
        self.image = None
        self.provider = None
        self.thumbnail = None
        self.timestamp = None
        self.title = None
        self.type = None
        self.url = None
        self.video = None
    
    @property
    def contents(self):
        """
        Returns the embed's contents.
        
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
    _data : `dict` of (`str`, `Any`) items
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
    __slots__ = ('_data',)
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
        self._data = data = {}
        
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
    
    @copy_docs(EmbedBase.__len__)
    def __len__(self):
        data = self._data
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
    
    @copy_docs(EmbedBase.__bool__)
    def __bool__(self):
        data = self._data
        data_length = len(data)
        if data_length == 0:
            return False
        
        if data_length == 1:
            try:
                field_datas = data['fields']
            except KeyError:
                pass
            else:
                if not field_datas:
                    return False
        
        return True
    
    
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
        data = self._data
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
    
    @classmethod
    def from_data(cls, data):
        """
        Creates an embed from the data sent by Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Embed data received from Discord.
        
        Returns
        -------
        self : ``Embed``
        """
        self = object.__new__(cls)
        self._data = data
        return self
    
    def to_data(self):
        """
        Returns the embed's `._data`.
        
        This method is for compatibility with other embed-likes. When sending embed in message this method is called
        for getting it's data.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return self._data
    
    @copy_docs(EmbedBase.clear)
    def clear(self):
        data = self._data
        fields = data.get('fields', None)
        data.clear()
        if (fields is not None):
            fields.clear()
            data['fields'] = fields
    
    # Properties
    
    # `.author`
    
    @property
    def author(self):
        """
        A get-set-del property for accessing the embed's author.
        
        Accepts and returns `None` or an ``EmbedAuthor`` object.
        """
        try:
            author_data = self._data['author']
        except KeyError:
            return None
        
        return EmbedAuthor.from_data(author_data)
    
    @author.setter
    def author(self, value):
        self._data['author'] = value.to_data()
    
    @author.deleter
    def author(self):
        try:
            del self._data['author']
        except KeyError:
            pass
    
    # `.color`
    
    @property
    def color(self):
        """
        A get-set-del property for accessing the embed's color.
        
        Accepts and returns `None` or a ``Color`` (/ `int`) object.
        """
        return self._data.get('color', None)
    
    @color.setter
    def color(self, value):
        self._data['color'] = value
    
    @color.deleter
    def color(self):
        try:
            del self._data['color']
        except KeyError:
            pass
    
    # `.description`
    
    @property
    def description(self):
        """
        A get-set-del property for accessing the embed's description.
        
        Accepts and returns `None` or a `str` instance.
        """
        return self._data.get('description', None)
    
    @description.setter
    def description(self, value):
        self._data['description'] = value
    
    @description.deleter
    def description(self):
        try:
            del self._data['description']
        except KeyError:
            pass
    
    # `.fields`
    
    @property
    def fields(self):
        try:
            field_datas = self._data['fields']
        except KeyError:
            self._data['fields'] = field_datas = []
        
        return _EmbedFieldsProxy(field_datas)
    
    @fields.setter
    def fields(self, value):
        """
        A get-set-del property for accessing the embed's fields.
        
        Accepts an `iterable` of ``EmbedField``objects. Meanwhile returns an ``_EmbedFieldsProxy`` instance,
        through what the respective embed's fields can be modified directly.
        """
        data = self._data
        try:
            fields_data = data['fields']
        except KeyError:
            fields_data = data['fields'] = []
        
        if type(value) is _EmbedFieldsProxy:
            new_fields_data = value._data
        else:
            new_fields_data = list(field.to_data() for field in value)
        
        fields_data.clear()
        fields_data.extend(new_fields_data)
    
    @fields.deleter
    def fields(self):
        try:
            field_datas = self._data['fields']
        except KeyError:
            pass
        else:
            field_datas.clear()
    
    # `.footer`
    
    @property
    def footer(self):
        """
        A get-set-del property for accessing the embed's footer.
        
        Accepts and returns `None` or an ``EmbedFooter`` object.
        """
        try:
            footer_data = self._data['footer']
        except KeyError:
            return None
        
        return EmbedFooter.from_data(footer_data)
    
    @footer.setter
    def footer(self, value):
        self._data['footer'] = value.to_data()
    
    @footer.deleter
    def footer(self):
        try:
            del self._data['footer']
        except KeyError:
            pass
    
    # `.image`
    
    @property
    def image(self):
        """
        A get-set-del property for accessing the embed's image.
        
        Accepts and returns `None` or an ``EmbedImage`` object.
        """
        try:
            image_data = self._data['image']
        except KeyError:
            return None
        
        return EmbedImage.from_data(image_data)
    
    @image.setter
    def image(self, value):
        self._data['image'] = value.to_data()
    
    @image.deleter
    def image(self):
        try:
            del self._data['image']
        except KeyError:
            pass
        
    # `.provider`
    
    @property
    def provider(self):
        """
        A get-del property for accessing the embed's provider.
        
        Returns `None` or an ``EmbedProvider`` object.
        
        Embed providers cannot be set, they are receive only.
        """
        try:
            provider_data = self._data['provider']
        except KeyError:
            return None
        
        return EmbedProvider.from_data(provider_data)
    
    @provider.deleter
    def provider(self):
        try:
            del self._data['provider']
        except KeyError:
            pass
    
    # `.thumbnail`
    
    @property
    def thumbnail(self):
        """
        A get-set-del property for accessing the embed's thumbnail.
        
        Accepts and returns `None` or an ``EmbedThumbnail`` object.
        """
        try:
            thumbnail_data = self._data['thumbnail']
        except KeyError:
            return None
        
        return EmbedThumbnail.from_data(thumbnail_data)
    
    @thumbnail.setter
    def thumbnail(self, value):
        self._data['thumbnail'] = value.to_data()
    
    @thumbnail.deleter
    def thumbnail(self):
        try:
            self._data['thumbnail']
        except KeyError:
            pass
    
    # `.timestamp`
    
    @property
    def timestamp(self):
        """
        A get-set-del property for accessing the embed's timestamp.
        
        Accepts and returns `None` or a `datetime` object.
        """
        try:
            timestamp_value = self._data['timestamp']
        except KeyError:
            return None
        
        return parse_time(timestamp_value)
    
    @timestamp.setter
    def timestamp(self, value):
        self._data['timestamp'] = value.isoformat()
    
    @timestamp.deleter
    def timestamp(self):
        try:
            del self._data['timestamp']
        except KeyError:
            pass
    
    # `.title`
    
    @property
    def title(self):
        """
        A get-set-del property for accessing the embed's title.
        
        Accepts and returns `None` or a `str` instance.
        """
        return self._data.get('title', None)
    
    @title.setter
    def title(self, value):
        self._data['title'] = value
    
    @title.deleter
    def title(self):
        try:
            del self._data['title']
        except KeyError:
            pass
    
    # `.type`
    
    @property
    def type(self):
        """
        A get-set-del property for accessing the embed's type.
        
        Accepts and returns `None` or a `str` instance.
        """
        return self._data.get('type', None)
    
    @type.setter
    def type(self, value):
        self._data['type'] = value
    
    @type.deleter
    def type(self):
        try:
            del self._data['type']
        except KeyError:
            pass
    
    # `.url`
    
    @property
    def url(self):
        """
        A get-set-del property for accessing the embed's url.
        
        Accepts and returns `None` or a `str` instance.
        """
        return self._data.get('url', None)
    
    @url.setter
    def url(self, value):
        self._data['url'] = value
    
    @url.deleter
    def url(self):
        try:
            del self._data['url']
        except KeyError:
            pass
    
    # `.video`
    
    @property
    def video(self):
        """
        A get-del property for accessing the embed's video.
        
        Returns `None` or an ``EmbedVideo`` object.
        
        Embed videos cannot be set, they are receive only.
        """
        try:
            video_data = self._data['video']
        except KeyError:
            return None
        
        return EmbedVideo.from_data(video_data)
    
    @video.deleter
    def video(self):
        try:
            del self._data['video']
        except KeyError:
            pass
    
    # Methods
    
    # author
    
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
        
        self._data['author'] = author_data
        return self
    
    # fields

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
            'name': name,
            'value': value,
        }
        
        if inline:
            field_data['inline'] = inline
        
        try:
            field_datas = self._data['fields']
        except KeyError:
            self._data['fields'] = [field_data]
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
            'name': name,
            'value': value,
        }
        
        if inline:
            field_data['inline'] = inline
        
        try:
            field_datas = self._data['fields']
        except KeyError:
            self._data['fields'] = [field_data]
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
            field_datas = self._data['fields']
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
            field_datas = self._data['fields']
        except KeyError:
            self._data['fields'] = [field_data]
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
            fields = self._data['fields']
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
            fields = self._data['fields']
        except KeyError:
            raise IndexError('Index out of the fields\' range.') from None
        
        try:
            del fields[index]
        except IndexError as err:
            err.args = ('Index out of the fields\' range.', )
            raise
    
    remove_field = del_field
    
    # footer
    
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
            'text': text,
        }
        
        if (icon_url is not None):
            footer_data['icon_url'] = icon_url
        
        self._data['footer'] = footer_data
        return self
    
    # image
    
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
            'url': url,
        }
        
        self._data['image'] = image_data
        return self
    
    # thumbnail
    
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
            'url': url,
        }
        
        self._data['thumbnail'] = thumbnail_data
        return self


class _EmbedFieldsProxy:
    """
    A reflection of an `Embed` object's fields. The instances of this type allow direct modifications of their
    respective embed's fields.
    
    Attributes
    ----------
    _data : `list` of (`dict` of (`str`, `Any`) items)
        Raw data containing the respective embed's fields.
    """
    __slots__ = ('_data',)
    def __init__(self, data):
        """
        Creates a ``_EmbedFieldsProxy`` object.
        
        Parameters
        ----------
        data : `list` of (`dict` of (`str`, `Any`) items)
            Raw data containing the respective embed's fields.
        """
        self._data = data
        
    def clear(self):
        """
        Removes all of the respective embed's fields.
        """
        self._data.clear()
    
    def __len__(self):
        """Returns how much fields the respective embed has."""
        return len(self._data)
    
    def __repr__(self):
        """Returns the representation of the object."""
        return f'<{self.__class__.__name__} length={len(self._data)}>'
    
    def __getitem__(self, index):
        """Returns the embed field on the given index."""
        return EmbedField.from_data(self._data[index])
    
    def __setitem__(self, index, field):
        """Sets the given embed field object on the given index."""
        self._data[index] = field.to_data()
    
    def __delitem__(self, index):
        """Deletes the field on the given index"""
        del self._data[index]
    
    def append(self, field):
        """
        Appends the respective embed's fields with the given field.
        
        Parameters
        ----------
        field : ``EmbedField``
            The field to append the embed's field with.
        """
        self._data.append(field.to_data())
    
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
        self._data.insert(index,field.to_data())
    
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
        
        self._data.append(field_data)
    
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
        
        self._data.insert(index, field_data)
    
    def __iter__(self):
        """
        Iterates over the respective embed's fields.
        
        This method is a generator.
        """
        for field_data in self._data:
            yield EmbedField.from_data(field_data)
    
    def __reversed__(self):
        """
        Reverse iterates over the respective embed's fields.
        
        This method is a generator.
        """
        for field_data in reversed(self._data):
            yield EmbedField.from_data(field_data)
