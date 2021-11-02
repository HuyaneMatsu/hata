__all__ = ('EmbedCore', )

from ...backend.utils import copy_docs

from ..utils import timestamp_to_datetime, sanitize_mentions, datetime_to_timestamp
from ..color import Color

from .embed_base import EmbedBase, EmbedFooter, EmbedImage, EmbedThumbnail, EmbedVideo, EmbedProvider, EmbedAuthor, \
    EmbedField

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
           timestamp = timestamp_to_datetime(timestamp_data)
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
            data['timestamp'] = datetime_to_timestamp(timestamp)
        
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
        try:
            author = kwargs.pop('author')
        except KeyError:
            author = self.author
            if (author is not None):
                author = author.copy()
        
        try:
            color = kwargs.pop('color')
        except KeyError:
            color = self.color
        
        try:
            description = kwargs.pop('description')
        except KeyError:
            description = self.description
        
        try:
            fields = kwargs.pop('fields')
        except KeyError:
            fields = self.fields
            if (fields is not None):
                fields = [field.copy() for field in fields]
        
        try:
            footer = kwargs.pop('footer')
        except KeyError:
            footer = self.footer
            if (footer is not None):
                footer = footer.copy()
        
        try:
            image = kwargs.pop('image')
        except KeyError:
            image = self.image
            if (image is not None):
                image = image.copy()
        
        try:
            provider = kwargs.pop('provider')
        except KeyError:
            provider = self.provider
            if (provider is not None):
                provider = provider.copy()
        
        try:
            thumbnail = kwargs.pop('thumbnail')
        except KeyError:
            thumbnail = self.thumbnail
            if (thumbnail is not None):
                thumbnail = thumbnail.copy()
        
        try:
            timestamp = kwargs.pop('timestamp')
        except KeyError:
            timestamp = self.timestamp
        
        try:
            title = kwargs.pop('title')
        except KeyError:
            title = self.title
        
        try:
            type_ = kwargs.pop('type')
        except KeyError:
            type_ = self.type
        
        try:
            url = kwargs.pop('url')
        except KeyError:
            url = self.url
        
        try:
            video = kwargs.pop('video')
        except KeyError:
            video = self.video
            if (video is not None):
                video = video.copy()
        
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: `{kwargs}`')
        
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
