__all__ = ('Emoji',)

from scarletio import export

from ...bases import DiscordEntity
from ...core import BUILTIN_EMOJIS, EMOJIS, GUILDS, UNICODE_TO_EMOJI
from ...http import urls as module_urls
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...role import RoleManagerType, create_partial_role_from_id
from ...user import ZEROUSER
from ...utils import DATETIME_FORMAT_CODE, DISCORD_EPOCH_START, id_to_datetime

from .constants import UNICODE_EMOJI_LIMIT
from .fields import (
    parse_animated, parse_available, parse_id, parse_managed, parse_name, parse_require_colons, parse_role_ids,
    parse_user, put_animated_into, put_available_into, put_id_into, put_managed_into, put_name_into,
    put_require_colons_into, put_role_ids_into, put_user_into, validate_animated, validate_available, validate_guild_id,
    validate_id, validate_managed, validate_name, validate_require_colons, validate_role_ids, validate_user
)


ROLE_MANAGER_TYPE_SUBSCRIPTION = RoleManagerType.subscription


PRECREATE_FIELDS = {
    'animated': ('animated', validate_animated),
    'available': ('available', validate_available),
    'guild': ('guild_id', validate_guild_id),
    'guild_id': ('guild_id', validate_guild_id),
    'managed': ('managed', validate_managed),
    'name': ('name', validate_name),
    'require_colons': ('require_colons', validate_require_colons),
    'role_ids': ('role_ids', validate_role_ids),
    'roles': ('role_ids', validate_role_ids),
    'user': ('user', validate_user),
}


