__all__ = ('Oauth2User',)

from scarletio import copy_docs

from ...localization.utils import LOCALE_DEFAULT
from ...user import OrinUserBase, PremiumType, UserFlag
from ...user.user.fields import (
    parse_email, parse_email_verified, parse_id, parse_locale, parse_mfa_enabled, parse_premium_type, put_email,
    put_email_verified, put_locale, put_mfa_enabled, put_oauth2_flags_into, put_premium_type,
    validate_email, validate_email_verified, validate_locale, validate_mfa_enabled, validate_premium_type
)

from ..oauth2_access import Oauth2Access


class Oauth2User(OrinUserBase):
    """
    Represents a Discord user with extra personal information. If a ``Oauth2User`` is  created it will NOT overwrite the
    already existing user with the same ID, if exists.
    
    Attributes
    ----------
    access : ``Oauth2Access``
        Source oauth2 access.
    
    avatar_hash : `int`
        The user's avatar's hash in `uint128`.
    
    avatar_type : ``IconType``
        The user's avatar's type.
    
    avatar_decoration : ``None | AvatarDecoration``
        The user's avatar decorations.
    
    banner_color : `None`, ``Color``
        The user's banner color if has any.
    
    banner_hash : `int`
        The user's banner's hash in `uint128`.
    
    banner_type : ``IconType``
        The user's banner's type.
    
    discriminator : `int`
        The user's discriminator. Given to avoid overlapping names.
    
    display_name : `None | str`
        The user's non-unique display name.
    
    email : `None | str`
        The user's email. Defaults to `None`.
    
    email_verified : `bool`
        Whether the email of the user is verified.
    
    flags : ``UserFlag``
        The user's user flags.
    
    id : `int`
        The user's unique identifier number.
    
    locale : ``Locale``
        The preferred locale by the user.
    
    mfa_enabled : `bool`
        Whether the user has two factor authorization enabled on the account.
    
    name : str
        The user's username.
    
    name_plate : ``None | NamePlate``
        The user's name plate.
    
    premium_type : ``PremiumType``
        The Nitro subscription type of the user.
    
    primary_guild_badge : ``None | GuildBadge``
        The user's primary guild's badge.
    """
    __slots__ = ('access', 'email', 'email_verified', 'locale', 'mfa_enabled', 'premium_type')
    
    def __new__(
        cls,
        *,
        avatar = ...,
        avatar_decoration = ...,
        banner = ...,
        banner_color = ...,
        discriminator = ...,
        display_name = ...,
        email = ...,
        email_verified = ...,
        flags = ...,
        locale = ...,
        mfa_enabled = ...,
        name = ...,
        name_plate = ...,
        premium_type = ...,
        primary_guild_badge = ...,
    ):
        """
        Creates a new partial oauth2 user with the given fields.
        
        Parameters
        ----------
        avatar : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The user's avatar.
        
        avatar_decoration : ``None | AvatarDecoration``, Optional (Keyword only)
            The user's avatar decoration.
        
        banner : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The user's banner.
        
        banner_color : `None`, ``Color``, `int`, Optional (Keyword only)
            The user's banner color.
        
        discriminator : `str`, `int`, Optional (Keyword only)
            The user's discriminator.
        
        display_name : `None | str`, Optional (Keyword only)
            The user's non-unique display name.
        
        email : `None, `str`, Optional (Keyword only)
            The user's email.
        
        email_verified : `bool`, Optional (Keyword only)
            Whether the email of the user is verified.
        
        flags : `int`, ``UserFlag``, Optional (Keyword only)
            The user's flags.
        
        locale : ``Locale``, `str`, Optional (Keyword only)
            The preferred locale by the user.
        
        mfa_enabled : `bool`, Optional (Keyword only)
            Whether the user has two factor authorization enabled on the account.
        
        name : `str`, Optional (Keyword only)
            The user's name.
        
        name_plate : ``None | NamePlate``, Optional (Keyword only)
            The user's name plate.
        
        premium_type : ``None | int | PremiumType``, Optional (Keyword only)
            The Nitro subscription type of the user.
        
        primary_guild_badge : ``None | GuildBadge``, Optional (Keyword only)
            The user's primary guild's badge.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # email
        if email is ...:
            email = None
        else:
            email = validate_email(email)
        
        # email_verified
        if email_verified is ...:
            email_verified = False
        else:
            email_verified = validate_email_verified(email_verified)
        
        # locale
        if locale is ...:
            locale = LOCALE_DEFAULT
        else:
            locale = validate_locale(locale)
        
        # mfa_enabled
        if mfa_enabled is ...:
            mfa_enabled = False
        else:
            mfa_enabled = validate_mfa_enabled(mfa_enabled)
        
        # premium_type
        if premium_type is ...:
            premium_type = PremiumType.none
        else:
            premium_type = validate_premium_type(premium_type)
        
        # Construct
        self = OrinUserBase.__new__(
            cls,
            avatar = avatar,
            avatar_decoration = avatar_decoration,
            banner = banner,
            banner_color = banner_color,
            discriminator = discriminator,
            display_name = display_name,
            flags = flags,
            name = name,
            name_plate = name_plate,
            primary_guild_badge = primary_guild_badge,
        )
        self.access = Oauth2Access()
        self.email = email
        self.email_verified = email_verified
        self.locale = locale
        self.mfa_enabled = mfa_enabled
        self.premium_type = premium_type
        return self
    
    
    @classmethod
    def from_data(cls, data, access):
        """
        Creates a new ``Oauth2User`` instance.
        
        Parameters
        ----------
        data : `dict<str, object>`
            User data.
        access : ``Oauth2Access``
            Source oauth2 access.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.access = access
        self.id = parse_id(data)
        self._update_attributes(data)
        return self
    
    
    @copy_docs(OrinUserBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False):
        data = OrinUserBase.to_data(self, defaults = defaults, include_internals = include_internals)
        put_email(self.email, data, defaults)
        put_email_verified(self.email_verified, data, defaults)
        put_locale(self.locale, data, defaults)
        put_mfa_enabled(self.mfa_enabled, data, defaults)
        put_oauth2_flags_into(self.flags, data, defaults)
        put_premium_type(self.premium_type, data, defaults)
        return data
    
    
    @copy_docs(OrinUserBase._update_attributes)
    def _update_attributes(self, data):
        OrinUserBase._update_attributes(self, data)
        
        self.email = parse_email(data)
        self.email_verified = parse_email_verified(data)
        self.locale = parse_locale(data)
        self.mfa_enabled = parse_mfa_enabled(data)
        self.premium_type = parse_premium_type(data)
    
    
    @copy_docs(OrinUserBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = OrinUserBase._difference_update_attributes(self, data)
        
        email = parse_email(data)
        if self.email != email:
            old_attributes['email'] = self.email
            self.email = email
        
        email_verified = parse_email_verified(data)
        if self.email_verified != email_verified:
            old_attributes['email_verified'] = self.email_verified
            self.email_verified = email_verified
        
        locale = parse_locale(data)
        if self.locale is not locale:
            old_attributes['locale'] = self.locale
            self.locale = locale
        
        mfa_enabled = parse_mfa_enabled(data)
        if self.mfa_enabled != mfa_enabled:
            old_attributes['mfa_enabled'] = self.mfa_enabled
            self.mfa_enabled = mfa_enabled
        
        premium_type = parse_premium_type(data)
        if self.premium_type is not premium_type:
            old_attributes['premium_type'] = self.premium_type
            self.premium_type = premium_type
        
        return old_attributes
    
    
    @copy_docs(OrinUserBase._set_default_attributes)
    def _set_default_attributes(self):
        OrinUserBase._set_default_attributes(self)
        
        self.access = Oauth2Access()
        self.email = None
        self.email_verified = False
        self.locale = LOCALE_DEFAULT
        self.mfa_enabled = False
        self.premium_type = PremiumType.none
    
    
    @copy_docs(OrinUserBase._set_default_attributes)
    def copy(self):
        new = OrinUserBase.copy(self)
        new.access = Oauth2Access()
        new.email = self.email
        new.email_verified = self.email_verified
        new.locale = self.locale
        new.mfa_enabled = self.mfa_enabled
        new.premium_type = self.premium_type
        return new
    
    
    def copy_with(
        self,
        *,
        avatar = ...,
        avatar_decoration = ...,
        banner = ...,
        banner_color = ...,
        discriminator = ...,
        display_name = ...,
        email = ...,
        email_verified = ...,
        flags = ...,
        locale = ...,
        mfa_enabled = ...,
        name = ...,
        name_plate = ...,
        premium_type = ...,
        primary_guild_badge = ...,
    ):
        """
        Creates a new partial oauth2 user with the given fields.
        
        Parameters
        ----------
        avatar : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The user's avatar.
        
        avatar_decoration : ``None | AvatarDecoration``, Optional (Keyword only)
            The user's avatar decoration.
        
        banner : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The user's banner.
        
        banner_color : `None`, ``Color``, `int`, Optional (Keyword only)
            The user's banner color.
        
        discriminator : `str`, `int`, Optional (Keyword only)
            The user's discriminator.
        
        display_name : `None | str`, Optional (Keyword only)
            The user's non-unique display name.
        
        email : `None, `str`, Optional (Keyword only)
            The user's email.
        
        email_verified : `bool`, Optional (Keyword only)
            Whether the email of the user is verified.
        
        flags : `int`, ``UserFlag``, Optional (Keyword only)
            The user's flags.
        
        locale : ``Locale``, `str`, Optional (Keyword only)
            The preferred locale by the user.
        
        mfa_enabled : `bool`, Optional (Keyword only)
            Whether the user has two factor authorization enabled on the account.
        
        name : `str`, Optional (Keyword only)
            The user's name.
        
        name_plate : ``None | NamePlate``, Optional (Keyword only)
            The user's name plate.
        
        premium_type : ``None | int | PremiumType``, Optional (Keyword only)
            The Nitro subscription type of the user.
        
        primary_guild_badge : ``None | GuildBadge``, Optional (Keyword only)
            The user's primary guild's badge.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # email
        if email is ...:
            email = self.email
        else:
            email = validate_email(email)
        
        # email_verified
        if email_verified is ...:
            email_verified = self.email_verified
        else:
            email_verified = validate_email_verified(email_verified)
        
        # locale
        if locale is ...:
            locale = self.locale
        else:
            locale = validate_locale(locale)
        
        # mfa_enabled
        if mfa_enabled is ...:
            mfa_enabled = self.mfa_enabled
        else:
            mfa_enabled = validate_mfa_enabled(mfa_enabled)
        
        # premium_type
        if premium_type is ...:
            premium_type = self.premium_type
        else:
            premium_type = validate_premium_type(premium_type)
        
        # Construct
        new = OrinUserBase.copy_with(
            self,
            avatar = avatar,
            avatar_decoration = avatar_decoration,
            banner = banner,
            banner_color = banner_color,
            discriminator = discriminator,
            display_name = display_name,
            flags = flags,
            name = name,
            name_plate = name_plate,
            primary_guild_badge = primary_guild_badge,
        )
        new.access = Oauth2Access()
        new.email = email
        new.email_verified = email_verified
        new.locale = locale
        new.mfa_enabled = mfa_enabled
        new.premium_type = premium_type
        return new
    
    
    @copy_docs(OrinUserBase._get_hash_partial)
    def _get_hash_partial(self):
        hash_value = OrinUserBase._get_hash_partial(self)
        
        # email
        email = self.email
        if (email is not None):
            hash_value ^= hash(email)
        
        # email_verified
        hash_value ^= self.email_verified << 3
        
        # locale
        hash_value ^= hash(self.locale)
        
        # mfa_enabled
        hash_value ^= self.mfa_enabled << 5
        
        # premium_type
        hash_value ^= hash(self.premium_type)
        
        return hash_value
    
    
    def _renew(self, data):
        """
        Renews the oauth2 user's access with the given data.
        
        Parameters
        ----------
        data : `None | dict<str, object>`
            Requested access data.
        """
        self.access._renew(data)
    
    
    # Reflect Oauth2Access
    @property
    def access_token(self):
        """
        Returns the oauth2 user's access's token.
        
        Returns
        -------
        access_token : `str`
        """
        return self.access.access_token
    
    
    @property
    def redirect_url(self):
        """
        Returns the oauth2 user's access's redirect url.
        
        Returns
        -------
        redirect_url : `str`
        """
        return self.access.redirect_url
    
    
    @property
    def refresh_token(self):
        """
        Returns the oauth2 user's access's refresh token.
        
        Returns
        -------
        refresh_token : `str`
        """
        return self.access.refresh_token
    
    
    @property
    def scopes(self):
        """
        Returns the oauth2 user's access's scopes.
        
        Returns
        -------
        scopes : `set` of `str`
        """
        return self.access.scopes
    
    
    def has_scope(self, scope):
        """
        Returns whether the oauth2 user's access has the given scope.
        
        Parameters
        ----------
        scope : ``Oauth2Scope``, `str`
            The scope to check out.
        
        Returns
        -------
        has_scope : `bool`
        
        Raises
        ------
        TypeError
            - If `scope` is neither `str`, ``Oauth2Scope``.
        """
        return self.access.has_scope(scope)
    
    
    def iter_scopes(self):
        """
        Iterates over the oauth2 user's scopes.
        
        This method is an iterable generator.
        
        Yields
        ------
        scope : ``Oauth2Scope``
        """
        return (yield from self.access.iter_scopes())
