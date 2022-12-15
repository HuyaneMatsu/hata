__all__ = ('Application', )

import warnings
from functools import partial as partial_func

from scarletio import BaseMethodDescriptor

from ...bases import DiscordEntity, ICON_TYPE_NONE, IconSlot
from ...core import APPLICATION_ID_TO_CLIENT, APPLICATIONS
from ...http import urls as module_urls
from ...user import ZEROUSER

from .constants import (
    BOT_PUBLIC_DEFAULT, BOT_REQUIRE_CODE_GRANT_DEFAULT, HOOK_DEFAULT, MAX_PARTICIPANTS_DEFAULT,
    OVERLAY_COMPATIBILITY_HOOK_DEFAULT, OVERLAY_DEFAULT
)
from .fields import (
    parse_aliases, parse_bot_public, parse_bot_require_code_grant, parse_custom_install_url, parse_deeplink_url,
    parse_description, parse_developers, parse_eula_id, parse_executables, parse_flags, parse_guild_id, parse_hook,
    parse_id, parse_install_parameters, parse_max_participants, parse_name, parse_overlay,
    parse_overlay_compatibility_hook, parse_owner, parse_primary_sku_id, parse_privacy_policy_url, parse_publishers,
    parse_role_connection_verification_url, parse_rpc_origins, parse_slug, parse_tags, parse_terms_of_service_url,
    parse_third_party_skus, parse_type, parse_verify_key, put_aliases_into, put_bot_public_into,
    put_bot_require_code_grant_into, put_custom_install_url_into, put_deeplink_url_into, put_description_into,
    put_developers_into, put_eula_id_into, put_executables_into, put_flags_into, put_guild_id_into, put_hook_into,
    put_id_into, put_install_parameters_into, put_max_participants_into, put_name_into,
    put_overlay_compatibility_hook_into, put_overlay_into, put_owner_into, put_primary_sku_id_into,
    put_privacy_policy_url_into, put_publishers_into, put_role_connection_verification_url_into, put_rpc_origins_into,
    put_slug_into, put_tags_into, put_terms_of_service_url_into, put_third_party_skus_into, put_type_into,
    put_verify_key_into, validate_aliases, validate_bot_public, validate_bot_require_code_grant,
    validate_custom_install_url, validate_deeplink_url, validate_description, validate_developers, validate_eula_id,
    validate_executables, validate_flags, validate_guild_id, validate_hook, validate_id, validate_install_parameters,
    validate_max_participants, validate_name, validate_overlay, validate_overlay_compatibility_hook, validate_owner,
    validate_primary_sku_id, validate_privacy_policy_url, validate_publishers,
    validate_role_connection_verification_url, validate_rpc_origins, validate_slug, validate_tags,
    validate_terms_of_service_url, validate_third_party_skus, validate_type, validate_verify_key
)
from .flags import ApplicationFlag
from .preinstanced import ApplicationType

# Invite application fields
#
# - bot_public
# - bot_require_code_grant
# - cover_image
# - description
# - flags
# - hook
# - icon
# - id
# - max_participants
# - name
# - privacy_policy_url
# - rpc_origins
# - splash
# - summary (Deprecated)
# - tags
# - type
# - terms_of_service_url
# - verify_key
#
# Own application fields
#
# - bot_public
# - bot_require_code_grant
# - custom_install_url
# - description
# - flags
# - guild_id
# - hook
# - icon
# - id
# - name
# - owner
# - primary_sku_id
# - slug
# - summary (deprecated)
# - tags
# - team
# - type
# - verify_key
#
# Extra from docs
# - role_connection_verification_url
# - rpc_origins
# - terms_of_service_url
# - privacy_policy_url
# - cover_image
# - install_params
#
# Detectable application fields
#
# - aliases
# - bot_public
# - bot_require_code_grant
# - cover_image
# - deeplink_uri
# - description
# - developers
# - eula_id
# - executables
# - flags
# - guild_id
# - hook
# - icon
# - id
# - name
# - overlay
# - overlay_compatibility_hook
# - primary_sku_id
# - privacy_policy_url
# - publishers
# - rpc_origins
# - slug
# - splash
# - summary (deprecated)
# - tags
# - terms_of_service_url
# - third_party_skus
# - type
# - verify_key
#
# Table format:
#
# +-------------------------------------+-----------+-----------+---------------+
# | Name                                | Own       | Invite    | Detectable    |
# +=====================================+===========+===========+===============+
# | aliases                             | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | bot_public                          | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | bot_require_code_grant              | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | cover_image                         | PROBABLY  | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | custom_install_url                  | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | deeplink_uri                        | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | description                         | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | developers                          | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | eula_id                             | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | executables                         | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | flags                               | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | guild_id                            | YES       | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | hook                                | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | icon                                | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | id                                  | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | install_params                      | PROBABLY  | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | max_participants                    | NO        | YES       | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | name                                | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | overlay                             | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | overlay_compatibility_hook          | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | owner                               | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | primary_sku_id                      | YES       | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | privacy_policy_url                  | PROBABLY  | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | publishers                          | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | role_connection_verification_url   | PROBABLY  | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | rpc_origins                         | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | slug                                | YES       | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | splash                              | PROBABLY  | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | summary                             | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | tags                                | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | team                                | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | terms_of_service_url                | PROBABLY  | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | third_party_skus                    | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | type                                | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | verify_key                          | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+


application_cover = IconSlot(
    'cover',
    'cover_image',
    module_urls.application_cover_url,
    module_urls.application_cover_url_as,
    add_updater = False,
)

application_icon = IconSlot(
    'icon',
    'icon',
    module_urls.application_icon_url,
    module_urls.application_icon_url_as,
    add_updater = False,
)

application_splash = IconSlot(
    'splash',
    'splash',
    None,
    None,
    add_updater = False,
)


