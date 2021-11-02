__all__ = ('Application', )

from ..bases import DiscordEntity, IconSlot, ICON_TYPE_NONE
from ..user import ZEROUSER, User, ClientUserBase
from ..core import APPLICATIONS
from ..preconverters import preconvert_snowflake, preconvert_bool, preconvert_str, preconvert_flag

from ..http import urls as module_urls

from .flags import ApplicationFlag
from .team import Team
from .miscellaneous import ApplicationExecutable, ApplicationSubEntity, ThirdPartySKU

class Application(DiscordEntity, immortal=True):
    """
    Represents a Discord application with all of it's spice.
    
    When a ``Client`` is created, it starts it's life with an empty application by default. However when the client
    logs in, it's application is requested, but it can be updated by ``Client.update_application_info`` anytime.
    
    Attributes
    ----------
    aliases : `None` or `list` of `str`
        Aliases of the application's name. Defaults to `None`.
    bot_public : `bool`.
        Whether not only the application's owner can join the application's bot to guilds. Defaults to `False`
    bot_require_code_grant : `bool`
        Whether the application's bot will only join a guild, when completing the full `oauth2` code grant flow.
        Defaults to `False`.
    cover_hash : `int`
        The application's store cover image's hash in `uint128`. If the application is sold at Discord, this image
        will be used at the store.
    cover_type : ``IconType``
        The application's store cover image's type.
    description : `str`
        The description of the application. Defaults to empty string.
    developers : `None` or `list` of ``ApplicationSubEntity``
        A list of the application's games' developers. Defaults to `None`.
    eula_id : `int`
        The end-user license agreement's id of the application. Defaults to `0` if not applicable.
    executables : `None` or `list` of ``ApplicationExecutable``
        A list of the application's executables. Defaults to `None`.
    flags : ``ApplicationFlag``
        The application's public flags.
    guild_id : `int`
        If the application is a game sold on Discord, this field tells in which guild it is.
        Defaults to `0` if not applicable.
    hook : `bool`
        Defaults to `False`.
    icon_hash : `int`
        The application's icon's hash as `uint128`.
    icon_type : ``IconType``
        The application's icon's type.
    id : `int`
        The application's id. Defaults to `0`. Meanwhile set as `0`, hashing the application will raise `RuntimeError`.
    name : `str`
        The name of the application. Defaults to empty string.
    overlay : `bool`
        Defaults to `False`.
    overlay_compatibility_hook : `bool`
        Defaults to `False`.
    owner : ``ClientUserBase`` or ``Team``
        The application's owner. Defaults to `ZEROUSER`.
    primary_sku_id : `int`
        If the application is a game sold on Discord, this field will be the id of the created `Game SKU`.
        Defaults to `0`.
    privacy_policy_url : `None` or `str`
        The url of the application's privacy policy. Defaults to `None`.
    publishers : `None` or `list` of ``ApplicationSubEntity``
        A list of the application's games' publishers. Defaults to `None`.
    rpc_origins : `None` or `list` of `str`
        A list of `rpc` origin urls, if `rpc` is enabled. Set as `None` if would be an empty list.
    slug : `None` or `str`
        If this application is a game sold on Discord, this field will be the url slug that links to the store page.
        Defaults to `None`.
    splash_hash : `int`
        The application's splash image's hash as `uint128`.
    splash_type : ``IconType``
        The application's splash image's type.
    summary : `str`
        If this application is a game sold on Discord, this field will be the summary field for the store page of its
        primary sku. Defaults to empty string.
    terms_of_service_url : `None` or `str`
        The url of the application's terms of service. Defaults to `None`.
    third_party_skus : `None` or `list` of ``ThirdPartySKU``
         A list of the application's third party stock keeping units. Defaults to `None`.
    verify_key : `str`
        A base64 encoded key for the GameSDK's `GetTicket`. Defaults to empty string.
    
    Notes
    -----
    The instances of the class support weakreferencing.
    """
    __slots__ = ('aliases', 'bot_public', 'bot_require_code_grant', 'description', 'developers', 'eula_id',
        'executables', 'flags', 'guild_id', 'hook', 'name', 'overlay', 'overlay_compatibility_hook', 'owner',
        'primary_sku_id', 'privacy_policy_url', 'publishers', 'rpc_origins', 'slug', 'summary', 'terms_of_service_url',
        'third_party_skus', 'verify_key')
    
    cover = IconSlot(
        'cover',
        'cover_image',
        module_urls.application_cover_url,
        module_urls.application_cover_url_as,
        add_updater = False,
    )
    icon = IconSlot(
        'icon',
        'icon',
        module_urls.application_icon_url,
        module_urls.application_icon_url_as,
        add_updater = False,
    )
    splash = IconSlot(
        'splash',
        'splash',
        None,
        None,
        add_updater = False,
    )
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an empty application, with it's default attributes set.
        
        Returns
        -------
        self : ``Application``
            The created application.
        """
        self = object.__new__(cls)
        
        self.id = 0
        self.name = ''
        self.description = ''
        self.rpc_origins = None
        self.bot_public = False
        self.bot_require_code_grant = False
        self.owner = ZEROUSER
        self.summary = ''
        self.verify_key = ''
        self.guild_id = None
        self.primary_sku_id = 0
        self.slug = None
        self.developers = None
        self.hook = None
        self.publishers = None
        self.executables = None
        self.third_party_skus = None
        self.overlay = False
        self.overlay_compatibility_hook = False
        self.aliases = None
        self.eula_id = 0
        self.flags = ApplicationFlag()
        self.privacy_policy_url = None
        self.terms_of_service_url = None
        
        self.cover_hash = 0
        self.cover_type = ICON_TYPE_NONE
        self.icon_hash = 0
        self.icon_type = ICON_TYPE_NONE
        self.splash_hash = 0
        self.splash_type = ICON_TYPE_NONE
        
        return self
    
    def _create_update(self, data, ready_data):
        """
        Creates a new application if the given data refers to an other one. Updates the application and returns it.
        
        Parameters
        ----------
        data : or `dict` of (`str`, `Any`) items, Optional
            Application data received from Discord.
        ready_data : `bool`
            Whether the application data was received from a ready event.
        
        Returns
        -------
        self : ``Application``
            The created or updated application.
        """
        application_id = int(data['id'])
        
        if self.id == 0:
            try:
                self = APPLICATIONS[application_id]
            except KeyError:
                self.id = application_id
                APPLICATIONS[application_id] = self
        
        if ready_data:
            try:
                flags = data['flags']
            except KeyError:
                flags = ApplicationFlag()
            else:
                flags = ApplicationFlag(flags)
            self.flags = flags
        else:
            self._update_attributes(data, set_owner=True)
        
        return self
    
    def __new__(cls, data):
        """
        Creates a new application with the given data. If the application already exists, updates it and returns that
        instead.
        
        Parameters
        ----------
        data : or `dict` of (`str`, `Any`) items, Optional
            Application data received from Discord.
        
        Returns
        -------
        self : `˙Application``
        """
        application_id = int(data['id'])
        try:
            self = APPLICATIONS[application_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = application_id
            self.flags = ApplicationFlag()
            self._update_attributes(data, set_owner=True)
        else:
            self._update_attributes(data)
        
        return self
    
    def __hash__(self):
        """Returns the application's hash value."""
        id_ = self.id
        if id_:
            return id_
        
        raise TypeError(f'Cannot hash partial {self.__class__.__name__} object.')
    
    @property
    def partial(self):
        """
        Returns whether the application is partial.
        
        An application if partial, if it's id is set as `0`.
        Returns
        -------
        partial : `bool`
        """
        return (self.id == 0)
    
    def __repr__(self):
        """Returns the application's representation"""
        result = [
            '<',
            self.__class__.__name__,
        ]
        
        id_ = self.id
        if id_:
            result.append(' id=')
            result.append(repr(id_))
            result.append(', name=')
            result.append(repr(self.name))
        else:
            result.append(' partial')
        
        result.append('>')
        
        return ''.join(result)
    
    
    def _update_attributes(self, data, set_owner=False):
        """
        Updates the application with the data received from Discord.
        
        Parameters
        ----------
        data : `None` or `dict` of (`str`, `Any`) items
            Application data received from Discord.
        set_owner : `bool`, Optional
            Whether the application's owner should be set from the given data. Defaults to `False`.
            Should be given as `True`, if the application is created or if it contains owner data.
        """
        self.name = data['name']
        
        self.description = data['description']
        
        rpc_origins = data.get('rpc_origins', None)
        if (rpc_origins is not None) and (not rpc_origins):
            rpc_origins = None
        
        self.rpc_origins = rpc_origins
        
        self.bot_public = data.get('bot_public', False)
        self.bot_require_code_grant = data.get('bot_require_code_grant', False)
        self.summary = data['summary']
        self.verify_key = data['verify_key']
        
        if set_owner:
            team_data = data.get('team', None)
            if team_data is None:
                owner_data = data.get('owner', None)
                if owner_data is None:
                    owner = ZEROUSER
                else:
                    owner = User(owner_data)
            else:
                owner = Team(team_data)
            
            self.owner = owner
        
        guild_id = data.get('guild_id', None)
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        
        self.guild_id = guild_id
        
        primary_sku_id = data.get('primary_sku_id', None)
        if primary_sku_id is None:
            primary_sku_id = None
        else:
            primary_sku_id = int(primary_sku_id)
        self.primary_sku_id = primary_sku_id
        
        self.slug = data.get('slug', None)
        
        self._set_cover(data)
        self._set_icon(data)
        
        developers_data = data.get('developers', None)
        if (developers_data is None) or (not developers_data):
            developers = None
        else:
            developers = [ApplicationSubEntity(developer_data) for developer_data in developers_data]
        
        self.developers = developers
        
        self.hook = data.get('hook', False)
        
        publishers_data = data.get('publishers', None)
        if (publishers_data is None) or (not publishers_data):
            publishers = None
        else:
            publishers = [ApplicationSubEntity(publisher_data) for publisher_data in publishers_data]
        
        self.publishers = publishers
        
        executables_data = data.get('executables', None)
        if (executables_data is None) or (not executables_data):
            executables = None
        else:
            executables = [ApplicationExecutable(executable_data) for executable_data in executables_data]
        
        self.executables = executables
        
        self._set_splash(data)
        
        third_party_skus_data = data.get('third_party_skus', None)
        if (third_party_skus_data is None) or (not third_party_skus_data):
            third_party_skus = None
        else:
            third_party_skus = [ThirdPartySKU(third_party_sku_data) for third_party_sku_data in third_party_skus_data]
        
        self.third_party_skus = third_party_skus
        
        self.overlay = data.get('overlay', False)
        self.overlay_compatibility_hook = data.get('overlay_compatibility_hook', False)
        
        aliases = data.get('aliases', None)
        if (aliases is not None) and (not aliases):
            aliases = None
        
        self.aliases = aliases
        
        eula_id = data.get('eula_id', None)
        if eula_id is None:
            eula_id = 0
        else:
            eula_id = int(eula_id)
        
        self.eula_id = eula_id
        
        # Update data may not contain flags, so do not set if missing.
        try:
            flags = data['flags']
        except KeyError:
            pass
        else:
            self.flags = ApplicationFlag(flags)
        
        privacy_policy_url = data.get('privacy_policy_url', None)
        if (privacy_policy_url is not None) and (not privacy_policy_url):
            privacy_policy_url = None
        self.privacy_policy_url = privacy_policy_url
        
        terms_of_service_url = data.get('terms_of_service_url', None)
        if (terms_of_service_url is not None) and (not terms_of_service_url):
            terms_of_service_url = None
        self.terms_of_service_url = terms_of_service_url
        
    @classmethod
    def precreate(cls, application_id, **kwargs):
        """
        Precreates an application with the given parameters.
        
        Parameters
        ----------
        application_id : `int` or `str`
            The application's id.
        **kwargs : keyword parameters
            Additional predefined attributes for the application.
        
        Other parameters
        ----------------
        bot_public : `bool`, Optional (Keyword only)
            Whether not only the application's owner can join the application's bot to guilds.
        bot_require_code_grant : `bool`, Optional (Keyword only)
            Whether the application's bot will only join a guild, when completing the full `oauth2` code grant flow.
        description : `str`, Optional (Keyword only)
            The description of the application.
        flags : `int` or ``ApplicationFlag``, Optional (Keyword only)
            The application's public flags. If not given as ``ApplicationFlag`` instance, then is converted to it.
        icon : `None`, ``Icon`` or `str`, Optional (Keyword only)
            The application's icon.
            
            > Mutually exclusive with `icon_type` and `icon_hash`.
        icon_type : ``IconType``, Optional (Keyword only)
            The application's icon's type.
            
            > Mutually exclusive with `icon`.
        icon_hash : `int`, Optional (Keyword only)
            The application's icon's hash.
            
            > Mutually exclusive with `icon`.
        owner : ``ClientUserBase`` or ``Team``
            The application's owner. Defaults to `ZEROUSER`.
            
            This field cannot be given as `snowflake`, because it might represent both ``UserBase`` instances  and
            ``Team``-s as well.
        privacy_policy_url : `None` or `str`, Optional (Keyword only)
            The url of the application's privacy policy.
        slug : `None` or `str`
            If this application is a game sold on Discord, this field will be the url slug that links to the store page.
        splash : `None`, ``Icon`` or `str`, Optional (Keyword only)
            The application's splash.
            
            > Mutually exclusive with `icon_type` and `icon_hash`.
        splash_type : ``IconType``, Optional (Keyword only)
            The application's icon's type.
            
            > Mutually exclusive with `icon`.
        splash_hash : `int`, Optional (Keyword only)
            The application's icon's hash.
            
            > Mutually exclusive with `icon`.
        
        summary : `str`, Optional (Keyword only)
            If this application is a game sold on Discord, this field will be the summary field for the store page of
            its primary sku.
        terms_of_service_url : `None` or `str`, Optional (Keyword only)
            The url of the application's terms of service.
        
        Returns
        -------
        application : `Application``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        application_id = preconvert_snowflake(application_id, 'application_id')
        
        if kwargs:
            processable = []
            
            for key in ('bot_public', 'bot_require_code_grant'):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    continue
                
                value = preconvert_bool(value, key)
                processable.append((key, value))
            
            for key in ('description', 'summary'):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    continue
                
                value = preconvert_str(value, key, 0, 1024)
                processable.append((key, value))
            
            try:
                flags = kwargs.pop('flags')
            except KeyError:
                pass
            else:
                flags = preconvert_flag(flags, 'flags', ApplicationFlag)
                processable.append(('flags', flags))
            
            cls.icon.preconvert(kwargs, processable)
            
            try:
                owner = kwargs.pop('owner')
            except KeyError:
                pass
            else:
                if not isinstance(owner, (ClientUserBase, Team)):
                    raise TypeError(f'`owner` can be given as `{ClientUserBase.__name__}`  or as '
                        f'{Team.__name__} instance, got {owner.__class__.__name__}.')
                
                processable.append(('owner', owner))
            
            for key in ('slug', 'privacy_policy_url', 'terms_of_service_url'):
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    continue
                
                if (value is None):
                    continue
                
                value = preconvert_str(value, key, 0, 1024)
                if not value:
                    continue
                
                processable.append((key, value))
            
            cls.splash.preconvert(kwargs, processable)
            
            if kwargs:
                raise TypeError(f'Unused or unsettable attributes: {kwargs}.')
            
        else:
            processable = None
        
        try:
            application = APPLICATIONS[application_id]
        except KeyError:
            application = cls._create_empty()
            application.id = application_id
            is_partial = True
        else:
            is_partial = application.partial
        
        if is_partial and (processable is not None):
            for item in processable:
                setattr(application, *item)
        
        return application
