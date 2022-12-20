__all__ = ('Emoji',)

from scarletio import export, include

from ..bases import DiscordEntity, id_sort_key
from ..bases import instance_or_id_to_instance, instance_or_id_to_snowflake, iterable_of_instance_or_id_to_snowflakes
from ..core import BUILTIN_EMOJIS, EMOJIS, GUILDS, UNICODE_TO_EMOJI
from ..http import urls as module_urls
from ..preconverters import preconvert_bool, preconvert_snowflake, preconvert_str
from ..role import Role, RoleManagerType, create_partial_role_from_id
from ..user import User, ZEROUSER
from ..utils import DATETIME_FORMAT_CODE, DISCORD_EPOCH_START, id_to_datetime


Client = include('Client')
Guild = include('Guild')

UNICODE_EMOJI_LIMIT = 1 << 21
ROLE_MANAGER_TYPE_SUBSCRIPTION = RoleManagerType.subscription

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
    id : `int`
        Unique identifier of the emoji.
    animated : `bool`
        Whether the emoji is animated.
    available : `bool`
        Whether the emoji is available.
    guild_id : `int`
        The emoji's guild's identifier.
    managed : `bool`
        Whether the emoji is managed by an integration.
    name : `str`
        The emoji's name.
    require_colons : `bool`
        Whether it is required to use colons for the emoji to show up.
    role_ids : `None`, `tuple` of `int`
        A set of role identifiers for which the custom emoji is whitelisted to. If the emoji is not limited for
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
    
    def __new__(cls, data, guild_id):
        """
        Creates a new emoji object from emoji data included with it's guild's. If the emoji already exists, picks that
        up instead of creating a new one.
        
        This method can not create builtin (unicode) emojis. Those are created when the library is loaded.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Emoji data received from Discord.
        guild_id : ``int``
            The emoji's guild's identifier.
        
        Returns
        -------
        emoji : ``Emoji``
        """
        emoji_id = int(data['id'])

        try:
            self = EMOJIS[emoji_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = emoji_id
            EMOJIS[emoji_id] = self
            
            try:
                user_data = data['user']
            except KeyError:
                user = ZEROUSER
            else:
                user = User.from_data(user_data)
            self.user = user
            
        else:
            # whenever we receive an emoji, it will have no user data included, so it is enough if we check for user
            # data only whenever we receive emoji data from a request or so.
            if not self.partial:
                
                if self.user is ZEROUSER:
                    try:
                        user_data = data['user']
                    except KeyError:
                        pass
                    else:
                        self.user = User.from_data(user_data)
                
                return self
        
        self._set_attributes(data, guild_id)
        
        return self
    
    
    @classmethod
    def precreate(cls, emoji_id, **kwargs):
        """
        Precreates the emoji by creating a partial one with the given parameters. When the emoji is loaded
        the precreated one will be picked up. If an already existing emoji would be precreated, returns that
        instead and updates that only, if that is partial.
        
        Parameters
        ----------
        emoji_id : `int`
            The emoji's id.
        **kwargs : keyword parameters
            Additional predefined attributes for the emoji.
        
        Other Parameters
        ----------------
        animated : `bool`, Optional (Keyword only)
             The emoji's ``.animated``.
        available : `bool`, Optional (Keyword only)
             The emoji's ``.available``.
        guild_id : ``Guild``, `int`, Optional (Keyword only)
             The emoji's ``.guild_id``.
        name : `str`, Optional (Keyword only)
            The emoji's ``.name``. Can be between length `2` and `32`.
        require_colons : `bool`, Optional (Keyword only)
             The emoji's ``.require_colons``.
        roles : `None`, `iterable` of (``Role``, `int`), Optional (Keyword only)
            The emoji's ``.roles``.
        user : ``ClientUserBase`, `int`, Optional (Keyword only)
            The emoji's ``.user``.
        
        Returns
        -------
        self : ``Emoji``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        emoji_id = preconvert_snowflake(emoji_id, 'emoji_id')
        
        if kwargs:
            processable = []
            
            try:
                name = kwargs.pop('name')
            except KeyError:
                pass
            else:
                name = preconvert_str(name, 'name', 2, 32)
                processable.append(('name', name))
            
            for attribute_name in ('animated', 'available', 'managed', 'require_colons',):
                try:
                    attribute_value = kwargs.pop(attribute_name)
                except KeyError:
                    pass
                else:
                    animated = preconvert_bool(attribute_value, attribute_name)
                    processable.append((attribute_name, animated))
            
            
            for attribute_name, attribute_type, converter in (
                ('guild_id', Guild, instance_or_id_to_snowflake),
                ('user', (User, Client), instance_or_id_to_instance),
            ):
                try:
                    attribute_value = kwargs.pop(attribute_name)
                except KeyError:
                    pass
                else:
                    attribute_value = converter(attribute_value, attribute_type, attribute_name)
                    processable.append((attribute_name, attribute_value))
            
            
            try:
                roles = kwargs.pop('roles')
            except KeyError:
                pass
            else:
                if (roles is not None):
                    role_ids = iterable_of_instance_or_id_to_snowflakes(roles, Role, 'roles')
                    if role_ids:
                        role_ids = tuple(sorted(role_ids))
                        processable.append(('role_ids', role_ids))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs!r}.')
        
        else:
            processable = None
        
        
        try:
            self = EMOJIS[emoji_id]
        except KeyError:
            self = cls._create_empty(emoji_id)
            
            EMOJIS[emoji_id] = self
        else:
            if not self.partial:
                return self
        
        if (processable is not None):
            for name, value in processable:
                setattr(self, name, value)
        
        return self
    
    
    def __repr__(self):
        """Returns the emoji's representation."""
        return f'<{self.__class__.__name__} id={self.id}, name={self.name!r}>'
    
    
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
        >>> emoji = Emoji.precreate(now_as_id(), name='nice')
        >>> emoji
        <Emoji id=712359434843586560, name='nice'>
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
        
        guild_id = self.guild_id
        if not guild_id:
            return True
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            return True
        
        return guild.partial
    
    
    def is_custom_emoji(self):
        """
        Returns whether the emoji is a custom emoji.
        
        Returns
        -------
        is_custom_emoji : `bool`
        """
        return (self.id >= UNICODE_EMOJI_LIMIT)
    
    
    def is_unicode_emoji(self):
        """
        Returns whether the emoji is a unicode emoji.
        
        Returns
        -------
        is_custom_emoji : `bool`
        """
        return (self.id < UNICODE_EMOJI_LIMIT)
    
    
    @property
    def as_reaction(self):
        """
        Returns the emoji's reaction form, which is used by the Discord API at requests when working with reactions.
        
        Returns
        -------
        as_reaction : `str`
        """
        if self.id < UNICODE_EMOJI_LIMIT:
            return self.unicode
        
        return f'{self.name}:{self.id}'
    
    
    @property
    def as_emoji(self):
        """
        Returns the emoji's emoji form. Should be used when sending an emoji within a ``Message``.
        
        Returns
        -------
        as_emoji : `str`
        """
        if self.id < UNICODE_EMOJI_LIMIT:
            return self.unicode
        
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
        id_ = self.id
        if id_ > UNICODE_EMOJI_LIMIT:
            created_at = id_to_datetime(id_)
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
        data`dict` of (`str`, `Any`) items
            Emoji's data.
        guild_id : `int`
            The emoji's guild's identifier.
        """
        # guild_id is not present in the payload, so we receive it from the parameters.
        self.guild_id = guild_id
        
        # unicode
        self.unicode = None
        
        # user
        self.user = ZEROUSER
        
        # Update sets every attributes, except `.user`. That is only ste if present in the payload.
        self._update_attributes(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the emoji with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Emoji's data received from Discord.
        """
        # animated
        self.animated = data.get('animated', False)
        
        # available
        self.available = data.get('available', True)
        
        # managed
        self.managed = data.get('managed', False)
        
        # name
        name = data['name']
        if name is None:
            name = ''
        self.name = name
        
        # require_colons
        self.require_colons = data.get('require_colons', True)
        
        # role_ids
        role_ids = data.get('roles', None)
        if (role_ids is None) or (not role_ids):
            role_ids = None
        else:
            role_ids = tuple(sorted(int(role_id) for role_id in role_ids))
        self.role_ids = role_ids
        
        # user
        try:
            user_data = data['user']
        except KeyError:
            pass
        else:
            self.user = User.from_data(user_data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the emoji and returns it's overwritten old attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Emoji data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
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
        | role_ids          | `None`, `tuple` of ``Role`` |
        +-------------------+-------------------------------+
        """
        old_attributes = {}
        
        require_colons = data.get('require_colons', True)
        if self.require_colons != require_colons:
            old_attributes['require_colons'] = self.require_colons
            self.require_colons = require_colons
        
        managed = data.get('managed', False)
        if self.managed != managed:
            old_attributes['managed'] = self.managed
            self.managed = managed
        
        animated = data.get('animated', False)
        if self.animated != animated:
            old_attributes['animated'] = self.animated
            self.animated = animated
        
        name = data['name']
        if name is None:
            name = ''
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        role_ids = data.get('roles', None)
        if (role_ids is None) or (not role_ids):
            role_ids = None
        else:
            role_ids = tuple(sorted(int(role_id) for role_id in role_ids))
        
        if self.role_ids != role_ids:
            old_attributes['role_ids'] = self.role_ids
            self.role_ids = role_ids
        
        try:
            user_data = data['user']
        except KeyError:
            pass
        else:
            self.user = User.from_data(user_data)
        
        available = data.get('available', True)
        if self.available != available:
            old_attributes['available'] = self.available
            self.available = available
        
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
        emoji : ``Emoji``
        """
        emoji_id = int(emoji_id)
        
        try:
            self = EMOJIS[emoji_id]
            if self.partial:
                self.name = name
                self.animated = animated
        except KeyError:
            self = cls._create_empty(emoji_id)
            self.name = name
            self.animated = animated
            EMOJIS[emoji_id] = self
        
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
        self : ``Emoji``
            The created emoji.
        """
        self = object.__new__(cls)
        self.id = emoji_id
        self.animated = False
        self.name = ''
        self.unicode = None
        self.guild_id = 0
        self.available = True
        self.require_colons = True
        self.managed = False
        self.user = ZEROUSER
        self.role_ids = None
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
        self : ``Emoji``
            The created emoji.
        """
        emoji_id = cls._last_unicode_id + 1
        cls._last_unicode_id = emoji_id
        
        self = object.__new__(cls)
        self.id = emoji_id
        self.animated = False
        self.name = unicode.name
        self.unicode = unicode.value
        self.guild_id = 0
        self.available = True
        self.require_colons = True
        self.managed = False
        self.user = ZEROUSER
        self.role_ids = None
        
        EMOJIS[emoji_id] = self
        UNICODE_TO_EMOJI[unicode.value] = self
        
        if register_by_name:
            BUILTIN_EMOJIS[unicode.get_system_name()] = self
            
            for alternative_name in unicode.iter_alternative_names():
                BUILTIN_EMOJIS[alternative_name] = self
        
        return self
    
    
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
                key = id_sort_key,
            ))
        
        return roles
    
    
    def iter_roles(self):
        """
        Iterates over the emoji's roles. Not like ``.roles``, this will not sort the roles of the emoji based on their
        position, instead uses teh default ordering (id).
        
        This method is an iterable generator.
        
        Yields
        ------
        role : ``Role``
        """
        role_ids = self.role_ids
        if (role_ids is not None):
            for role_id in role_ids:
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
