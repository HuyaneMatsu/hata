__all__ = ('UserOA2',)

from ..user import UserFlag, UserBase, PremiumType

from .helpers import parse_locale

class UserOA2(UserBase):
    """
    Represents a Discord user with extra personal information. If a ``UserOA2`` is  created it will NOT overwrite the
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
    banner_hash : `int`
        The user's banner's hash in `uint128`.
    banner_type : ``IconType``
        The user's banner's type.
    email : `None` or `str`
        The user's email. Defaults to empty string.
    flags : ``UserFlag``
        The user's user flags.
    locale : `str`
        The preferred locale by the user.
    mfa : `bool`
        Whether the user has two factor authorization enabled on the account.
    premium_type : ``PremiumType``
        The Nitro subscription type of the user.
    system : `bool`
        Whether the user is an Official Discord System user (part of the urgent message system).
    verified : `bool`
        Whether the email of the user is verified.
    """
    __slots__ = ('access', 'email', 'flags', 'locale', 'mfa', 'premium_type', 'system', 'verified', )
    
    def __init__(self, data, access):
        self.access = access
        self.id = int(data['id'])
        self.name = data['username']
        self.discriminator = int(data['discriminator'])
        
        self._set_avatar(data)
        self._set_banner(data)
        
        self.mfa = data.get('mfa_enabled', False)
        self.verified = data.get('verified', False)
        self.email = data.get('email', None)
        
        try:
            flags = data['flags']
        except KeyError:
            flags = data.get('public_flags', 0)
        
        self.flags = UserFlag(flags)
        self.premium_type = PremiumType.get(data.get('premium_type', 0))
        self.locale = parse_locale(data)
        self.system = data.get('system', False)
    
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
    def is_bot(self):
        """
        Returns whether the oauth2 user represents a bot account.
        
        Returns
        -------
        is_bot : `bool` = `False`
        """
        return False
    
    # Reflect OA2Access
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