COMMON_CONSTRUCT_RELATIONS = {
    'aliases': ('aliases', validate_aliases),
    'bot_public': ('bot_public', validate_bot_public),
    'bot_require_code_grant': ('bot_require_code_grant', validate_bot_require_code_grant),
    'custom_install_url': ('custom_install_url', validate_custom_install_url),
    'deeplink_url': ('deeplink_url', validate_deeplink_url),
    'description': ('description', validate_description),
    'developers': ('developers', validate_developers),
    'eula_id': ('eula_id', validate_eula_id),
    'executables': ('executables', validate_executables),
    'flags': ('flags', validate_flags),
    'guild_id': ('guild_id', validate_guild_id),
    'hook': ('hook', validate_hook),
    'install_parameters': ('install_parameters', validate_install_parameters),
    'max_participants': ('max_participants', validate_max_participants),
    'name': ('name', validate_name),
    'overlay': ('overlay', validate_overlay),
    'overlay_compatibility_hook': ('overlay_compatibility_hook', validate_overlay_compatibility_hook),
    'owner': ('owner', validate_owner),
    'primary_sku_id': ('primary_sku_id', validate_primary_sku_id),
    'privacy_policy_url': ('privacy_policy_url', validate_privacy_policy_url),
    'publishers': ('publishers', validate_publishers),
    'role_connection_verification_url': ('role_connection_verification_url', validate_role_connection_verification_url),
    'rpc_origins': ('rpc_origins', validate_rpc_origins),
    'slug': ('slug', validate_slug),
    'tags': ('tags', validate_tags),
    'terms_of_service_url': ('terms_of_service_url', validate_terms_of_service_url),
    'third_party_skus': ('third_party_skus', validate_third_party_skus),
    'application_type': ('type', validate_type),
    'verify_key': ('verify_key', validate_verify_key),
}

PRECREATE_RELATIONS = {
    **COMMON_CONSTRUCT_RELATIONS,
    'cover': ('cover', application_cover.validate_icon),
    'icon': ('icon', application_icon.validate_icon),
    'splash': ('splash', application_splash.validate_icon),
}

NEW_RELATIONS = {
    **COMMON_CONSTRUCT_RELATIONS,
    'cover': ('cover', partial_func(application_cover.validate_icon, allow_data = True)),
    'icon': ('icon', partial_func(application_icon.validate_icon, allow_data = True)),
    'splash': ('splash', partial_func(application_splash.validate_icon, allow_data = True)),
}


def process_application_constructor_parameters(keyword_parameters, field_relations):
    """
    Helpers function to process parameters passed to an ``Application`` constructor.
    
    Parameters
    ----------
    keyword_parameters : `dict` of (`str`, `object`) items
        Keyword parameters passed to an application constructor.
    
    field_relations : `dict` of `tuple` (`str`, `callable`)
        Field relations used for parameter name lookup.
    
    Returns
    -------
    processable : `list` of `tuple` (`str`, `object`)
        Processed field names and their values that can be set by the constructor.
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
        - Extra parameter(s).
    ValueError
        - If an parameter's value is incorrect.
    """
    processable = []
    extra = None
    
    while keyword_parameters:
        field_name, field_value = keyword_parameters.popitem() 
        try:
            attribute_name, validator = field_relations[field_name]
        except KeyError:
            if extra is None:
                extra = {}
            extra[field_name] = field_value
            continue
        
        attribute_value = validator(field_value)
        processable.append((attribute_name, attribute_value))
        continue
        
    if (extra is not None):
        raise TypeError(
            f'Unused or unsettable keyword parameters: {extra!r}.'
        )
    
    return processable


