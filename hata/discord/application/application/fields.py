__all__ = ()

from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, flag_parser_factory, force_string_parser_factory, int_parser_factory,
    int_postprocess_parser_factory, nullable_array_parser_factory, nullable_entity_array_parser_factory,
    nullable_entity_parser_factory, nullable_string_parser_factory, preinstanced_array_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, entity_id_putter_factory,
    flag_optional_putter_factory, force_string_putter_factory, int_optional_postprocess_putter_factory,
    int_putter_factory, nullable_entity_array_putter_factory, nullable_entity_optional_putter_factory,
    nullable_string_array_optional_putter_factory, nullable_string_putter_factory, preinstanced_array_putter_factory,
    preinstanced_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, flag_validator_factory, force_string_validator_factory,
    int_conditional_validator_factory, nullable_entity_array_validator_factory, nullable_entity_validator_factory,
    nullable_string_array_validator_factory, nullable_string_validator_factory, preinstanced_array_validator_factory,
    preinstanced_validator_factory, url_array_optional_validator_factory, url_optional_validator_factory
)
from ...guild import Guild
from ...user import ClientUserBase, User, ZEROUSER

from ..application_entity import ApplicationEntity
from ..application_executable import ApplicationExecutable
from ..application_install_parameters import ApplicationInstallParameters
from ..application_integration_type_configuration import ApplicationIntegrationTypeConfiguration
from ..embedded_activity_configuration import EmbeddedActivityConfiguration
from ..eula import EULA
from ..team import Team
from ..third_party_sku import ThirdPartySKU

from .constants import (
    BOT_PUBLIC_DEFAULT, BOT_REQUIRES_CODE_GRANT_DEFAULT, DESCRIPTION_LENGTH_MAX, HOOK_DEFAULT,
    INTEGRATION_PUBLIC_DEFAULT, INTEGRATION_REQUIRES_CODE_GRANT_DEFAULT, MAX_PARTICIPANTS_DEFAULT, NAME_LENGTH_MAX,
    NAME_LENGTH_MIN, OVERLAY_COMPATIBILITY_HOOK_DEFAULT, OVERLAY_DEFAULT
)
from .flags import (
    ApplicationDiscoveryEligibilityFlags, ApplicationFlag, ApplicationMonetizationEligibilityFlags,
    ApplicationOverlayMethodFlags
)
from .preinstanced import (
    ApplicationDiscoverabilityState, ApplicationEventWebhookEventType, ApplicationEventWebhookState,
    ApplicationExplicitContentFilterLevel, ApplicationIntegrationType, ApplicationInteractionEventType,
    ApplicationInteractionVersion, ApplicationInternalGuildRestriction, ApplicationMonetizationState,
    ApplicationRPCState, ApplicationStoreState, ApplicationType, ApplicationVerificationState
)

# aliases

parse_aliases = nullable_array_parser_factory('aliases')
put_aliases_into = nullable_string_array_optional_putter_factory('aliases')
validate_aliases = nullable_string_array_validator_factory('aliases')

# approximate_guild_count

parse_approximate_guild_count = int_parser_factory('approximate_guild_count', 0)
put_approximate_guild_count_into = int_putter_factory('approximate_guild_count')
validate_approximate_guild_count = int_conditional_validator_factory(
    'approximate_guild_count',
    0,
    (lambda approximate_guild_count : approximate_guild_count >= 0),
    '>= 0',
)

# approximate_user_install_count

parse_approximate_user_install_count = int_parser_factory('approximate_user_install_count', 0)
put_approximate_user_install_count_into = int_putter_factory('approximate_user_install_count')
validate_approximate_user_install_count = int_conditional_validator_factory(
    'approximate_user_install_count',
    0,
    (lambda approximate_user_install_count : approximate_user_install_count >= 0),
    '>= 0',
)

# bot_public

parse_bot_public = bool_parser_factory('bot_public', BOT_PUBLIC_DEFAULT)
put_bot_public_into = bool_optional_putter_factory('bot_public', BOT_PUBLIC_DEFAULT)
validate_bot_public = bool_validator_factory('bot_public', BOT_PUBLIC_DEFAULT)

# bot_requires_code_grant

