__all__ = ('Application', )

from functools import partial as partial_func
from warnings import warn

from scarletio import BaseMethodDescriptor, export

from ...bases import DiscordEntity, ICON_TYPE_NONE, IconSlot
from ...core import APPLICATIONS, APPLICATION_ID_TO_CLIENT, GUILDS
from ...http.urls import (
    build_application_cover_url, build_application_cover_url_as, build_application_icon_url,
    build_application_icon_url_as
)
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...user import ZEROUSER

from ..application_integration_type_configuration import ApplicationIntegrationTypeConfiguration

from .constants import (
    BOT_PUBLIC_DEFAULT, BOT_REQUIRES_CODE_GRANT_DEFAULT, HOOK_DEFAULT, INTEGRATION_PUBLIC_DEFAULT,
    INTEGRATION_REQUIRES_CODE_GRANT_DEFAULT, MAX_PARTICIPANTS_DEFAULT, OVERLAY_COMPATIBILITY_HOOK_DEFAULT,
    OVERLAY_DEFAULT
)
from .fields import (
    parse_aliases, parse_approximate_guild_count, parse_approximate_user_install_count, parse_bot_public,
    parse_bot_requires_code_grant, parse_creator_monetization_state, parse_custom_install_url, parse_deeplink_url,
    parse_description, parse_developers, parse_discoverability_state, parse_discovery_eligibility_flags,
    parse_embedded_activity_configuration, parse_eula_id, parse_event_webhook_event_types, parse_event_webhook_state,
    parse_event_webhook_url, parse_executables, parse_explicit_content_filter_level, parse_flags, parse_guild_id,
    parse_hook, parse_id, parse_install_parameters, parse_integration_public, parse_integration_requires_code_grant,
    parse_integration_types, parse_integration_types_configuration, parse_interaction_endpoint_url,
    parse_interaction_event_types, parse_interaction_version, parse_internal_guild_restriction, parse_max_participants,
    parse_monetization_eligibility_flags, parse_monetization_state, parse_monetized, parse_name, parse_overlay,
    parse_overlay_compatibility_hook, parse_overlay_method_flags, parse_owner, parse_primary_sku_id,
    parse_privacy_policy_url, parse_publishers, parse_redirect_urls, parse_role_connection_verification_url,
    parse_rpc_origins, parse_rpc_state, parse_slug, parse_store_state, parse_tags, parse_terms_of_service_url,
    parse_third_party_skus, parse_type, parse_verification_state, parse_verify_key, put_aliases,
    put_approximate_guild_count, put_approximate_user_install_count, put_bot_public,
    put_bot_requires_code_grant, put_creator_monetization_state, put_custom_install_url,
    put_deeplink_url, put_description, put_developers, put_discoverability_state,
    put_discovery_eligibility_flags, put_embedded_activity_configuration, put_eula_id,
    put_event_webhook_event_types, put_event_webhook_state, put_event_webhook_url, put_executables,
    put_explicit_content_filter_level, put_flags, put_guild_id, put_hook, put_id,
    put_install_parameters, put_integration_public, put_integration_requires_code_grant,
    put_integration_types_configuration, put_integration_types, put_interaction_endpoint_url,
    put_interaction_event_types, put_interaction_version, put_internal_guild_restriction,
    put_max_participants, put_monetization_eligibility_flags, put_monetization_state, put_monetized,
    put_name, put_overlay_compatibility_hook, put_overlay, put_overlay_method_flags, put_owner,
    put_primary_sku_id, put_privacy_policy_url, put_publishers, put_redirect_urls,
    put_role_connection_verification_url, put_rpc_origins, put_rpc_state, put_slug,
    put_store_state, put_tags, put_terms_of_service_url, put_third_party_skus, put_type,
    put_verification_state, put_verify_key, validate_aliases, validate_approximate_guild_count,
    validate_approximate_user_install_count, validate_bot_public, validate_bot_requires_code_grant,
    validate_creator_monetization_state, validate_custom_install_url, validate_deeplink_url, validate_description,
    validate_developers, validate_discoverability_state, validate_discovery_eligibility_flags,
    validate_embedded_activity_configuration, validate_eula_id, validate_event_webhook_event_types,
    validate_event_webhook_state, validate_event_webhook_url, validate_executables,
    validate_explicit_content_filter_level, validate_flags, validate_guild_id, validate_hook, validate_id,
    validate_install_parameters, validate_integration_public, validate_integration_requires_code_grant,
    validate_integration_types, validate_integration_types_configuration, validate_interaction_endpoint_url,
    validate_interaction_event_types, validate_interaction_version, validate_internal_guild_restriction,
    validate_max_participants, validate_monetization_eligibility_flags, validate_monetization_state, validate_monetized,
    validate_name, validate_overlay, validate_overlay_compatibility_hook, validate_overlay_method_flags, validate_owner,
    validate_primary_sku_id, validate_privacy_policy_url, validate_publishers, validate_redirect_urls,
    validate_role_connection_verification_url, validate_rpc_origins, validate_rpc_state, validate_slug,
    validate_store_state, validate_tags, validate_terms_of_service_url, validate_third_party_skus, validate_type,
    validate_verification_state, validate_verify_key
)
from .flags import (
    ApplicationDiscoveryEligibilityFlags, ApplicationFlag, ApplicationMonetizationEligibilityFlags,
    ApplicationOverlayMethodFlags
)
from .preinstanced import (
    ApplicationDiscoverabilityState, ApplicationEventWebhookState, ApplicationExplicitContentFilterLevel,
    ApplicationInteractionVersion, ApplicationInternalGuildRestriction, ApplicationMonetizationState,
    ApplicationRPCState, ApplicationStoreState, ApplicationType, ApplicationVerificationState
)

# Invite application fields
#
# - bot_public
# - bot_requires_code_grant
# - cover_image
# - description
# - embedded_activity_configuration
# - flags
# - hook
# - icon
# - id
# - max_participants
# - monetized
# - name
# - privacy_policy_url
# - rpc_origins
# - splash
# - summary (Deprecated)
# - tags
# - terms_of_service_url
# - type
# - verify_key
#
# Own application fields
#
# - approximate_guild_count
# - approximate_user_install_count
# - bot_public
# - bot_requires_code_grant
# - creator_monetization_state
# - custom_install_url
# - description
# - developers
# - discoverability_state
# - discovery_eligibility_flags
# - explicit_content_filter_level
# - flags
# - guild_id
# - hook
# - icon
# - id
# - install_params
# - integration_public
# - integration_requires_code_grant
# - integration_types
# - integration_types_configuration
# - interaction_endpoint_url
# - interaction_event_types
# - interaction_version
# - internal_guild_restriction
# - monetization_eligibility_flags
# - monetization_state
# - monetized
# - name
# - owner
# - primary_sku_id
# - privacy_policy_url
# - publishers
# - redirect_urls
# - role_connection_verification_url
# - rpc_origins
# - rpc_state
# - slug
# - store_state
# - summary (deprecated)
# - tags
# - team
# - terms_of_service_url
# - type
# - verification_state
# - verify_key
#
# Extra from docs
#
# - guild -> this one is documented, but never received
# - cover_image
# - event_webhooks_types
# - event_webhook_state
# - event_webhook_url
#
# Detectable application fields:
# The ones with `X` were already missing on last update. Omit them on next if they will be still missing.
#
# - aliases
# - bot_public - X
# - bot_requires_code_grant - X
# - cover_image - X
# - deeplink_uri - X
# - description - X
# - developers - X
# - eula_id - X
# - executables
# - flags - X
# - guild_id - X
# - hook
# - icon - X
# - id
# - name
# - overlay
# - overlay_compatibility_hook
# - overlay_method_flags
# - primary_sku_id - X
# - privacy_policy_url - X
# - publishers - X
# - rpc_origins - X
# - slug - X
# - splash - X
# - summary (deprecated) - X
# - tags - X
# - terms_of_service_url - X
# - third_party_skus - X
# - type - X
# - verify_key - X
#
# Cache fields for other use
# - _cache_emojis
#
# Table format:
#
# +-------------------------------------+-----------+-----------+---------------+
# | Name                                | Own       | Invite    | Detectable    |
# +=====================================+===========+===========+===============+
# | aliases                             | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | approximate_guild_count             | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | approximate_user_install_count      | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | bot_public                          | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | bot_requires_code_grant             | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | cover_image                         | PROBABLY  | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | creator_monetization_state          | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | custom_install_url                  | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | deeplink_uri                        | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | description                         | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | developers                          | YES       | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | discoverability_state               | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | discovery_eligibility_flags         | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | embedded_activity_configuration     | NO        | YES       | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | eula_id                             | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | event_webhooks_types                | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | event_webhooks_status               | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | event_webhooks_url                  | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | executables                         | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | explicit_content_filter_level       | YES       | NO        | NO            |
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
# | install_parameters                  | PROBABLY  | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | integration_public                  | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | integration_requires_code_grant     | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | integration_types                   | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | integration_types_configuration     | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | interaction_endpoint_url            | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | interaction_event_types             | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | interaction_version                 | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | internal_guild_restriction          | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | max_participants                    | NO        | YES       | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | monetization_eligibility_flags      | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | monetization_state                  | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | monetized                           | YES       | YES       | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | name                                | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | overlay                             | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | overlay_compatibility_hook          | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | overlay_method_flags                | NO        | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | owner                               | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | primary_sku_id                      | YES       | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | privacy_policy_url                  | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | publishers                          | YES       | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | redirect_urls                       | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | role_connection_verification_url    | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | rpc_origins                         | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | rpc_state                           | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | slug                                | YES       | NO        | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | splash                              | PROBABLY  | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+
# | store_state                         | YES       | NO        | NO            |
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
# | verification_state                  | YES       | NO        | NO            |
# +-------------------------------------+-----------+-----------+---------------+
# | verify_key                          | YES       | YES       | YES           |
# +-------------------------------------+-----------+-----------+---------------+


