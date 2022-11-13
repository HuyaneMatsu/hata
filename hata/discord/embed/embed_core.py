__all__ = ('EmbedCore', )

from scarletio import copy_docs

from ..color import Color
from ..utils import datetime_to_timestamp, sanitize_mentions, timestamp_to_datetime

from .embed_base import (
    EmbedAuthor, EmbedBase, EmbedField, EmbedFooter, EmbedImage, EmbedProvider, EmbedThumbnail, EmbedVideo
)


class EmbedCore(EmbedBase):
    """
    Represents Discord embedded content. There are two defined embed classes, the other one is ``Embed``.
    
    Each embed what is received from Discord is stored as ``EmbedCore`` object for better operation support. This
    embed type is a valid embed type to send, but it is more cumbersome to build up, because it requires extra
    imports and it is slower to serialize.
    
    Attributes
    ----------
    author : `None`, ``EmbedAuthor``
        Author information.
    color : `None`, ``Color``, `int`
        The color code of the embed. Passing `0` means black, not like at the case of roles.
    description : `None`, `str`
        The main content of the embed.
    fields : `list` of ``EmbedField``
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
        Timestamp of the embed's content. Shows up next to the ``.footer`` separated with a `'|'` character.
    title : `None`, `str`
        The title of the embed. Shows at the top with intense white characters.
    type : `None`, `str`
        The type of the embed. Can be one of `EXTRA_EMBED_TYPES`'s elements. Webhook embeds' type must be `'rich'`.
    url : `None`, `str`
        Url of the embed. If defined, the embed's `title` will show up as a hyper link pointing to the `url`.
    video : `None`, `EmbedVideo`
        Video information.
    """
    __slots__ = (
        'author', 'color', 'description', 'fields', 'footer', 'image', 'provider', 'thumbnail', 'timestamp', 'title',
        'type', 'url', 'video'
    )
    
    def __init__(self, title=None, description = None, color = None, url = None, timestamp=None, type_='rich'):
        """
        Creates an embed core instance. Accepts the base parameters of the embed and sets the other ones as `None`.
        
        Parameters
        ----------
        title : `None`, `str` = `None`, Optional
            The title of the embed. Shows at the top with intense white characters.
        description : `None`, `str` = `None`, Optional
            The main content of the embed.
        color : `None`, ``Color``, `int` = `None`, Optional
            The color code of the embed. Passing `0` means black, not like at the case of roles.
        url : `None`, `str` = `None`, Optional
            Url of the embed. If defined, the embed's `title` will show up as a hyper link pointing to the `url`.
        timestamp : `None`, `datetime` = `None`, Optional
            Timestamp of the embed's content. Shows up next to the `footer` separated with a `'|'` character.
        type_ : `None`, `str` = `'rich'`, Optional
            The type of the embed. Defaults to `'rich'`.
        """
        self.author = None
        self.color = color
        self.description = description
        self.fields = []
        self.footer = None
        self.image = None
        self.provider = None
        self.thumbnail = None
        self.timestamp = timestamp
        self.title = title
        self.type = type_ # must be `rich` for webhook embeds
        self.url = url
        self.video = None
    
    
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
        
        # author
        try:
            author_data = data['author']
        except KeyError:
            author = None
        else:
            author = EmbedAuthor.from_data(author_data)
        self.author = author
        
        # color
        try:
            color_data = data['color']
        except KeyError:
            color = None
        else:
            color = Color(color_data)
        self.color = color
        
        # description
        self.description = data.get('description', None)
        
        #fields
        try:
            field_datas = data['fields']
        except KeyError:
            fields = []
        else:
            fields = [EmbedField.from_data(field_data) for field_data in field_datas]
        self.fields = fields
        
        # footer
        try:
            footer_data = data['footer']
        except KeyError:
            footer = None
        else:
            footer = EmbedFooter.from_data(footer_data)
        self.footer = footer
        
        # image
        try:
            image_data = data['image']
        except KeyError:
            image = None
        else:
            image = EmbedImage.from_data(image_data)
        self.image = image
        
        # provider
        try:
            provider_data = data['provider']
        except KeyError:
            provider = None
        else:
            provider = EmbedProvider.from_data(provider_data)
        self.provider = provider
        
        # thumbnail
        try:
            thumbnail_data = data['thumbnail']
        except KeyError:
            thumbnail = None
        else:
            thumbnail = EmbedThumbnail.from_data(thumbnail_data)
        self.thumbnail = thumbnail
        
        # timestamp
        try:
            timestamp_data = data['timestamp']
        except KeyError:
            timestamp = None
        else:
           timestamp = timestamp_to_datetime(timestamp_data)
        self.timestamp = timestamp
        
        # title
        self.title = data.get('title', None)
        
        # type
        self.type = data.get('type', None)
        
        # url
        self.url = data.get('url', None)
        
        # video
        try:
            video_data = data['video']
        except KeyError:
            video = None
        else:
            video = EmbedVideo.from_data(video_data)
        self.video = video
        
        return self
    
    
    def to_data(self):
        """
        Converts the embed core to json serializable `dict` representing it.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        # author
        author = self.author
        if (author is not None):
            data['author'] = author.to_data()
        
        # color
        color = self.color
        if (color is not None):
            data['color'] = color
        
        # description
        description = self.description
        if (description is not None):
            data['description'] = description
        
        # fields
        fields = self.fields
        if (fields is not None) and fields:
            data['fields'] = [field.to_data() for field in fields]
        
        # footer
        footer = self.footer
        if (footer is not None):
            data['footer'] = footer.to_data()
        
        # image
        image = self.image
        if (image is not None):
            data['image'] = image.to_data()
        
        # provider
        # Receive only
        
        # thumbnail
        thumbnail = self.thumbnail
        if (thumbnail is not None):
            data['thumbnail'] = thumbnail.to_data()
        
        # timestamp
        timestamp = self.timestamp
        if (timestamp is not None):
            data['timestamp'] = datetime_to_timestamp(timestamp)
        
        # title
        title = self.title
        if (title is not None):
            data['title'] = title
        
        # type
        type_ = self.type
        if (type_ is not None):
            data['type'] = type_
        
        # url
        url = self.url
        if (url is not None):
            data['url'] = url
        
        # video
        # Receive only
        
        return data
    
    
    @copy_docs(EmbedBase.clear)
    def clear(self):
        self.author = None
        self.color = None
        self.description = None
        fields = self.fields
        if (fields is not None):
            fields.clear()
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
        
        # author
        new.author = self.author
        
        # color
        new.color = self.color
        
        # description
        description = self.description
        if (description is not None):
            description = sanitize_mentions(description, message.guild)
        new.description = description
        
        # fields
        new.fields = [
            type(field)(field.name, sanitize_mentions(field.value, message.guild), inline=field.inline)
            for field in self.fields
        ]
        
        # footer
        new.footer = self.footer
        
        # image
        new.image = self.image
        
        # provider
        new.provider = self.provider
        
        # thumbnail
        new.thumbnail = self.thumbnail
        
        # timestamp
        new.timestamp = self.timestamp
        
        # title
        new.title = self.title
        
        # type
        new.type = self.type
        
        # url
        new.url = self.url
        
        # video
        new.video = self.video
        
        return new
    
    
    @copy_docs(EmbedBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.author = self.author
        new.color = self.color
        new.description = self.description
        
        fields = self.fields
        if (fields is not None):
            fields = [field.copy() for field in fields]
        new.fields = fields
        
        new.footer = self.footer
        new.image = self.image
        new.provider = self.provider
        new.thumbnail = self.thumbnail
        new.timestamp = self.timestamp
        new.title = self.title
        new.type = self.type
        new.url = self.url
        new.video = self.video
        
        return new
    
    
    @copy_docs(EmbedBase.copy_with)
    def copy_with(self, **kwargs):
        # author
        try:
            author = kwargs.pop('author')
        except KeyError:
            author = self.author
            if (author is not None):
                author = author.copy()
        
        # color
        try:
            color = kwargs.pop('color')
        except KeyError:
            color = self.color
        
        # description
        try:
            description = kwargs.pop('description')
        except KeyError:
            description = self.description
        
        # fields
        try:
            fields = kwargs.pop('fields')
        except KeyError:
            fields = self.fields
            if (fields is not None):
                fields = [field.copy() for field in fields]
        
        # footer
        try:
            footer = kwargs.pop('footer')
        except KeyError:
            footer = self.footer
            if (footer is not None):
                footer = footer.copy()
        
        # image
        try:
            image = kwargs.pop('image')
        except KeyError:
            image = self.image
            if (image is not None):
                image = image.copy()
        
        # provider
        try:
            provider = kwargs.pop('provider')
        except KeyError:
            provider = self.provider
            if (provider is not None):
                provider = provider.copy()
        
        # thumbnail
        try:
            thumbnail = kwargs.pop('thumbnail')
        except KeyError:
            thumbnail = self.thumbnail
            if (thumbnail is not None):
                thumbnail = thumbnail.copy()
        
        # timestamp
        try:
            timestamp = kwargs.pop('timestamp')
        except KeyError:
            timestamp = self.timestamp
        
        # title
        try:
            title = kwargs.pop('title')
        except KeyError:
            title = self.title
        
        # type
        try:
            type_ = kwargs.pop('type')
        except KeyError:
            type_ = self.type
        
        # url
        try:
            url = kwargs.pop('url')
        except KeyError:
            url = self.url
        
        # video
        try:
            video = kwargs.pop('video')
        except KeyError:
            video = self.video
            if (video is not None):
                video = video.copy()
        
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
        
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
        new.type = type_
        new.url = url
        new.video = video
        
        return new