parse_bot_requires_code_grant = bool_parser_factory('bot_require_code_grant', BOT_REQUIRES_CODE_GRANT_DEFAULT)
put_bot_requires_code_grant_into = bool_optional_putter_factory('bot_require_code_grant', BOT_REQUIRES_CODE_GRANT_DEFAULT)
validate_bot_requires_code_grant = bool_validator_factory('bot_requires_code_grant', BOT_REQUIRES_CODE_GRANT_DEFAULT)

# creator_monetization_state

parse_creator_monetization_state = preinstanced_parser_factory(
    'creator_monetization_state', ApplicationMonetizationState, ApplicationMonetizationState.none
)
put_creator_monetization_state_into = preinstanced_putter_factory('creator_monetization_state')
validate_creator_monetization_state = preinstanced_validator_factory(
    'creator_monetization_state', ApplicationMonetizationState
)

# custom_install_url

parse_custom_install_url = nullable_string_parser_factory('custom_install_url')
put_custom_install_url_into = url_optional_putter_factory('custom_install_url')
validate_custom_install_url = url_optional_validator_factory('custom_install_url')

# deeplink_url

parse_deeplink_url = nullable_string_parser_factory('deeplink_uri')
put_deeplink_url_into = url_optional_putter_factory('deeplink_uri')
validate_deeplink_url = url_optional_validator_factory('deeplink_url')

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', 0, DESCRIPTION_LENGTH_MAX)

# developers

parse_developers = nullable_entity_array_parser_factory('developers', ApplicationEntity)
put_developers_into = nullable_entity_array_putter_factory('developers', ApplicationEntity)
validate_developers = nullable_entity_array_validator_factory('developers', ApplicationEntity)

# discoverability_state

parse_discoverability_state = preinstanced_parser_factory(
    'discoverability_state', ApplicationDiscoverabilityState, ApplicationDiscoverabilityState.none
)
put_discoverability_state_into = preinstanced_putter_factory('discoverability_state')
validate_discoverability_state = preinstanced_validator_factory(
    'discoverability_state', ApplicationDiscoverabilityState
)


# discovery_eligibility_flags

parse_discovery_eligibility_flags = flag_parser_factory(
    'discovery_eligibility_flags', ApplicationDiscoveryEligibilityFlags
)
put_discovery_eligibility_flags_into = flag_optional_putter_factory(
    'discovery_eligibility_flags', ApplicationDiscoveryEligibilityFlags()
)
validate_discovery_eligibility_flags = flag_validator_factory(
    'discovery_eligibility_flags', ApplicationDiscoveryEligibilityFlags
)


# embedded_activity_configuration

parse_embedded_activity_configuration = nullable_entity_parser_factory(
    'embedded_activity_config', EmbeddedActivityConfiguration
)
put_embedded_activity_configuration_into = nullable_entity_optional_putter_factory(
    'embedded_activity_config', EmbeddedActivityConfiguration
)
validate_embedded_activity_configuration = nullable_entity_validator_factory(
    'embedded_activity_configuration', EmbeddedActivityConfiguration
)


# eula_id

parse_eula_id = entity_id_parser_factory('eula_id')
put_eula_id_into = entity_id_optional_putter_factory('eula_id')
validate_eula_id = entity_id_validator_factory('eula_id', EULA)


# event_webhook_event_types

parse_event_webhook_event_types = preinstanced_array_parser_factory(
    'event_webhooks_types', ApplicationEventWebhookEventType
)
put_event_webhook_event_types_into = preinstanced_array_putter_factory('event_webhooks_types')
validate_event_webhook_event_types = preinstanced_array_validator_factory(
    'event_webhook_event_types', ApplicationEventWebhookEventType
)


# event_webhook_state

parse_event_webhook_state = preinstanced_parser_factory(
    'event_webhooks_status', ApplicationEventWebhookState, ApplicationEventWebhookState.none
)
put_event_webhook_state_into = preinstanced_putter_factory('event_webhooks_status')
validate_event_webhook_state = preinstanced_validator_factory(
    'event_webhook_state', ApplicationEventWebhookState
)


# event_webhook_url

parse_event_webhook_url = nullable_string_parser_factory('event_webhooks_url')
put_event_webhook_url_into = url_optional_putter_factory('event_webhooks_url')
validate_event_webhook_url = url_optional_validator_factory('event_webhook_url')


# executables

