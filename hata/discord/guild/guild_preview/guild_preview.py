__all__ = ('GuildPreview', )

from ...bases import DiscordEntity, IconSlot
from ...http import urls as module_urls
from ...utils import DATETIME_FORMAT_CODE

from .fields import (
    parse_approximate_online_count, parse_approximate_user_count, parse_description, parse_emojis, parse_features,
    parse_id, parse_name, parse_stickers, put_approximate_online_count_into, put_approximate_user_count_into,
    put_description_into, put_emojis_into, put_features_into, put_id_into, put_name_into, put_stickers_into,
    validate_approximate_online_count, validate_approximate_user_count, validate_description, validate_emojis,
    validate_features, validate_id, validate_name, validate_stickers
)


class GuildPreview(DiscordEntity):
    """
    A preview of a public guild.
    
    Attributes
    ----------
    approximate_online_count : `int`
        Approximate amount of online users at the represented guild.
    approximate_user_count : `int`
        Approximate amount of users at the represented guild.
    description : `None`, `str`
        Description of the guild.
    discovery_splash_hash : `int`
        The guild's discovery splash's hash in `uint128`.
    discovery_splash_type : ``IconType``
        The guild discovery splash's type.
    emojis : `dict` of (`int`, ``Emoji``) items
        The emojis of the guild stored in `emoji_id` - `emoji` relation.
    features : `None`, `tuple` of ``GuildFeature``
        The guild's features.
    icon_hash : `int`
        The guild's icon's hash in `uint128`.
    icon_type : ``IconType``
        The guild's icon's type.
    id : `int`
        The represented guild's identifier.
    invite_splash_hash : `int`
        The guild's invite splash's hash in `uint128`.
    invite_splash_type : ``IconType``
        the guild's invite splash's type.
    stickers : `dict` of (`int`, ``Sticker``) items
        The stickers of the guild stored in `sticker_id` - `sticker` relation.
    name : `str`
        The name of the guild.
    """
    __slots__ = (
        'approximate_online_count', 'approximate_user_count','description', 'emojis', 'features', 'name', 'stickers'
    )
    
    icon = IconSlot(
        'icon',
        'icon',
        module_urls.guild_icon_url,
        module_urls.guild_icon_url_as,
    )
    
    invite_splash = IconSlot(
        'invite_splash',
        'splash',
        module_urls.guild_invite_splash_url,
        module_urls.guild_invite_splash_url_as,
    )
    
    discovery_splash = IconSlot(
        'discovery_splash',
        'discovery_splash',
        module_urls.guild_discovery_splash_url,
        module_urls.guild_discovery_splash_url_as,
    )
    
    
    def __new__(
        cls,
        *,
        approximate_online_count = ...,
        approximate_user_count = ...,
        description = ...,
        discovery_splash = ...,
        emojis = ...,
        features = ...,
        guild_id = ...,
        icon = ...,
        invite_splash = ...,
        stickers = ...,
        name = ...,
    ):
        """
        Creates a new guild preview with the given fields.
        
        Parameters
        ----------
        approximate_online_count : `int`, Optional (Keyword only)
            Approximate amount of online users at the represented guild.
        approximate_user_count : `int`, Optional (Keyword only)
            Approximate amount of users at the represented guild.
        description : `None`, `str`, Optional (Keyword only)
            Description of the guild.
        discovery_splash : `None`, ``Icon``, `str`, Optional (Keyword only)
            The guild's discovery splash.
        emojis : `None`, `iterable` of ``Emoji``, Optional (Keyword only)
            The emojis of the guild.
        features : `None`, `iterable` of ``GuildFeature``, Optional (Keyword only)
            The guild's features.
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The represented guild's identifier.
        icon : `None`, ``Icon``, `str`, Optional (Keyword only)
            The guild's icon.
        invite_splash : `None`, ``Icon``, `str`, Optional (Keyword only)
            The guild's invite splash.
        stickers : `None`, `iterable` of ``Sticker``, Optional (Keyword only)
            The stickers of the guild.
        name : `str`, Optional (Keyword only)
            The name of the guild.
        
        Raises
        ------
        TypeError
            - Parameter with incorrect type given.
        ValueError
            - Parameter with incorrect value given.
        """
        # approximate_online_count
        if approximate_online_count is ...:
            approximate_online_count = 0
        else:
            approximate_online_count = validate_approximate_online_count(approximate_online_count)
        
        # approximate_user_count
        if approximate_user_count is ...:
            approximate_user_count = 0
        else:
            approximate_user_count = validate_approximate_user_count(approximate_user_count)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # discovery_splash
        if discovery_splash is ...:
            discovery_splash = None
        else:
            discovery_splash = cls.discovery_splash.validate_icon(discovery_splash)
        
        # emojis
        if emojis is ...:
            emojis = {}
        else:
            emojis = validate_emojis(emojis)
        
        # features
        if features is ...:
            features = None
        else:
            features = validate_features(features)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_id(guild_id)
        
        # icon
        if icon is ...:
            icon = None
        else:
            icon = cls.icon.validate_icon(icon)
        
        # invite_splash
        if invite_splash is ...:
            invite_splash = None
        else:
            invite_splash = cls.invite_splash.validate_icon(invite_splash)
    
        # stickers
        if stickers is ...:
            stickers = {}
        else:
            stickers = validate_stickers(stickers)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # Construct
        self = object.__new__(cls)
        self.approximate_online_count = approximate_online_count
        self.approximate_user_count = approximate_user_count
        self.description = description
        self.discovery_splash = discovery_splash
        self.emojis = emojis
        self.features = features
        self.icon = icon
        self.id = guild_id
        self.invite_splash = invite_splash
        self.stickers = stickers
        self.name = name
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a guild preview from the requested guild preview data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received guild preview data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        guild_id = parse_id(data)
        
        self = object.__new__(cls)
        self.approximate_online_count = parse_approximate_online_count(data)
        self.approximate_user_count = parse_approximate_user_count(data)
        self.description = parse_description(data)
        self._set_discovery_splash(data)
        self.emojis = parse_emojis(data, {}, guild_id)
        self.features = parse_features(data)
        self._set_icon(data)
        self.id = guild_id
        self._set_invite_splash(data)
        self.stickers = parse_stickers(data, {})
        self.name = parse_name(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the guild preview to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_approximate_online_count_into(self.approximate_online_count, data, defaults)
        put_approximate_user_count_into(self.approximate_user_count, data, defaults)
        put_description_into(self.description, data, defaults)
        type(self).discovery_splash.put_into(self.discovery_splash, data, defaults)
        put_emojis_into(self.emojis, data, defaults)
        put_features_into(self.features, data, defaults)
        type(self).icon.put_into(self.icon, data, defaults)
        put_id_into(self.id, data, defaults)
        type(self).invite_splash.put_into(self.invite_splash, data, defaults)
        put_stickers_into(self.stickers, data, defaults)
        put_name_into(self.name, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the guild preview's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        sticker_id = self.id
        if sticker_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(self.id))
            repr_parts.append(',')
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __format__(self, code):
        """
        Formats the guild preview in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        channel : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        
        Examples
        --------
        ```py
        >>> from hata import Client, KOKORO
        >>> TOKEN = 'a token goes here'
        >>> client = Client(TOKEN)
        >>> guild_id = 302094807046684672
        >>> guild_preview = KOKORO.run(client.guild_preview_get(guild_id))
        >>> guild_preview
        <GuildPreview id = 302094807046684672, name = 'MINECRAFT'>
        >>> # no code stands for `guild_preview.name`.
        >>> f'{guild_preview}'
        'MINECRAFT'
        >>> # 'c' stands for created at.
        >>> f'{guild_preview:c}'
        '2017.04.13-14:56:54'
        ```
        """
        if not code:
            return self.name
        
        if code == 'c':
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}.'
        )
    
    
    def __eq__(self, other):
        """Returns whether the two guild previews are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two guild previews are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return (not self._is_equal_same_type(other))
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two guild previews are equal. Type of other must be same as type of self.
        
        Parameters
        ----------
        other : `<instance<type<self>>`
            The other guild preview to compare self to.
        
        Returns
        -------
        is_equal : `bool`
        """
        # approximate_online_count
        if self.approximate_online_count != other.approximate_online_count:
            return False
        
        # approximate_user_count
        if self.approximate_user_count != other.approximate_user_count:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # discovery_splash_hash
        if self.discovery_splash_hash != other.discovery_splash_hash:
            return False
        
        # discovery_splash_type
        if self.discovery_splash_type != other.discovery_splash_type:
            return False
        
        # emojis
        if self.emojis != other.emojis:
            return False
        
        # features
        if self.features != other.features:
            return False
        
        # icon_hash
        if self.icon_hash != other.icon_hash:
            return False
        
        # icon_type
        if self.icon_type != other.icon_type:
            return False
        
        # id
        if self.id != other.id:
            return False
        
        # invite_splash_hash
        if self.invite_splash_hash != other.invite_splash_hash:
            return False
        
        # invite_splash_type
        if self.invite_splash_type != other.invite_splash_type:
            return False
        
        # stickers
        if self.stickers != other.stickers:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the guild preview."""
        hash_value = 0
        
        # approximate_online_count
        hash_value ^= self.approximate_online_count
        
        # approximate_user_count
        hash_value ^= self.approximate_user_count << 12
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # discovery_splash
        hash_value ^= hash(self.discovery_splash)
        
        # emojis
        emojis = self.emojis
        hash_value ^= len(emojis) << 1
        for emoji in emojis.values():
            hash_value ^= hash(emoji)
        
        # features
        features = self.features
        hash_value ^= len(features) << 5
        for feature in features:
            hash_value ^= hash(feature)
        
        # icon
        hash_value ^= hash(self.icon)
        
        # id
        hash_value ^= self.id
        
        # invite_splash
        hash_value ^= hash(self.invite_splash)
        
        # stickers
        stickers = self.stickers
        hash_value ^= len(stickers) << 9
        for sticker in stickers.values():
            hash_value ^= hash(sticker)
        
        # name
        name = self.name
        if (description is None) or (description != name):
            hash_value ^= hash(name)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the guild preview.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.approximate_online_count = self.approximate_online_count
        new.approximate_user_count = self.approximate_user_count
        new.description = self.description
        new.discovery_splash_hash = self.discovery_splash_hash
        new.discovery_splash_type = self.discovery_splash_type
        new.emojis = self.emojis.copy()
        features = self.features
        if (features is not None):
            features = (*features,)
        new.features = features
        new.icon_hash = self.icon_hash
        new.icon_type = self.icon_type
        new.id = self.id
        new.invite_splash_hash = self.invite_splash_hash
        new.invite_splash_type = self.invite_splash_type
        new.stickers = self.stickers.copy()
        new.name = self.name
        return new
    
    
    def copy_with(
        self,
        *,
        approximate_online_count = ...,
        approximate_user_count = ...,
        description = ...,
        discovery_splash = ...,
        emojis = ...,
        features = ...,
        guild_id = ...,
        icon = ...,
        invite_splash = ...,
        stickers = ...,
        name = ...,
    ):
        """
        Copies the guild preview with the given fields.
        
        Parameters
        ----------
        approximate_online_count : `int`, Optional (Keyword only)
            Approximate amount of online users at the represented guild.
        approximate_user_count : `int`, Optional (Keyword only)
            Approximate amount of users at the represented guild.
        description : `None`, `str`, Optional (Keyword only)
            Description of the guild.
        discovery_splash : `None`, ``Icon``, `str`, Optional (Keyword only)
            The guild's discovery splash.
        emojis : `None`, `iterable` of ``Emoji``, Optional (Keyword only)
            The emojis of the guild.
        features : `None`, `iterable` of ``GuildFeature``, Optional (Keyword only)
            The guild's features.
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The represented guild's identifier.
        icon : `None`, ``Icon``, `str`, Optional (Keyword only)
            The guild's icon.
        invite_splash : `None`, ``Icon``, `str`, Optional (Keyword only)
            The guild's invite splash.
        stickers : `None`, `iterable` of ``Sticker``, Optional (Keyword only)
            The stickers of the guild.
        name : `str`, Optional (Keyword only)
            The name of the guild.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - Parameter with incorrect type given.
        ValueError
            - Parameter with incorrect value given.
        """
        # approximate_online_count
        if approximate_online_count is ...:
            approximate_online_count = self.approximate_online_count
        else:
            approximate_online_count = validate_approximate_online_count(approximate_online_count)
        
        # approximate_user_count
        if approximate_user_count is ...:
            approximate_user_count = self.approximate_user_count
        else:
            approximate_user_count = validate_approximate_user_count(approximate_user_count)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # discovery_splash
        if discovery_splash is ...:
            discovery_splash = self.discovery_splash
        else:
            discovery_splash = type(self).discovery_splash.validate_icon(discovery_splash)
        
        # emojis
        if emojis is ...:
            emojis = self.emojis.copy()
        else:
            emojis = validate_emojis(emojis)
        
        # features
        if features is ...:
            features = self.features
            if (features is not None):
                features = (*features,)
        else:
            features = validate_features(features)
        
        # guild_id
        if guild_id is ...:
            guild_id = self.id
        else:
            guild_id = validate_id(guild_id)
        
        # icon
        if icon is ...:
            icon = self.icon
        else:
            icon = type(self).icon.validate_icon(icon)
        
        # invite_splash
        if invite_splash is ...:
            invite_splash = self.invite_splash
        else:
            invite_splash = type(self).invite_splash.validate_icon(invite_splash)
    
        # stickers
        if stickers is ...:
            stickers = self.stickers.copy()
        else:
            stickers = validate_stickers(stickers)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # Construct
        new = object.__new__(type(self))
        new.approximate_online_count = approximate_online_count
        new.approximate_user_count = approximate_user_count
        new.description = description
        new.discovery_splash = discovery_splash
        new.emojis = emojis
        new.features = features
        new.icon = icon
        new.id = guild_id
        new.invite_splash = invite_splash
        new.stickers = stickers
        new.name = name
        return new
    
    
    def iter_features(self):
        """
        Iterates over the features of the represented guild.
        
        This method is an iterable generator.
        
        Yields
        ------
        feature : ``GuildFeature``
        """
        features = self.features
        if (features is not None):
            yield from features
    
    
    def has_feature(self, feature):
        """
        Returns whether the represented guild has the give feature.
        
        Parameters
        ----------
        feature : ``GuildFeature``
            The feature to look for.
        
        Returns
        -------
        has_feature : `bool`
        """
        features = self.features
        if features is None:
            return False
        
        return feature in features
