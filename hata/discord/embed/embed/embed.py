__all__ = ('Embed',)

import warnings

from scarletio import RichAttributeErrorBaseType

from ...utils import sanitize_mentions

from ..embed_author import EmbedAuthor
from ..embed_field import EmbedField
from ..embed_footer import EmbedFooter
from ..embed_image import EmbedImage
from ..embed_thumbnail import EmbedThumbnail
from ..embed_video import EmbedVideo

from .fields import (
    parse_author, parse_color, parse_description, parse_fields, parse_footer, parse_image, parse_provider,
    parse_thumbnail, parse_timestamp, parse_title, parse_type, parse_url, parse_video, put_author_into, put_color_into,
    put_description_into, put_fields_into, put_footer_into, put_image_into, put_provider_into, put_thumbnail_into,
    put_timestamp_into, put_title_into, put_type_into, put_url_into, put_video_into, validate_author, validate_color,
    validate_description, validate_fields, validate_footer, validate_image, validate_provider, validate_thumbnail,
    validate_timestamp, validate_title, validate_type, validate_url, validate_video
)
from .preinstanced import EmbedType


class Embed(RichAttributeErrorBaseType):
    """
    Represents Discord embedded content.
    
    Attributes
    ----------
    author : `None`, ``EmbedAuthor``
        Author information.
    color : `None`, ``Color``
        The color code of the embed. Passing `0` means black, not like at the case of roles.
    description : `None`, `str`
        The main content of the embed.
    fields : `None`, `list` of ``EmbedField``
        Fields' information.
    footer : `None`, ``EmbedFooter``
        Footer information.
    image : `None`, ``EmbedImage``
        Image information.
    provider : `None`, ``EmbedProvider``
        Provider information.
    thumbnail : `None`, ``EmbedThumbnail``
        Thumbnail information.
    timestamp : `None`, `datetime`
        Timestamp of the embed's content. Shows up next to the ``.footer``.
    title : `None`, `str`
        The title of the embed. Shows at the top with intense white characters.
    type : ``EmbedType``
        The type of the embed.Webhook embeds' type must be `EmbedType.rich`.
    url : `None`, `str`
        Url of the embed. If defined, the embed's `title` will show up as a hyper link pointing to the `url`.
    video : `None`, ``EmbedVideo``
        Video information.
    
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
        await client.message_create(channel, embed = embed, file = ('image.png', file))
    ```
    
    Note that you should use async io wrappers, but one which do not closes on `.close` either, but it resets
    itself instead, because if the request fails, the io would be closed and the request could not be done the
    second time.
    """
    __slots__ = (
        'author', 'color', 'description', 'fields', 'footer', 'image', 'provider', 'thumbnail', 'timestamp', 'title',
        'type', 'url', 'video'
    )
    
    def __new__(
        cls,
        title = ...,
        description = ...,
        *extra_positional_parameters, # For deprecations
        type_ = ..., # Deprecated
        author = ...,
        color = ...,
        embed_type = ...,
        fields = ...,
        footer = ...,
        image = ...,
        provider = ...,
        thumbnail = ...,
        timestamp = ...,
        url = ...,
        video = ...,
    ):
        """
        Creates an embed.
        
        Parameters
        ----------
        title : `None`, `str`, Optional
            The title of the embed. Shows at the top with intense white characters.
        description : `None`, `str`, Optional
            The main content of the embed.
        author : `None`, ``EmbedAuthor``, Optional (Keyword only)
            Author information.
        color : `None`, ``Color``, `int`, Optional (Keyword only)
            The color code of the embed. Passing `0` means black, not like at the case of roles.
        embed_type : `EmbedType`, `str`, Optional (Keyword only)
            The type of the embed. Defaults to `EmbedType.rich`.
        fields : `None`, `iterable` of ``EmbedField``, Optional (Keyword only)
            Fields' information.
        footer : `None`, ``EmbedFooter``, Optional (Keyword only)
            Footer information.
        image : `None`, ``EmbedImage``, Optional (Keyword only)
            Image information.
        provider : `None`, ``EmbedProvider``, Optional (Keyword only)
            Provider information.
        thumbnail : `None`, ``EmbedThumbnail``, Optional (Keyword only)
            Thumbnail information.
        timestamp : `None`, `datetime`, Optional (Keyword only)
            Timestamp of the embed's content. Shows up next to the `footer`.
        url : `None`, `str`, Optional (Keyword only)
            Url of the embed. If defined, the embed's `title` will show up as a hyper link pointing to the `url`.
        video : `None`, `EmbedVideo`, Optional (Keyword only)
            Video information.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # Handle deprecations, there is a lot!
        if extra_positional_parameters:
            extra_positional_parameter_length = len(extra_positional_parameters)
            if extra_positional_parameter_length >= 4:
                warnings.warn(
                    (
                        f'`embed_type` parameter of `{cls.__name__}.__new__` is moved to be a keyword only '
                        f'parameter and the positional usage is deprecated and will be removed in 2023 August.'
                    ),
                    FutureWarning,
                    stacklevel = 2,
                )
                
                embed_type = extra_positional_parameters[3]
            
            
            if extra_positional_parameter_length >= 3:
                warnings.warn(
                    (
                        f'`timestamp` parameter of `{cls.__name__}.__new__` is moved to be a keyword only '
                        f'parameter and the positional usage is deprecated and will be removed in 2023 August.'
                    ),
                    FutureWarning,
                    stacklevel = 2,
                )
                
                timestamp = extra_positional_parameters[2]
            
            
            if extra_positional_parameter_length >= 2:
                warnings.warn(
                    (
                        f'`url` parameter of `{cls.__name__}.__new__` is moved to be a keyword only '
                        f'parameter and the positional usage is deprecated and will be removed in 2023 August.'
                    ),
                    FutureWarning,
                    stacklevel = 2,
                )
                
                url = extra_positional_parameters[1]
            
            
            if extra_positional_parameter_length >= 1:
                warnings.warn(
                    (
                        f'`color` parameter of `{cls.__name__}.__new__` is moved to be a keyword only '
                        f'parameter and the positional usage is deprecated and will be removed in 2023 August.'
                    ),
                    FutureWarning,
                    stacklevel = 2,
                )
                
                color = extra_positional_parameters[0]
        
        
        if (type_ is not ...):
            warnings.warn(
                (
                    f'`type_` parameter of `{cls.__name__}.__new__` has been renamed to `embed_type`. '
                    f'The option for using `type_` will be removed in 2023 August.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            embed_type = type_
        
        # Validate parameters
        
        # title
        if title is ...:
            title = None
        else:
            title = validate_title(title)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # author
        if author is ...:
            author = None
        else:
            author = validate_author(author)
        
        # color
        if color is ...:
            color = None
        else:
            color = validate_color(color)
        
        # embed_type
        if embed_type is ...:
            embed_type = EmbedType.rich
        else:
            embed_type = validate_type(embed_type)
        
        # fields
        if fields is ...:
            fields = None
        else:
            fields = validate_fields(fields)
        
        # footer
        if footer is ...:
            footer = None
        else:
            footer = validate_footer(footer)
        
        # image
        if image is ...:
            image = None
        else:
            image = validate_image(image)
        
        # provider
        if provider is ...:
            provider = None
        else:
            provider = validate_provider(provider)
        
        # thumbnail
        if thumbnail is ...:
            thumbnail = None
        else:
            thumbnail = validate_thumbnail(thumbnail)
        
        # timestamp
        if timestamp is ...:
            timestamp = None
        else:
            timestamp = validate_timestamp(timestamp)
        
        # url
        if url is ...:
            url = None
        else:
            url = validate_url(url)
        # video
        if video is ...:
            video = None
        else:
            video = validate_video(video)
        
        self = object.__new__(cls)
        self.author = author
        self.color = color
        self.description = description
        self.fields = fields
        self.footer = footer
        self.image = image
        self.provider = provider
        self.thumbnail = thumbnail
        self.timestamp = timestamp
        self.title = title
        self.type = embed_type
        self.url = url
        self.video = video
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates an embed object from the data sent by Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Embed data received from Discord.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.author = parse_author(data)
        self.color = parse_color(data)
        self.description = parse_description(data)
        self.fields = parse_fields(data)
        self.footer = parse_footer(data)
        self.image = parse_image(data)
        self.provider = parse_provider(data)
        self.thumbnail = parse_thumbnail(data)
        self.timestamp = parse_timestamp(data)
        self.title = parse_title(data)
        self.type = parse_type(data)
        self.url = parse_url(data)
        self.video = parse_video(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the embed core to json serializable `dict` representing it.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_author_into(self.author, data, defaults, include_internals = include_internals)
        put_color_into(self.color, data, defaults)
        put_description_into(self.description, data, defaults)
        put_fields_into(self.fields, data, defaults)
        put_footer_into(self.footer, data, defaults, include_internals = include_internals)
        put_image_into(self.image, data, defaults, include_internals = include_internals)
        put_thumbnail_into(self.thumbnail, data, defaults, include_internals = include_internals)
        put_timestamp_into(self.timestamp, data, defaults)
        put_title_into(self.title, data, defaults)
        put_type_into(self.type, data, defaults)
        put_url_into(self.url, data, defaults)
        
        if include_internals:
            put_provider_into(self.provider, data, defaults, include_internals = include_internals)
            put_video_into(self.video, data, defaults, include_internals = include_internals)
        
        return data
    
    
    def clear(self):
        """
        Clears the embed.
        """
        self.author = None
        self.color = None
        self.description = None
        self.fields = None
        self.footer = None
        self.image = None
        self.provider = None
        self.thumbnail = None
        self.timestamp = None
        self.title = None
        self.type = None
        self.url = None
        self.video = None
    
    
    def _update_sizes(self, data):
        """
        Updates the size information of the embed.
        
        Called when a ``Message`` is edited, but no `edited` timestamp is included with the data. Returns `0` if
        received data does not contain images, if does, then `1`.
        
        This method tries to update the embed's `image`, `thumbnail` amd `video` with their sizes. If any of those is
        not set already (for any reason), then it also creates them.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
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
                thumbnail.height = thumbnail_data.get('height', 0)
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
    
    
    def _set_sizes(self, data):
        """
        Updates the size information of the embed.
        
        Familiar to ``._update_sizes`` but it not checks whether the embed's images change, just updates them.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
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
        length = 0
        
        for content in self.iter_contents():
            length += len(content)
        
        return length
    
    
    def __bool__(self):
        """Returns whether the embed is not empty."""
        # author
        author = self.author
        if (author is not None) and author:
            return True
        
        # color
        if (self.color is not None):
            return True
        
        # description
        description = self.description
        if (description is not None) and description:
            return True
        
        # fields
        for field in self.iter_fields():
            if field:
                return True
        
        # footer
        footer = self.footer
        if (footer is not None) and footer:
            return True
        
        # image
        image = self.image
        if (image is not None) and image:
            return True
        
        # provider
        provider = self.provider
        if (provider is not None) and provider:
            return True
        
        # thumbnail
        thumbnail = self.thumbnail
        if (thumbnail is not None) and thumbnail:
            return True
        
        # timestamp
        if (self.timestamp is not None):
            return True
        
        # title
        title = self.title
        if (title is not None) and title:
            return True
        
        # type
        # Not applicable
        
        # url
        if (self.url is not None):
            return True
        
        # video
        video = self.video
        if (video is not None) and video:
            return True
        
        return False
    
    
    def __repr__(self):
        """Returns the representation of the embed."""
        return f'<{self.__class__.__name__} length = {len(self)}>'
    
    
    def __eq__(self, other):
        """Returns whether the two embeds are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # author
        if self.author != other.author:
            return False
        
        # color
        if self.color != other.color:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # fields
        if self.fields != other.fields:
            return False
        
        # footer
        if self.footer != other.footer:
            return False
        
        # image
        if self.image != other.image:
            return False
        
        # provider
        if self.provider != other.provider:
            return False
        
        # thumbnail
        if self.thumbnail != other.thumbnail:
            return False
        
        # timestamp
        if self.timestamp != other.timestamp:
            return False
        
        # title
        if self.title != other.title:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # url
        if self.url != other.url:
            return False
        
        # video
        if self.video != other.video:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the embed's hash value."""
        hash_value = 0
        
        # author
        author = self.author
        if (author is not None):
            hash_value ^= 1 << 0
            hash_value ^= hash(author)
        
        # color
        color = self.color
        if (color is not None):
            hash_value ^= 1 << 1
            hash_value ^= color
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= 1 << 2
            hash_value ^= hash(description)
        
        # fields
        fields = self.fields
        if (fields is not None):
            hash_value ^= len(fields) << 3
            
            for field in fields:
                hash_value ^= hash(field)
        
        # footer
        footer = self.footer
        if (footer is not None):
            hash_value ^= 1 << 8
            hash_value ^= hash(footer)
        
        # image
        image = self.image
        if (image is not None):
            hash_value ^= 1 << 9
            hash_value ^= hash(image)
        
        # provider
        provider = self.provider
        if (provider is not None):
            hash_value ^= 1 << 10
            hash_value ^= hash(provider)
        
        # thumbnail
        thumbnail = self.thumbnail
        if (thumbnail is not None):
            hash_value ^= 1 << 11
            hash_value ^= hash(thumbnail)
        
        # timestamp
        timestamp = self.timestamp
        if (timestamp is not None):
            hash_value ^= 1 << 12
            hash_value ^= hash(timestamp)
        
        # title
        title = self.title
        if (title is not None):
            hash_value ^= 1 << 13
            hash_value ^= hash(title)
        
        # type
        hash_value ^= hash(self.type)
        
        # url
        url = self.url
        if (url is not None):
            hash_value ^= 1 << 14
            hash_value ^= hash(url)
        
        # video
        video = self.video
        if (video is not None):
            hash_value ^= 1 << 15
            hash_value ^= hash(video)
        
        return hash_value
    
    
    def clean_copy(self, guild = None):
        """
        Creates a clean copy of the embed by removing the mentions in it's contents.
        
        Parameters
        ----------
        guild : `None`, ``Guild`` = `None`, Optional
            The respective guild as a context to look up guild specific names of entities.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        author = self.author
        if (author is not None):
            author = author.clean_copy(guild)
        new.author = author
        
        new.color = self.color
        new.description = sanitize_mentions(self.description, guild)
        
        fields = self.fields
        if (fields is not None):
            fields = [field.clean_copy(guild) for field in fields]
        new.fields = fields
        
        footer = self.footer
        if (footer is not None):
            footer = footer.clean_copy(guild)
        new.footer = footer
        
        image = self.image
        if (image is not None):
            image = image.clean_copy(guild)
        new.image = image
        
        provider = self.provider
        if (provider is not None):
            provider = provider.clean_copy(guild)
        new.provider = provider
        
        thumbnail = self.thumbnail
        if (thumbnail is not None):
            thumbnail = thumbnail.clean_copy(guild)
        new.thumbnail = thumbnail
        
        new.timestamp = self.timestamp
        new.title = sanitize_mentions(self.title, guild)
        new.type = self.type
        new.url = self.url
        
        video = self.video
        if (video is not None):
            video = video.clean_copy(guild)
        new.video = video
        
        return new
    
    
    def copy(self):
        """
        Copies the embed.
        
        Returns
        -------
        new : `instance<type<self>`
        """
        new = object.__new__(type(self))
        
        author = self.author
        if (author is not None):
            author = author.copy()
        new.author = author
        
        new.color = self.color
        new.description = self.description
        
        fields = self.fields
        if (fields is not None):
            fields = [field.copy() for field in fields]
        new.fields = fields
        
        footer = self.footer
        if (footer is not None):
            footer = footer.copy()
        new.footer = footer
        
        image = self.image
        if (image is not None):
            image = image.copy()
        new.image = image
        
        provider = self.provider
        if (provider is not None):
            provider = provider.copy()
        new.provider = provider
        
        thumbnail = self.thumbnail
        if (thumbnail is not None):
            thumbnail = thumbnail.copy()
        new.thumbnail = thumbnail
        
        new.timestamp = self.timestamp
        new.title = self.title
        new.type = self.type
        new.url = self.url
        
        video = self.video
        if (video is not None):
            video = video.copy()
        new.video = video
        
        return new
    
    
    def copy_with(
        self,
        *,
        author = ...,
        color = ...,
        description = ...,
        embed_type = ...,
        fields = ...,
        footer = ...,
        image = ...,
        provider = ...,
        thumbnail = ...,
        timestamp = ...,
        title = ...,
        url = ...,
        video = ...
    ):
        """
        Copies the embed with the given parameters.
        
        Parameters
        ----------
        author : `None`, ``EmbedAuthor``, Optional (Keyword only)
            Author information.
        color : `None`, ``Color``, `int`, Optional (Keyword only)
            The color code of the embed. Passing `0` means black, not like at the case of roles.
        description : `None`, `str`, Optional (Keyword only)
            The main content of the embed.
        embed_type : ``EmbedType``, `str`, Optional (Keyword only)
            The type of the embed. Webhook embed's type must be `EmbedType.rich`.
        fields : `None`, `iterable` of ``EmbedField``, Optional (Keyword only)
            Fields' information.
        footer : `None`, ``EmbedFooter``, Optional (Keyword only)
            Footer information.
        image : `None`, ``EmbedImage``, Optional (Keyword only)
            Image information.
        provider : `None`, ``EmbedProvider``, Optional (Keyword only)
            Provider information.
        thumbnail : `None`, ``EmbedThumbnail``, Optional (Keyword only)
            Thumbnail information.
        timestamp : `None`, `datetime`, Optional (Keyword only)
            Timestamp of the embed's content. Shows up next to the ``.footer``.
        title : `None`, `str`, Optional (Keyword only)
            The title of the embed. Shows at the top with intense white characters.
        url : `None`, `str`, Optional (Keyword only)
            Url of the embed. If defined, the embed's `title` will show up as a hyper link pointing to the `url`.
        video : `None`, `EmbedVideo`, Optional (Keyword only)
            Video information.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # author
        if author is ...:
            author = self.author
            if (author is not None):
                author = author.copy()
        else:
            author = validate_author(author)
        
        # color
        if color is ...:
            color = self.color
        else:
            color = validate_color(color)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # fields
        if fields is ...:
            fields = self.fields
            if (fields is not None):
                fields = [field.copy() for field in fields]
        else:
            fields = validate_fields(fields)
        
        # footer
        if footer is ...:
            footer = self.footer
            if (footer is not None):
                footer = footer.copy()
        else:
            footer = validate_footer(footer)
        
        # image
        if image is ...:
            image = self.image
            if (image is not None):
                image = image.copy()
        else:
            image = validate_image(image)
        
        # provider
        if provider is ...:
            provider = self.provider
            if (provider is not None):
                provider = provider.copy()
        else:
            provider = validate_provider(provider)
        
        # thumbnail
        if thumbnail is ...:
            thumbnail = self.thumbnail
            if (thumbnail is not None):
                thumbnail = thumbnail.copy()
        else:
            thumbnail = validate_thumbnail(thumbnail)
        
        # timestamp
        if timestamp is ...:
            timestamp = self.timestamp
        else:
            timestamp = validate_timestamp(timestamp)
        
        # title
        if title is ...:
            title = self.title
        else:
            title = validate_title(title)
        
        # type
        if embed_type is ...:
            embed_type = self.type
        else:
            embed_type = validate_type(embed_type)
        
        # url
        if url is ...:
            url = self.url
        else:
            url = validate_url(url)
        
        # video
        if video is ...:
            video = self.video
            if (video is not None):
                video = video.copy()
        else:
            video = validate_video(video)
        
        new = object.__new__(type(self))
        new.author = author
        new.color = color
        new.description = description
        new.fields = fields
        new.footer = footer
        new.image = image
        new.provider = provider
        new.thumbnail = thumbnail
        new.timestamp = timestamp
        new.title = title
        new.type = embed_type
        new.url = url
        new.video = video
        return new
    
    # Extra Utility
    
    def iter_fields(self):
        """
        Iterates over the fields of the embed.
        
        This method is an iterable generator.
        
        Yields
        ------
        field : ``EmbedField``
        """
        fields = self.fields
        if (fields is not None):
            yield from fields
    
    
    def iter_contents(self):
        """
        Iterates over the embed's contents.
        
        This method is an iterable generator.
        
        Yields
        -------
        contents : `str`
        """
        provider = self.provider
        if (provider is not None):
            yield from provider.iter_contents()
        
        author = self.author
        if (author is not None):
            yield from author.iter_contents()
        
        title = self.title
        if (title is not None):
            yield title
        
        description = self.description
        if (description is not None):
            yield description
        
        for field in self.iter_fields():
            yield from field.iter_contents()
        
        footer = self.footer
        if (footer is not None):
            yield from footer.iter_contents()
    
    
    @property
    def contents(self):
        """
        Returns the embed's contents.
        
        The embed's contents are the following:
        - `.author.name`
        - `.description`
        - `.fields[n].name`
        - `.fields[n].value`
        - `.title`
        - `.footer.text`
        - `.provider.name`
        
        Returns
        -------
        contents : `list` of `str`
        """
        return [*self.iter_contents()]
    
    # Field adder methods

    def add_author(self, name = None, icon_url = None, url = None):
        """
        Adds an ``EmbedAuthor`` to the embed with the given parameters.
        
        Parameters
        ----------
        name : `None`, `str` = `None`, Optional
            The name of the author.
        icon_url : `None`, `str` = `None`, Optional
            An url of the author's icon. Can be http(s) or attachment.
        url : `None`, `str` = `None`, Optional
            The url of the author.
        
        Returns
        -------
        self : `self`
        """
        self.author = EmbedAuthor(name, icon_url, url)
        return self
    
    # fields

    def add_field(self, name, value, inline = False):
        """
        Adds an ``EmbedField`` to the end of the embed's fields.
        
        Parameters
        ----------
        name : `str`
            The name of the field.
        value : `str`
            The value of the field.
        inline : `bool` = `False`, Optional
            Whether this field should display inline.
        
        Returns
        -------
        self : `self`
        """
        field = EmbedField(name, value, inline)
        
        fields = self.fields
        if fields is None:
            fields = []
            self.fields = fields
        
        fields.append(field)
        return self
    
    
    def insert_field(self, index, name, value, inline = False):
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
        inline : `bool` = `False`, Optional
            Whether this field should display inline.
        
        Returns
        -------
        self : `self`
        """
        field = EmbedField(name, value, inline)
        
        fields = self.fields
        if fields is None:
            fields = []
            self.fields = fields
        
        fields.insert(index, field)
        return self
    
    
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
        fields = self.fields
        if fields is None:
            raise IndexError(
                f'Index out of the fields\' range, got index = {index!r}; length = 0.'
            ) from None
        
        try:
            field = fields[index]
        except IndexError:
            raise IndexError(
                f'Index out of the fields\' range, got index = {index!r}; length = {len(fields)!r}.'
            ) from None
        
        return field
    
    
    def append_field(self, field):
        """
        Appends the embed's fields with the given field.
        
        Parameters
        ----------
        field : ``EmbedField``
            The field to append the embed's field with.
        """
        if not isinstance(field, EmbedField):
            raise TypeError(
                f'`field` can be `{EmbedField.__name__}`, got {field.__class__.__name__}; {field!r}.'
            )
        
        fields = self.fields
        if fields is None:
            fields = []
            self.fields = fields
        
        fields.append(field)
    
    
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
        if not isinstance(field, EmbedField):
            raise TypeError(
                f'`field` can be `{EmbedField.__name__}`, got {field.__class__.__name__}; {field!r}.'
            )
        
        fields = self.fields
        if fields is None:
            raise IndexError(
                f'Index out of the fields\' range, got index={index!r}; length = 0.'
            ) from None
        
        
        try:
            fields[index] = field
        except IndexError:
            raise IndexError(
                f'Index out of the fields\' range, got index={index!r}; length = {len(fields)!r}.'
            ) from None
    
    
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
        fields = self.fields
        if fields is None:
            raise IndexError(
                f'Index out of the fields\' range, got index = {index!r}; length = 0.'
            )
        
        try:
            del fields[index]
        except IndexError:
            raise IndexError(
                f'Index out of the fields\' range, got index = {index!r}; length = {len(fields)!r}.'
            ) from None
        
        if not fields:
            self.fields = None
    
    remove_field = del_field
    
    # footer
    
    def add_footer(self, text, icon_url = None):
        """
        Adds an ``EmbedFooter`` to the embed with the given parameters.
        
        Parameters
        ----------
        text : `str`
            The footer's text.
        icon_url : `None`, `str` = `None`, Optional
            An url of the footer's icon. Can be http(s) or attachment.
        
        Returns
        -------
        self : `self`
        """
        self.footer = EmbedFooter(text, icon_url)
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
        self : `self`
        """
        self.image = EmbedImage(url)
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
        self : `self`
        """
        self.thumbnail = EmbedThumbnail(url)
        return self
    
    
    @property
    def _data(self):
        """
        Deprecated and will be removed in 2023 August.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}._data` is deprecated, and will be removed in 2023 August. '
                f'Please use `.to_data()` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.to_data(include_internals = True)
    
    
    @_data.setter
    def _data(self, data):
        warnings.warn(
            (
                f'`{self.__class__.__name__}._data` is deprecated, and will be removed in 2023 August. '
                f'Please use `.from_data(data)` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        self.author = parse_author(data)
        self.color = parse_color(data)
        self.description = parse_description(data)
        self.fields = parse_fields(data)
        self.footer = parse_footer(data)
        self.image = parse_image(data)
        self.provider = parse_provider(data)
        self.thumbnail = parse_thumbnail(data)
        self.timestamp = parse_timestamp(data)
        self.title = parse_title(data)
        self.type = parse_type(data)
        self.url = parse_url(data)
        self.video = parse_video(data)