parse_executables = nullable_entity_array_parser_factory('executables', ApplicationExecutable)
put_executables_into = nullable_entity_array_putter_factory('executables', ApplicationExecutable)
validate_executables = nullable_entity_array_validator_factory('executables', ApplicationExecutable)


# explicit_content_filter_level

parse_explicit_content_filter_level = preinstanced_parser_factory(
    'explicit_content_filter', ApplicationExplicitContentFilterLevel, ApplicationExplicitContentFilterLevel.none
)
put_explicit_content_filter_level_into = preinstanced_putter_factory('explicit_content_filter')
validate_explicit_content_filter_level = preinstanced_validator_factory(
    'explicit_content_filter_level', ApplicationExplicitContentFilterLevel
)


# flags

parse_flags = flag_parser_factory('flags', ApplicationFlag)
put_flags_into = flag_optional_putter_factory('flags', ApplicationFlag())
validate_flags = flag_validator_factory('flags', ApplicationFlag)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)

# hook

parse_hook = bool_parser_factory('hook', HOOK_DEFAULT)
put_hook_into = bool_optional_putter_factory('hook', HOOK_DEFAULT)
validate_hook = bool_validator_factory('hook', HOOK_DEFAULT)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('application_id')

# install_parameters

parse_install_parameters = nullable_entity_parser_factory('install_params', ApplicationInstallParameters)
put_install_parameters_into = nullable_entity_optional_putter_factory('install_params', ApplicationInstallParameters)
validate_install_parameters = nullable_entity_validator_factory('install_parameters', ApplicationInstallParameters)


# integration_public

parse_integration_public = bool_parser_factory('integration_public', INTEGRATION_PUBLIC_DEFAULT)
put_integration_public_into = bool_optional_putter_factory('integration_public', INTEGRATION_PUBLIC_DEFAULT)
validate_integration_public = bool_validator_factory('integration_public', INTEGRATION_PUBLIC_DEFAULT)


# integration_requires_code_grant

parse_integration_requires_code_grant = bool_parser_factory(
    'integration_require_code_grant', INTEGRATION_REQUIRES_CODE_GRANT_DEFAULT
)
put_integration_requires_code_grant_into = bool_optional_putter_factory(
    'integration_require_code_grant', INTEGRATION_REQUIRES_CODE_GRANT_DEFAULT
)
validate_integration_requires_code_grant = bool_validator_factory(
    'integration_requires_code_grant', INTEGRATION_REQUIRES_CODE_GRANT_DEFAULT
)

# integration_types

parse_integration_types = preinstanced_array_parser_factory('integration_types', ApplicationIntegrationType)
put_integration_types_into = preinstanced_array_putter_factory('integration_types')
validate_integration_types = preinstanced_array_validator_factory('integration_types', ApplicationIntegrationType)


# integration_types_configuration

def parse_integration_types_configuration(data):
    """
    Parses application integration types configuration.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    integration_types_configuration : `None | dict<ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration>`
    """
    configurations_data = data.get('integration_types_config', None)
    if (configurations_data is None) or (not configurations_data):
        return None
    
    integration_types_configuration = {}
    for key, value in configurations_data.items():
        integration_type = ApplicationIntegrationType.get(ApplicationIntegrationType.VALUE_TYPE(key))
        integration_type_configuration = ApplicationIntegrationTypeConfiguration.from_data(value)
        integration_types_configuration[integration_type] = integration_type_configuration
    
    return integration_types_configuration