APPLICATION_COVER = IconSlot('cover', 'cover_image', add_updater = False)
APPLICATION_ICON = IconSlot('icon', 'icon', add_updater = False)
APPLICATION_SPLASH = IconSlot('splash', 'splash', add_updater = False)


COMMON_CONSTRUCT_FIELDS = {
    'aliases': ('aliases', validate_aliases),
    'approximate_guild_count': ('approximate_guild_count', validate_approximate_guild_count),
    'approximate_user_install_count': ('approximate_user_install_count', validate_approximate_user_install_count),
    'bot_public': ('bot_public', validate_bot_public),
    'bot_requires_code_grant': ('bot_requires_code_grant', validate_bot_requires_code_grant),
    'creator_monetization_state': ('creator_monetization_state', validate_creator_monetization_state),
    'custom_install_url': ('custom_install_url', validate_custom_install_url),
    'deeplink_url': ('deeplink_url', validate_deeplink_url),
    'description': ('description', validate_description),
    'developers': ('developers', validate_developers),
    'discoverability_state': ('discoverability_state', validate_discoverability_state),
    'discovery_eligibility_flags': ('discovery_eligibility_flags', validate_discovery_eligibility_flags),
    'embedded_activity_configuration': ('embedded_activity_configuration', validate_embedded_activity_configuration),
    'eula_id': ('eula_id', validate_eula_id),
    'event_webhook_event_types': ('event_webhook_event_types', validate_event_webhook_event_types),
    'event_webhook_state': ('event_webhook_state', validate_event_webhook_state),
    'event_webhook_url': ('event_webhook_url', validate_event_webhook_url),
    'executables': ('executables', validate_executables),
    'explicit_content_filter_level': ('explicit_content_filter_level', validate_explicit_content_filter_level),
    'flags': ('flags', validate_flags),
    'guild_id': ('guild_id', validate_guild_id),
    'hook': ('hook', validate_hook),
    'install_parameters': ('install_parameters', validate_install_parameters),
    'integration_public': ('integration_public', validate_integration_public),
    'integration_requires_code_grant': ('integration_requires_code_grant', validate_integration_requires_code_grant),
    'integration_types': ('integration_types', validate_integration_types),
    'integration_types_configuration': ('integration_types_configuration', validate_integration_types_configuration),
    'interaction_endpoint_url': ('interaction_endpoint_url', validate_interaction_endpoint_url),
    'interaction_event_types': ('interaction_event_types', validate_interaction_event_types),
    'interaction_version': ('interaction_version', validate_interaction_version),
    'internal_guild_restriction': ('internal_guild_restriction', validate_internal_guild_restriction),
    'max_participants': ('max_participants', validate_max_participants),
    'monetization_eligibility_flags': ('monetization_eligibility_flags', validate_monetization_eligibility_flags),
    'monetization_state': ('monetization_state', validate_monetization_state),
    'monetized': ('monetized', validate_monetized),
    'name': ('name', validate_name),
    'overlay': ('overlay', validate_overlay),
    'overlay_compatibility_hook': ('overlay_compatibility_hook', validate_overlay_compatibility_hook),
    'overlay_method_flags': ('overlay_method_flags', validate_overlay_method_flags),
    'owner': ('owner', validate_owner),
    'primary_sku_id': ('primary_sku_id', validate_primary_sku_id),
    'privacy_policy_url': ('privacy_policy_url', validate_privacy_policy_url),
    'publishers': ('publishers', validate_publishers),
    'redirect_urls': ('redirect_urls', validate_redirect_urls),
    'role_connection_verification_url': ('role_connection_verification_url', validate_role_connection_verification_url),
    'rpc_origins': ('rpc_origins', validate_rpc_origins),
    'rpc_state': ('rpc_state', validate_rpc_state),
    'slug': ('slug', validate_slug),
    'store_state': ('store_state', validate_store_state),
    'tags': ('tags', validate_tags),
    'terms_of_service_url': ('terms_of_service_url', validate_terms_of_service_url),
    'third_party_skus': ('third_party_skus', validate_third_party_skus),
    'application_type': ('type', validate_type),
    'verification_state': ('verification_state', validate_verification_state),
    'verify_key': ('verify_key', validate_verify_key),
}

PRECREATE_FIELDS = {
    **COMMON_CONSTRUCT_FIELDS,
    'cover': ('cover', APPLICATION_COVER.validate_icon),
    'icon': ('icon', APPLICATION_ICON.validate_icon),
    'splash': ('splash', APPLICATION_SPLASH.validate_icon),
}

NEW_FIELDS = {
    **COMMON_CONSTRUCT_FIELDS,
    'cover': ('cover', partial_func(APPLICATION_COVER.validate_icon, allow_data = True)),
    'icon': ('icon', partial_func(APPLICATION_ICON.validate_icon, allow_data = True)),
    'splash': ('splash', partial_func(APPLICATION_SPLASH.validate_icon, allow_data = True)),
}


