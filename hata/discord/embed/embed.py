__all__ = ('Embed', )

from scarletio import copy_docs

from ..utils import datetime_to_timestamp, timestamp_to_datetime

from .embed_base import (
    EmbedAuthor, EmbedBase, EmbedField, EmbedFooter, EmbedImage, EmbedProvider, EmbedThumbnail, EmbedVideo,
    _warn_bad_embed_author_constructor_parameter_order
)


RICH_EMBED_FIELDS = frozenset((
    'author',
    'auto_moderation_message',
    'fields',
    'footer',
    'image',
    'provider',
    'thumbnail',
    'video',
))


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
        await client.message_create(channel, embed = embed, file=('image.png', file))
    ```
    
    Note that you should use async io wrappers, but one which do not closes on `.close` either, but it resets
    itself instead, because if the request fails, the io would be closed and the request could not be done the
    second time.
    """
    __slots__ = ('_data',)
    
    def __init__(self, title=None, description = None, color = None, url = None, timestamp=None, type_='rich'):
        """
        Creates an embed instance. Accepts the base parameters of the embed.
        
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
        self._data = data = {}
        
        # color
        if (color is not None):
            data['color'] = color
        
        # description
        if (description is not None):
            if not isinstance(description, str):
                description = str(description)
            
            data['description'] = description
        
        # title
        if (title is not None):
            if not isinstance(title, str):
                title = str(title)
            
            data['title'] = title
            
        # type
        if (type_ is not None):
            data['type'] = type_
        
        # url
        if (url is not None):
            data['url'] = url
        
        # timestamp
        if (timestamp is not None):
            data['timestamp'] = datetime_to_timestamp(timestamp)
    
    
    @copy_docs(EmbedBase.__len__)
    def __len__(self):
        data = self._data
        length = 0
        
        # author
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
                length += len(author_name)
        
        # color
        # Not applicable
        
        
        # description
        try:
            description = data['description']
        except KeyError:
            pass
        else:
            length += len(description)
        
        # fields
        try:
            field_datas = data['fields']
        except KeyError:
            pass
        else:
            for field_data in field_datas:
                length += len(field_data['name'])
                length += len(field_data['value'])
        
        # footer
        try:
            footer_data = data['footer']
        except KeyError:
            pass
        else:
            length += len(footer_data['text'])
        
        # image
        # Not applicable
        
        # provider
        try:
            provider_data = data['provider']
        except KeyError:
            pass
        else:
            try:
                provider_name = provider_data['name']
            except KeyError:
                pass
            else:
                length += len(provider_name)
        
        # thumbnail
        # Not applicable
        
        # timestamp
        # Not applicable
        
        # title
        try:
            title = data['title']
        except KeyError:
            pass
        else:
            length += len(title)
        
        # type
        # Not applicable
        
        # url
        # Not applicable
        
        # video
        # Not applicable
        
        return length
    
    
    @copy_docs(EmbedBase.__bool__)
    def __bool__(self):
        data = self._data
        data_length = len(data) - ('type' in data)
        
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
    @copy_docs(EmbedBase.contents)
    def contents(self):
        data = self._data
        contents = []
        
        # author
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
                contents.append(author_name)
        
        # color
        # Not a text field
        
        # description
        try:
            description = data['description']
        except KeyError:
            pass
        else:
            contents.append(description)
        
        # fields
        try:
            field_datas = data['fields']
        except KeyError:
            pass
        else:
            for field_data in field_datas:
                contents.append(field_data['name'])
                contents.append(field_data['value'])
        
        # footer
        try:
            footer_data = data['footer']
        except KeyError:
            pass
        else:
            contents.append(footer_data['text'])
        

        # image
        # Has no text fields
        
        # provider
        try:
            provider_data = data['provider']
        except KeyError:
            pass
        else:
            try:
                provider_name = provider_data['name']
            except KeyError:
                pass
            else:
                contents.append(provider_name)
                
        # thumbnail
        # Has no text fields
        
        # title
        try:
            title = data['title']
        except KeyError:
            pass
        else:
            contents.append(title)
        
        # type
        # Not a text field
        
        # url
        # Not a text field
        
        # type
        # Not a text field
        
        # url
        # Not a text field
        
        # video
        # Has no text fields
        
        return contents
    
    
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
    
    
    @copy_docs(EmbedBase.copy)
    def copy(self):
        new_data = {}
        
        for key, value in self._data.items():
            if value is None:
                continue
            
            if key in RICH_EMBED_FIELDS:
                if key == 'fields':
                    value = [field_data.copy() for field_data in value]
                
                else:
                    value = value.copy()
            
            new_data[key] = value
        
        new = object.__new__(type(self))
        new._data = new_data
        return new
    
    
    @copy_docs(EmbedBase.copy_with)
    def copy_with(self, **kwargs):
        data = self._data
        
        # author
        try:
            author = kwargs.pop('author')
        except KeyError:
            author_data = data.get('author', None)
            if (author_data is not None):
                author_data = author_data.copy()
        else:
            if (author is None):
                author_data = None
            else:
                author_data = author.to_data()
        
        # color
        try:
            color = kwargs.pop('color')
        except KeyError:
            color = data.get('color', None)
        
        # description
        try:
            description = kwargs.pop('description')
        except KeyError:
            description = data.get('description', None)
        
        # fields
        try:
            fields = kwargs.pop('fields')
        except KeyError:
            field_datas = data.get('fields', None)
            if (field_datas is not None):
                field_datas = [field_data.copy() for field_data in field_datas]
        else:
            if (fields is None):
                field_datas = None
            else:
                field_datas = [field.to_data() for field in fields]
        
        # footer
        try:
            footer = kwargs.pop('footer')
        except KeyError:
            footer_data = data.get('footer', None)
            if (footer_data is not None):
                footer_data = footer_data.copy()
        else:
            if (footer is None):
                footer_data = None
            else:
                footer_data = footer.to_data()
        
        # image
        try:
            image = kwargs.pop('image')
        except KeyError:
            image_data = data.get('image', None)
            if (image_data is not None):
                image_data = image_data.copy()
        else:
            if (image is None):
                image_data = None
            else:
                image_data = image.to_data()
        
        # provider
        try:
            provider = kwargs.pop('provider')
        except KeyError:
            provider_data = data.get('provider', None)
            if (provider_data is not None):
                provider_data = provider_data.copy()
        else:
            if (provider is None):
                provider_data = None
            else:
                provider_data = provider.to_data()
        
        # thumbnail
        try:
            thumbnail = kwargs.pop('thumbnail')
        except KeyError:
            thumbnail_data = data.get('thumbnail', None)
            if (thumbnail_data is not None):
                thumbnail_data = thumbnail_data.copy()
        else:
            if (thumbnail is None):
                thumbnail_data = None
            else:
                thumbnail_data  = thumbnail.to_data()
        
        # timestamp
        try:
            timestamp = kwargs.pop('timestamp')
        except KeyError:
            timestamp_data = data.get('timestamp', None)
        else:
            if (timestamp is None):
                timestamp_data = None
            else:
                timestamp_data = datetime_to_timestamp(timestamp)
        
        # title
        try:
            title = kwargs.pop('title')
        except KeyError:
            title = data.get('title', None)
        
        # type
        try:
            type_ = kwargs.pop('type')
        except KeyError:
            type_ = data.get('type_', None)
        
        # url
        try:
            url = kwargs.pop('url')
        except KeyError:
            url = data.get('url', None)
        
        # video
        try:
            video = kwargs.pop('video')
        except KeyError:
            video_data = data.get('video', None)
            if (video_data is not None):
                video_data = video_data.copy()
        else:
            if (video is None):
                video_data = None
            else:
                video_data = video.to_data()
        
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
        
        
        new_data = {}
        
        # author
        if (author_data is not None):
            new_data['author'] = author_data
        
        # color
        if (color is not None):
            new_data['color'] = color
        
        #description
        if (description is not None):
            if not isinstance(description, str):
                description = str(description)
            
            new_data['description'] = description
        
        # fields
        if (field_datas is not None):
            new_data['fields'] = field_datas
        
        # footer
        if (footer_data is not None):
            new_data['footer'] = footer_data
        
        # image
        if (image_data is not None):
            new_data['image'] = image_data
        
        # provider
        if (provider_data is not None):
            new_data['provider'] = provider_data
        
        # thumbnail
        if (thumbnail_data is not None):
            new_data['thumbnail'] = thumbnail_data
        
        # timestamp
        if (timestamp_data is not None):
            new_data['timestamp'] = timestamp_data
        
        # title
        if (title is not None):
            if not isinstance(title, str):
                title = str(title)
            
            new_data['title'] = title
        
        # type
        if (type_ is not None):
            new_data['type'] = type_
        
        # url
        if (url is not None):
            new_data['url'] = url
        
        # video
        if (video_data is not None):
            new_data['video'] = video_data
        
        new = object.__new__(type(self))
        new._data = new_data
        return new
    
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
        
        Accepts and returns `None` or a `str`.
        """
        return self._data.get('description', None)
    
    @description.setter
    def description(self, value):
        if value is None:
            try:
                del self._data['description']
            except KeyError:
                pass
        else:
            if not isinstance(value, str):
                value = str(value)
            
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
        
        Accepts an `iterable` of ``EmbedField``objects. Meanwhile returns an ``_EmbedFieldsProxy``,
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
        
        return timestamp_to_datetime(timestamp_value)
    
    @timestamp.setter
    def timestamp(self, value):
        self._data['timestamp'] = datetime_to_timestamp(value)
    
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
        
        Accepts and returns `None` or a `str`.
        """
        return self._data.get('title', None)
    
    @title.setter
    def title(self, value):
        if value is None:
            try:
                del self._data['title']
            except KeyError:
                pass
        else:
            if not isinstance(value, str):
                value = str(value)
            
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
        
        Accepts and returns `None` or a `str`.
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
        
        Accepts and returns `None` or a `str`.
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
    
    def add_author(self, name=None, icon_url = None, url = None):
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
        self : ``Embed``
        """
        if (name is not None) and (not isinstance(name, str)):
            name = str(name)
        
        name, icon_url = _warn_bad_embed_author_constructor_parameter_order(name, icon_url)
        
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
        inline : `bool` = `False`, Optional
            Whether this field should display inline.
        
        Returns
        -------
        self : ``Embed``
        """
        if not isinstance(name, str):
            name = str(name)
        
        if not isinstance(value, str):
            value = str(value)
        
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
        inline : `bool` = `False`, Optional
            Whether this field should display inline.
        """
        if not isinstance(name, str):
            name = str(name)
        
        if not isinstance(value, str):
            value = str(value)
        
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
            raise IndexError(
                f'Index out of the fields\' range, got index={index!r}; count=0.'
            ) from None
        
        try:
            field_data = field_datas[index]
        except IndexError:
            raise IndexError(
                f'Index out of the fields\' range, got index={index!r}; count={len(field_datas)!r}.'
            ) from None
        
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
            field_datas = self._data['fields']
        except KeyError:
            raise IndexError(
                f'Index out of the fields\' range, got index={index!r}; count=0.'
            ) from None
        
        field_data = field.to_data()
        
        try:
            field_datas[index] = field_data
        except IndexError:
            raise IndexError(
                f'Index out of the fields\' range, got index={index!r}; count={len(field_datas)!r}.'
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
        try:
            field_datas = self._data['fields']
        except KeyError:
            raise IndexError(
                f'Index out of the fields\' range, got index={index!r}; count=0.'
            ) from None
        
        try:
            del field_datas[index]
        except IndexError:
            raise IndexError(
                f'Index out of the fields\' range, got index={index!r}; count={len(field_datas)!r}.'
            ) from None
    
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
        self : ``Embed``
        """
        if not isinstance(text, str):
            text = str(text)
        
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
        inline : `bool` = `False`, Optional
            Whether this field should display inline.
        """
        if not isinstance(name, str):
            name = str(name)
        
        if not isinstance(value, str):
            value = str(value)
        
        field_data = {
            'name': name,
            'value': value,
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
        inline : `bool` = `False`, Optional
            Whether this field should display inline.
        """
        if not isinstance(name, str):
            name = str(name)
        
        if not isinstance(value, str):
            value = str(value)
        
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