def put_integration_types_configuration_into(integration_types_configuration, data, defaults):
    """
    Puts the application's owner data into the given `data` json serializable object.
    
    Parameters
    ----------
    integration_types_configuration : `None | dict<ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration>`
        Integration types configuration to serialize.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    configurations_data = {}
    
    if (integration_types_configuration is not None):
        for integration_type, integration_type_configuration in integration_types_configuration.items():
            key = str(integration_type.value)
            value = integration_type_configuration.to_data(defaults = defaults)
            configurations_data[key] = value 
    
    data['integration_types_config'] = configurations_data
    return data


def validate_integration_types_configuration(integration_types_configuration):
    """
    Validates the given `integration_types_configuration` value.
    
    Parameters
    ----------
    integration_types_configuration : \
            `None | dict<ApplicationIntegrationType | int, ApplicationIntegrationTypeConfiguration>`
        Integration types configuration to validate.
    
    Returns
    -------
    integration_types_configuration : `None | dict<ApplicationIntegrationType, ApplicationIntegrationTypeConfiguration>`
    
    Raises
    ------
    TypeError
        - If `integration_types_configuration`'s type is invalid.
    """
    if integration_types_configuration is None:
        return None
    
    if not isinstance(integration_types_configuration, dict):
        raise TypeError(
            f'`integration_types_configuration` can be `None`,'
            f'`dict<{ApplicationIntegrationType.__name__} | {ApplicationIntegrationType.VALUE_TYPE.__name__}, '
            f'{ApplicationIntegrationTypeConfiguration.__name__}`, got '
            f'{type(integration_types_configuration).__name__}; {integration_types_configuration!r}.'
        )
    
    if not integration_types_configuration:
        return None
    
    validated_integration_types_configuration = {}
    
    for key, value in integration_types_configuration.items():
        if isinstance(key, ApplicationIntegrationType):
            integration_type = key
        
        elif isinstance(key, ApplicationIntegrationType.VALUE_TYPE):
            integration_type = ApplicationIntegrationType.get(key)
        
        else:
            raise TypeError(
                f'`integration_types_configuration` keys can be '
                f'`{ApplicationIntegrationType.__name__}`, `{ApplicationIntegrationType.VALUE_TYPE.__name__}`, '
                f'got {type(key).__name__}; {key!r}; '
                f'integration_types_configuration = {integration_types_configuration!r}.'
            )
        
        if isinstance(value, ApplicationIntegrationTypeConfiguration):
            integration_type_configuration = value
        
        else:
            raise TypeError(
                f'`integration_types_configuration` values can be `{ApplicationIntegrationTypeConfiguration.__name__}`, '
                f'got {type(value).__name__}; {value!r}; '
                f'integration_types_configuration = {integration_types_configuration!r}.'
            )
        
        validated_integration_types_configuration[integration_type] = integration_type_configuration
    
    return validated_integration_types_configuration


# interaction_endpoint_url

parse_interaction_endpoint_url = nullable_string_parser_factory('interactions_endpoint_url')
put_interaction_endpoint_url_into = url_optional_putter_factory('interactions_endpoint_url')
validate_interaction_endpoint_url = url_optional_validator_factory('interaction_endpoint_url')


# interaction_event_types

parse_interaction_event_types = preinstanced_array_parser_factory(
    'interactions_event_types', ApplicationInteractionEventType
)
put_interaction_event_types_into = preinstanced_array_putter_factory('interactions_event_types')
validate_interaction_event_types = preinstanced_array_validator_factory(
    'interaction_event_types', ApplicationInteractionEventType
)

# interaction_version

parse_interaction_version = preinstanced_parser_factory(
    'interactions_version', ApplicationInteractionVersion, ApplicationInteractionVersion.none
)
put_interaction_version_into = preinstanced_putter_factory('interactions_version')
validate_interaction_version = preinstanced_validator_factory('interaction_version', ApplicationInteractionVersion)


# internal_guild_restriction

parse_internal_guild_restriction = preinstanced_parser_factory(
    'internal_guild_restriction', ApplicationInternalGuildRestriction, ApplicationInternalGuildRestriction.none
)
put_internal_guild_restriction_into = preinstanced_putter_factory('internal_guild_restriction')
validate_internal_guild_restriction = preinstanced_validator_factory(
    'internal_guild_restriction', ApplicationInternalGuildRestriction
)

# max_participants

parse_max_participants = int_postprocess_parser_factory(
    'max_participants',
    MAX_PARTICIPANTS_DEFAULT,
    (lambda max_participants: MAX_PARTICIPANTS_DEFAULT if max_participants == -1 else max_participants),
)
put_max_participants_into = int_optional_postprocess_putter_factory(
    'max_participants',
    MAX_PARTICIPANTS_DEFAULT,   
    (lambda max_participants: -1 if max_participants == MAX_PARTICIPANTS_DEFAULT else max_participants),
)
validate_max_participants = int_conditional_validator_factory(
    'max_participants',
    MAX_PARTICIPANTS_DEFAULT,
    (lambda width : width >= 0),
    '>= 0',
)


# monetization_eligibility_flags

parse_monetization_eligibility_flags = flag_parser_factory(
    'monetization_eligibility_flags', ApplicationMonetizationEligibilityFlags
)
put_monetization_eligibility_flags_into = flag_optional_putter_factory(
    'monetization_eligibility_flags', ApplicationMonetizationEligibilityFlags()
)
validate_monetization_eligibility_flags = flag_validator_factory(
    'monetization_eligibility_flags', ApplicationMonetizationEligibilityFlags
)


# monetization_state

parse_monetization_state = preinstanced_parser_factory(
    'monetization_state', ApplicationMonetizationState, ApplicationMonetizationState.none
)
put_monetization_state_into = preinstanced_putter_factory('monetization_state')
validate_monetization_state = preinstanced_validator_factory(
    'monetization_state', ApplicationMonetizationState
)


# monetized

parse_monetized = bool_parser_factory('is_monetized', False)
put_monetized_into = bool_optional_putter_factory('is_monetized', False)
validate_monetized = bool_validator_factory('monetized', False)

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# overlay

parse_overlay = bool_parser_factory('overlay', OVERLAY_DEFAULT)
put_overlay_into = bool_optional_putter_factory('overlay', OVERLAY_DEFAULT)
validate_overlay = bool_validator_factory('overlay', OVERLAY_DEFAULT)

# overlay_compatibility_hook

parse_overlay_compatibility_hook = bool_parser_factory('overlay_compatibility_hook', OVERLAY_COMPATIBILITY_HOOK_DEFAULT)
put_overlay_compatibility_hook_into = bool_optional_putter_factory(
    'overlay_compatibility_hook', OVERLAY_COMPATIBILITY_HOOK_DEFAULT
)
validate_overlay_compatibility_hook = bool_validator_factory(
    'overlay_compatibility_hook', OVERLAY_COMPATIBILITY_HOOK_DEFAULT
)

# overlay_method_flags

parse_overlay_method_flags = flag_parser_factory('overlay_methods', ApplicationOverlayMethodFlags)
put_overlay_method_flags_into = flag_optional_putter_factory('overlay_methods', ApplicationOverlayMethodFlags())
validate_overlay_method_flags = flag_validator_factory('overlay_method_flags', ApplicationOverlayMethodFlags)

# owner

def parse_owner(data):
    """
    Parses the application owner.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Application data.
    
    Returns
    -------
    owner : ``ClientUserBase``, ``Team``
    """
    team_data = data.get('team', None)
    if team_data is None:
        user_data = data.get('owner', None)
        if user_data is None:
            owner = ZEROUSER
        else:
            owner = User.from_data(user_data)
    else:
        owner = Team.from_data(team_data)
    
    return owner


def put_owner_into(owner, data, defaults):
    """
    Puts the application's owner data into the given `data` json serializable object.
    
    Parameters
    ----------
    owner : ``ClientUserBase``, ``Team``
        The application's owner.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if owner is ZEROUSER:
        team_data = None
        user_data = None
    
    elif isinstance(owner, ClientUserBase):
        team_data = None
        user_data = owner.to_data(defaults = defaults, include_internals = True)
        
    elif isinstance(owner, Team):
        team_data = owner.to_data(defaults = defaults, include_internals = True)
        user_data = owner.to_data_user()
    
    else:
        team_data = None
        user_data = None
    
    if (team_data is not None) or defaults:
        data['team'] = team_data
    
    if (user_data is not None) or defaults:
        data['owner'] = user_data
    
    return data


