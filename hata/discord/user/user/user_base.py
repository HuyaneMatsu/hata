__all__ = ('UserBase', )

import warnings
from re import I as re_ignore_case, compile as re_compile, escape as re_escape

from scarletio import copy_docs, include

from ...bases import DiscordEntity, ICON_TYPE_NONE, Icon, IconSlot, IconType, PlaceHolder, PlaceHolderFunctional
from ...color import Color
from ...http import urls as module_urls
from ...localization.utils import LOCALE_DEFAULT
from ...utils import DATETIME_FORMAT_CODE

from .fields import (
    parse_name, put_banner_color_into, put_bot_into, put_discriminator_into, put_display_name_into, put_flags_into,
    put_id_into, put_name_into, validate_name
)
from .flags import UserFlag
from .preinstanced import DefaultAvatar, PremiumType, Status


ZEROUSER = include('ZEROUSER')


class UserBase(DiscordEntity, immortal = True):
    """
    Base class for user instances.
    
    Attributes
    ----------
    avatar_hash : `int`
        The user's avatar's hash in `uint128`.
    avatar_type : ``IconType``
        The user's avatar's type.
    id : `int`
        The client's unique identifier number.
    name : str
        The client's username.
    
    Notes
    -----
    Instances of this type are weakreferable.
    """
    __slots__ = ('name', )
    
    avatar = IconSlot('avatar', 'avatar', module_urls.user_avatar_url, module_urls.user_avatar_url_as)
    
    def __new__(
        cls,
        *,
        avatar = ...,
        name = ...,
    ):
        """
        Creates a new partial user with the given fields.
        
        Parameters
        ----------
        avatar : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar.
        name : `str`, Optional (Keyword only)
            The user's name.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # avatar
        if avatar is ...:
            avatar = None
        else:
            avatar = cls.avatar.validate_icon(avatar, allow_data = True)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # Construct
        new = object.__new__(cls)
        new.avatar = avatar
        new.id = 0
        new.name = name
        return new
    
    
    def _update_attributes(self, data):
        """
        Updates the user with the given data by overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            User data received from Discord.
        """
        self._set_avatar(data)
        self.name = parse_name(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the user and returns it's overwritten attributes as a `dict` with a `attribute-name` - `old-value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            User data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        
        +-----------------------+-----------------------+-----------------------+
        | Keys                  | Values                | Applicable for        |
        +=======================+=======================+=======================+
        | avatar                | ``Icon``              | all                   |
        +-----------------------+-----------------------+-----------------------+
        | avatar_decoration     | ``Icon``              | ``Client``, ``User``  |
        +-----------------------+-----------------------+-----------------------+
        | banner                | ``Icon``              | ``Client``, ``User``  |
        +-----------------------+-----------------------+-----------------------+
        | banner_color          | `None`, ``Color``     | ``Client``, ``User``  |
        +-----------------------+-----------------------+-----------------------+
        | channel_id            | `int`                 | ``Webhook``           |
        +-----------------------+-----------------------+-----------------------+
        | discriminator         | `int`                 | ``Client``, ``User``  |
        +-----------------------+-----------------------+-----------------------+
        | display_name          | `None`, `str`         | ``Client``, ``User``  |
        +-----------------------+-----------------------+-----------------------+
        | email                 | `None`, `str`         | ``Client``            |
        +-----------------------+-----------------------+-----------------------+
        | email_verified        | `bool`                | ``Client``            |
        +-----------------------+-----------------------+-----------------------+
        | flags                 | ``UserFlag``          | ``Client``, ``User``  |
        +-----------------------+-----------------------+-----------------------+
        | locale                | ``Locale``            | ``Client``            |
        +-----------------------+-----------------------+-----------------------+
        | mfa                   | `bool`                | ``Client``            |
        +-----------------------+-----------------------+-----------------------+
        | name                  | `str`                 | all                   |
        +-----------------------+-----------------------+-----------------------+
        | premium_type          | ``PremiumType``       | ``Client``            |
        +-----------------------+-----------------------+-----------------------+
        """
        old_attributes = {}
        
        self._update_avatar(data, old_attributes)
        
        name = parse_name(data)
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        return old_attributes
    
    
    @classmethod
    def _create_empty(cls, user_id):
        """
        Creates a user with its default attributes values set.
        
        Parameters
        ----------
        user_id : `int`
            The user's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = user_id
        self._set_default_attributes()
        return self
    
    
    def _set_default_attributes(self):
        """
        Sets the user's attribute's to their default.
        """
        self.avatar_hash = 0
        self.avatar_type = ICON_TYPE_NONE
        self.name = ''
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new user from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            User data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        raise NotImplementedError(
            f'`{cls.__class__.__name__}` does not support `.from_data` operation, please call it on a sub-type of it.'
        )
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Tries to convert the user back to a json serializable dictionary.
        
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
        
        type(self).avatar.put_into(self.avatar, data, defaults, as_data = not include_internals)
        
        banner_slot = type(self).banner
        if isinstance(banner_slot, IconSlot):
            banner_slot.put_into(self.banner, data, defaults, as_data = not include_internals)
        else:
            if defaults:
                data['banner'] = None
        
        avatar_decoration_slot = type(self).avatar_decoration
        if isinstance(avatar_decoration_slot, IconSlot):
            avatar_decoration_slot.put_into(self.avatar_decoration, data, defaults, as_data = not include_internals)
        else:
            if defaults:
                data['avatar_decoration'] = None
        
        put_banner_color_into(self.banner_color, data, defaults)
        put_discriminator_into(self.discriminator, data, defaults)
        put_display_name_into(self.display_name, data, defaults)
        put_name_into(self.name, data, defaults)
        
        if include_internals:
            put_bot_into(self.bot, data, defaults)
            put_id_into(self.id, data, defaults)
            put_flags_into(self.flags, data, defaults)
        
        return data
    
    
    def copy(self):
        """
        Copies the user returning a new partial one.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.avatar = self.avatar
        new.id = 0
        new.name = self.name
        return new
    
    
    def copy_with(
        self,
        *,
        avatar = ...,
        name = ...,
    ):
        """
        Copies the user with the given fields.
        
        Parameters
        ----------
        avatar : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The user's avatar.
        name : `str`, Optional (Keyword only)
            The user's name.
        
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
        # avatar
        if avatar is ...:
            avatar = self.avatar
        else:
            avatar = type(self).avatar.validate_icon(avatar, allow_data = True)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # Construct
        new = object.__new__(type(self))
        new.avatar = avatar
        new.id = 0
        new.name = name
        return new
    
    
    def __repr__(self):
        """Returns the user's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        user_id = self.id
        if user_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(user_id))
            repr_parts.append(',')
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.full_name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __format__(self, code):
        """
        Formats the user in a format string.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        user : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        
        Examples
        --------
        ```py
        >>> from hata import User, now_as_id
        >>> user = User.precreate(now_as_id(), name = 'Neko', discriminator = 2012)
        >>> user
        <User id = 730233383967260672, name = 'Neko#2012'>
        >>> # no code stands for `user.name`.
        >>> f'{user}'
        'Neko'
        >>> # 'f' stands for full name
        >>> f'{user:f}'
        'Neko#2012'
        >>> # 'm' stands for mention.
        >>> f'{user:m}'
        '<@730233383967260672>'
        >>> # 'c' stands for created at.
        >>> f'{user:c}'
        '2020.07.08-01:26:45'
        ```
        """
        if not code:
            return self.name
        
        if code == 'f':
            return self.full_name
        
        if code == 'm':
            return self.mention
        
        if code == 'c':
            return format(self.created_at, DATETIME_FORMAT_CODE)
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}, {"c"!r}, {"f"!r}, {"m"!r}.'
        )
    
    def __hash__(self):
        """Returns the user's hash."""
        user_id = self.id
        if user_id or (self is ZEROUSER):
            return user_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Returns a partial user's hash value.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # avatar
        hash_value ^= hash(self.avatar)
        
        # id | Internal -> skip
        
        # name
        hash_value ^= hash(self.name)
        
        return hash_value
    
    
    # Sorting
    
    def __gt__(self, other):
        """Returns whether the user's id is greater than the other's."""
        if not isinstance(other, UserBase):
            return NotImplemented
        
        return self.id > other.id
    
    
    def __ge__(self, other):
        """Returns whether the user's id is greater or equal to the other."""
        if not isinstance(other, UserBase):
            return NotImplemented
        
        if self.id > other.id:
            return True
        
        return self._is_equal_same_type(other)
    
    
    def __eq__(self, other):
        """Return whether the user's id is equal to the other."""
        if not isinstance(other, UserBase):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the user's id is different as the other's."""
        if not isinstance(other, UserBase):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def __le__(self, other):
        """Returns whether the user's id is less or equal to the other."""
        if not isinstance(other, UserBase):
            return NotImplemented
        
        if self.id < other.id:
            return True
        
        return self._is_equal_same_type(other)
    
    
    def __lt__(self, other):
        """Returns whether the user's id is less than the other's."""
        if not isinstance(other, UserBase):
            return NotImplemented
        
        return self.id < other.id
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two users are equal. `self` and `other` must be the same type.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other user.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if ((self_id or self is ZEROUSER) and (other_id or other is ZEROUSER)):
            return self_id == other_id
        
        return self._compare_attributes(other)
    
    
    def _compare_user_attributes_extended(self, other):
        """
        Compares the two user's user attributes (excluding id obviously).
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other user.
        
        Returns
        -------
        is_equal : `bool`
        """
        # activities
        if (self.activities != other.activities):
            return False
        
        # avatar_hash
        if (self.avatar_hash != other.avatar_hash):
            return False
        
        # avatar_type
        if (self.avatar_type != other.avatar_type):
            return False
        
        # avatar_decoration_hash
        if (self.avatar_decoration_hash != other.avatar_decoration_hash):
            return False
        
        # avatar_decoration_type
        if (self.avatar_decoration_type != other.avatar_decoration_type):
            return False
        
        # banner_color
        if (self.banner_color != other.banner_color):
            return False
        
        # banner_hash
        if (self.banner_hash != other.banner_hash):
            return False
        
        # banner_type
        if (self.banner_type != other.banner_type):
            return False
        
        # bot
        if (self.bot != other.bot):
            return False
        
        # discriminator
        if (self.discriminator != other.discriminator):
            return False
        
        # display_name
        if (self.display_name != other.display_name):
            return False
        
        # email
        if (self.email != other.email):
            return False
        
        # email_verified
        if (self.email_verified != other.email_verified):
            return False
        
        # flags
        if (self.flags != other.flags):
            return False
        
        # locale
        if (self.locale is not other.locale):
            return False
        
        # mfa
        if (self.mfa != other.mfa):
            return False
        
        # name
        if (self.name != other.name):
            return False
        
        # premium_type
        if (self.premium_type is not other.premium_type):
            return False
        
        # status
        if (self.status is not other.status):
            return False
        
        # statuses
        if (self.statuses != other.statuses):
            return False
        
        return True
    
    
    _compare_attributes = _compare_user_attributes_extended
    
    # Place holders
    
    activities = PlaceHolder(
        None,
        """
        Returns the user's activities.
        
        Returns
        -------
        activities : `None`, `list` of ``Activity``
        """
    )
    
    
    avatar_decoration = PlaceHolderFunctional(
        (lambda : Icon(IconType.none, 0)),
        """
        Returns the user's avatar decoration.
        
        Returns
        -------
        avatar_decoration : ``Icon``
        """
    )
    
    
    avatar_decoration_hash = PlaceHolder(
        0,
        """
        Returns the user's avatar decoration's hash.
        
        Returns
        -------
        avatar_decoration_hash : `int`
        """,
    )
    
    
    avatar_decoration_type = PlaceHolder(
        IconType.none,
        """
        Returns the user's avatar decoration's type.
        
        Returns
        -------
        avatar_decoration_type : ``IconType``
        """,
    )
    
    
    banner = PlaceHolderFunctional(
        (lambda : Icon(IconType.none, 0)),
        """
        Returns the user's banner.
        
        Returns
        -------
        banner : ``Icon``
        """
    )
    
    
    banner_color = PlaceHolder(
        None,
        """
        Returns the user's banner color.
        
        Returns
        -------
        banner_color : `None`, ``Color``
        """
    )
    
    
    banner_hash = PlaceHolder(
        0,
        """
        Returns the user's banner's hash.
        
        Returns
        -------
        banner_hash : `int`
        """,
    )
    
    
    banner_type = PlaceHolder(
        IconType.none,
        """
        Returns the user's banner's type.
        
        Returns
        -------
        banner_type : ``IconType``
        """,
    )
    
    
    @property
    @copy_docs(module_urls.user_banner_url)
    def banner_url(self):
        return None
    
    
    @copy_docs(module_urls.user_banner_url_as)
    def banner_url_as(self, ext = None, size = None):
        return None
    
    
    @property
    @copy_docs(module_urls.user_avatar_decoration_url)
    def avatar_decoration_url(self):
        return None
    
    
    @copy_docs(module_urls.user_avatar_decoration_url_as)
    def avatar_decoration_url_as(self, ext = None, size = None):
        return None
    
    
    bot = PlaceHolder(
        False,
        """
        Returns whether the user is a bot or a user account.
        
        Returns
        -------
        bot : `bool`
        """,
    )
    
    
    discriminator = PlaceHolder(
        0,
        """
        Returns the user's discriminator.
        
        Returns
        -------
        discriminator : `bool`
        """,
    )
    
    
    display_name = PlaceHolder(
        None,
        """
        Returns the user's non-unique display name.
        
        Returns
        -------
        display_name : `None`, `str`
        """,
    )
    
    
    email = PlaceHolder(
        None,
        """
        Returns the user's email.
        
        Returns
        -------
        email : `None`, `str`
        """,
    )
    
    
    email_verified = PlaceHolder(
        False,
        """
        Returns the user's email is verified.
        
        Returns
        -------
        email_verified : `bool`
        """,
    )
    
    
    flags = PlaceHolder(
        UserFlag(),
        """
        Returns the user's flags.
        
        Returns
        -------
        flags : ``UserFlag``
        """
    )
    
    
    guild_profiles = PlaceHolderFunctional(
        (lambda : {}),
        """
        Returns a dictionary, which contains the user's guild profiles. If the user is member of a guild, then it should
        have a respective guild profile accordingly.
        
        Returns
        -------
        guild_profiles : `dict` of (`int`, ``GuildProfile``) items
        """
    )
    
    
    locale = PlaceHolder(
        LOCALE_DEFAULT,
        """
        Returns preferred locale by the user.
        
        Returns
        -------
        locale : ``Locale``
        """
    )
    
    
    mfa = PlaceHolder(
        False,
        """
        Returns whether the user has two factor authorization enabled on the account.
        
        Returns
        -------
        mfa : `bool`
        """
    )
    
    
    premium_type = PlaceHolder(
        PremiumType.none,
        """
        Returns the Nitro subscription type of the user.
        
        Returns
        -------
        premium_type : ``PremiumType``
        """
    )
    
    
    status = PlaceHolder(
        Status.offline,
        """
        Returns the user's display status.
        
        Returns
        -------
        status  ``Status``
        """
    )
    
    
    statuses = PlaceHolder(
        None,
        """
        Returns the user's statuses for each platform.
        
        Returns
        -------
        statuses : `None`, `dict` of (`str`, `str`) items
        """
    )
    
    
    thread_profiles = PlaceHolder(
        None,
        """
        Returns the user's activities.
        
        Returns
        -------
        activities : `None`, `tuple` of ``Activity``
        """
    )
    
    # Properties
    
    @property
    def full_name(self):
        """
        The user's name with it's discriminator.
        
        Returns
        -------
        full_name : `str`
        """
        discriminator = self.discriminator
        if discriminator:
            return f'{self.name}#{discriminator:0>4}'
        
        return self.name
    
    
    @property
    def mention(self):
        """
        The mention of the user.
        
        Returns
        -------
        mention : `str`
        """
        return f'<@{self.id}>'
    
    
    @property
    def mention_nick(self):
        """
        The mention to the user's nick.
        
        Returns
        -------
        mention : `str`
        
        Notes
        -----
        It actually has nothing to do with the user's nickname > <.
        """
        return f'<@!{self.id}>'
    
    
    @property
    def default_avatar_url(self):
        """
        Returns the user's default avatar's url.
        
        Returns
        -------
        default_avatar_url : `str`
        """
        return DefaultAvatar.for_(self).url
    
    
    @property
    def default_avatar(self):
        """
        Returns the user's default avatar.
        
        Returns
        -------
        default_avatar : ``DefaultAvatar``
        """
        return DefaultAvatar.for_(self)
    
    
    def iter_activities(self):
        """
        Iterates over the user's activities.
        
        This method is an iterable generator.
        
        Yields
        ------
        activity : ``Activity``
        """
        activities = self.activities
        if (activities is not None):
            yield from activities
    
    
    @property
    def is_bot(self):
        """
        Returns whether the user is a bot or a user account.
        
        This property is deprecated and will be removed in 2023 August.
        
        Returns
        -------
        bot : `bool`
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.is_bot` is deprecated and will be removed in 2023 August.'
                f'Please use `.bot` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.bot
    
    
    @property
    def verified(self):
        """
        Deprecated and will be removed in 2023 August.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.verified` is deprecated and will be removed in 2023 August.'
                f'Please use `.email_verified` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.email_verified
    
    
    @property
    def partial(self):
        """
        Returns whether the user is partial. Partial users have only their ``.id`` set and every other field might not
        reflect the reality.
        
        Returns
        -------
        partial : `bool`
        """
        return True
    
    
    @property
    def activity(self):
        """
        Returns the user's top activity if applicable. If not.
        
        Returns
        -------
        activity : ``Activity``, `None`
        """
        return None
    
    
    @property
    def custom_activity(self):
        """
        Returns the user's custom activity if applicable.
        
        Returns
        -------
        activity : ``Activity``, `None`
        """
        return None
    
    
    @property
    def platform(self):
        """
        Returns the user's top status's platform. If the user is offline it will return an empty string.
        
        Returns
        -------
        platform : `str`
        """
        return ''
    
    
    def get_status_by_platform(self, platform):
        """
        Gets the user's status by the given platform.
        
        Parameters
        ----------
        platform : `str`
            The platform to get the status for.
        
        Returns
        -------
        status : ``Status``
            Defaults to `status.offline` if the user has no specific status for the given platform.
        """
        return Status.offline
    
    
    def color_at(self, guild):
        """
        Returns the user's color at the given guild.
        
        Parameters
        ----------
        guild : `None`, ``Guild``, `int`
            The guild, where the user's color will be checked.
            
            Can be given as `None`.

        Returns
        -------
        color : ``Color``
        """
        return Color()
    
    
    def name_at(self, guild):
        """
        Returns the user's name at the given guild.
        
        Parameters
        ----------
        guild : `None`, ``Guild``, `int`
            The guild, where the user's nick will be checked.
            
            Can be given as `None`.

        Returns
        -------
        name : `str`
        """
        display_name = self.display_name
        if (display_name is not None):
            return display_name
        
        return self.name
    
    
    def has_name_like(self, name):
        """
        Returns whether the user's name is like the given string.
        
        Parameters
        ----------
        name : `str`
            The name of the user.
        
        Returns
        -------
        has_name_like : `bool`
        """
        if name.startswith('@'):
            name = name[1:]
        
        name_length = len(name)
        if name_length < 1:
            return False
        
        if name_length > 5:
            if name_length > 37:
                return False
            
            if name[-5] == '#':
                try:
                    discriminator = int(name[-4:])
                except ValueError:
                    pass
                else:
                    stripped_name = name[:-5]
                    if (self.discriminator == discriminator) and (self.name == stripped_name):
                        return True
        
        if name_length > 32:
            return False
        
        pattern = re_compile(re_escape(name), re_ignore_case)
        
        if pattern.search(self.name) is not None:
            return True
        
        display_name = self.display_name
        if (display_name is not None) and (pattern.search(display_name) is not None):
            return True
        
        return False
    
    
    def has_name_like_at(self, name, guild):
        """
        Returns whether the user's name is like the given string.
        
        Parameters
        ----------
        name : `str`
            The name of the user.
        
        guild : `None`, ``Guild``, `int`
            The guild, where the user's nick will be also checked.
            
            Can be given as `None`.
        
        Returns
        -------
        has_name_like : `bool`
        """
        return self.has_name_like(name)
    
    
    def mentioned_in(self, message):
        """
        Returns whether the user is mentioned at a given message.
        
        Parameters
        ----------
        message : ``Message``
            The message, what's mentions will be checked.
        
        Returns
        -------
        mentioned : `bool`
        """
        if message.mentioned_everyone:
            return True
        
        mentioned_users = message.mentioned_users
        if (mentioned_users is not None) and (self in mentioned_users):
            return True
        
        mentioned_roles = message.mentioned_roles
        if (mentioned_roles is not None):
            guild_id = message.guild_id
            if guild_id:
                try:
                    guild_profile = self.guild_profiles[guild_id]
                except KeyError:
                    pass
                else:
                    roles = guild_profile.roles
                    if (roles is not None):
                        for role in roles:
                            if role in mentioned_roles:
                                return True
        
        return False
    
    
    def has_role(self, role):
        """
        Returns whether the user has the given role.
        
        Parameters
        ----------
        role : ``Role``
            The role what will be checked.

        Returns
        -------
        has_role : `bool`
        """
        return False
    
    
    def top_role_at(self, guild, default = None):
        """
        Returns the top role of the user at the given guild.
        
        Parameters
        ----------
        guild : `None`, ``Guild``, `int`
            The guild where the user's top role will be looked up.
        
        default : `object` = `None`, Optional
            If the user is not a member of the guild, or if has no roles there, then the given default value is returned.
            Defaults to `None`.
        
        Returns
        -------
        top_role ``Role``, `default`
        """
        return default
    
    
    def can_use_emoji(self, emoji):
        """
        Returns whether the user can use the given emoji.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to check.
        
        Returns
        -------
        can_use_emoji : `bool`
        """
        if emoji.is_unicode_emoji():
            return True
        
        return False
    
    
    def has_higher_role_than(self, role):
        """
        Returns whether the user has higher role than the given role at it's respective guild.
        
        If the user is the owner of the guild, then returns `True` even if it has lower role.
        
        Parameters
        ----------
        role : ``Role``
            The role to check.
        
        Returns
        -------
        has_higher_role_than : `bool`
        """
        return False
    
    
    def has_higher_role_than_at(self, user, guild):
        """
        Returns whether the user has higher role as the other one at the given guild.
        
        Parameters
        ----------
        user : ``User``
            The other user to check.
        guild : ``Guild``, `None`, `int`
            The guild where the users' top roles will be checked.
            
            Can be given as `None`.
        
        Returns
        -------
        has_higher_role_than_at : `bool`
        """
        return False
    
    
    def get_guild_profile_for(self, guild):
        """
        Returns the user's guild profile for the given guild.
        
        Parameters
        ----------
        guild : `None`, ``Guild``, `int`
            The guild to get guild profile for.
        
        Returns
        -------
        guild_profile : `None`, ``Guild``
        """
        return None
    
    
    def iter_guilds_and_profiles(self):
        """
        Iterates over the guild profiles of the user.
        
        This method is an iterable generator.
        
        Yields
        ------
        guild : ``Guild``
            The guild profile's guild.
        guild_profile : ``GuildProfile``
            The user's guild profile in the guild.
        """
        return
        yield
    
    
    def iter_guilds(self):
        """
        Iterates over the guilds of the user.
        
        This method is an iterable generator.
        
        Yields
        ------
        guild : ``Guild``
            The guild profile's guild.
        """
        return
        yield
    
    
    def is_boosting(self, guild):
        """
        Returns whether the user is boosting the given guild.
        
        Parameters
        ----------
        guild : `None`, ``Guild``, `int`
            The guild to get whether the user is booster of.
        
        Returns
        -------
        is_boosting : `bool`
        """
        return False
    
    
    avatar_url_for = module_urls.user_avatar_url_for
    avatar_url_for_as = module_urls.user_avatar_url_for_as
    avatar_url_at = module_urls.user_avatar_url_at
    avatar_url_at_as = module_urls.user_avatar_url_at_as
    
    
    def _delete(self):
        """
        Deletes the user from it's guilds.
        """
        pass
    
    
    def _difference_update_presence(self, data):
        """
        Updates the user's presence and returns it's overwritten attributes as a `dict` with a `attribute-name` -
        `old-value` relation. An exception from this is `activities`, because that's a ``ActivityChange``
        containing all the changes of the user's activities.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received guild member data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        +---------------+-------------------------------------------+
        | Keys          | Values                                    |
        +===============+===========================================+
        | activities    | ``ActivityChange``                        |
        +---------------+-------------------------------------------+
        | status        | ``Status``                                |
        +---------------+-------------------------------------------+
        | statuses      | `None`, `dict` of (`str`, `str`) items    |
        +---------------+-------------------------------------------+
        """
        return {}
    
    
    def _update_presence(self, data):
        """
        Updates the user's presences with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received guild member data.
        """
        pass
    
    
    @classmethod
    def _update_profile(cls, data, guild):
        """
        First tries to find the user, then it's respective guild profile for the given guild to update it.
        
        If the method cannot find the user, or the respective guild profile, then creates them.
        
        Not like ``._difference_update_profile``, this method not calculates changes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received guild member data.
        guild : ``Guild``
            The respective guild of the profile to update.
        
        Returns
        -------
        user : ``ClientUserbase``
            The updated user.
        """
        raise NotImplementedError
    
    
    @classmethod
    def _difference_update_profile(cls, data, guild):
        """
        First tries to find the user, then it's respective guild profile for the given guild to update it.
        
        If the method cannot find the user, or the respective guild profile, then creates them.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received guild member data.
        guild : ``Guild``
            The respective guild of the profile to update.

        Returns
        -------
        user : ``ClientUserBase``
            The respective user.
        old_attributes : `dict` of (`str`, `object`) items
            The changed attributes of the respective guild profile as a `dict` with `attribute-name` - `old-attribute`
            relation.
            
            The possible keys and values within `old_attributes` are all optional and they can be any of the following:
            +-------------------+-------------------------------+
            | Keys              | Values                        |
            +===================+===============================+
            | avatar            | ``Icon``                      |
            +-------------------+-------------------------------+
            | boosts_since      | `None`, `datetime`            |
            +-------------------+-------------------------------+
            | flags             | `None`, ``GuildProfileFlags`` |
            +-------------------+-------------------------------+
            | nick              | `None`, `str`                 |
            +-------------------+-------------------------------+
            | pending           | `bool`                        |
            +-------------------+-------------------------------+
            | role_ids          | `None`, `tuple` of `int`      |
            +-------------------+-------------------------------+
            | timed_out_until   | `None`, `datetime`            |
            +-------------------+-------------------------------+
        """
        raise NotImplementedError
