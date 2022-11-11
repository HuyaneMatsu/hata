__all__ = ('Oauth2User',)

from scarletio import copy_docs

from ..localization.utils import get_locale
from ..user import PremiumType, UserBase, UserFlag


class Oauth2User(UserBase):
    """
    Represents a Discord user with extra personal information. If a ``Oauth2User`` is  created it will NOT overwrite the
    already existing user with the same ID, if exists.
    
    Attributes
    ----------
    id : `int`
        The user's unique identifier number.
    name : str
        The user's username.
    discriminator : `int`
        The user's discriminator. Given to avoid overlapping names.
    avatar_hash : `int`
        The user's avatar's hash in `uint128`.
    avatar_type : ``IconType``
        The user's avatar's type.
    banner_color : `None`, ``Color``
        The user's banner color if has any.
    banner_hash : `int`
        The user's banner's hash in `uint128`.
    banner_type : ``IconType``
        The user's banner's type.
    access : ``Oauth2Access``
        Source oauth2 access.
    email : `None`, `str`
        The user's email. Defaults to empty string.
    flags : ``UserFlag``
        The user's user flags.
    locale : ``Locale``
        The preferred locale by the user.
    mfa : `bool`
        Whether the user has two factor authorization enabled on the account.
    premium_type : ``PremiumType``
        The Nitro subscription type of the user.
    verified : `bool`
        Whether the email of the user is verified.
    """
    __slots__ = ('access', 'email', 'flags', 'locale', 'mfa', 'premium_type', 'system', 'verified', )
    
    def __init__(self, data, access):
        """
        Creates a new ``Oauth2User`` instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            User data.
        access : ``Oauth2Access``
            Source oauth2 access.
        """
        self.access = access
        self.id = int(data['id'])
        
        self._update_attributes(data)
    
    
    @copy_docs(UserBase._update_attributes)
    def _update_attributes(self, data):
        UserBase._update_attributes(self, data)
        
        self.mfa = data.get('mfa_enabled', False)
        self.verified = data.get('verified', False)
        self.email = data.get('email', None)
        
        try:
            flags = data['flags']
        except KeyError:
            flags = data.get('public_flags', 0)
        
        self.flags = UserFlag(flags)
        
        self.premium_type = PremiumType.get(data.get('premium_type', 0))
        self.locale = get_locale(data.get('locale', None))
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the user and returns it's old attributes in a `dict` with `attribute-name`, `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            All item in the returned dictionary is optional.
            
            +-----------------------+-----------------------+
            | Keys                  | Values                |
            +=======================+=======================+
            | avatar                | ``Icon``              |
            +-----------------------+-----------------------+
            | banner                | ``Icon``              |
            +-----------------------+-----------------------+
            | banner_color          | `None`, ``Color``     |
            +-----------------------+-----------------------+
            | discriminator         | `int`                 |
            +-----------------------+-----------------------+
            | email                 | `None`, `str`         |
            +-----------------------+-----------------------+
            | flags                 | ``UserFlag``          |
            +-----------------------+-----------------------+
            | locale                | ``Locale``            |
            +-----------------------+-----------------------+
            | mfa                   | `bool`                |
            +-----------------------+-----------------------+
            | name                  | `str                  |
            +-----------------------+-----------------------+
            | premium_type          | ``PremiumType``       |
            +-----------------------+-----------------------+
            | verified              | `bool`                |
            +-----------------------+-----------------------+
        """
        old_attributes = UserBase._update_attributes(self, data)
        
        mfa = data.get('mfa_enabled', False)
        if self.mfa != mfa:
            old_attributes['mfa'] = self.mfa
            self.mfa = mfa
        
        
        verified = data.get('verified', False)
        if self.verified != verified:
            old_attributes['verified'] = self.verified
            self.verified = verified
        
        
        email = data.get('email', None)
        if self.email != email:
            old_attributes['email'] = self.email
            self.email = email
        
        
        try:
            flags = data['flags']
        except KeyError:
            flags = data.get('public_flags', 0)
        if self.flags != flags:
            old_attributes['flags'] = self.flags
            self.flags = UserFlag(flags)
        
        
        premium_type = PremiumType.get(data.get('premium_type', 0))
        if self.premium_type is not premium_type:
            old_attributes['premium_type'] = premium_type
            self.premium_type = premium_type
        
        
        locale = get_locale(data.get('locale', None))
        if self.locale is not locale:
            old_attributes['locale'] = self.locale
            self.locale = locale
        
        
        return old_attributes
    
    @property
    def partial(self):
        """
        Returns whether the oauth2 user object is partial.
        
        Returns
        -------
        partial : `bool` = `False`
        """
        return False
    
    
    @property
    def bot(self):
        """
        Returns whether the oauth2 user represents a bot account.
        
        Returns
        -------
        bot : `bool` = `False`
        """
        return False
    
    
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
    
    
    def _renew(self, data):
        """
        Renews the oauth2 user's access with the given data.
        
        Parameters
        ----------
        data : `None` or (`dict` of (`str`, `Any`))
            Requested access data.
        """
        self.access._renew(data)
    
    
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