def validate_owner(owner):
    """
    Validates the given application owner.
    
    Parameters
    ----------
    owner : `None`, ``ClientUserBase``, ``Team``
        The application's owner.
    
    Returns
    -------
    owner : ``ClientUserBase``, ``Team``
    
    Raises
    ------
    TypeError
        - If `owner`'s type is incorrect.
    """
    if owner is None:
        owner = ZEROUSER
    
    elif not isinstance(owner, (ClientUserBase, Team)):
        raise TypeError(
            f'`owner` can be `None`, `{ClientUserBase.__name__}`, {Team.__name__}, '
            f'got {type(owner).__name__}; {owner!r}'
        )
    
    return owner

# primary_sku_id

parse_primary_sku_id = entity_id_parser_factory('primary_sku_id')
put_primary_sku_id_into = entity_id_optional_putter_factory('primary_sku_id')
validate_primary_sku_id = entity_id_validator_factory('primary_sku_id')

# privacy_policy_url

parse_privacy_policy_url = nullable_string_parser_factory('privacy_policy_url')
put_privacy_policy_url_into = url_optional_putter_factory('privacy_policy_url')
validate_privacy_policy_url = url_optional_validator_factory('privacy_policy_url')

# publishers

parse_publishers = nullable_entity_array_parser_factory('publishers', ApplicationEntity)
put_publishers_into = nullable_entity_array_putter_factory('publishers', ApplicationEntity)
validate_publishers = nullable_entity_array_validator_factory('publishers', ApplicationEntity)