class Application(DiscordEntity, immortal = True):
    """
    Represents a Discord application with all of it's spice.
    
    When a ``Client`` is created, it starts it's life with an empty application by default. However when the client
    logs in, it's application is requested, but it can be updated by ``Client.update_application_info`` anytime.
    
    Attributes
    ----------
    aliases : `None`, `tuple` of `str`
        Aliases of the application's name.
    
    bot_public : `bool`.
        Whether not only the application's owner can join the application's bot to guilds.
        Defaults to `False`
    
    bot_require_code_grant : `bool`
        Whether the application's bot will only join a guild, when completing the full `oauth2` code grant flow.
        Defaults to `False`.
    
    cover_hash : `int`
        The application's store cover image's hash in `uint128`. If the application is sold at Discord, this image
        will be used at the store.
    
    cover_type : ``IconType``
        The application's store cover image's type.
    
    custom_install_url : `None`, `str`
        The application's default custom authorization link if enabled.
        Defaults to `None`.
    
    deeplink_url : `None, `str`
        Deeplink of the application.
        Defaults to `None`.
    
    description : `None`, `str`
        The description of the application. Defaults to empty string.
        Defaults to `None`.
    
    developers : `None`, `tuple` of ``ApplicationEntity``
        The application's games' developers.
        Defaults to `None`.
    
    eula_id : `int`
        The end-user license agreement's id of the application.
        Defaults to `0` if not applicable.
    
    executables : `None`, `tuple` of ``ApplicationExecutable``
        The application's executables.
        Defaults to `None`.
    
    flags : ``ApplicationFlag``
        The application's public flags.
    
    guild_id : `int`
        If the application is a game sold on Discord, this field tells in which guild it is.
        Defaults to `0` if not applicable.
    
    hook : `bool`
        Defaults to `False`.
    
    install_parameters : `None`, ``ApplicationInstallParameters``
        Settings for the application's default in-app authorization link, if enabled.
    
    icon_hash : `int`
        The application's icon's hash as `uint128`.
    
    icon_type : ``IconType``
        The application's icon's type.
    
    id : `int`
        The application's id.
        Defaults to `0`.
    
    max_participants : `int`
        The maximal amount of users, who can join the application's embedded activity.
        Defaults to `0`.
    
    name : `str`
        The name of the application. Defaults to empty string.
    
    overlay : `bool`
        Defaults to `False`.
    
    overlay_compatibility_hook : `bool`
        Defaults to `False`.
    
    owner : ``ClientUserBase``, ``Team``
        The application's owner.
        Defaults to `ZEROUSER`.
    
    primary_sku_id : `int`
        If the application is a game sold on Discord, this field will be the id of the created `Game SKU`.
    
    privacy_policy_url : `None`, `str`
        The url of the application's privacy policy.
        Defaults to `None`.
    
    publishers : `None`, `tuple` of ``ApplicationEntity``
        A list of the application's games' publishers.
        Defaults to `None`.
    
    role_connection_verification_url : `None`, `str`
        The application's role connection verification entry point
    
    rpc_origins : `None`, `tuple` of `str`
        The application's `rpc` origin urls, if `rpc` is enabled.
        Defaults to `None`.
    
    slug : `None`, `str`
        If this application is a game sold on Discord, this field will be the url slug that links to the store page.
        Defaults to `None`.
    
    splash_hash : `int`
        The application's splash image's hash as `uint128`.
    
    splash_type : ``IconType``
        The application's splash image's type.
    
    tags : `None`, `tuple` of `str`
        Up to 5 tags describing the content and functionality of the application.
        Defaults to `None`.
    
    terms_of_service_url : `None`, `str`
        The url of the application's terms of service.
        Defaults to `None`.
    
    third_party_skus : `None`, `tuple` of ``ThirdPartySKU``
         The application's third party stock keeping units.
         Defaults to `None`.
    
    type : ``ApplicationType``
        The application's type.
    
    verify_key : `None`, `str`
        A base64 encoded key for the Game SDK's `GetTicket`.
        Defaults to `None`.
    
    Notes
    -----
    The instances of the class support weakreferencing.
    """
    __slots__ = (
        'aliases', 'bot_public', 'bot_require_code_grant', 'custom_install_url', 'deeplink_url', 'description',
        'developers', 'eula_id', 'executables', 'flags', 'guild_id', 'hook', 'install_parameters', 'max_participants',
        'name', 'overlay', 'overlay_compatibility_hook', 'owner', 'primary_sku_id', 'privacy_policy_url', 'publishers',
        'role_connection_verification_url', 'rpc_origins', 'slug', 'tags', 'terms_of_service_url', 'third_party_skus',
        'type', 'verify_key'
    )
    
    cover = application_cover
    icon = application_icon
    splash = application_splash
    
    @classmethod
    def _create_empty(cls, application_id):
        """
        Creates an empty application, with it's default attributes set.
        
        Parameters
        ----------
        application_id : `int`
            The application's default identifier.
        
        Returns
        -------
        self : ``Application``
            The created application.
        """
        self = object.__new__(cls)
        
        self.aliases = None
        self.bot_public = BOT_PUBLIC_DEFAULT
        self.bot_require_code_grant = BOT_REQUIRE_CODE_GRANT_DEFAULT
        self.cover_hash = 0
        self.cover_type = ICON_TYPE_NONE
        self.custom_install_url = None
        self.deeplink_url = None
        self.description = None
        self.developers = None
        self.eula_id = 0
        self.executables = None
        self.flags = ApplicationFlag()
        self.guild_id = 0
        self.hook = HOOK_DEFAULT
        self.install_parameters = None
        self.icon_hash = 0
        self.icon_type = ICON_TYPE_NONE
        self.id = application_id
        self.max_participants = MAX_PARTICIPANTS_DEFAULT
        self.name = ''
        self.overlay = OVERLAY_DEFAULT
        self.overlay_compatibility_hook = OVERLAY_COMPATIBILITY_HOOK_DEFAULT
        self.owner = ZEROUSER
        self.primary_sku_id = 0
        self.privacy_policy_url = None
        self.publishers = None
        self.role_connection_verification_url = None
        self.rpc_origins = None
        self.slug = None
        self.splash_hash = 0
        self.splash_type = ICON_TYPE_NONE
        self.tags = None
        self.terms_of_service_url = None
        self.third_party_skus = None
        self.type = ApplicationType.none
        self.verify_key = None
        
        return self
    
    
    @classmethod
    def _base_method_from_data_constructor(cls, self, data):
        """
        Helper method to create the application when calling a base-method from-data constructor.
        
        Parameters
        ----------
        self : `None`, `instance<cls>>`
            The application instance the method was called if any.
        
        data : `dict` of (`str`, `object`) items
            Application data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        application_id = parse_id(data)
        
        if (self is None):
            try:
                self = APPLICATIONS[application_id]
            except KeyError:
                self = cls._create_empty(application_id)
                APPLICATIONS[application_id] = self
        
        elif (self.id == 0):
            try:
                self = APPLICATIONS[application_id]
            except KeyError:
                self.id = application_id
                APPLICATIONS[application_id] = self
        
        elif (self.id != application_id):
            try:
                self = APPLICATIONS[application_id]
            except KeyError:
                self = cls._create_empty(application_id)
                APPLICATIONS[application_id] = self
        
        return self
    
    
    @classmethod
    def _from_data_constructor(cls, data):
        """
        Helper method to create the application when calling a from-data constructor.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Application data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        application_id = parse_id(data)
        
        try:
            self = APPLICATIONS[application_id]
        except KeyError:
            self = cls._create_empty(application_id)
            APPLICATIONS[application_id] = self
        
        return self
    

    @classmethod
    def from_data(cls, data):
        """
        Creates a new application with the given data.
        
        Please use a specialised method instead:
        
        - ``.from_data_ready``
        - ``.from_data_own``
        - ``.from_data_invite``
        - ``.from_data_detectable``
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Application data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        warnings.warn(
            (
                f'`{cls.__name__}` has specialized data-based constructors. They are: `.from_data_ready`, '
                f' `.from_data_own`, `.from_data_invite`, `.from_data_detectable`. Please use own of those instead.'
            ),
            RuntimeWarning,
            stacklevel = 2,
        )
        
        self = cls._from_data_constructor(data)
        self._update_attributes_common(data)
        return self
    
    
    @BaseMethodDescriptor
    def from_data_ready(cls, self, data):
        """
        Creates a new application if the given data refers to an other one. Updates the application and returns it.
        
        This method is called in a `ready` event parser to update the client's application.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Application data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = cls._base_method_from_data_constructor(self, data)
        self._update_attributes_ready(data)
        return self
    
    
    @BaseMethodDescriptor
    def from_data_own(cls, self, data):
        """
        Creates a new application if the given data refers to an other one. Updates the application and returns it.
        
        This method is called when a client updates it's own application.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Application data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = cls._base_method_from_data_constructor(self, data)
        self._update_attributes_own(data)
        return self
    
    
    @classmethod
    def from_data_invite(cls, data):
        """
        Creates an application from the given data. If the application already exists picks it up.
        
        This method is called when an invite contains application data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Application data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = cls._from_data_constructor(data)
        self._update_attributes_invite(data)
        return self
    
    
    @classmethod
    def from_data_detectable(cls, data):
        """
        Creates an application from the given data. If the application already exists picks it up.
        
        This method is called when the detectable applications are requested.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Application data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = cls._from_data_constructor(data)
        self._update_attributes_detectable(data)
        return self
    
    
    def _update_attributes_ready(self, data):
        """
        Updates the application's attributes from a ready event application data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items, Optional
            Application data.
        """
        self.flags = parse_flags(data)
    
    
    def _update_attributes_own(self, data):
        """
        Updates the application's attributes when it's own data was requested.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items, Optional
            Application data.
        """
        self._update_attributes_common(data)
        self.custom_install_url = parse_custom_install_url(data)
        self.guild_id = parse_guild_id(data)
        self.install_parameters = parse_install_parameters(data)
        self.owner = parse_owner(data)
        self.primary_sku_id = parse_primary_sku_id(data)
        self.role_connection_verification_url = parse_role_connection_verification_url(data)
        self.slug = parse_slug(data)
    
    
    def _update_attributes_invite(self, data):
        """
        Updates the application's attributes when it's data is part of an invite.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items, Optional
            Application data.
        """
        self._update_attributes_common(data)
        self.max_participants = parse_max_participants(data)
    
    
    def _update_attributes_detectable(self, data):
        """
        Updates the application's attributes when requesting all detectable applications.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items, Optional
            Application data.
        """
        self._update_attributes_common(data)
        self.aliases = parse_aliases(data)
        self.deeplink_url = parse_deeplink_url(data)
        self.developers = parse_developers(data)
        self.eula_id = parse_eula_id(data)
        self.executables = parse_executables(data)
        self.guild_id = parse_guild_id(data)
        self.overlay = parse_overlay(data)
        self.overlay_compatibility_hook = parse_overlay_compatibility_hook(data)
        self.primary_sku_id = parse_primary_sku_id(data)
        self.publishers = parse_publishers(data)
        self.slug = parse_slug(data)
        self.third_party_skus = parse_third_party_skus(data)
    
    
    def _update_attributes_common(self, data):
        """
        Updates the commonly distributed fields of the application.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items, Optional
            Application data.
        """
        self.bot_public = parse_bot_public(data)
        self.bot_require_code_grant = parse_bot_require_code_grant(data)
        self._set_cover(data)
        self.description = parse_description(data)
        self.flags = parse_flags(data)
        self.hook = parse_hook(data)
        self._set_icon(data)
        self.name = parse_name(data)
        self.privacy_policy_url = parse_privacy_policy_url(data)
        self.rpc_origins = parse_rpc_origins(data)
        self._set_splash(data)
        self.tags = parse_tags(data)
        self.terms_of_service_url = parse_terms_of_service_url(data)
        self.type = parse_type(data)
        self.verify_key = parse_verify_key(data)
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Convert the application back to a json serializable dictionary.
        
        Please use a specialised method instead:
        
        - ``.to_data_ready``
        - ``.to_data_own``
        - ``.to_data_invite``
        - ``.to_data_detectable``
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `str`) items
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}` has specialized to-data converters. They are: `.to_data_ready`, '
                f' `.to_data_own`, `.to_data_invite`, `.to_data_detectable`. Please use own of those instead.'
            ),
            RuntimeWarning,
            stacklevel = 2,
        )
        
        return self._to_data_common(defaults, include_internals)
    
    
    def to_data_ready(self, *, defaults = False, include_internals = False):
        """
        Convert the application to a json serializable dictionary matching a ready event application one.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `str`) items
        """
        data = {}
        put_flags_into(self.flags, data, defaults)
        if include_internals:
            put_id_into(self.id, data, defaults)
        return data
    
    
    def to_data_own(self, *, defaults = False, include_internals = False):
        """
        Convert the application to a json serializable dictionary matching the payload received from requesting the
        client's own payload.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `str`) items
        """
        data = self._to_data_common(defaults, include_internals)
        put_custom_install_url_into(self.custom_install_url, data, defaults)
        put_guild_id_into(self.guild_id, data, defaults)
        put_install_parameters_into(self.install_parameters, data, defaults)
        if include_internals:
            put_owner_into(self.owner, data, defaults)
        put_primary_sku_id_into(self.primary_sku_id, data, defaults)
        put_role_connection_verification_url_into(self.role_connection_verification_url, data, defaults)
        put_slug_into(self.slug, data, defaults)
        return data
    
    
    def to_data_invite(self, *, defaults = False, include_internals = False):
        """
        Convert the application to a json serializable dictionary matching an invite's application data.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `str`) items
        """
        data = self._to_data_common(defaults, include_internals)
        put_max_participants_into(self.max_participants, data, defaults)
        return data
    
    
    def to_data_detectable(self, *, defaults = False, include_internals = False):
        """
        Convert the application to a json serializable dictionary matching a detectable application's data.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `str`) items
        """
        data = self._to_data_common(defaults, include_internals)
        put_aliases_into(self.aliases, data, defaults)
        put_deeplink_url_into(self.deeplink_url, data, defaults)
        put_developers_into(self.developers, data, defaults, include_internals = True)
        put_eula_id_into(self.eula_id, data, defaults)
        put_executables_into(self.executables, data, defaults)
        put_guild_id_into(self.guild_id, data, defaults)
        put_overlay_into(self.overlay, data, defaults)
        put_overlay_compatibility_hook_into(self.overlay_compatibility_hook, data, defaults)
        put_primary_sku_id_into(self.primary_sku_id, data, defaults)
        put_publishers_into(self.publishers, data, defaults, include_internals = True)
        put_slug_into(self.slug, data, defaults)
        put_third_party_skus_into(self.third_party_skus, data, defaults)
        return data
    
    
    def _to_data_common(self, defaults, include_internals):
        """
        Convert the application back to a json serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool`
            Whether default values should be included as well.
        include_internals : `bool`
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `str`) items
        """
        data = {}
        put_bot_public_into(self.bot_public, data, defaults)
        put_bot_require_code_grant_into(self.bot_require_code_grant, data, defaults)
        type(self).cover.put_into(self.cover, data, defaults, as_data = not include_internals)
        put_description_into(self.description, data, defaults)
        put_flags_into(self.flags, data, defaults)
        put_hook_into(self.hook, data, defaults)
        if include_internals:
            put_id_into(self.id, data, defaults)
        type(self).icon.put_into(self.icon, data, defaults, as_data = not include_internals)
        put_name_into(self.name, data, defaults)
        put_privacy_policy_url_into(self.privacy_policy_url, data, defaults)
        put_rpc_origins_into(self.rpc_origins, data, defaults)
        type(self).splash.put_into(self.splash, data, defaults, as_data = not include_internals)
        put_tags_into(self.tags, data, defaults)
        put_terms_of_service_url_into(self.terms_of_service_url, data, defaults)
        put_type_into(self.type, data, defaults)
        put_verify_key_into(self.verify_key, data, defaults)
        return data
    
    
    def _create_update(self, data, ready_data):
        """
        Creates a new application if the given data refers to an other one. Updates the application and returns it.
        
        Deprecated and will be removed in 2023 Marc.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items, Optional
            Application data received from Discord.
        ready_data : `bool`
            Whether the application data was received from a ready event.
        
        Returns
        -------
        self : ``Application``
            The created or updated application.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.embedded_activity_configuration` is deprecated and will be removed in '
                f'2023 Marc.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        if ready_data:
            self = self.from_data_ready(data)
        else:
            self = self.from_data_own(data)
        return self
    
    
    def __hash__(self):
        """Returns the application's hash value."""
        application_id = self.id
        if application_id:
            return application_id
        
        return self._get_hash_partial()
    
        
    def _get_hash_partial(self):
        """
        Hashes the attributes of the application.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # aliases
        aliases = self.aliases
        if (aliases is not None):
            hash_value ^= len(aliases) << 0
            
            for alias in aliases:
                hash_value ^= hash(alias)
        
        # bot_public
        hash_value ^= self.bot_public << 4
        
        # bot_require_code_grant
        hash_value ^= self.bot_require_code_grant << 5
        
        # cover
        hash_value ^= hash(self.cover)
        
        # custom_install_url
        custom_install_url = self.custom_install_url
        if (custom_install_url is not None):
            hash_value ^= hash(custom_install_url)
        
        # deeplink_url
        deeplink_url = self.deeplink_url
        if (deeplink_url is not None):
            hash_value ^= hash(deeplink_url)
        
        description = self.description
        if (description is not None) and (description != self.name):
            hash_value ^= hash(description)
        
        # developers
        developers = self.developers
        if (developers is not None):
            hash_value ^= len(developers) << 6
            
            for developer in developers:
                hash_value ^= hash(developer)
        
        # eula_id
        hash_value ^= self.eula_id
        
        # executables
        executables = self.executables
        if (executables is not None):
            hash_value ^= len(executables) << 10
            
            for executable in executables:
                hash_value ^= hash(executable)
        
        # flags
        hash_value ^= self.flags
        
        # guild_id
        hash_value ^= hash(self.guild_id)
        
        # hook
        hash_value ^= self.hook << 14
        
        # install_parameters
        install_parameters = self.install_parameters
        if (install_parameters is not None):
            hash_value ^= hash(install_parameters)
        
        # icon
        hash_value ^= hash(self.icon)
        
        # max_participants
        hash_value ^= self.max_participants << 15
        
        # name
        hash_value ^= hash(self.name)
        
        # overlay
        hash_value ^= self.overlay << 19
        
        # overlay_compatibility_hook
        hash_value ^= self.overlay_compatibility_hook << 20
        
        # owner
        owner = self.owner
        if (owner is not ZEROUSER):
            hash_value ^= hash(owner)
        
        # primary_sku_id
        hash_value ^= self.primary_sku_id
        
        # privacy_policy_url
        privacy_policy_url = self.privacy_policy_url
        if (privacy_policy_url is not None):
            hash_value ^= hash(privacy_policy_url)
        
        # publishers
        publishers = self.publishers
        if (publishers is not None):
            hash_value ^= len(publishers) << 21
            
            for publisher in publishers:
                hash_value ^= hash(publisher)
        
        # role_connection_verification_url
        role_connection_verification_url = self.role_connection_verification_url
        if (role_connection_verification_url is not None):
            hash_value ^= hash(role_connection_verification_url)
        
        # rpc_origins
        rpc_origins = self.rpc_origins
        if (rpc_origins is not None):
            hash_value ^= len(rpc_origins) << 25
            
            for rpc_origin in rpc_origins:
                hash_value ^= hash(rpc_origin)
        
        # slug
        slug = self.slug
        if (slug is not None):
            hash_value ^= hash(slug)
        
        # splash
        hash_value ^= hash(self.splash)
        
        # tags
        tags = self.tags
        if (tags is not None):
            hash_value ^= len(tags) << 29
            
            for tag in tags:
                hash_value ^= hash(tag)
        
        # terms_of_service_url
        terms_of_service_url = self.terms_of_service_url
        if (terms_of_service_url is not None):
            hash_value ^= hash(terms_of_service_url)
        
        # third_party_skus
        third_party_skus = self.third_party_skus
        if (third_party_skus is not None):
            hash_value ^= len(third_party_skus) << 1
            
            for third_party_sku in third_party_skus:
                hash_value ^= hash(third_party_sku)
        
        # type
        hash_value ^= hash(self.type) << 5
        
        # verify_key
        verify_key = self.verify_key
        if (verify_key is not None):
            hash_value ^= hash(verify_key)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two applications are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two applications are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self is equal to other. Other must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            if self.id != other.id:
                return False
        
        # aliases
        if self.aliases != other.aliases:
            return False
        
        # bot_public
        if self.bot_public != other.bot_public:
            return False
        
        # bot_require_code_grant
        if self.bot_require_code_grant != other.bot_require_code_grant:
            return False
        
        # cover_hash
        if self.cover_hash != other.cover_hash:
            return False
        
        # cover_type
        if self.cover_type != other.cover_type:
            return False
        
        # custom_install_url
        if self.custom_install_url != other.custom_install_url:
            return False
        
        # deeplink_url
        if self.deeplink_url != other.deeplink_url:
            return False
        
        # description
        if self.description != other.description:
            return False
        
        # developers
        if self.developers != other.developers:
            return False
        
        # eula_id
        if self.eula_id != other.eula_id:
            return False
        
        # executables
        if self.executables != other.executables:
            return False
        
        # flags
        if self.flags != other.flags:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        # hook
        if self.hook != other.hook:
            return False
        
        # install_parameters
        if self.install_parameters != other.install_parameters:
            return False
        
        # icon_hash
        if self.icon_hash != other.icon_hash:
            return False
        
        # icon_type
        if self.icon_type != other.icon_type:
            return False
        
        # max_participants
        if self.max_participants != other.max_participants:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # overlay
        if self.overlay != other.overlay:
            return False
        
        # overlay_compatibility_hook
        if self.overlay_compatibility_hook != other.overlay_compatibility_hook:
            return False
        
        # owner
        if self.owner != other.owner:
            return False
        
        # primary_sku_id
        if self.primary_sku_id != other.primary_sku_id:
            return False
        
        # privacy_policy_url
        if self.privacy_policy_url != other.privacy_policy_url:
            return False
        
        # publishers
        if self.publishers != other.publishers:
            return False
        
        # role_connection_verification_url
        if self.role_connection_verification_url != other.role_connection_verification_url:
            return False
        
        # rpc_origins
        if self.rpc_origins != other.rpc_origins:
            return False
        
        # slug
        if self.slug != other.slug:
            return False
        
        # splash_hash
        if self.splash_hash != other.splash_hash:
            return False
        
        # splash_type
        if self.splash_type != other.splash_type:
            return False
        
        # tags
        if self.tags != other.tags:
            return False
        
        # terms_of_service_url
        if self.terms_of_service_url != other.terms_of_service_url:
            return False
        
        # third_party_skus
        if self.third_party_skus != other.third_party_skus:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # verify_key
        if self.verify_key != other.verify_key:
            return False
        
        return True
    
    
    def __repr__(self):
        """Returns the application's representation"""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        application_id = self.id
        if application_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(application_id))
            repr_parts.append(',')
        else:
            repr_parts.append(' (partial)')
    
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __new__(cls, **keyword_parameters):
        """
        Creates a partial application with the given parameters.
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Additional parameters defining the attributes of the application.
        
        Other parameters
        ----------------
        aliases : `None`, `iterable` of `str`, Optional (Keyword only)
            Aliases of the application's name.
        
        application_type : `int`, ``ApplicationType``, Optional (Keyword only)
            The application's type.
        
        bot_public : `bool`, Optional (Keyword only)
            Whether not only the application's owner can join the application's bot to guilds.
            
        bot_require_code_grant : `bool`, Optional (Keyword only)
            Whether the application's bot will only join a guild, when completing the full `oauth2` code grant flow.
        
        cover : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The application's cover.
        
        custom_install_url : `None`, `str`, Optional (Keyword only)
            The application's default custom authorization link if enabled.
        
        deeplink_url : `None, `str`, Optional (Keyword only)
            Deeplink of the application.
        
        description : `None`, `str`, Optional (Keyword only)
            The description of the application.
        
        developers : `None`, `iterable` of ``ApplicationEntity``, Optional (Keyword only)
            The application's games' developers.
        
        eula_id : `int`, Optional (Keyword only)
            The end-user license agreement's id of the application.
        
        executables : `None`, `iterable` of ``ApplicationExecutable``, Optional (Keyword only)
            The application's executables.
        
        flags : `int`, ``ApplicationFlag``, Optional (Keyword only)
            The application's public flags.
        
        guild_id : `int`, Optional (Keyword only)
            If the application is a game sold on Discord, this field tells in which guild it is.
        
        hook : `bool`, Optional (Keyword only)
            ???
        
        install_parameters : `None`, ``ApplicationInstallParameters``, Optional (Keyword only)
            Settings for the application's default in-app authorization link, if enabled.
        
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The application's icon.
        
        max_participants : `int`, Optional (Keyword only)
            The maximal amount of users, who can join the application's embedded activity.
        
        name : `str`, Optional (Keyword only)
            The name of the application. Defaults to empty string.
        
        overlay : `bool`, Optional (Keyword only)
            ???
        
        overlay_compatibility_hook : `bool`, Optional (Keyword only)
            ???
        
        owner : ``ClientUserBase``, ``Team``, Optional (Keyword only)
            The application's owner.
        
        primary_sku_id : `int`, Optional (Keyword only)
            If the application is a game sold on Discord, this field will be the id of the created `Game SKU`.
        
        privacy_policy_url : `None`, `str`, Optional (Keyword only)
            The url of the application's privacy policy.
        
        publishers : `None`, `iterable` of ``ApplicationEntity``, Optional (Keyword only)
            A list of the application's games' publishers.
        
        role_connection_verification_url : `None`, `str`, Optional (Keyword only)
            The application's role connection verification entry point
        
        rpc_origins : `None`, `iterable` of `str`, Optional (Keyword only)
            The application's `rpc` origin urls, if `rpc` is enabled.
        
        slug : `None`, `str`, Optional (Keyword only)
            If this application is a game sold on Discord, this field will be the url slug that links to the store page.
        
        splash : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The application's splash.
        
        tags : `None`, `iterable` of `str`, Optional (Keyword only)
            Up to 5 tags describing the content and functionality of the application.
        
        terms_of_service_url : `None`, `str`, Optional (Keyword only)
            The url of the application's terms of service.
        
        third_party_skus : `None`, `iterable` of ``ThirdPartySKU``, Optional (Keyword only)
             The application's third party stock keeping units.
        
        verify_key : `None`, `str`, Optional (Keyword only)
            A base64 encoded key for the Game SDK's `GetTicket`.
        
        Returns
        -------
        application : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra parameter(s).
        ValueError
            - If an parameter's value is incorrect.
        """
        if keyword_parameters:
            processable = process_application_constructor_parameters(keyword_parameters, NEW_RELATIONS)
        else:
            processable = None
        
        self = cls._create_empty(0)
        
        if (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    
    @classmethod
    def precreate(cls, application_id, **keyword_parameters):
        """
        Precreates an application with the given parameters.
        
        Parameters
        ----------
        application_id : `int`, `str`
            The application's id.
        
        **keyword_parameters : Keyword parameters
            Additional parameters defining the attributes of the application.
        
        Other parameters
        ----------------
        aliases : `None`, `iterable` of `str`, Optional (Keyword only)
            Aliases of the application's name.
        
        application_type : `int`, ``ApplicationType``, Optional (Keyword only)
            The application's type.
        
        bot_public : `bool`, Optional (Keyword only)
            Whether not only the application's owner can join the application's bot to guilds.
            
        bot_require_code_grant : `bool`, Optional (Keyword only)
            Whether the application's bot will only join a guild, when completing the full `oauth2` code grant flow.
        
        cover : `None`, ``Icon``, `str`, Optional (Keyword only)
            The application's cover.
        
        custom_install_url : `None`, `str`, Optional (Keyword only)
            The application's default custom authorization link if enabled.
        
        deeplink_url : `None, `str`, Optional (Keyword only)
            Deeplink of the application.
        
        description : `None`, `str`, Optional (Keyword only)
            The description of the application.
        
        developers : `None`, `iterable` of ``ApplicationEntity``, Optional (Keyword only)
            The application's games' developers.
        
        eula_id : `int`, Optional (Keyword only)
            The end-user license agreement's id of the application.
        
        executables : `None`, `iterable` of ``ApplicationExecutable``, Optional (Keyword only)
            The application's executables.
        
        flags : `int`, ``ApplicationFlag``, Optional (Keyword only)
            The application's public flags.
        
        guild_id : `int`, Optional (Keyword only)
            If the application is a game sold on Discord, this field tells in which guild it is.
        
        hook : `bool`, Optional (Keyword only)
            ???
        
        install_parameters : `None`, ``ApplicationInstallParameters``, Optional (Keyword only)
            Settings for the application's default in-app authorization link, if enabled.
        
        icon : `None`, ``Icon``, `str`, Optional (Keyword only)
            The application's icon.
        
        max_participants : `int`, Optional (Keyword only)
            The maximal amount of users, who can join the application's embedded activity.
        
        name : `str`, Optional (Keyword only)
            The name of the application. Defaults to empty string.
        
        overlay : `bool`, Optional (Keyword only)
            ???
        
        overlay_compatibility_hook : `bool`, Optional (Keyword only)
            ???
        
        owner : ``ClientUserBase``, ``Team``, Optional (Keyword only)
            The application's owner.
        
        primary_sku_id : `int`, Optional (Keyword only)
            If the application is a game sold on Discord, this field will be the id of the created `Game SKU`.
        
        privacy_policy_url : `None`, `str`, Optional (Keyword only)
            The url of the application's privacy policy.
        
        publishers : `None`, `iterable` of ``ApplicationEntity``, Optional (Keyword only)
            A list of the application's games' publishers.
        
        role_connection_verification_url : `None`, `str`, Optional (Keyword only)
            The application's role connection verification entry point
        
        rpc_origins : `None`, `iterable` of `str`, Optional (Keyword only)
            The application's `rpc` origin urls, if `rpc` is enabled.
        
        slug : `None`, `str`, Optional (Keyword only)
            If this application is a game sold on Discord, this field will be the url slug that links to the store page.
        
        splash : `None`, ``Icon``, `str`, Optional (Keyword only)
            The application's splash.
        
        tags : `None`, `iterable` of `str`, Optional (Keyword only)
            Up to 5 tags describing the content and functionality of the application.
        
        terms_of_service_url : `None`, `str`, Optional (Keyword only)
            The url of the application's terms of service.
        
        third_party_skus : `None`, `iterable` of ``ThirdPartySKU``, Optional (Keyword only)
             The application's third party stock keeping units.
        
        verify_key : `None`, `str`, Optional (Keyword only)
            A base64 encoded key for the Game SDK's `GetTicket`.
        
        
        Returns
        -------
        application : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra parameter(s).
        ValueError
            - If an parameter's value is incorrect.
        """
        application_id = validate_id(application_id)
        
        if keyword_parameters:
            processable = process_application_constructor_parameters(keyword_parameters, PRECREATE_RELATIONS)
        else:
            processable = None
        
        try:
            self = APPLICATIONS[application_id]
        except KeyError:
            self = cls._create_empty(application_id)
            APPLICATIONS[application_id] = self
            update = True
        else:
            update = self.partial
        
        if update and (processable is not None):
            for item in processable:
                setattr(self, *item)
        
        return self
    
    
    def copy_with(self, **keyword_parameters):
        """
        Copies the application with the given attributes replaced.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Parameters
        ----------
        **keyword_parameters : Keyword parameters
            Additional parameters defining the attributes of the copy.
        
        Other parameters
        ----------------
        aliases : `None`, `iterable` of `str`, Optional (Keyword only)
            Aliases of the application's name.
        
        application_type : `int`, ``ApplicationType``, Optional (Keyword only)
            The application's type.
        
        bot_public : `bool`, Optional (Keyword only)
            Whether not only the application's owner can join the application's bot to guilds.
            
        bot_require_code_grant : `bool`, Optional (Keyword only)
            Whether the application's bot will only join a guild, when completing the full `oauth2` code grant flow.
        
        cover : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The application's cover.
        
        custom_install_url : `None`, `str`, Optional (Keyword only)
            The application's default custom authorization link if enabled.
        
        deeplink_url : `None, `str`, Optional (Keyword only)
            Deeplink of the application.
        
        description : `None`, `str`, Optional (Keyword only)
            The description of the application.
        
        developers : `None`, `iterable` of ``ApplicationEntity``, Optional (Keyword only)
            The application's games' developers.
        
        eula_id : `int`, Optional (Keyword only)
            The end-user license agreement's id of the application.
        
        executables : `None`, `iterable` of ``ApplicationExecutable``, Optional (Keyword only)
            The application's executables.
        
        flags : `int`, ``ApplicationFlag``, Optional (Keyword only)
            The application's public flags.
        
        guild_id : `int`, Optional (Keyword only)
            If the application is a game sold on Discord, this field tells in which guild it is.
        
        hook : `bool`, Optional (Keyword only)
            ???
        
        install_parameters : `None`, ``ApplicationInstallParameters``, Optional (Keyword only)
            Settings for the application's default in-app authorization link, if enabled.
        
        icon : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The application's icon.
        
        max_participants : `int`, Optional (Keyword only)
            The maximal amount of users, who can join the application's embedded activity.
        
        name : `str`, Optional (Keyword only)
            The name of the application. Defaults to empty string.
        
        overlay : `bool`, Optional (Keyword only)
            ???
        
        overlay_compatibility_hook : `bool`, Optional (Keyword only)
            ???
        
        owner : ``ClientUserBase``, ``Team``, Optional (Keyword only)
            The application's owner.
        
        primary_sku_id : `int`, Optional (Keyword only)
            If the application is a game sold on Discord, this field will be the id of the created `Game SKU`.
        
        privacy_policy_url : `None`, `str`, Optional (Keyword only)
            The url of the application's privacy policy.
        
        publishers : `None`, `iterable` of ``ApplicationEntity``, Optional (Keyword only)
            A list of the application's games' publishers.
        
        role_connection_verification_url : `None`, `str`, Optional (Keyword only)
            The application's role connection verification entry point
        
        rpc_origins : `None`, `iterable` of `str`, Optional (Keyword only)
            The application's `rpc` origin urls, if `rpc` is enabled.
        
        slug : `None`, `str`, Optional (Keyword only)
            If this application is a game sold on Discord, this field will be the url slug that links to the store page.
        
        splash : `None`, ``Icon``, `str`, `bytes-like`, Optional (Keyword only)
            The application's splash.
        
        tags : `None`, `iterable` of `str`, Optional (Keyword only)
            Up to 5 tags describing the content and functionality of the application.
        
        terms_of_service_url : `None`, `str`, Optional (Keyword only)
            The url of the application's terms of service.
        
        third_party_skus : `None`, `iterable` of ``ThirdPartySKU``, Optional (Keyword only)
             The application's third party stock keeping units.
        
        verify_key : `None`, `str`, Optional (Keyword only)
            A base64 encoded key for the Game SDK's `GetTicket`.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra parameter(s).
        ValueError
            - If an parameter's value is incorrect.
        """
        if keyword_parameters:
            processable = process_application_constructor_parameters(keyword_parameters, NEW_RELATIONS)
        else:
            processable = None
        
        new = self.copy()
        
        if (processable is not None):
            for item in processable:
                setattr(new, *item)
        
        return new
    
    
    def copy(self):
        """
        Copies the application returning a new partial one.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        aliases = self.aliases
        if (aliases is not None):
            aliases = (*aliases,)
        new.aliases = aliases
        new.bot_public = self.bot_public
        new.bot_require_code_grant = self.bot_require_code_grant
        new.cover_hash = self.cover_hash
        new.cover_type = self.cover_type
        new.custom_install_url = self.custom_install_url
        new.deeplink_url = self.deeplink_url
        new.description = self.description
        developers = self.developers
        if (developers is not None):
            developers = (*(developer.copy() for developer in developers),)
        new.developers = developers
        new.eula_id = self.eula_id
        executables = self.executables
        if (executables is not None):
            executables = (*(executable.copy() for executable in executables),)
        new.executables = executables
        new.flags = self.flags
        new.guild_id = self.guild_id
        new.hook = self.hook
        install_parameters = self.install_parameters
        if (install_parameters is not None):
            install_parameters = install_parameters.copy()
        new.install_parameters = install_parameters
        new.icon_hash = self.icon_hash
        new.icon_type = self.icon_type
        new.id = 0
        new.max_participants = self.max_participants
        new.name = self.name
        new.overlay = self.overlay
        new.overlay_compatibility_hook = self.overlay_compatibility_hook
        new.owner = self.owner # Do not copy ~ yet
        new.primary_sku_id = self.primary_sku_id
        new.privacy_policy_url = self.privacy_policy_url
        publishers = self.publishers
        if (publishers is not None):
            publishers = (*(publisher.copy() for publisher in publishers),)
        new.publishers = publishers
        new.role_connection_verification_url = self.role_connection_verification_url
        rpc_origins = self.rpc_origins
        if (rpc_origins is not None):
            rpc_origins = (*rpc_origins,)
        new.rpc_origins = rpc_origins
        new.slug = self.slug
        new.splash_hash = self.splash_hash
        new.splash_type = self.splash_type
        tags = self.tags
        if (tags is not None):
            tags = (*tags,)
        new.tags = tags
        new.terms_of_service_url = self.terms_of_service_url
        third_party_skus = self.third_party_skus
        if (third_party_skus is not None):
            third_party_skus = (*(third_party_sku.copy() for third_party_sku in third_party_skus),)
        new.third_party_skus = third_party_skus
        new.type = self.type
        new.verify_key = self.verify_key
        return new
    
    
    @property
    def partial(self):
        """
        Returns whether the application is partial.
        
        Returns
        -------
        partial : `bool`
        """
        application_id = self.id
        if not application_id:
            return True
        
        try:
            client = APPLICATION_ID_TO_CLIENT[application_id]
        except KeyError:
            return True
        
        if not client.running:
            return True
        
        return False
    
    
    @property
    def embedded_activity_configuration(self):
        """
        Deprecated and will be removed in 2023 Marc.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.embedded_activity_configuration` is deprecated and will be removed in '
                f'2023 Marc.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return None
    
    
    def iter_aliases(self):
        """
        Iterates over the aliases of the application.
        
        This method is an iterable generator.
        
        Yields
        ------
        alias : `str`
        """
        aliases = self.aliases
        if (aliases is not None):
            yield from aliases
    
    
    def iter_developers(self):
        """
        Iterates over the developers of the application.
        
        This method is an iterable generator.
        
        Yields
        ------
        developer : ``ApplicationEntity``
        """
        developers = self.developers
        if (developers is not None):
            yield from developers
    
    
    def iter_executables(self):
        """
        Iterates over the executables of the application.
        
        This method is an iterable generator.
        
        Yields
        ------
        executable : ``ApplicationExecutable``
        """
        executables = self.executables
        if (executables is not None):
            yield from executables
    
    
    def iter_publishers(self):
        """
        Iterates over the publishers of the application.
        
        This method is an iterable generator.
        
        Yields
        ------
        publisher : ``ApplicationEntity``
        """
        publishers = self.publishers
        if (publishers is not None):
            yield from publishers
    
    
    def iter_rpc_origins(self):
        """
        Iterates over the rpc origins of the application.
        
        This method is an iterable generator.
        
        Yields
        ------
        rpc_origin : `str`
        """
        rpc_origins = self.rpc_origins
        if (rpc_origins is not None):
            yield from rpc_origins
    
    
    def iter_tags(self):
        """
        Iterates over the tags of the application.
        
        This method is an iterable generator.
        
        Yields
        ------
        alias : `str`
        """
        tags = self.tags
        if (tags is not None):
            yield from tags
    
    
    def iter_third_party_skus(self):
        """
        Iterates over the third party sku-s of the application.
        
        This method is an iterable generator.
        
        Yields
        ------
        third_party_sku : ``ThirdPartySKU``
        """
        third_party_skus = self.third_party_skus
        if (third_party_skus is not None):
            yield from third_party_skus