@export
class Emoji(DiscordEntity, immortal = True):
    """
    Represents a Discord emoji. It can be custom or builtin (unicode) emoji as well. Builtin emojis are loaded when the
    module is imported and they are stores at `BUILTIN_EMOJIS` dictionary. At `BUILTIN_EMOJIS` the keys are the
    emoji's names, so it is easy to access any Discord unicode emoji like that.
    
    Custom emojis are loaded with ``Guild``-s on startup, but new partial custom emojis can be created later as well,
    when a ``Message`` receives any reaction.
    
    Attributes
    ----------
    animated : `bool`
        Whether the emoji is animated.
    available : `bool`
        Whether the emoji is available.
    guild_id : `int`
        The emoji's guild's identifier.
    id : `int`
        Unique identifier of the emoji.
    managed : `bool`
        Whether the emoji is managed by an integration.
    name : `str`
        The emoji's name.
    require_colons : `bool`
        Whether it is required to use colons for the emoji to show up.
    role_ids : `None`, `tuple` of `int`
        Role identifiers for which the custom emoji is whitelisted to. If the emoji is not limited for
        specific roles, then this value is set to `None`. If the emoji is a builtin (unicode) emoji, then this
        attribute is set to `None` as  well.
    unicode : `None`, `str`
        At the case of custom emojis this attribute is always `None`, but at the case of builtin (unicode) emojis this
        attribute stores the emoji's unicode representation.
    user : ``ClientUserBase``
        The creator of the custom emoji. The emoji must be requested from Discord's API, or it's user will be just
        the default `ZEROUSER`.
    
    Class Attributes
    ----------------
    _last_unicode_id : `int`
        The most recently created unicode emoji's identifier.
    
    See Also
    --------
    - ``create_partial_emoji`` : A function to create an emoji object from partial emoji data.
    - ``parse_emoji`` : Parses a partial emoji object out from text.
    """
    __slots__ = (
        'animated', 'available', 'guild_id', 'managed', 'name', 'require_colons', 'role_ids', 'unicode', 'user'
    )
    
    _last_unicode_id = 0
    
    
    def __new__(
        cls,
        *,
        animated = ...,
        available = ...,
        managed = ...,
        name = ...,
        require_colons = ...,
        role_ids = ...,
        user = ...,
    ):
        """
        Creates a partial emoji with the given fields.
        
        Parameters
        ----------
        animated : `bool`, Optional (Keyword only)
             Whether the emoji is animated.
        available : `bool`, Optional (Keyword only)
             Whether the emoji is available.
        managed : `bool`, Optional (Keyword only)
            Whether the emoji is managed by an integration.
        name : `str`, Optional (Keyword only)
            The emoji's name.
        require_colons : `bool`, Optional (Keyword only)
             Whether it is required to use colons for the emoji to show up.
        role_ids : `None`, `iterable` of (``Role``, `int`), Optional (Keyword only)
            Role identifiers for which the custom emoji is whitelisted to.
        user : ``ClientUserBase`, `int`, Optional (Keyword only)
            The creator of the custom emoji.
        
        Raises
        ------
        TypeError
            - A parameter's type is incorrect.
        ValueError
            - A parameter's value is incorrect.
        """
        # animated
        if animated is ...:
            animated = False
        else:
            animated = validate_animated(animated)
        
        # available
        if available is ...:
            available = True
        else:
            available = validate_available(available)
        
        # managed
        if managed is ...:
            managed = False
        else:
            managed = validate_managed(managed)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # require_colons
        if require_colons is ...:
            require_colons = False
        else:
            require_colons = validate_require_colons(require_colons)
        
        # role_ids
        if role_ids is ...:
            role_ids = None
        else:
            role_ids = validate_role_ids(role_ids)
        
        # user
        if user is ...:
            user = ZEROUSER
        else:
            user = validate_user(user)
        
        # Construct
        self = object.__new__(cls)
        self.animated = animated
        self.available = available
        self.guild_id = 0
        self.id = 0
        self.managed = managed
        self.name = name
        self.require_colons = require_colons
        self.role_ids = role_ids
        self.unicode = None
        self.user = user
        return self
    
    
    @classmethod
    def from_data(cls, data, guild_id = 0):
        """
        Creates a new emoji object from emoji data included with it's guild's. If the emoji already exists, picks that
        up instead of creating a new one.
        
        This method can not create builtin (unicode) emojis. Those are created when the library is loaded.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Emoji data received from Discord.
        guild_id : `int` = `0`, Optional
            The emoji's guild's identifier.
        
        Returns
        -------
        emoji : `instance<cls>`
        """
        emoji_id = parse_id(data)
        
        try:
            self = EMOJIS[emoji_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = emoji_id
            self._set_attributes(data, guild_id)
            
            EMOJIS[emoji_id] = self
        
        else:
            # whenever we receive an emoji, it will have no user data included, so it is enough if we check for user
            # data only whenever we receive emoji data from a request or so.
            if not self.partial:
                # Set user if received
                user = parse_user(data)
                if user is not ZEROUSER:
                    self.user = user
                
                return self
            
            self._set_attributes(data, guild_id)
        
        # Do not register, since that ruins `client.events.emoji_create` after a `client.emoji_create` call.
        # try:
        #     guild = GUILDS[guild_id]
        # except KeyError:
        #     pass
        # else:
        #     guild.emojis[emoji_id] = self
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the emoji to a json serializable object.
        
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
        
        put_name_into(self.name, data, defaults)
        put_role_ids_into(self.role_ids, data, defaults)
        
        if include_internals:
            put_animated_into(self.animated, data, defaults)
            put_available_into(self.available, data, defaults)
            put_id_into(self.id, data, defaults)
            put_managed_into(self.managed, data, defaults)
            put_require_colons_into(self.require_colons, data, defaults)
            put_user_into(self.user, data, defaults, include_internals = include_internals)
        
        return data
    
    
    @classmethod
    def precreate(cls, emoji_id, **keyword_parameters):
        """
        Precreates the emoji by creating a partial one with the given parameters. When the emoji is loaded
        the precreated one will be picked up. If an already existing emoji would be precreated, returns that
        instead and updates that only, if that is partial.
        
        Parameters
        ----------
        emoji_id : `int`
            The emoji's id.
        **keyword_parameters : keyword parameters
            Additional predefined attributes for the emoji.
        
        Other Parameters
        ----------------
        animated : `bool`, Optional (Keyword only)
             Whether the emoji is animated.
        available : `bool`, Optional (Keyword only)
             Whether the emoji is available.
        guild : ``Guild``, `int`, Optional (Keyword only)
            Alternative for `guild_id`.
        guild_id : ``Guild``, `int`, Optional (Keyword only)
             The emoji's guild's identifier.
        managed : `bool`, Optional (Keyword only)
            Whether the emoji is managed by an integration.
        name : `str`, Optional (Keyword only)
            The emoji's name.
        require_colons : `bool`, Optional (Keyword only)
             Whether it is required to use colons for the emoji to show up.
        role_ids : `None`, `iterable` of (``Role``, `int`), Optional (Keyword only)
            Role identifiers for which the custom emoji is whitelisted to.
        roles : `None`, `iterable` of (``Role``, `int`), Optional (Keyword only)
            Alternative for `role_ids`.
        user : ``ClientUserBase`, `int`, Optional (Keyword only)
            The creator of the custom emoji.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - A parameter's type is incorrect.
            - Extra parameters given.
        ValueError
            - A parameter's value is incorrect.
        """
        emoji_id = validate_id(emoji_id)

        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = EMOJIS[emoji_id]
        except KeyError:
            self = cls._create_empty(emoji_id)
            EMOJIS[emoji_id] = self
        else:
            if not self.partial:
                return self
        
        if (processed is not None):
            for name, value in processed:
                setattr(self, name, value)
        
        return self
    
    
    def __repr__(self):
        """Returns the emoji's representation"""
        repr_parts = ['<', self.__class__.__name__]
        
        emoji_id = self.id
        if emoji_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(self.id))
            repr_parts.append(',')
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __format__(self, code):
        """
        Formats the emoji in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        emoji : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        
        Examples
        --------
        ```py
        >>> from hata import Emoji, now_as_id, BUILTIN_EMOJIS
        >>> emoji = Emoji.precreate(now_as_id(), name = 'nice')
        >>> emoji
        <Emoji id = 712359434843586560, name = 'nice'>
        >>> # no code returns the emoji's emoji format as a shortcut in f string formatting.
        >>> f'{emoji}'
        '<:nice:712359434843586560>'
        >>> # 'e' stands for emoji format.
        >>> f'{emoji:e}'
        '<:nice:712359434843586560>'
        >>> # 'r' stands for reaction format.
        >>> f'{emoji:r}'
        'nice:712359434843586560'
        >>> # 'c' stands for created at.
        >>> f'{emoji:c}'
        '2020.05.19-17:42:04'
        >>> # The following works with builtin (unicode) emojis as well.
        >>> emoji = BUILTIN_EMOJIS['heart']
        >>> f'{emoji}'
        '❤️'
        >>> f'{emoji:e}'
        '❤️'
        >>> f'{emoji:r}'
        '❤️'
        >>> f'{emoji:c}'
        '2015.01.01-00:00:00'
        ```
        """
        if not code:
            return self.as_emoji
        
        if code == 'e':
            return self.as_emoji
        
        if code == 'r':
            return self.as_reaction
        
        if code == 'c':
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}, {"e"!r}, {"f"!r}.'
        )
    
    
    def __hash__(self):
        """Returns the emoji's hash."""
        emoji_id = self.id
        if emoji_id:
            return emoji_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Returns a partial emoji's hash value.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # animated
        hash_value ^= self.animated
        
        # available
        hash_value ^= self.available << 1
        
        # managed
        hash_value ^= self.managed << 2
        
        # name
        hash_value ^= hash(self.name)
        
        # require_colons
        hash_value ^= self.require_colons << 3
        
        # role_ids
        role_ids = self.role_ids
        if (role_ids is not None):
            hash_value ^= len(role_ids) << 4
            
            for role_id in role_ids:
                hash_value ^= role_id
        
        # user
        hash_value ^= hash(self.user)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two emojis are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two emojis are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two emojis are equal. `self` and `other` must be the same type.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other emoji.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if (self_id and other_id):
            return self_id == other_id
        
        # animated
        if (self.animated != other.animated):
            return False
        
        # available
        if (self.available != other.available):
            return False
        
        # guild_id
        # Skip | non-partial
        
        # managed
        if (self.managed != other.managed):
            return False
        
        # name
        if (self.name != other.name):
            return False
        
        # require_colons
        if (self.require_colons != other.require_colons):
            return False
        
        # role_ids
        if (self.role_ids != other.role_ids):
            return False
        
        # unicode
        # Skip | non-partial
        
        # user
        if (self.user != other.user):
            return False
        
        return True
    
    
    @property
    def partial(self):
        """
        Returns whether the emoji is partial.
        
        Returns
        -------
        partial : `bool`
        """
        if (self.unicode is not None):
            return False
        
        emoji_id = self.id
        if not emoji_id:
            return True
        
        guild_id = self.guild_id
        if not guild_id:
            return True
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            return True
        
        if self.id not in guild.emojis:
            return True
        
        return guild.partial
    
    
    def is_custom_emoji(self):
        """
        Returns whether the emoji is a custom emoji.
        
        Returns
        -------
        is_custom_emoji : `bool`
        """
        return (self.unicode is None)
    
    
    def is_unicode_emoji(self):
        """
        Returns whether the emoji is a unicode emoji.
        
        Returns
        -------
        is_unicode_emoji : `bool`
        """
        return (self.unicode is not None)
    
    
    @property
    def as_reaction(self):
        """
        Returns the emoji's reaction form, which is used by the Discord API at requests when working with reactions.
        
        Returns
        -------
        as_reaction : `str`
        """
        unicode = self.unicode
        if (unicode is not None):
            return unicode
        
        return f'{self.name}:{self.id}'
    
    
    @property
    def as_emoji(self):
        """
        Returns the emoji's emoji form. Should be used when sending an emoji within a ``Message``.
        
        Returns
        -------
        as_emoji : `str`
        """
        unicode = self.unicode
        if (unicode is not None):
            return unicode
        
        if self.animated:
            return f'<a:{self.name}:{self.id}>'
        else:
            return f'<:{self.name}:{self.id}>'
    
    
    @property
    def created_at(self):
        """
        When the emoji was created. If the emoji is unicode emoji, then returns Discord epoch's start.
        
        Returns
        -------
        created_at : `datetime`
        """
        emoji_id = self.id
        if emoji_id > UNICODE_EMOJI_LIMIT:
            created_at = id_to_datetime(emoji_id)
        else:
            created_at = DISCORD_EPOCH_START
        
        return created_at
    
    
    url = property(module_urls.emoji_url)
    url_as = module_urls.emoji_url_as
    
    
    def _set_attributes(self, data, guild_id):
        """
        Sets the attributes of the emoji from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Emoji  data.
        guild_id : `int`
            The emoji's guild's identifier.
        """
        self.guild_id = guild_id
        self.unicode = None
        self.user = ZEROUSER
        
        self._update_attributes(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the emoji with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Emoji's data received from Discord.
        """
        self.animated = parse_animated(data)
        self.available = parse_available(data)
        self.managed = parse_managed(data)
        self.name = parse_name(data)
        self.require_colons = parse_require_colons(data)
        self.role_ids = parse_role_ids(data)
        
        # set user if applicable
        user = parse_user(data)
        if user is not ZEROUSER:
            self.user = user
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the emoji and returns it's overwritten old attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Emoji data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +-------------------+-------------------------------+
        | Keys              | Values                        |
        +===================+===============================+
        | animated          | `bool`                        |
        +-------------------+-------------------------------+
        | available         | `bool`                        |
        +-------------------+-------------------------------+
        | managed           | `bool`                        |
        +-------------------+-------------------------------+
        | name              | `int`                         |
        +-------------------+-------------------------------+
        | require_colons    | `bool`                        |
        +-------------------+-------------------------------+
        | role_ids          | `None`, `tuple` of `int`      |
        +-------------------+-------------------------------+
        """
        old_attributes = {}
        
        # animated
        animated = parse_animated(data)
        if self.animated != animated:
            old_attributes['animated'] = self.animated
            self.animated = animated
        
        # available
        available = parse_available(data)
        if self.available != available:
            old_attributes['available'] = self.available
            self.available = available
        
        # managed
        managed = parse_managed(data)
        if self.managed != managed:
            old_attributes['managed'] = self.managed
            self.managed = managed
        
        # name
        name = parse_name(data)
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        # require_colons
        require_colons = parse_require_colons(data)
        if self.require_colons != require_colons:
            old_attributes['require_colons'] = self.require_colons
            self.require_colons = require_colons
        
        # role_ids
        role_ids = parse_role_ids(data)
        if self.role_ids != role_ids:
            old_attributes['role_ids'] = self.role_ids
            self.role_ids = role_ids
        
        # set user if applicable
        user = parse_user(data)
        if user is not ZEROUSER:
            self.user = user
        
        return old_attributes
    
    
    @classmethod
    def _create_partial(cls, emoji_id, name, animated):
        """
        Creates a new emoji from the given partial data.
        
        Parameters
        ----------
        emoji_id : `int`
            The emoji's identifier.
        name : `str`
            The emoji's name.
        animated : `bool`
            Whether the emoji is animated.
        
        Returns
        -------
        emoji : `instance<cls>`
        """
        try:
            self = EMOJIS[emoji_id]
        except KeyError:
            self = cls._create_empty(emoji_id)
            EMOJIS[emoji_id] = self
        else:
            if not self.partial:
                return self
        
        self.name = name
        self.animated = animated
        
        return self
    
    
    @classmethod
    def _create_empty(cls, emoji_id):
        """
        Creates an empty emoji with the given identifier.
        
        Parameters
        ----------
        emoji_id : `int`
            The emoji's identifier.
        
        Returns
        -------
        self : `instance<cls>`
            The created emoji.
        """
        self = object.__new__(cls)
        self.animated = False
        self.available = True
        self.guild_id = 0
        self.id = emoji_id
        self.managed = False
        self.name = ''
        self.require_colons = True
        self.role_ids = None
        self.unicode = None
        self.user = ZEROUSER
        return self
    
    
    @classmethod
    def _create_unicode(cls, unicode, register_by_name):
        """
        Creates a new unicode emoji with the given identifier.
        
        Parameters
        ----------
        unicode : ``Unicode``
            The emoji's unicode value.
        register_by_name : `bool`
            Whether the emoji should be registered by name.
        
        Returns
        -------
        self : `instance<cls>`
            The created emoji.
        """
        emoji_id = cls._last_unicode_id + 1
        cls._last_unicode_id = emoji_id
        
        self = object.__new__(cls)
        self.animated = False
        self.available = True
        self.id = emoji_id
        self.guild_id = 0
        self.managed = False
        self.name = unicode.name
        self.require_colons = True
        self.role_ids = None
        self.unicode = unicode.value
        self.user = ZEROUSER
        
        EMOJIS[emoji_id] = self
        UNICODE_TO_EMOJI[unicode.value] = self
        
        if register_by_name:
            BUILTIN_EMOJIS[unicode.get_system_name()] = self
            
            for alternative_name in unicode.iter_alternative_names():
                BUILTIN_EMOJIS[alternative_name] = self
        
        return self
    
    
    def copy(self):
        """
        Copies the emoji returning a partial one.
        
        > Supports only custom emojis.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.animated = self.animated
        new.available = self.available
        new.guild_id = 0
        new.id = 0
        new.managed = self.managed
        new.name = self.name
        new.require_colons = self.require_colons
        role_ids = self.role_ids
        if (role_ids is not None):
            role_ids = (*role_ids,)
        new.role_ids = role_ids
        new.unicode = None
        new.user = self.user
        return new
    
    
    def copy_with(
        self,
        *,
        animated = ...,
        available = ...,
        managed = ...,
        name = ...,
        require_colons = ...,
        role_ids = ...,
        user = ...,
    ):
        """
        Copies the emoji with the given fields returning a partial one.
        
        > Supports only custom emojis.
        
        Parameters
        ----------
        animated : `bool`, Optional (Keyword only)
             Whether the emoji is animated.
        available : `bool`, Optional (Keyword only)
             Whether the emoji is available.
        managed : `bool`, Optional (Keyword only)
            Whether the emoji is managed by an integration.
        name : `str`, Optional (Keyword only)
            The emoji's name.
        require_colons : `bool`, Optional (Keyword only)
             Whether it is required to use colons for the emoji to show up.
        role_ids : `None`, `iterable` of (``Role``, `int`), Optional (Keyword only)
            Role identifiers for which the custom emoji is whitelisted to.
        user : ``ClientUserBase`, `int`, Optional (Keyword only)
            The creator of the custom emoji.
        
        Returns
        -------
        emoji : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - A parameter's type is incorrect.
        ValueError
            - A parameter's value is incorrect.
        """
        # animated
        if animated is ...:
            animated = self.animated
        else:
            animated = validate_animated(animated)
        
        # available
        if available is ...:
            available = self.available
        else:
            available = validate_available(available)
        
        # managed
        if managed is ...:
            managed = self.managed
        else:
            managed = validate_managed(managed)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # require_colons
        if require_colons is ...:
            require_colons = self.require_colons
        else:
            require_colons = validate_require_colons(require_colons)
        
        # role_ids
        if role_ids is ...:
            role_ids = self.role_ids
            if (role_ids is not None):
                role_ids = (*role_ids,)
        else:
            role_ids = validate_role_ids(role_ids)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
        
        # Construct
        new = object.__new__(type(self))
        new.animated = animated
        new.available = available
        new.guild_id = 0
        new.id = 0
        new.managed = managed
        new.name = name
        new.require_colons = require_colons
        new.role_ids = role_ids
        new.unicode = None
        new.user = user
        return new
    
    
    @property
    def guild(self):
        """
        Returns the guild of the emoji.
        
        Returns `None` if the emoji has no bound emoji, or if the emoji's guild is not cached.
        
        Returns
        -------
        guild : `None`, ``Guild``
            The emoji's guild.
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def roles(self):
        """
        Returns the roles of which members the emoji's usage is restricted to.
        
        Returns
        -------
        roles : `None`, `tuple` of ``Role``
        """
        role_ids = self.role_ids
        if role_ids is None:
            roles = None
        else:
            roles = tuple(sorted(
                (create_partial_role_from_id(role_id) for role_id in role_ids),
            ))
        
        return roles
    
    
    def iter_role_ids(self):
        """
        Iterates over the emoji's roles' identifiers.
        
        This method is an iterable generator.
        
        Yields
        ------
        role_id : `int`
        """
        role_ids = self.role_ids
        if (role_ids is not None):
            yield from role_ids
    
    
    def iter_roles(self):
        """
        Iterates over the emoji's roles. Not like ``.roles``, this will not sort the roles of the emoji based on their
        position, instead uses the default ordering (id).
        
        This method is an iterable generator.
        
        Yields
        ------
        role : ``Role``
        """
        for role_id in self.iter_role_ids():
            yield create_partial_role_from_id(role_id)
    
    
    def is_premium(self):
        """
        Returns whether the role is a premium one.
        
        Returns
        -------
        is_premium : `bool`
        """
        for role in self.iter_roles():
            if role.manager_type is ROLE_MANAGER_TYPE_SUBSCRIPTION:
                return True
        
        return False
