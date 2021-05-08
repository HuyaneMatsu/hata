__all__ = ('BUILTIN_EMOJIS', 'UNICODE_TO_EMOJI', 'Emoji')

from ..bases import DiscordEntity
from ..core import EMOJIS
from ..utils import id_to_time, DISCORD_EPOCH_START, DATETIME_FORMAT_CODE
from ..user import User, ZEROUSER
from ..preconverters import preconvert_str, preconvert_bool, preconvert_snowflake
from ..role import create_partial_role

from .. import urls as module_urls

UNICODE_EMOJI_LIMIT = 1<<21

BUILTIN_EMOJIS = {}
UNICODE_TO_EMOJI = {}


class Emoji(DiscordEntity, immortal=True):
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
    guild : `None` or ``Guild``
        The emoji's guild. Can be set as `None` if:
        - If the emoji is a builtin (unicode).
        - If the emoji's guild is unknown.
        - If the emoji is deleted.
    managed : `bool`
        Whether the emoji is managed by an integration.
    name : `int`
        The emoji's name.
    roles : `None` or `list` of ``Role`` objects
        The set of roles for which the custom emoji is whitelisted to. If the emoji is not limited for specific roles,
        then this value is set to `None`. If the emoji is a builtin (unicode) emoji, then this attribute is set to
        `None` as  well.
    unicode : `None` or `str`
        At the case of custom emojis this attribute is always `None`, but at the case of builtin (unicode) emojis this
        attribute stores the emoji's unicode representation.
    user : ``User`` or ``Client``
        The creator of the custom emoji. The emoji must be requested from Discord's API, or it's user will be just
        the default `ZEROUSER`.
        
    See Also
    --------
    - ``create_partial_emoji`` : A function to create an emoji object from partial emoji data.
    - ``parse_emoji`` : Parses a partial emoji object out from text.
    """
    __slots__ = ('animated', 'available', 'guild', 'managed', 'name', 'require_colons', 'roles', 'unicode', 'user', )
    
    def __new__(cls, data, guild):
        """
        Creates a new emoji object from emoji data included with it's guild's. If the emoji already exists, picks that
        up instead of creating a new one.
        
        This method can not create builtin (unicode) emojis. Those are created when the library is loaded.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Emoji data received from Discord.
        guild : ``Guild``
            The guild of the emoji.
        
        Returns
        -------
        emoji : ``Emoji``
        """
        emoji_id = int(data['id'])

        try:
            emoji = EMOJIS[emoji_id]
        except KeyError:
            emoji = object.__new__(cls)
            emoji.id = emoji_id
            EMOJIS[emoji_id] = emoji
        else:
            # whenever we receive an emoji, it will have no user data included,
            # so it is enough if we check for user data only whenever we
            # receive emoji data from a request or so.
            if (emoji.guild is not None):
                if not emoji.user.id:
                    try:
                        user_data = data['user']
                    except KeyError:
                        pass
                    else:
                        emoji.user = User(user_data)
                return emoji
        
        name = data['name']
        if name is None:
            name = ''
        
        emoji.name = name
        emoji.animated = data.get('animated', False)
        emoji.require_colons= data.get('require_colons', True)
        emoji.managed = data.get('managed', False)
        emoji.guild = guild
        emoji.available = data.get('available', True)
        emoji.user = ZEROUSER
        emoji.unicode = None
        
        role_ids = data.get('roles', None)
        if (role_ids is None) or (not role_ids):
            roles = None
        else:
            roles = sorted(create_partial_role(int(role_id)) for role_id in role_ids)
        
        emoji.roles = roles
        
        return emoji
    
    @classmethod
    def precreate(cls, emoji_id, **kwargs):
        """
        Precreates the emoji by creating a partial one with the given parameters. When the emoji is loaded
        the precrated one will be picked up. If an already existing emoji would be precreated, returns that
        instead and updates that only, if that is partial.
        
        Parameters
        ----------
        emoji_id : `snowflake`
            The emoji's id.
        **kwargs : keyword arguments
            Additional predefined attributes for the emoji.
        
        Other Parameters
        ----------------
        name : `str`, Optional (Keyword only)
            The emoji's ``.name``. Can be between length `2` and `32`.
        animated : `bool`, Optional (Keyword only)
            Whether the emoji is animated.
        
        Returns
        -------
        emoji : ``Emoji``
        
        Raises
        ------
        TypeError
            If any argument's type is bad or if unexpected argument is passed.
        ValueError
            If an argument's type is good, but it's value is unacceptable.
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
                processable.append(('name',name))
            
            try:
                animated = kwargs.pop('animated')
            except KeyError:
                pass
            else:
                animated = preconvert_bool(animated, 'animated')
                processable.append(('animated', animated))
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        else:
            processable = None
        
        try:
            emoji = EMOJIS[emoji_id]
        except KeyError:
            emoji = object.__new__(cls)
            
            emoji.name = ''
            emoji.animated = False
            emoji.id = emoji_id 
            emoji.guild = None
            emoji.unicode = None
            emoji.user = ZEROUSER
            
            EMOJIS[emoji_id]= emoji
        else:
            if (emoji.guild is not None) or (emoji.unicode is not None):
                return emoji
        
        if (processable is not None):
            for name, value in processable:
                setattr(emoji, name, value)
        
        return emoji
    
    def __str__(self):
        """Returns the emoji's name."""
        return self.name
    
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
        >>> # no code stands for str(emoji)
        >>> f'{emoji}'
        'nice'
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
        'heart'
        >>> f'{emoji:e}'
        '❤️'
        >>> f'{emoji:r}'
        '❤️'
        >>> f'{emoji:c}'
        '2015.01.01-00:00:00'
        ```
        """
        if not code:
            return self.name
        
        if code == 'e':
            if self.id < UNICODE_EMOJI_LIMIT:
                return self.unicode
            
            if self.animated:
                return f'<a:{self.name}:{self.id}>'
            else:
                return f'<:{self.name}:{self.id}>'
        
        if code == 'r':
            if self.id < UNICODE_EMOJI_LIMIT:
                return self.unicode
            
            return f'{self.name}:{self.id}'
        
        if code == 'c':
            return self.created_at.__format__(DATETIME_FORMAT_CODE)
        
        raise ValueError(f'Unknown format code {code!r} for object of type {self.__class__.__name__!r}')
    
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
        
        if (self.guild is not None):
            return False
        
        return True
    
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
            created_at = id_to_time(id_)
        else:
            created_at = DISCORD_EPOCH_START
        
        return created_at

    url = property(module_urls.emoji_url)
    url_as = module_urls.emoji_url_as
    
    def _delete(self):
        """
        Removes the emoji's references.
        
        Used when the emoji is deleted.
        """
        guild = self.guild
        if guild is None:
            return
        
        del guild.emojis[self.id]
        self.roles = None
        self.guild = None
        self.available = False
        
    def _update_no_return(self, data):
        """
        Updates the emoji with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Emojis data received from Discord
        """
        self.require_colons = data.get('require_colons', True)
        self.managed = data.get('managed', False)
        
        self.animated = data.get('animated', False)
        
        name = data['name']
        if name is None:
            name = ''
        
        self.name = name
        
        role_ids = data.get('roles', None)
        if (role_ids is None) or (not role_ids):
            roles = None
        else:
            roles = sorted(create_partial_role(int(role_id)) for role_id in role_ids)
        
        self.roles = roles
        
        try:
            user_data = data['user']
        except KeyError:
            pass
        else:
            self.user = User(user_data)

        self.available = data.get('available', True)
            
    def _update(self, data):
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
        | roles             | `None` or `set` of ``Role``   |
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
            roles = None
        else:
            roles = sorted(create_partial_role(int(role_id)) for role_id in role_ids)
        
        if self.roles != roles:
            old_attributes['roles'] = self.roles
            self.roles = roles
        
        try:
            user_data = data['user']
        except KeyError:
            pass
        else:
            self.user = User(user_data)
        
        available = data.get('available', True)
        if self.available != available:
            old_attributes['available'] = self.available
            self.available = available
        
        return old_attributes
    
    @classmethod
    def _from_parsed_group(cls, groups):
        """
        Creates a new emoji from the given parsed out groups.
        
        Parameters
        ----------
        groups : `tuple` ((`str` or `None`), `str`, `str`)
            A tuple, which contains whether the emoji to create is animated (element 0), the emoji's name (element 1) and
            the emoji's id. (element 2).
        
        Returns
        -------
        emoji : ``Emoji``
        """
        animated, name, emoji_id = groups
        emoji_id = int(emoji_id)
        
        try:
            emoji = EMOJIS[emoji_id]
            if emoji.guild is None:
                emoji.name = name
        except KeyError:
            emoji = object.__new__(cls)
            emoji.id = emoji_id
            emoji.animated = (animated is not None)
            emoji.name = name
            emoji.unicode = None
            emoji.guild = None
            emoji.available = True
            emoji.require_colons = True
            emoji.managed = False
            emoji.user = ZEROUSER
            emoji.roles = None
            EMOJIS[emoji_id] = emoji
        
        return emoji