# redirect_urls

def parse_redirect_urls(data):
    """
    Parses out `redirect_urls` value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<str>`
    """
    string_array = data.get('redirect_uris', None)
    if string_array is None:
        return None
    
    parsed_values = None
    
    for string in string_array:
        if string is None:
            continue
        
        if parsed_values is None:
            parsed_values = []
        
        parsed_values.append(string)
    
    if parsed_values is None:
        return None
    
    parsed_values.sort()
    return tuple(parsed_values)


put_redirect_urls_into = nullable_string_array_optional_putter_factory('redirect_uris')
validate_redirect_urls = nullable_string_array_validator_factory('redirect_urls')
 

# role_connection_verification_url

parse_role_connection_verification_url = nullable_string_parser_factory('role_connections_verification_url')
put_role_connection_verification_url_into = url_optional_putter_factory('role_connections_verification_url')
validate_role_connection_verification_url = url_optional_validator_factory('role_connection_verification_url')

# rpc_origins

parse_rpc_origins = nullable_array_parser_factory('rpc_origins')
put_rpc_origins_into = nullable_string_array_optional_putter_factory('rpc_origins')
validate_rpc_origins = url_array_optional_validator_factory('rpc_origins')


# rpc_state

parse_rpc_state = preinstanced_parser_factory('rpc_application_state', ApplicationRPCState, ApplicationRPCState.none)
put_rpc_state_into = preinstanced_putter_factory('rpc_application_state')
validate_rpc_state = preinstanced_validator_factory('rpc_state', ApplicationRPCState)

# slug

parse_slug = nullable_string_parser_factory('slug')
put_slug_into = url_optional_putter_factory('slug')
validate_slug = url_optional_validator_factory('slug')

# store_state

parse_store_state = preinstanced_parser_factory(
    'store_application_state', ApplicationStoreState, ApplicationStoreState.none
)
put_store_state_into = preinstanced_putter_factory('store_application_state')
validate_store_state = preinstanced_validator_factory('store_state', ApplicationStoreState)

# tags

parse_tags = nullable_array_parser_factory('tags')
put_tags_into = nullable_string_array_optional_putter_factory('tags')
validate_tags = nullable_string_array_validator_factory('tags')

# terms_of_service_url

parse_terms_of_service_url = nullable_string_parser_factory('terms_of_service_url')
put_terms_of_service_url_into = url_optional_putter_factory('terms_of_service_url')
validate_terms_of_service_url = url_optional_validator_factory('terms_of_service_url')

# third_party_skus

parse_third_party_skus = nullable_entity_array_parser_factory('third_party_skus', ThirdPartySKU)
put_third_party_skus_into = nullable_entity_array_putter_factory('third_party_skus', ThirdPartySKU)
validate_third_party_skus = nullable_entity_array_validator_factory('third_party_skus', ThirdPartySKU)

# type

parse_type = preinstanced_parser_factory('type', ApplicationType, ApplicationType.none)


def put_type_into(application_type, data, defaults):
    """
    Puts the application's type into the given `data` json serializable object.
    
    Parameters
    ----------
    application_type : ``ApplicationType``
        The application's type.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    if application_type is ApplicationType.none:
        value = None
    else:
        value = application_type.value
    
    data['type'] = value
    return data


validate_type = preinstanced_validator_factory('application_type', ApplicationType)


# verification_state

parse_verification_state = preinstanced_parser_factory(
    'verification_state', ApplicationVerificationState, ApplicationVerificationState.none
)
put_verification_state_into = preinstanced_putter_factory('verification_state')
validate_verification_state = preinstanced_validator_factory('verification_state', ApplicationVerificationState)


# verify_key

parse_verify_key = nullable_string_parser_factory('verify_key')
put_verify_key_into = nullable_string_putter_factory('verify_key')
validate_verify_key = nullable_string_validator_factory('verify_key', 0, 1024)