@export
class Application(DiscordEntity, immortal = True):
    """
    Represents a Discord application with all of it's spice.
    
    When a ``Client`` is created, it starts it's life with an empty application by default. However when the client
    logs in, it's application is requested, but it can be updated by ``Client.update_application_info`` anytime.
    
    Attributes
    ----------
    _cache_emojis : `None | dict<int, Emoji>`
        Application emoji cache.
    
    aliases : `None | tuple<str>`
        Aliases of the application's name.
    
    approximate_guild_count : `int`
        The approximate count of the guilds the application is in.
    
    approximate_user_install_count : `int`
        The approximate count of the users who installed the application.
    
    bot_public : `bool`.
        Whether not only the application's owner can join the application's bot to guilds.
        Defaults to `False`
    
    bot_requires_code_grant : `bool`
        Whether the application's bot will only join a guild when completing the full `oauth2` code grant flow.
        Defaults to `False`.
    
    cover_hash : `int`
        The application's store cover image's hash in `uint128`. If the application is sold at Discord, this image
        will be used at the store.
    
    cover_type : ``IconType``
        The application's store cover image's type.
    
    creator_monetization_state : ``ApplicationMonetizationState``
        The monetization state of the creator.
    
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
    
    discoverability_state : ``ApplicationDiscoverabilityState``
        The application's state towards being discoverable.
        Defaults to `ApplicationDiscoverabilityState.none`.
    
    discovery_eligibility_flags : ``ApplicationDiscoveryEligibilityFlags``
        Represents which step the application passed to be eligible for discoverability.
    
    embedded_activity_configuration : `None`, ``EmbeddedActivityConfiguration``
        Configuration for the application's embedded activity.
        Defaults to `None`.
    
    eula_id : `int`
        The end-user license agreement's id of the application.
        Defaults to `0` if not applicable.
    
    event_webhook_event_types : `None | tuple<ApplicationEventWebhookEventType>`
        The type event of eventy received through event webhook.
    
    event_webhook_state : ``ApplicationEventWebhookState``
        The state of the event webhook.
    
    event_webhook_url : ˙None | str`
        The url where the event webhook requests are going.
    
    executables : `None`, `tuple` of ``ApplicationExecutable``
        The application's executables.
        Defaults to `None`.
    
    explicit_content_filter_level : ``ApplicationExplicitContentFilterLevel``
        Represents an application's explicit content filter level.
    
    flags : ``ApplicationFlag``
        The application's public flags.
    
    guild_id : `int`
        If the application is a game sold on Discord, this field tells in which guild it is.
        Defaults to `0` if not applicable.
    
    hook : `bool`
        Whether the application's bot is allowed to hook into the application's game directly.
        Defaults to `False`.
    
    install_parameters : `None`, ``ApplicationInstallParameters``
        Settings for the application's default in-app authorization link, if enabled.
    
    integration_public : `bool`.
        Whether not only the application's owner can install the application's integration.
        Defaults to `False`
    
    integration_requires_code_grant : `bool`
        Whether the application's integration will only be installed when completing the full `oauth2` code grant flow.
        Defaults to `False`.
    
    integration_types : `None | tuple<ApplicationIntegrationType>`
        The enabled options where the application can be integrated to.
    
    integration_types_configuration : `None | dict<ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration>`
        Integration type specific configuration for installing the application.
    
    interaction_endpoint_url : `None`, `str`
        Whether and to which url should interaction events be sent to.
        Defaults to `None`.
    
    interaction_event_types : `None`, `tuple` of ``ApplicationInteractionEventType``
        Which event types should be sent to ``.interaction_endpoint_url``.
        ``.interaction_version`` must be ``ApplicationInteractionVersion.selective``.
        Defaults to `None`.
    
    interaction_version : ``ApplicationInteractionVersion``
        The type of interaction to send towards ``.interaction_endpoint_url``.
        Defaults to ``ApplicationInteractionVersion.none``.
    
    internal_guild_restriction : ``ApplicationInternalGuildRestriction``
        The application's internal guild restriction.
    
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
    
    monetization_eligibility_flags : ``ApplicationMonetizationEligibilityFlags``
        Represents which step the application passed to be eligible for monetization.
    
    monetization_state : ``ApplicationMonetizationState``
        The application's state towards monetization.
    
    monetized : `bool`
        Whether the application is monetized.
        Defaults to `False`.
    
    name : `str`
        The name of the application. Defaults to empty string.
    
    overlay : `bool`
        Defaults to `False`.
    
    overlay_compatibility_hook : `bool`
        Defaults to `False`.
    
    overlay_method_flags : ``ApplicationOverlayMethodFlags``
        Represents which features the application's overlaying supports.
    
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
    
    redirect_urls : `None | tuple<str>`
        Configured oauth2 redirect urls.
        Defaults to `None`.
    
    role_connection_verification_url : `None`, `str`
        The application's role connection verification entry point
    
    rpc_origins : `None | tuple<str>`
        The application's `rpc` origin urls, if `rpc` is enabled.
        Defaults to `None`.
    
    rpc_state : ``ApplicationRPCState``
        The application's state towards having having approved rpc.
    
    slug : `None`, `str`
        If this application is a game sold on Discord, this field will be the url slug that links to the store page.
        Defaults to `None`.
    
    splash_hash : `int`
        The application's splash image's hash as `uint128`.
    
    splash_type : ``IconType``
        The application's splash image's type.
    
    store_state : ``ApplicationStoreState``
        The application's state towards having approved store.
    
    tags : `None | tuple<str>`
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
    
    verification_state : ``ApplicationVerificationState``
        The application's state towards verification.
    
    verify_key : `None`, `str`
        A base64 encoded key for the Game SDK's `GetTicket`.
        Defaults to `None`.
    
    Notes
    -----
    The instances of the class support weakreferencing.
    """
    __slots__ = (
        '_cache_emojis', 'aliases', 'approximate_guild_count', 'approximate_user_install_count', 'bot_public',
        'bot_requires_code_grant', 'creator_monetization_state', 'custom_install_url', 'deeplink_url', 'description',
        'developers', 'discoverability_state', 'discovery_eligibility_flags',  'embedded_activity_configuration',
        'eula_id', 'event_webhook_event_types', 'event_webhook_state', 'event_webhook_url', 'executables',
        'explicit_content_filter_level', 'flags', 'guild_id', 'hook', 'install_parameters', 'integration_public',
        'integration_requires_code_grant', 'integration_types', 'integration_types_configuration',
        'interaction_endpoint_url', 'interaction_event_types', 'interaction_version', 'internal_guild_restriction',
        'max_participants', 'monetization_eligibility_flags', 'monetization_state', 'monetized', 'name', 'overlay',
        'overlay_compatibility_hook', 'overlay_method_flags', 'owner', 'primary_sku_id', 'privacy_policy_url',
        'publishers', 'redirect_urls', 'role_connection_verification_url', 'rpc_origins', 'rpc_state', 'slug',
        'store_state', 'tags', 'terms_of_service_url', 'third_party_skus', 'type', 'verification_state', 'verify_key'
    )
    
    cover = APPLICATION_COVER
    icon = APPLICATION_ICON
    splash = APPLICATION_SPLASH
    
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

        self._cache_emojis = None
        self.aliases = None
        self.approximate_guild_count = 0
        self.approximate_user_install_count = 0
        self.bot_public = BOT_PUBLIC_DEFAULT
        self.bot_requires_code_grant = BOT_REQUIRES_CODE_GRANT_DEFAULT
        self.cover_hash = 0
        self.cover_type = ICON_TYPE_NONE
        self.creator_monetization_state = ApplicationMonetizationState.none
        self.custom_install_url = None
        self.deeplink_url = None
        self.description = None
        self.developers = None
        self.discoverability_state = ApplicationDiscoverabilityState.none
        self.discovery_eligibility_flags = ApplicationDiscoveryEligibilityFlags()
        self.embedded_activity_configuration = None
        self.eula_id = 0
        self.event_webhook_event_types = None
        self.event_webhook_state = ApplicationEventWebhookState.none
        self.event_webhook_url = None
        self.executables = None
        self.explicit_content_filter_level = ApplicationExplicitContentFilterLevel.none
        self.flags = ApplicationFlag()
        self.guild_id = 0
        self.hook = HOOK_DEFAULT
        self.icon_hash = 0
        self.icon_type = ICON_TYPE_NONE
        self.id = application_id
        self.install_parameters = None
        self.integration_public = INTEGRATION_PUBLIC_DEFAULT
        self.integration_requires_code_grant = INTEGRATION_REQUIRES_CODE_GRANT_DEFAULT
        self.integration_types = None
        self.integration_types_configuration = None
        self.interaction_endpoint_url = None
        self.interaction_event_types = None
        self.interaction_version = ApplicationInteractionVersion.none
        self.internal_guild_restriction = ApplicationInternalGuildRestriction.none
        self.max_participants = MAX_PARTICIPANTS_DEFAULT
        self.monetization_eligibility_flags = ApplicationMonetizationEligibilityFlags()
        self.monetization_state = ApplicationMonetizationState.none
        self.monetized = False
        self.name = ''
        self.overlay = OVERLAY_DEFAULT
        self.overlay_compatibility_hook = OVERLAY_COMPATIBILITY_HOOK_DEFAULT
        self.overlay_method_flags = ApplicationOverlayMethodFlags()
        self.owner = ZEROUSER
        self.primary_sku_id = 0
        self.privacy_policy_url = None
        self.publishers = None
        self.redirect_urls = None
        self.role_connection_verification_url = None
        self.rpc_origins = None
        self.rpc_state = ApplicationRPCState.none
        self.slug = None
        self.splash_hash = 0
        self.splash_type = ICON_TYPE_NONE
        self.store_state = ApplicationStoreState.none
        self.tags = None
        self.terms_of_service_url = None
        self.third_party_skus = None
        self.type = ApplicationType.none
        self.verification_state = ApplicationVerificationState.none
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
        
        data : `dict<str, object>`
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
        data : `dict<str, object>`
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
        data : `dict<str, object>`
            Application data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        warn(
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
        data : `dict<str, object>`
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
        data : `dict<str, object>`
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
        data : `dict<str, object>`
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
        data : `dict<str, object>`
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
        data : `dict<str, object>`, Optional
            Application data.
        """
        self.flags = parse_flags(data)
    
    
    def _update_attributes_own(self, data):
        """
        Updates the application's attributes when it's own data was requested.
        
        Parameters
        ----------
        data : `dict<str, object>`, Optional
            Application data.
        """
        self._update_attributes_common(data)
        self.approximate_guild_count = parse_approximate_guild_count(data)
        self.approximate_user_install_count = parse_approximate_user_install_count(data)
        self.creator_monetization_state = parse_creator_monetization_state(data)
        self.custom_install_url = parse_custom_install_url(data)
        self.developers = parse_developers(data)
        self.discoverability_state = parse_discoverability_state(data)
        self.discovery_eligibility_flags = parse_discovery_eligibility_flags(data)
        self.event_webhook_event_types = parse_event_webhook_event_types(data)
        self.event_webhook_state = parse_event_webhook_state(data)
        self.event_webhook_url = parse_event_webhook_url(data)
        self.explicit_content_filter_level = parse_explicit_content_filter_level(data)
        self.guild_id = parse_guild_id(data)
        self.install_parameters = parse_install_parameters(data)
        self.integration_public = parse_integration_public(data)
        self.integration_requires_code_grant = parse_integration_requires_code_grant(data)
        self.integration_types = parse_integration_types(data)
        self.integration_types_configuration = parse_integration_types_configuration(data)
        self.interaction_endpoint_url = parse_interaction_endpoint_url(data)
        self.interaction_event_types = parse_interaction_event_types(data)
        self.interaction_version = parse_interaction_version(data)
        self.internal_guild_restriction = parse_internal_guild_restriction(data)
        self.monetization_eligibility_flags = parse_monetization_eligibility_flags(data)
        self.monetization_state = parse_monetization_state(data)
        self.monetized = parse_monetized(data)
        self.owner = parse_owner(data)
        self.primary_sku_id = parse_primary_sku_id(data)
        self.publishers = parse_publishers(data)
        self.redirect_urls = parse_redirect_urls(data)
        self.role_connection_verification_url = parse_role_connection_verification_url(data)
        self.rpc_state = parse_rpc_state(data)
        self.slug = parse_slug(data)
        self.store_state = parse_store_state(data)
        self.verification_state = parse_verification_state(data)
    
    
    def _update_attributes_invite(self, data):
        """
        Updates the application's attributes when it's data is part of an invite.
        
        Parameters
        ----------
        data : `dict<str, object>`, Optional
            Application data.
        """
        self._update_attributes_common(data)
        self.embedded_activity_configuration = parse_embedded_activity_configuration(data)
        self.max_participants = parse_max_participants(data)
        self.monetized = parse_monetized(data)
    
    
    def _update_attributes_detectable(self, data):
        """
        Updates the application's attributes when requesting all detectable applications.
        
        Parameters
        ----------
        data : `dict<str, object>`, Optional
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
        self.overlay_method_flags = parse_overlay_method_flags(data)
        self.primary_sku_id = parse_primary_sku_id(data)
        self.publishers = parse_publishers(data)
        self.slug = parse_slug(data)
        self.third_party_skus = parse_third_party_skus(data)
    
    
    def _update_attributes_common(self, data):
        """
        Updates the commonly distributed fields of the application.
        
        Parameters
        ----------
        data : `dict<str, object>`, Optional
            Application data.
        """
        self.bot_public = parse_bot_public(data)
        self.bot_requires_code_grant = parse_bot_requires_code_grant(data)
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
        
        This one is method is used for templating only.
        If you want direct underlaying functionality please use a specialised method instead:
        
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
        data : `dict<str, object>`
        """
        data = {}
        
        if include_internals:
            warn(
                (
                    f'`{self.__class__.__name__}` has specialized to-data converters if you wanna include internal '
                    f'fields. They are: `.to_data_ready`, `.to_data_own`, `.to_data_invite`, `.to_data_detectable`. '
                    f'Please use any of those instead.'
                ),
                RuntimeWarning,
                stacklevel = 2,
            )
            
            put_id(self.id, data, defaults)
        
        type(self).cover.put_into(self.cover, data, defaults, as_data = not include_internals)
        put_custom_install_url(self.custom_install_url, data, defaults)
        put_description(self.description, data, defaults)
        put_flags(self.flags, data, defaults)
        type(self).icon.put_into(self.icon, data, defaults, as_data = not include_internals)
        put_install_parameters(self.install_parameters, data, defaults)
        put_interaction_endpoint_url(self.interaction_endpoint_url, data, defaults)
        put_role_connection_verification_url(self.role_connection_verification_url, data, defaults)
        put_tags(self.tags, data, defaults)
        return data
    
    
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
        data : `dict<str, object>`
        """
        data = {}
        put_flags(self.flags, data, defaults)
        if include_internals:
            put_id(self.id, data, defaults)
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
        data : `dict<str, object>`
        """
        data = self._to_data_common(defaults, include_internals)
        put_approximate_guild_count(self.approximate_guild_count, data, defaults)
        put_approximate_user_install_count(self.approximate_user_install_count, data, defaults)
        put_creator_monetization_state(self.creator_monetization_state, data, defaults)
        put_custom_install_url(self.custom_install_url, data, defaults)
        put_developers(self.developers, data, defaults, include_internals = True)
        put_discoverability_state(self.discoverability_state, data, defaults)
        put_discovery_eligibility_flags(self.discovery_eligibility_flags, data, defaults)
        put_event_webhook_event_types(self.event_webhook_event_types, data, defaults)
        put_event_webhook_state(self.event_webhook_state, data, defaults)
        put_event_webhook_url(self.event_webhook_url, data, defaults)
        put_explicit_content_filter_level(self.explicit_content_filter_level, data, defaults)
        put_guild_id(self.guild_id, data, defaults)
        put_install_parameters(self.install_parameters, data, defaults)
        put_integration_public(self.integration_public, data, defaults)
        put_integration_requires_code_grant(self.integration_requires_code_grant, data, defaults)
        put_integration_types(self.integration_types, data, defaults)
        put_integration_types_configuration(self.integration_types_configuration, data, defaults)
        put_interaction_endpoint_url(self.interaction_endpoint_url, data, defaults)
        put_interaction_event_types(self.interaction_event_types, data, defaults)
        put_interaction_version(self.interaction_version, data, defaults)
        put_internal_guild_restriction(self.internal_guild_restriction, data, defaults)
        put_monetization_eligibility_flags(self.monetization_eligibility_flags, data, defaults)
        put_monetization_state(self.monetization_state, data, defaults)
        put_monetized(self.monetized, data, defaults)
        if include_internals:
            put_owner(self.owner, data, defaults)
        put_primary_sku_id(self.primary_sku_id, data, defaults)
        put_publishers(self.publishers, data, defaults, include_internals = True)
        put_redirect_urls(self.redirect_urls, data, defaults)
        put_role_connection_verification_url(self.role_connection_verification_url, data, defaults)
        put_rpc_state(self.rpc_state, data, defaults)
        put_slug(self.slug, data, defaults)
        put_store_state(self.store_state, data, defaults)
        put_verification_state(self.verification_state, data, defaults)
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
        data : `dict<str, object>`
        """
        data = self._to_data_common(defaults, include_internals)
        put_embedded_activity_configuration(self.embedded_activity_configuration, data, defaults)
        put_max_participants(self.max_participants, data, defaults)
        put_monetized(self.monetized, data, defaults)
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
        data : `dict<str, object>`
        """
        data = self._to_data_common(defaults, include_internals)
        put_aliases(self.aliases, data, defaults)
        put_deeplink_url(self.deeplink_url, data, defaults)
        put_developers(self.developers, data, defaults, include_internals = True)
        put_eula_id(self.eula_id, data, defaults)
        put_executables(self.executables, data, defaults)
        put_guild_id(self.guild_id, data, defaults)
        put_overlay(self.overlay, data, defaults)
        put_overlay_compatibility_hook(self.overlay_compatibility_hook, data, defaults)
        put_overlay_method_flags(self.overlay_method_flags, data, defaults)
        put_primary_sku_id(self.primary_sku_id, data, defaults)
        put_publishers(self.publishers, data, defaults, include_internals = True)
        put_slug(self.slug, data, defaults)
        put_third_party_skus(self.third_party_skus, data, defaults)
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
        data : `dict<str, object>`
        """
        data = {}
        put_bot_public(self.bot_public, data, defaults)
        put_bot_requires_code_grant(self.bot_requires_code_grant, data, defaults)
        type(self).cover.put_into(self.cover, data, defaults, as_data = not include_internals)
        put_description(self.description, data, defaults)
        put_flags(self.flags, data, defaults)
        put_hook(self.hook, data, defaults)
        if include_internals:
            put_id(self.id, data, defaults)
        type(self).icon.put_into(self.icon, data, defaults, as_data = not include_internals)
        put_name(self.name, data, defaults)
        put_privacy_policy_url(self.privacy_policy_url, data, defaults)
        put_rpc_origins(self.rpc_origins, data, defaults)
        type(self).splash.put_into(self.splash, data, defaults, as_data = not include_internals)
        put_tags(self.tags, data, defaults)
        put_terms_of_service_url(self.terms_of_service_url, data, defaults)
        put_type(self.type, data, defaults)
        put_verify_key(self.verify_key, data, defaults)
        return data
    
    
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
        
        # approximate_guild_count
        hash_value ^= self.approximate_guild_count << 8
        
        # approximate_user_install_count
        hash_value ^= self.approximate_user_install_count <<35
        
        # bot_public
        hash_value ^= self.bot_public << 4
        
        # bot_requires_code_grant
        hash_value ^= self.bot_requires_code_grant << 5
        
        # cover
        hash_value ^= hash(self.cover)
        
        # creator_monetization_state
        hash_value ^= hash(self.creator_monetization_state) << 7
        
        # custom_install_url
        custom_install_url = self.custom_install_url
        if (custom_install_url is not None):
            hash_value ^= hash(custom_install_url)
        
        # integration_public
        hash_value ^= self.integration_public << 2
        
        # integration_requires_code_grant
        hash_value ^= self.integration_requires_code_grant << 9
        
        # integration_types
        integration_types = self.integration_types
        if (integration_types is not None):
            hash_value ^= len(integration_types) << 33
            
            for integration_type in integration_types:
                hash_value ^= hash(integration_type)
        
        # integration_types_configuration
        integration_types_configuration = self.integration_types_configuration
        if (integration_types_configuration is not None):
            hash_value ^= len(integration_types_configuration) << 34
            
            for integration_type, integration_type_configuration in integration_types_configuration.items():
                hash_value ^= hash(integration_type) & hash(integration_type_configuration)
        
        # interaction_endpoint_url
        interaction_endpoint_url = self.interaction_endpoint_url
        if (interaction_endpoint_url is not None):
            hash_value ^= hash(interaction_endpoint_url)
        
        # interaction_event_types
        interaction_event_types = self.interaction_event_types
        if (interaction_event_types is not None):
            hash_value ^= len(interaction_event_types) << 22
            
            for interaction_event_type in interaction_event_types:
                hash_value ^= hash(interaction_event_type)
        
        # interaction_version
        hash_value ^= hash(self.interaction_version) << 23
        
        # internal_guild_restriction
        hash_value ^= hash(self.internal_guild_restriction) << 24
        
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
        
        # discoverability_state
        hash_value ^= hash(self.discoverability_state) << 16
        
        # discovery_eligibility_flags
        hash_value ^= self.discovery_eligibility_flags << 17
        
        # embedded_activity_configuration
        embedded_activity_configuration = self.embedded_activity_configuration
        if (embedded_activity_configuration is not None):
            hash_value ^= hash(embedded_activity_configuration)
        
        # eula_id
        hash_value ^= self.eula_id
        
        # event_webhook_event_types
        event_webhook_event_types = self.event_webhook_event_types
        if (event_webhook_event_types is not None):
            hash_value ^ len(event_webhook_event_types) << 36
            
            for event_webhook_event_type in event_webhook_event_types:
                hash_value ^= hash(event_webhook_event_type)
        
        # event_webhook_state
        hash_value ^= hash(self.event_webhook_state) << 37
        
        # event_webhook_url
        event_webhook_url = self.event_webhook_url
        if (event_webhook_url is not None):
            hash_value ^= hash(event_webhook_url)
        
        # executables
        executables = self.executables
        if (executables is not None):
            hash_value ^= len(executables) << 10
            
            for executable in executables:
                hash_value ^= hash(executable)
        
        # explicit_content_filter_level
        hash_value ^= hash(self.explicit_content_filter_level) << 11
        
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
        
        # monetization_eligibility_flags
        hash_value ^= hash(self.monetization_eligibility_flags) << 26
        
        # monetization_state
        hash_value ^= hash(self.monetization_state) << 27
        
        # monetized
        hash_value ^= self.monetized << 18
        
        # name
        hash_value ^= hash(self.name)
        
        # overlay
        hash_value ^= self.overlay << 19
        
        # overlay_compatibility_hook
        hash_value ^= self.overlay_compatibility_hook << 20
        
        # overlay_method_flags
        hash_value ^= self.overlay_method_flags << 32
        
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
        
        # redirect_urls
        redirect_urls = self.redirect_urls
        if (redirect_urls is not None):
            hash_value ^= len(redirect_urls) << 28
            
            for redirect_url in redirect_urls:
                hash_value ^= hash(redirect_url)
        
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
        
        # rpc_state
        hash_value ^= hash(self.rpc_state) << 30
        
        # slug
        slug = self.slug
        if (slug is not None):
            hash_value ^= hash(slug)
        
        # store_state
        hash_value ^= hash(self.store_state) << 31
        
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
        
        # verification_state
        hash_value ^= hash(self.verification_state)
        
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
        
        # approximate_guild_count
        if self.approximate_guild_count != other.approximate_guild_count:
            return False
        
        # approximate_user_install_count
        if self.approximate_user_install_count != other.approximate_user_install_count:
            return False
        
        # bot_public
        if self.bot_public != other.bot_public:
            return False
        
        # bot_requires_code_grant
        if self.bot_requires_code_grant != other.bot_requires_code_grant:
            return False
        
        # cover_hash
        if self.cover_hash != other.cover_hash:
            return False
        
        # cover_type
        if self.cover_type != other.cover_type:
            return False
        
        # creator_monetization_state
        if self.creator_monetization_state != other.creator_monetization_state:
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
        
        # discoverability_state
        if self.discoverability_state != other.discoverability_state:
            return False
        
        # discovery_eligibility_flags
        if self.discovery_eligibility_flags != other.discovery_eligibility_flags:
            return False
        
        # embedded_activity_configuration
        if self.embedded_activity_configuration != other.embedded_activity_configuration:
            return False
        
        # eula_id
        if self.eula_id != other.eula_id:
            return False
        
        # event_webhook_event_types
        if self.event_webhook_event_types != other.event_webhook_event_types:
            return False
        
        # event_webhook_state
        if self.event_webhook_state != other.event_webhook_state:
            return False
        
        # event_webhook_url
        if self.event_webhook_url != other.event_webhook_url:
            return False
        
        # executables
        if self.executables != other.executables:
            return False
        
        # explicit_content_filter_level
        if self.explicit_content_filter_level is not other.explicit_content_filter_level:
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
        
        # integration_public
        if self.integration_public != other.integration_public:
            return False
        
        # integration_requires_code_grant
        if self.integration_requires_code_grant != other.integration_requires_code_grant:
            return False
        
        # integration_types
        if self.integration_types != other.integration_types:
            return False
        
        # integration_types_configuration
        if self.integration_types_configuration != other.integration_types_configuration:
            return False
        
        # interaction_endpoint_url
        if self.interaction_endpoint_url != other.interaction_endpoint_url:
            return False
        
        # interaction_event_types
        if self.interaction_event_types != other.interaction_event_types:
            return False
        
        # interaction_version
        if self.interaction_version is not other.interaction_version:
            return False
        
        # internal_guild_restriction
        if self.internal_guild_restriction is not other.internal_guild_restriction:
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
        
        # monetization_eligibility_flags
        if self.monetization_eligibility_flags != other.monetization_eligibility_flags:
            return False
        
        # monetization_state
        if self.monetization_state is not other.monetization_state:
            return False
        
        # monetized
        if self.monetized != other.monetized:
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
        
        # overlay_method_flags
        if self.overlay_method_flags != other.overlay_method_flags:
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
        
        # redirect_urls
        if self.redirect_urls != other.redirect_urls:
            return False
        
        # role_connection_verification_url
        if self.role_connection_verification_url != other.role_connection_verification_url:
            return False
        
        # rpc_origins
        if self.rpc_origins != other.rpc_origins:
            return False
        
        # rpc_state
        if self.rpc_state != other.rpc_state:
            return False
        
        # slug
        if self.slug != other.slug:
            return False
        
        # store_state
        if self.store_state != other.store_state:
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
        
        # verification_state
        if self.verification_state is not other.verification_state:
            return False
        
        # verify_key
        if self.verify_key != other.verify_key:
            return False
        
        return True
    
    
    def __repr__(self):
        """Returns the application's representation"""
        repr_parts = [
            '<',
            type(self).__name__,
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
        
        Other Parameters
        ----------------
        aliases : `None`, `iterable` of `str`, Optional (Keyword only)
            Aliases of the application's name.
        
        approximate_guild_count : `int`, Optional (Keyword only)
            The approximate count of the guilds the application is in.
    
        approximate_user_install_count : `int`, Optional (Keyword only)
            The approximate count of the users who installed the application.
        
        application_type : `int`, ``ApplicationType``, Optional (Keyword only)
            The application's type.
        
        bot_public : `bool`, Optional (Keyword only)
            Whether not only the application's owner can join the application's bot to guilds.
        
        bot_requires_code_grant : `bool`, Optional (Keyword only)
            Whether the application's bot will only join a guild when completing the full `oauth2` code grant flow.
        
        cover : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The application's cover.
        
        creator_monetization_state : ``ApplicationMonetizationState``, `int`, Optional (Keyword only)
            The monetization state of the creator.
        
        custom_install_url : `None`, `str`, Optional (Keyword only)
            The application's default custom authorization link if enabled.
        
        deeplink_url : `None, `str`, Optional (Keyword only)
            Deeplink of the application.
        
        description : `None`, `str`, Optional (Keyword only)
            The description of the application.
        
        developers : `None`, `iterable` of ``ApplicationEntity``, Optional (Keyword only)
            The application's games' developers.
        
        discoverability_state : ``ApplicationDiscoverabilityState``, `int`, Optional (Keyword only)
            The application's state towards being discoverable.
        
        discovery_eligibility_flags : ``ApplicationDiscoveryEligibilityFlags``, `int`, Optional (Keyword only)
            Represents which step the application passed to be eligible for discoverability.
        
        embedded_activity_configuration : `None`, ``EmbeddedActivityConfiguration``, Optional (Keyword only)
            Configuration for the application's embedded activity.
        
        eula_id : `int`, Optional (Keyword only)
            The end-user license agreement's id of the application.
        
        event_webhook_event_types : `None | iterable<ApplicationEventWebhookEventType | str>`, Optional (Keyword only)
            The type event of eventy received through event webhook.
        
        event_webhook_state : ApplicationEventWebhookState | int`, Optional (Keyword only)
            The state of the event webhook.
        
        event_webhook_url : ˙None | str`, Optional (Keyword only)
            The url where the event webhook requests are going.
        
        executables : `None`, `iterable` of ``ApplicationExecutable``, Optional (Keyword only)
            The application's executables.
        
        explicit_content_filter_level : ``ApplicationExplicitContentFilterLevel``, `int`, Optional (Keyword only)
            Represents an application's explicit content filter level.
        
        flags : `int`, ``ApplicationFlag``, Optional (Keyword only)
            The application's public flags.
        
        guild_id : `int`, Optional (Keyword only)
            If the application is a game sold on Discord, this field tells in which guild it is.
        
        hook : `bool`, Optional (Keyword only)
            Whether the application's bot is allowed to hook into the application's game directly.
        
        icon : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The application's icon.
        
        install_parameters : `None`, ``ApplicationInstallParameters``, Optional (Keyword only)
            Settings for the application's default in-app authorization link, if enabled.
        
        integration_public : `bool`., Optional (Keyword only)
            Whether not only the application's owner can install the application's integration.
        
        integration_requires_code_grant : `bool`, Optional (Keyword only)
            Whether the application's integration will only be installed when completing the full `oauth2` code
            grant flow.
    
        integration_types : `None | iterable<ApplicationIntegrationType | int>`, Optional (Keyword only)
            The enabled options where the application can be integrated to.
        
        integration_types_configuration : \
                `None | dict<ApplicationIntegrationType | int, ApplicationIntegrationTypeConfiguration>` \
                , Optional (Keyword only)
            Integration type specific configuration for installing the application.
        
        interaction_endpoint_url : `None`, `str`, Optional (Keyword only)
            Whether and to which url should interaction events be sent to.
        
        interaction_event_types : `None`, `iterable` of ``ApplicationInteractionEventType``, `iterable` of `str` \
                , Optional (Keyword only)
            Which event types should be sent to ``.interaction_endpoint_url``.
        
        interaction_version : ``ApplicationInteractionVersion``, `int`, Optional (Keyword only)
            The type of interaction to send towards ``.interaction_endpoint_url``.
        
        internal_guild_restriction : ``ApplicationInternalGuildRestriction``, `int`, Optional (Keyword only)
            The application's internal guild restriction.
        
        max_participants : `int`, Optional (Keyword only)
            The maximal amount of users, who can join the application's embedded activity.
        
        monetization_eligibility_flags : ``ApplicationMonetizationEligibilityFlags``, `int`, Optional (Keyword only)
            Represents which step the application passed to be eligible for monetization.
            
        monetization_state : ``ApplicationMonetizationState``, `int`, Optional (Keyword only)
            The application's state towards monetization.
        
        monetized : `bool``, Optional (Keyword only)
            Whether the application is monetized.
        
        name : `str`, Optional (Keyword only)
            The name of the application. Defaults to empty string.
        
        overlay : `bool`, Optional (Keyword only)
            ???
        
        overlay_compatibility_hook : `bool`, Optional (Keyword only)
            ???
    
        overlay_method_flags : ``ApplicationOverlayMethodFlags``, `int`, Optional (Keyword only)
            Represents which features the application's overlaying supports.
        
        owner : ``ClientUserBase``, ``Team``, Optional (Keyword only)
            The application's owner.
        
        primary_sku_id : `int`, Optional (Keyword only)
            If the application is a game sold on Discord, this field will be the id of the created `Game SKU`.
        
        privacy_policy_url : `None`, `str`, Optional (Keyword only)
            The url of the application's privacy policy.
        
        publishers : `None`, `iterable` of ``ApplicationEntity``, Optional (Keyword only)
            A list of the application's games' publishers.
    
        redirect_urls : `None | str | iterable<str>`, Optional (Keyword only)
            Configured oauth2 redirect urls.
        
        role_connection_verification_url : `None`, `str`, Optional (Keyword only)
            The application's role connection verification entry point
        
        rpc_origins : `None`, `iterable` of `str`, Optional (Keyword only)
            The application's `rpc` origin urls, if `rpc` is enabled.
        
        rpc_state : ``ApplicationRPCState``, `int`, Optional (Keyword only)
            The application's state towards having having approved rpc.
        
        slug : `None`, `str`, Optional (Keyword only)
            If this application is a game sold on Discord, this field will be the url slug that links to the store page.
        
        splash : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The application's splash.
        
        store_state : ``ApplicationStoreState``, `int`, Optional (Keyword only)
            The application's state towards having approved store.
        
        tags : `None`, `iterable` of `str`, Optional (Keyword only)
            Up to 5 tags describing the content and functionality of the application.
        
        terms_of_service_url : `None`, `str`, Optional (Keyword only)
            The url of the application's terms of service.
        
        third_party_skus : `None`, `iterable` of ``ThirdPartySKU``, Optional (Keyword only)
             The application's third party stock keeping units.
        
        verification_state : ``ApplicationVerificationState``, `int`, Optional (Keyword only)
            The application's state towards verification.
        
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
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, NEW_FIELDS)
        else:
            processed = None
        
        self = cls._create_empty(0)
        
        if (processed is not None):
            for item in processed:
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
        
        Other Parameters
        ----------------
        aliases : `None`, `iterable` of `str`, Optional (Keyword only)
            Aliases of the application's name.
    
        approximate_guild_count : `int`, Optional (Keyword only)
            The approximate count of the guilds the application is in.
    
        approximate_user_install_count : `int`, Optional (Keyword only)
            The approximate count of the users who installed the application.
        
        application_type : `int`, ``ApplicationType``, Optional (Keyword only)
            The application's type.
        
        bot_public : `bool`, Optional (Keyword only)
            Whether not only the application's owner can join the application's bot to guilds.
            
        bot_requires_code_grant : `bool`, Optional (Keyword only)
            Whether the application's bot will only join a guild when completing the full `oauth2` code grant flow.
        
        cover : ``None | str | Icon``, Optional (Keyword only)
            The application's cover.
        
        creator_monetization_state : ``ApplicationMonetizationState``, `int`, Optional (Keyword only)
            The monetization state of the creator.
        
        custom_install_url : `None`, `str`, Optional (Keyword only)
            The application's default custom authorization link if enabled.
        
        deeplink_url : `None, `str`, Optional (Keyword only)
            Deeplink of the application.
        
        description : `None`, `str`, Optional (Keyword only)
            The description of the application.
        
        developers : `None`, `iterable` of ``ApplicationEntity``, Optional (Keyword only)
            The application's games' developers.
        
        discoverability_state : ``ApplicationDiscoverabilityState``, `int`, Optional (Keyword only)
            The application's state towards being discoverable.
        
        discovery_eligibility_flags : ``ApplicationDiscoveryEligibilityFlags``, `int`, Optional (Keyword only)
            Represents which step the application passed to be eligible for discoverability.
        
        embedded_activity_configuration : `None`, ``EmbeddedActivityConfiguration``, Optional (Keyword only)
            Configuration for the application's embedded activity.
        
        eula_id : `int`, Optional (Keyword only)
            The end-user license agreement's id of the application.
        
        event_webhook_event_types : `None | iterable<ApplicationEventWebhookEventType | str>`, Optional (Keyword only)
            The type event of eventy received through event webhook.
        
        event_webhook_state : ApplicationEventWebhookState | int`, Optional (Keyword only)
            The state of the event webhook.
        
        event_webhook_url : ˙None | str`, Optional (Keyword only)
            The url where the event webhook requests are going.
        
        executables : `None`, `iterable` of ``ApplicationExecutable``, Optional (Keyword only)
            The application's executables.
        
        explicit_content_filter_level : ``ApplicationExplicitContentFilterLevel``, `int`, Optional (Keyword only)
            Represents an application's explicit content filter level.
        
        flags : `int`, ``ApplicationFlag``, Optional (Keyword only)
            The application's public flags.
        
        guild_id : `int`, Optional (Keyword only)
            If the application is a game sold on Discord, this field tells in which guild it is.
        
        hook : `bool`, Optional (Keyword only)
            Whether the application's bot is allowed to hook into the application's game directly.
        
        icon : ``None | str | Icon``, Optional (Keyword only)
            The application's icon.
        
        install_parameters : `None`, ``ApplicationInstallParameters``, Optional (Keyword only)
            Settings for the application's default in-app authorization link, if enabled.
        
        integration_public : `bool`., Optional (Keyword only)
            Whether not only the application's owner can install the application's integration.
        
        integration_requires_code_grant : `bool`, Optional (Keyword only)
            Whether the application's integration will only be installed when completing the full `oauth2` code
            grant flow.
    
        integration_types : `None | iterable<ApplicationIntegrationType | int>`, Optional (Keyword only)
            The enabled options where the application can be integrated to.
        
        
        integration_types_configuration : \
                `None | dict<ApplicationIntegrationType | int, ApplicationIntegrationTypeConfiguration>` \
                , Optional (Keyword only)
            Integration type specific configuration for installing the application.
        
        interaction_endpoint_url : `None`, `str`, Optional (Keyword only)
            Whether and to which url should interaction events be sent to.
        
        interaction_event_types : `None`, `iterable` of ``ApplicationInteractionEventType``, `iterable` of `str` \
                , Optional (Keyword only)
            Which event types should be sent to ``.interaction_endpoint_url``.
        
        interaction_version : ``ApplicationInteractionVersion``, `int`, Optional (Keyword only)
            The type of interaction to send towards ``.interaction_endpoint_url``.
        
        internal_guild_restriction : ``ApplicationInternalGuildRestriction``, `int`, Optional (Keyword only)
            The application's internal guild restriction.
        
        max_participants : `int`, Optional (Keyword only)
            The maximal amount of users, who can join the application's embedded activity.
        
        monetization_eligibility_flags : ``ApplicationMonetizationEligibilityFlags``, `int`, Optional (Keyword only)
            Represents which step the application passed to be eligible for monetization.
            
        monetization_state : ``ApplicationMonetizationState``, `int`, Optional (Keyword only)
            The application's state towards monetization.
        
        monetized : `bool``, Optional (Keyword only)
            Whether the application is monetized.
        
        name : `str`, Optional (Keyword only)
            The name of the application. Defaults to empty string.
        
        overlay : `bool`, Optional (Keyword only)
            ???
        
        overlay_compatibility_hook : `bool`, Optional (Keyword only)
            ???
    
        overlay_method_flags : ``ApplicationOverlayMethodFlags``, `int`, Optional (Keyword only)
            Represents which features the application's overlaying supports.
        
        owner : ``ClientUserBase``, ``Team``, Optional (Keyword only)
            The application's owner.
        
        primary_sku_id : `int`, Optional (Keyword only)
            If the application is a game sold on Discord, this field will be the id of the created `Game SKU`.
        
        privacy_policy_url : `None`, `str`, Optional (Keyword only)
            The url of the application's privacy policy.
        
        publishers : `None`, `iterable` of ``ApplicationEntity``, Optional (Keyword only)
            A list of the application's games' publishers.
    
        redirect_urls : `None | str | iterable<str>`, Optional (Keyword only)
            Configured oauth2 redirect urls.
        
        role_connection_verification_url : `None`, `str`, Optional (Keyword only)
            The application's role connection verification entry point
        
        rpc_origins : `None`, `iterable` of `str`, Optional (Keyword only)
            The application's `rpc` origin urls, if `rpc` is enabled.
        
        rpc_state : ``ApplicationRPCState``, `int`, Optional (Keyword only)
            The application's state towards having having approved rpc.
        
        slug : `None`, `str`, Optional (Keyword only)
            If this application is a game sold on Discord, this field will be the url slug that links to the store page.
        
        splash : ``None | str | Icon``, Optional (Keyword only)
            The application's splash.
        
        store_state : ``ApplicationStoreState``, `int`, Optional (Keyword only)
            The application's state towards having approved store.
        
        tags : `None`, `iterable` of `str`, Optional (Keyword only)
            Up to 5 tags describing the content and functionality of the application.
        
        terms_of_service_url : `None`, `str`, Optional (Keyword only)
            The url of the application's terms of service.
        
        third_party_skus : `None`, `iterable` of ``ThirdPartySKU``, Optional (Keyword only)
             The application's third party stock keeping units.
        
        verification_state : ``ApplicationVerificationState``, `int`, Optional (Keyword only)
            The application's state towards verification.
        
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
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = APPLICATIONS[application_id]
        except KeyError:
            self = cls._create_empty(application_id)
            APPLICATIONS[application_id] = self
            update = True
        else:
            update = self.partial
        
        if update and (processed is not None):
            for item in processed:
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
        
        Other Parameters
        ----------------
        aliases : `None`, `iterable` of `str`, Optional (Keyword only)
            Aliases of the application's name.
    
        approximate_guild_count : `int`, Optional (Keyword only)
            The approximate count of the guilds the application is in.
    
        approximate_user_install_count : `int`, Optional (Keyword only)
            The approximate count of the users who installed the application.
        
        application_type : `int`, ``ApplicationType``, Optional (Keyword only)
            The application's type.
        
        bot_public : `bool`, Optional (Keyword only)
            Whether not only the application's owner can join the application's bot to guilds.
            
        bot_requires_code_grant : `bool`, Optional (Keyword only)
            Whether the application's bot will only join a guild when completing the full `oauth2` code grant flow.
        
        cover : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The application's cover.
        
        creator_monetization_state : ``ApplicationMonetizationState``, `int`, Optional (Keyword only)
            The monetization state of the creator.
        
        custom_install_url : `None`, `str`, Optional (Keyword only)
            The application's default custom authorization link if enabled.
        
        deeplink_url : `None, `str`, Optional (Keyword only)
            Deeplink of the application.
        
        description : `None`, `str`, Optional (Keyword only)
            The description of the application.
        
        developers : `None`, `iterable` of ``ApplicationEntity``, Optional (Keyword only)
            The application's games' developers.
        
        discoverability_state : ``ApplicationDiscoverabilityState``, `int`, Optional (Keyword only)
            The application's state towards being discoverable.
        
        discovery_eligibility_flags : ``ApplicationDiscoveryEligibilityFlags``, `int`, Optional (Keyword only)
            Represents which step the application passed to be eligible for discoverability.

        embedded_activity_configuration : `None`, ``EmbeddedActivityConfiguration``, Optional (Keyword only)
            Configuration for the application's embedded activity.
        
        eula_id : `int`, Optional (Keyword only)
            The end-user license agreement's id of the application.
        
        event_webhook_event_types : `None | iterable<ApplicationEventWebhookEventType | str>`, Optional (Keyword only)
            The type event of eventy received through event webhook.
        
        event_webhook_state : ApplicationEventWebhookState | int`, Optional (Keyword only)
            The state of the event webhook.
        
        event_webhook_url : ˙None | str`, Optional (Keyword only)
            The url where the event webhook requests are going.
        
        executables : `None`, `iterable` of ``ApplicationExecutable``, Optional (Keyword only)
            The application's executables.
        
        explicit_content_filter_level : ``ApplicationExplicitContentFilterLevel``, `int`, Optional (Keyword only)
            Represents an application's explicit content filter level.
        
        flags : `int`, ``ApplicationFlag``, Optional (Keyword only)
            The application's public flags.
        
        guild_id : `int`, Optional (Keyword only)
            If the application is a game sold on Discord, this field tells in which guild it is.
        
        hook : `bool`, Optional (Keyword only)
            Whether the application's bot is allowed to hook into the application's game directly.
        
        icon : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The application's icon.
        
        install_parameters : `None`, ``ApplicationInstallParameters``, Optional (Keyword only)
            Settings for the application's default in-app authorization link, if enabled.
        
        integration_public : `bool`., Optional (Keyword only)
            Whether not only the application's owner can install the application's integration.
        
        integration_requires_code_grant : `bool`, Optional (Keyword only)
            Whether the application's integration will only be installed when completing the full `oauth2` code
            grant flow.
        
        integration_types : `None | iterable<ApplicationIntegrationType | int>`, Optional (Keyword only)
            The enabled options where the application can be integrated to.
        
        integration_types_configuration : \
                `None | dict<ApplicationIntegrationType | int, ApplicationIntegrationTypeConfiguration>` \
                , Optional (Keyword only)
            Integration type specific configuration for installing the application.
        
        interaction_endpoint_url : `None`, `str`, Optional (Keyword only)
            Whether and to which url should interaction events be sent to.
        
        interaction_event_types : `None`, `iterable` of ``ApplicationInteractionEventType``, `iterable` of `str` \
                , Optional (Keyword only)
            Which event types should be sent to ``.interaction_endpoint_url``.
        
        interaction_version : ``ApplicationInteractionVersion``, `int`, Optional (Keyword only)
            The type of interaction to send towards ``.interaction_endpoint_url``.
        
        internal_guild_restriction : ``ApplicationInternalGuildRestriction``, `int`, Optional (Keyword only)
            The application's internal guild restriction.
        
        max_participants : `int`, Optional (Keyword only)
            The maximal amount of users, who can join the application's embedded activity.
        
        monetization_eligibility_flags : ``ApplicationMonetizationEligibilityFlags``, `int`, Optional (Keyword only)
            Represents which step the application passed to be eligible for monetization.
            
        monetization_state : ``ApplicationMonetizationState``, `int`, Optional (Keyword only)
            The application's state towards monetization.
        
        monetized : `bool``, Optional (Keyword only)
            Whether the application is monetized.
        
        name : `str`, Optional (Keyword only)
            The name of the application. Defaults to empty string.
        
        overlay : `bool`, Optional (Keyword only)
            ???
        
        overlay_compatibility_hook : `bool`, Optional (Keyword only)
            ???
    
        overlay_method_flags : ``ApplicationOverlayMethodFlags``, `int`, Optional (Keyword only)
            Represents which features the application's overlaying supports.
        
        owner : ``ClientUserBase``, ``Team``, Optional (Keyword only)
            The application's owner.
        
        primary_sku_id : `int`, Optional (Keyword only)
            If the application is a game sold on Discord, this field will be the id of the created `Game SKU`.
        
        privacy_policy_url : `None`, `str`, Optional (Keyword only)
            The url of the application's privacy policy.
        
        publishers : `None`, `iterable` of ``ApplicationEntity``, Optional (Keyword only)
            A list of the application's games' publishers.
    
        redirect_urls : `None | str | iterable<str>`, Optional (Keyword only)
            Configured oauth2 redirect urls.
        
        role_connection_verification_url : `None`, `str`, Optional (Keyword only)
            The application's role connection verification entry point
        
        rpc_origins : `None`, `iterable` of `str`, Optional (Keyword only)
            The application's `rpc` origin urls, if `rpc` is enabled.
        
        rpc_state : ``ApplicationRPCState``, `int`, Optional (Keyword only)
            The application's state towards having having approved rpc.
        
        slug : `None`, `str`, Optional (Keyword only)
            If this application is a game sold on Discord, this field will be the url slug that links to the store page.
        
        splash : ``None | str | bytes-like | Icon``, Optional (Keyword only)
            The application's splash.
        
        store_state : ``ApplicationStoreState``, `int`, Optional (Keyword only)
            The application's state towards having approved store.
        
        tags : `None`, `iterable` of `str`, Optional (Keyword only)
            Up to 5 tags describing the content and functionality of the application.
        
        terms_of_service_url : `None`, `str`, Optional (Keyword only)
            The url of the application's terms of service.
        
        third_party_skus : `None`, `iterable` of ``ThirdPartySKU``, Optional (Keyword only)
             The application's third party stock keeping units.
        
        verification_state : ``ApplicationVerificationState``, `int`, Optional (Keyword only)
            The application's state towards verification.
        
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
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, NEW_FIELDS)
        else:
            processed = None
        
        new = self.copy()
        
        if (processed is not None):
            for item in processed:
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
        new._cache_emojis = None
        aliases = self.aliases
        if (aliases is not None):
            aliases = (*aliases,)
        new.aliases = aliases
        new.approximate_guild_count = self.approximate_guild_count
        new.approximate_user_install_count = self.approximate_user_install_count
        new.bot_public = self.bot_public
        new.bot_requires_code_grant = self.bot_requires_code_grant
        new.cover_hash = self.cover_hash
        new.cover_type = self.cover_type
        new.creator_monetization_state = self.creator_monetization_state
        new.custom_install_url = self.custom_install_url
        new.deeplink_url = self.deeplink_url
        new.description = self.description
        developers = self.developers
        if (developers is not None):
            developers = (*(developer.copy() for developer in developers),)
        new.developers = developers
        new.discoverability_state = self.discoverability_state
        new.discovery_eligibility_flags = self.discovery_eligibility_flags
        embedded_activity_configuration = self.embedded_activity_configuration
        if (embedded_activity_configuration is not None):
            embedded_activity_configuration = embedded_activity_configuration.copy()
        new.embedded_activity_configuration = embedded_activity_configuration
        new.eula_id = self.eula_id
        event_webhook_event_types = self.event_webhook_event_types
        if (event_webhook_event_types is not None):
            event_webhook_event_types = (*event_webhook_event_types,)
        new.event_webhook_event_types = event_webhook_event_types
        new.event_webhook_state = self.event_webhook_state
        new.event_webhook_url = self.event_webhook_url
        executables = self.executables
        if (executables is not None):
            executables = (*(executable.copy() for executable in executables),)
        new.executables = executables
        new.explicit_content_filter_level = self.explicit_content_filter_level
        new.flags = self.flags
        new.guild_id = self.guild_id
        new.hook = self.hook
        install_parameters = self.install_parameters
        if (install_parameters is not None):
            install_parameters = install_parameters.copy()
        new.install_parameters = install_parameters
        new.integration_public = self.integration_public
        new.integration_requires_code_grant = self.integration_requires_code_grant
        integration_types = self.integration_types
        if (integration_types is not None):
            integration_types = (*integration_types,)
        new.integration_types = integration_types
        integration_types_configuration = self.integration_types_configuration
        if (integration_types_configuration is not None):
            integration_types_configuration = {
                integration_type : integration_type_configuration.copy()
                for integration_type, integration_type_configuration
                in integration_types_configuration.items()
            }
        new.integration_types_configuration = integration_types_configuration
        new.interaction_endpoint_url = self.interaction_endpoint_url
        interaction_event_types = self.interaction_event_types
        if (interaction_event_types is not None):
            interaction_event_types = (*interaction_event_types,)
        new.interaction_event_types = interaction_event_types
        new.interaction_version = self.interaction_version
        new.internal_guild_restriction = self.internal_guild_restriction
        new.icon_hash = self.icon_hash
        new.icon_type = self.icon_type
        new.id = 0
        new.max_participants = self.max_participants
        new.monetization_eligibility_flags = self.monetization_eligibility_flags
        new.monetization_state = self.monetization_state
        new.monetized = self.monetized
        new.name = self.name
        new.overlay = self.overlay
        new.overlay_compatibility_hook = self.overlay_compatibility_hook
        new.overlay_method_flags = self.overlay_method_flags
        new.owner = self.owner # Do not copy ~ yet
        new.primary_sku_id = self.primary_sku_id
        new.privacy_policy_url = self.privacy_policy_url
        publishers = self.publishers
        if (publishers is not None):
            publishers = (*(publisher.copy() for publisher in publishers),)
        new.publishers = publishers
        redirect_urls = self.redirect_urls
        if (redirect_urls is not None):
            redirect_urls = (*redirect_urls,)
        new.redirect_urls = redirect_urls
        new.role_connection_verification_url = self.role_connection_verification_url
        rpc_origins = self.rpc_origins
        if (rpc_origins is not None):
            rpc_origins = (*rpc_origins,)
        new.rpc_origins = rpc_origins
        new.rpc_state = self.rpc_state
        new.slug = self.slug
        new.splash_hash = self.splash_hash
        new.splash_type = self.splash_type
        new.store_state = self.store_state
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
        new.verification_state = self.verification_state
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
    
    
    @property
    def guild(self):
        """
        Returns the application's guild. The guild must be cached.
        
        Returns
        -------
        guild : ``None | Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    def iter_event_webhook_event_types(self):
        """
        Iterates over the event webhook event types of the application
        
        This method is an iterable generator.
        
        Yields
        ------
        event_webhook_event_type : ``ApplicationEventWebhookEventType``
        """
        event_webhook_event_types = self.event_webhook_event_types
        if (event_webhook_event_types is not None):
            yield from event_webhook_event_types
    
    
    def iter_interaction_event_types(self):
        """
        Iterates over the selected interaction event types of the application.
        
        This method is an iterable generator.
        
        Yields
        ------
        interaction_event_type : ``ApplicationInteractionEventType``
        """
        interaction_event_types = self.interaction_event_types
        if (interaction_event_types is not None):
            yield from interaction_event_types


    def iter_redirect_urls(self):
        """
        Iterates over the redirect urls of the application.
        
        This method is an iterable generator.
        
        Yields
        ------
        redirect_url : `str`
        """
        redirect_urls = self.redirect_urls
        if (redirect_urls is not None):
            yield from redirect_urls
    
    
    def has_integration_type(self, integration_type):
        """
        Returns whether the application has the given integration type enabled.
        
        Parameters
        ----------
        integration_type : `int`, ``ApplicationIntegrationType``
            The integration type to check.
        
        Returns
        -------
        hash_integration_type : `bool`
        """
        integration_types = self.integration_types
        if integration_types is None:
            return False
        
        return integration_type in integration_types
    
    
    def iter_integration_types(self):
        """
        Iterates over the integration types that the application has enabled.
        
        Yields
        ------
        integration_type : ``ApplicationIntegrationType``
        """
        integration_types = self.integration_types
        if (integration_types is not None):
            yield from integration_types
    
    
    def get_integration_type_configuration(self, integration_type):
        """
        Returns the application's configuration for the given integration type.
        
        Parameters
        ----------
        integration_type : `int`, ``ApplicationIntegrationType``
            The integration type to get configuration for.
        
        Returns
        -------
        configuration : ``ApplicationIntegrationTypeConfiguration``
        """
        integration_types_configuration = self.integration_types_configuration
        if (integration_types_configuration is not None):
            try:
                return integration_types_configuration[integration_type]
            except KeyError:
                pass
        
        return ApplicationIntegrationTypeConfiguration._create_empty()
    
    
    # emoji cache
    
    def _add_cache_emoji(self, emoji):
        """
        Adds an emoji to the application's cached emojis.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to add.
        """
        cache_emojis = self._cache_emojis
        if cache_emojis is None:
            cache_emojis = {}
            self._cache_emojis = cache_emojis
        
        cache_emojis[emoji.id] = emoji
    
    
    def _delete_cache_emoji_by_id(self, emoji_id):
        """
        Deletes an emoji from the application's cached emojis by its identifier.
        
        Parameters
        ----------
        emoji_id : `int`
            The emoji identifier to delete.
        
        Returns
        -------
        success : `bool`
        """
        cache_emojis = self._cache_emojis
        if cache_emojis is None:
            return False
        
        try:
            del cache_emojis[emoji_id]
        except KeyError:
            return False
        
        if not cache_emojis:
            self._cache_emojis = None
        
        return True
    
    
    def _has_cache_emoji_by_id(self, emoji_id):
        """
        Returns whether the application has the given emoji cached by its identifier.
        
        Parameters
        ----------
        emoji_id : `int`
            The emoji identifier to check for.
        
        Returns
        -------
        has_emoji : `bool`
        """
        cache_emojis = self._cache_emojis
        if cache_emojis is None:
            return False
        
        return emoji_id in cache_emojis
    
    
    # urls
    
    @property
    def cover_url(self):
        """
        Returns the application's cover's url. If the application has no cover, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_application_cover_url(self.id, self.cover_type, self.cover_hash)
    
    
    def cover_url_as(self, ext = None, size = None):
        """
        Returns the application's cover's url. If the application has no cover, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
            If the application has animated cover, it can be `'gif'` as well.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_application_cover_url_as(self.id, self.cover_type, self.cover_hash, ext, size)
    
    
    @property
    def icon_url(self):
        """
        Returns the application's icon's url. If the application has no icon, then returns `None`.
        
        Returns
        -------
        url : `None | str`
        """
        return build_application_icon_url(self.id, self.icon_type, self.icon_hash)
    
    
    def icon_url_as(self, ext = None, size = None):
        """
        Returns the application's icon's url. If the application has no icon, then returns `None`.
        
        Parameters
        ----------
        ext : `None | str` = `None`, Optional
            The extension of the image's url. Can be any of: `'jpg'`, `'jpeg'`, `'png'`, `'webp'`.
            If the application has animated icon, it can be `'gif'` as well.
        
        size : `None | int` = `None`, Optional
            The preferred minimal size of the image's url.
        
        Returns
        -------
        url : `None | str`
        """
        return build_application_icon_url_as(self.id, self.icon_type, self.icon_hash, ext, size)
