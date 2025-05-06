from warnings import catch_warnings, simplefilter as apply_simple_filter

import vampytest

from ....bases import Icon, IconType
from ....permission import Permission
from ....user import User

from ...application_entity import ApplicationEntity
from ...application_executable import ApplicationExecutable
from ...application_install_parameters import ApplicationInstallParameters
from ...application_integration_type_configuration import ApplicationIntegrationTypeConfiguration
from ...embedded_activity_configuration import EmbeddedActivityConfiguration
from ...third_party_sku import ThirdPartySKU

from ..application import Application
from ..flags import (
    ApplicationDiscoveryEligibilityFlags, ApplicationFlag, ApplicationMonetizationEligibilityFlags,
    ApplicationOverlayMethodFlags
)
from ..preinstanced import (
    ApplicationDiscoverabilityState, ApplicationEventWebhookEventType, ApplicationEventWebhookState,
    ApplicationExplicitContentFilterLevel, ApplicationIntegrationType, ApplicationInteractionEventType,
    ApplicationInteractionVersion, ApplicationInternalGuildRestriction, ApplicationMonetizationState,
    ApplicationRPCState, ApplicationStoreState, ApplicationType, ApplicationVerificationState
)

from .test__Application__constructor import _assert_fields_set


def test__Application__from_data__warning_and_attributes():
    """
    Tests whether `Application.from_data`` works as intended.
    
    Case: Warning & attributes.
    """
    application_id = 202211290015
    
    data = {
        'id': str(application_id),
    }
    
    with catch_warnings(record = True) as warnings:
        apply_simple_filter('always')
        
        application = Application.from_data(data)
        _assert_fields_set(application)
        vampytest.assert_eq(application.id, application_id)
        
        vampytest.assert_eq(len(warnings), 1)


def test__Application__from_data__caching():
    """
    Tests whether `Application.from_data`` works as intended.
    
    Case: Caching.
    """
    application_id = 202211290016
    
    data = {
        'id': application_id,
    }
    
    with catch_warnings():
        apply_simple_filter('ignore')
        
        application = Application.from_data(data)
        test_application = Application.from_data(data)
        
        vampytest.assert_is(application, test_application)


def test__Application__from_data_ready__attributes():
    """
    Tests whether ``Application.from_data_ready`` works as intended.
    
    Case: Attributes.
    """
    application_id = 202211290017
    flags = ApplicationFlag(96)
    
    data = {
        'id': str(application_id),
        'flags': int(flags),
    }
    
    application = Application.from_data_ready(data)
    _assert_fields_set(application)
    vampytest.assert_eq(application.id, application_id)
    
    vampytest.assert_eq(application.flags, flags)


def test__Application__from_data_ready__caching():
    """
    Tests whether ``Application.from_data_ready`` works as intended.
    
    Case: Caching.
    """
    application_id = 202211290018
    
    data = {
        'id': str(application_id),
    }
    
    application = Application.from_data_ready(data)
    test_application = Application.from_data_ready(data)
    
    vampytest.assert_is(application, test_application)


def test__Application__from_data_ready__overwriting_partial():
    """
    Tests whether ``Application.from_data_ready`` works as intended.
    
    Case: Overwriting partial.
    """
    application_id = 202211290026
    
    data = {
        'id': str(application_id),
    }
    
    application = Application()
    test_application = application.from_data_ready(data)
    vampytest.assert_is(application, test_application)


def test__Application__from_data_ready__overwriting_full():
    """
    Tests whether ``Application.from_data_ready`` works as intended.
    
    Case: Overwriting full.
    """
    application_id_1 = 202211290027
    application_id_2 = 202211290028
    
    data = {
        'id': str(application_id_2),
    }
    
    application = Application.precreate(application_id_1)
    test_application = application.from_data_ready(data)
    vampytest.assert_is_not(application, test_application)


def test__Application__from_data_own__attributes():
    """
    Tests whether ``Application.from_data_own`` works as intended.
    
    Case: Attributes.
    """
    application_id = 202211290019
    
    approximate_guild_count = 11
    approximate_user_install_count = 13
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    description = 'dancing'
    flags = ApplicationFlag(96)
    hook = True
    icon = Icon(IconType.static, 12)
    name = 'Kaenbyou Rin'
    privacy_policy_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    splash = Icon(IconType.static, 66)
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    application_type = ApplicationType.game
    verify_key = 'hell'
    
    creator_monetization_state = ApplicationMonetizationState.disabled
    custom_install_url = 'https://orindance.party/'
    developers = [ApplicationEntity.precreate(202312030000, name = 'BrainDead')]
    discoverability_state = ApplicationDiscoverabilityState.blocked
    discovery_eligibility_flags = ApplicationDiscoveryEligibilityFlags(9)
    event_webhook_event_types = [
        ApplicationEventWebhookEventType.application_authorization,
        ApplicationEventWebhookEventType.entitlement_create
    ]
    event_webhook_state = ApplicationEventWebhookState.enabled
    event_webhook_url = 'https://orindance.party/event-webhook'
    explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    guild_id = 202211290020
    install_parameters = ApplicationInstallParameters(permissions = 8)
    integration_public = True
    integration_requires_code_grant = True
    integration_types = [ApplicationIntegrationType.user_install]
    integration_types_configuration = {
        ApplicationIntegrationType.user_install: ApplicationIntegrationTypeConfiguration(
            install_parameters = ApplicationInstallParameters(permissions = 8),
        ),
        ApplicationIntegrationType.guild_install: ApplicationIntegrationTypeConfiguration(
            install_parameters = ApplicationInstallParameters(permissions = 123),
        ),
    }
    interaction_endpoint_url = 'https://orindance.party/'
    interaction_event_types = [ApplicationInteractionEventType.none]
    interaction_version = ApplicationInteractionVersion.selective
    internal_guild_restriction = ApplicationInternalGuildRestriction.restricted
    monetization_eligibility_flags = ApplicationMonetizationEligibilityFlags(17)
    monetization_state = ApplicationMonetizationState.disabled
    monetized = True
    owner = User.precreate(202211290021)
    primary_sku_id = 202211290022
    publishers = [ApplicationEntity.precreate(202312040000, name = 'Brain')]
    redirect_urls = ['https://orindance.party/']
    role_connection_verification_url = 'https://orindance.party/'
    rpc_state = ApplicationRPCState.approved
    slug = 'https://orindance.party/'
    store_state = ApplicationStoreState.approved
    verification_state = ApplicationVerificationState.approved
    
    data = {
        'id': str(application_id),
        'approximate_guild_count': approximate_guild_count,
        'approximate_user_install_count': approximate_user_install_count,
        'bot_public': bot_public,
        'bot_require_code_grant': bot_requires_code_grant,
        'cover_image': cover.as_base_16_hash,
        'description': description,
        'flags': int(flags),
        'hook': hook,
        'icon': icon.as_base_16_hash,
        'name': name,
        'privacy_policy_url': privacy_policy_url,
        'rpc_origins': rpc_origins,
        'splash': splash.as_base_16_hash,
        'tags': tags,
        'terms_of_service_url': terms_of_service_url,
        'type': application_type.value,
        'verify_key': verify_key,
        
        'creator_monetization_state': creator_monetization_state.value,
        'custom_install_url': custom_install_url,
        'developers': [developer.to_data(defaults = True, include_internals = True) for developer in developers],
        'discoverability_state': discoverability_state.value,
        'discovery_eligibility_flags': int(discovery_eligibility_flags),
        'event_webhooks_types': [
            event_webhook_event_type.value for event_webhook_event_type in event_webhook_event_types
        ], 
        'event_webhooks_status': event_webhook_state.value,
        'event_webhooks_url': event_webhook_url,
        'explicit_content_filter': explicit_content_filter_level.value,
        'guild_id': str(guild_id),
        'install_params': install_parameters.to_data(defaults = True),
        'integration_public': integration_public,
        'integration_require_code_grant': integration_requires_code_grant,
        'integration_types': [integration_type.value for integration_type in integration_types],
        'integration_types_config': {
            str(integration_type.value) : integration_type_configuration.to_data()
            for integration_type, integration_type_configuration
            in integration_types_configuration.items()
        },
        'interactions_endpoint_url': interaction_endpoint_url,
        'interactions_event_types': [
            interaction_event_type.value for interaction_event_type in interaction_event_types
        ],
        'interactions_version': interaction_version.value,
        'internal_guild_restriction': internal_guild_restriction.value,
        'monetization_eligibility_flags': int(monetization_eligibility_flags),
        'monetization_state': monetization_state.value,
        'is_monetized': monetized,
        'owner': owner.to_data(defaults = True, include_internals = True),
        'team': None,
        'primary_sku_id': str(primary_sku_id),
        'publishers': [publisher.to_data(defaults = True, include_internals = True) for publisher in publishers],
        'redirect_uris': redirect_urls,
        'role_connections_verification_url': role_connection_verification_url,
        'rpc_application_state': rpc_state.value,
        'slug': slug,
        'store_application_state': store_state.value,
        'verification_state': verification_state.value,
    }
    
    application = Application.from_data_own(data)
    _assert_fields_set(application)
    vampytest.assert_eq(application.id, application_id)
    
    vampytest.assert_eq(application.approximate_guild_count, approximate_guild_count)
    vampytest.assert_eq(application.approximate_user_install_count, approximate_user_install_count)
    vampytest.assert_eq(application.bot_public, bot_public)
    vampytest.assert_eq(application.bot_requires_code_grant, bot_requires_code_grant)
    vampytest.assert_eq(application.cover, cover)
    vampytest.assert_is(application.creator_monetization_state, creator_monetization_state)
    vampytest.assert_eq(application.custom_install_url, custom_install_url)
    vampytest.assert_is(application.discoverability_state, discoverability_state)
    vampytest.assert_eq(application.discovery_eligibility_flags, discovery_eligibility_flags)
    vampytest.assert_eq(application.description, description)
    vampytest.assert_eq(application.developers, tuple(developers))
    vampytest.assert_eq(application.event_webhook_event_types, tuple(event_webhook_event_types))
    vampytest.assert_is(application.event_webhook_state, event_webhook_state)
    vampytest.assert_eq(application.event_webhook_url, event_webhook_url)
    vampytest.assert_is(application.explicit_content_filter_level, explicit_content_filter_level)
    vampytest.assert_eq(application.flags, flags)
    vampytest.assert_eq(application.guild_id, guild_id)
    vampytest.assert_eq(application.hook, hook)
    vampytest.assert_eq(application.icon, icon)
    vampytest.assert_eq(application.install_parameters, install_parameters)
    vampytest.assert_eq(application.integration_public, integration_public)
    vampytest.assert_eq(application.integration_requires_code_grant, integration_requires_code_grant)
    vampytest.assert_eq(application.integration_types, tuple(integration_types))
    vampytest.assert_eq(application.integration_types_configuration, integration_types_configuration)
    vampytest.assert_eq(application.interaction_endpoint_url, interaction_endpoint_url)
    vampytest.assert_eq(application.interaction_event_types, tuple(interaction_event_types))
    vampytest.assert_is(application.interaction_version, interaction_version)
    vampytest.assert_is(application.internal_guild_restriction, internal_guild_restriction)
    vampytest.assert_eq(application.monetization_eligibility_flags, monetization_eligibility_flags)
    vampytest.assert_is(application.monetization_state, monetization_state)
    vampytest.assert_eq(application.monetized, monetized)
    vampytest.assert_eq(application.name, name)
    vampytest.assert_eq(application.owner, owner)
    vampytest.assert_eq(application.primary_sku_id, primary_sku_id)
    vampytest.assert_eq(application.privacy_policy_url, privacy_policy_url)
    vampytest.assert_eq(application.publishers, tuple(publishers))
    vampytest.assert_eq(application.redirect_urls, tuple(redirect_urls))
    vampytest.assert_eq(application.role_connection_verification_url, role_connection_verification_url)
    vampytest.assert_eq(application.rpc_origins, tuple(rpc_origins))
    vampytest.assert_is(application.rpc_state, rpc_state)
    vampytest.assert_eq(application.slug, slug)
    vampytest.assert_eq(application.splash, splash)
    vampytest.assert_is(application.store_state, store_state)
    vampytest.assert_eq(application.tags, tuple(tags))
    vampytest.assert_eq(application.terms_of_service_url, terms_of_service_url)
    vampytest.assert_is(application.type, application_type)
    vampytest.assert_eq(application.verify_key, verify_key)
    vampytest.assert_is(application.verification_state, verification_state)


def test__Application__from_data_own__caching():
    """
    Tests whether ``Application.from_data_own`` works as intended.
    
    Case: Caching.
    """
    application_id = 202211290023
    
    data = {
        'id': str(application_id),
    }
    
    application = Application.from_data_own(data)
    test_application = Application.from_data_own(data)
    
    vampytest.assert_is(application, test_application)


def test__Application__from_data_own__overwriting_partial():
    """
    Tests whether ``Application.from_data_own`` works as intended.
    
    Case: Overwriting partial.
    """
    application_id = 202211290029
    
    data = {
        'id': str(application_id),
    }
    
    application = Application()
    test_application = application.from_data_own(data)
    vampytest.assert_is(application, test_application)


def test__Application__from_data_own__overwriting_full():
    """
    Tests whether ``Application.from_data_own`` works as intended.
    
    Case: Overwriting full.
    """
    application_id_1 = 202211290030
    application_id_2 = 202211290031
    
    data = {
        'id': str(application_id_2),
    }
    
    application = Application.precreate(application_id_1)
    test_application = application.from_data_own(data)
    vampytest.assert_is_not(application, test_application)


def test__Application__from_data_invite__attributes():
    """
    Tests whether ``Application.from_data_invite`` works as intended.
    
    Case: Attributes.
    """
    application_id = 202211290024
    
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    description = 'dancing'
    flags = ApplicationFlag(96)
    hook = True
    icon = Icon(IconType.static, 12)
    name = 'Kaenbyou Rin'
    privacy_policy_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    splash = Icon(IconType.static, 66)
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    application_type = ApplicationType.game
    verify_key = 'hell'
    
    embedded_activity_configuration = EmbeddedActivityConfiguration(position = 6)
    max_participants = 23
    monetized = True
    
    data = {
        'id': str(application_id),
        'bot_public': bot_public,
        'bot_require_code_grant': bot_requires_code_grant,
        'cover_image': cover.as_base_16_hash,
        'description': description,
        'flags': int(flags),
        'hook': hook,
        'icon': icon.as_base_16_hash,
        'name': name,
        'privacy_policy_url': privacy_policy_url,
        'rpc_origins': rpc_origins,
        'splash': splash.as_base_16_hash,
        'tags': tags,
        'terms_of_service_url': terms_of_service_url,
        'type': application_type.value,
        'verify_key': verify_key,
        
        'embedded_activity_config': embedded_activity_configuration.to_data(),
        'max_participants': max_participants,
        'is_monetized': monetized,
    }
    
    application = Application.from_data_invite(data)
    _assert_fields_set(application)
    vampytest.assert_eq(application.id, application_id)
    
    vampytest.assert_eq(application.bot_public, bot_public)
    vampytest.assert_eq(application.bot_requires_code_grant, bot_requires_code_grant)
    vampytest.assert_eq(application.cover, cover)
    vampytest.assert_eq(application.description, description)
    vampytest.assert_eq(application.embedded_activity_configuration, embedded_activity_configuration)
    vampytest.assert_eq(application.flags, flags)
    vampytest.assert_eq(application.hook, hook)
    vampytest.assert_eq(application.icon, icon)
    vampytest.assert_eq(application.max_participants, max_participants)
    vampytest.assert_eq(application.monetized, monetized)
    vampytest.assert_eq(application.name, name)
    vampytest.assert_eq(application.privacy_policy_url, privacy_policy_url)
    vampytest.assert_eq(application.rpc_origins, tuple(rpc_origins))
    vampytest.assert_eq(application.splash, splash)
    vampytest.assert_eq(application.tags, tuple(tags))
    vampytest.assert_eq(application.terms_of_service_url, terms_of_service_url)
    vampytest.assert_is(application.type, application_type)
    vampytest.assert_eq(application.verify_key, verify_key)


def test__Application__from_data_invite__caching():
    """
    Tests whether ``Application.from_data_invite`` works as intended.
    
    Case: Caching.
    """
    application_id = 202211290025
    
    data = {
        'id': str(application_id),
    }
    
    application = Application.from_data_invite(data)
    test_application = Application.from_data_invite(data)
    
    vampytest.assert_is(application, test_application)


def test__Application__from_data_detectable__attributes():
    """
    Tests whether ``Application.from_data_detectable`` works as intended.
    
    Case: Attributes.
    """
    application_id = 202211290032
    
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    description = 'dancing'
    flags = ApplicationFlag(96)
    hook = True
    icon = Icon(IconType.static, 12)
    name = 'Kaenbyou Rin'
    privacy_policy_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    splash = Icon(IconType.static, 66)
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    application_type = ApplicationType.game
    verify_key = 'hell'
    
    aliases = ['orin', 'rin']
    deeplink_url = 'https://orindance.party/'
    developers = [ApplicationEntity.precreate(202211290033, name = 'BrainDead')]
    eula_id = 202211290034
    executables = [ApplicationExecutable(name = 'Okuu')]
    guild_id = 202211290035
    overlay = True
    overlay_compatibility_hook = True
    overlay_method_flags = ApplicationOverlayMethodFlags(26)
    primary_sku_id = 202211290036
    publishers = [ApplicationEntity.precreate(202211290037, name = 'Brain')]
    slug = 'https://orindance.party/'
    third_party_skus = [ThirdPartySKU(distributor = 'Dead')]
    
    data = {
        'id': str(application_id),
        'bot_public': bot_public,
        'bot_require_code_grant': bot_requires_code_grant,
        'cover_image': cover.as_base_16_hash,
        'description': description,
        'flags': int(flags),
        'hook': hook,
        'icon': icon.as_base_16_hash,
        'name': name,
        'privacy_policy_url': privacy_policy_url,
        'rpc_origins': rpc_origins,
        'splash': splash.as_base_16_hash,
        'tags': tags,
        'terms_of_service_url': terms_of_service_url,
        'type': application_type.value,
        'verify_key': verify_key,
        
        'aliases': aliases,
        'deeplink_uri': deeplink_url,
        'developers': [developer.to_data(defaults = True, include_internals = True) for developer in developers],
        'eula_id': str(eula_id),
        'executables': [executable.to_data(defaults = True) for executable in executables],
        'guild_id': str(guild_id),
        'overlay': overlay,
        'overlay_compatibility_hook': overlay_compatibility_hook,
        'overlay_methods': int(overlay_method_flags),
        'primary_sku_id': str(primary_sku_id),
        'publishers': [publisher.to_data(defaults = True, include_internals = True) for publisher in publishers],
        'slug': slug,
        'third_party_skus': [third_party_sku.to_data(defaults = True) for third_party_sku in third_party_skus]
    }
    
    application = Application.from_data_detectable(data)
    _assert_fields_set(application)
    vampytest.assert_eq(application.id, application_id)
    
    vampytest.assert_eq(application.aliases, tuple(aliases))
    vampytest.assert_eq(application.bot_public, bot_public)
    vampytest.assert_eq(application.bot_requires_code_grant, bot_requires_code_grant)
    vampytest.assert_eq(application.cover, cover)
    vampytest.assert_eq(application.deeplink_url, deeplink_url)
    vampytest.assert_eq(application.description, description)
    vampytest.assert_eq(application.developers, tuple(developers))
    vampytest.assert_eq(application.eula_id, eula_id)
    vampytest.assert_eq(application.executables, tuple(executables))
    vampytest.assert_eq(application.flags, flags)
    vampytest.assert_eq(application.guild_id, guild_id)
    vampytest.assert_eq(application.hook, hook)
    vampytest.assert_eq(application.icon, icon)
    vampytest.assert_eq(application.name, name)
    vampytest.assert_eq(application.overlay, overlay)
    vampytest.assert_eq(application.overlay_compatibility_hook, overlay_compatibility_hook)
    vampytest.assert_eq(application.overlay_method_flags, overlay_method_flags)
    vampytest.assert_eq(application.primary_sku_id, primary_sku_id)
    vampytest.assert_eq(application.privacy_policy_url, privacy_policy_url)
    vampytest.assert_eq(application.publishers, tuple(publishers))
    vampytest.assert_eq(application.rpc_origins, tuple(rpc_origins))
    vampytest.assert_eq(application.slug, slug)
    vampytest.assert_eq(application.splash, splash)
    vampytest.assert_eq(application.tags, tuple(tags))
    vampytest.assert_eq(application.terms_of_service_url, terms_of_service_url)
    vampytest.assert_eq(application.third_party_skus, tuple(third_party_skus))
    vampytest.assert_is(application.type, application_type)
    vampytest.assert_eq(application.verify_key, verify_key)


def test__Application__from_data_detectable__caching():
    """
    Tests whether ``Application.from_data_detectable`` works as intended.
    
    Case: Caching.
    """
    application_id = 202211290038
    
    data = {
        'id': str(application_id),
    }
    
    application = Application.from_data_detectable(data)
    test_application = Application.from_data_detectable(data)
    
    vampytest.assert_is(application, test_application)


def test__Application__to_data__include_internals():
    """
    Tests whether `Application.to_data`` works as intended.
    
    Case: warning & defaults & internals
    """
    application_id = 202211290039
    
    application = Application.precreate(
        application_id,
    )
    
    with catch_warnings(record = True) as warnings:
        apply_simple_filter('always')
        
        data = application.to_data(defaults = True, include_internals = True)
        
        vampytest.assert_eq(len(warnings), 1)
    
    vampytest.assert_in('id', data)
    vampytest.assert_eq(data['id'], str(application_id))


def test__Application__to_data__default():
    """
    Tests whether `Application.to_data`` works as intended.
    
    Case: defaults
    """
    cover = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0Aayaya'
    custom_install_url = 'https://orindance.party/'
    description = 'koishi'
    flags = ApplicationFlag(56)
    icon = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0Aayaya'
    install_parameters = ApplicationInstallParameters(permissions = Permission(12))
    interaction_endpoint_url = 'https://orindance.party/'
    role_connection_verification_url = 'https://orindance.party/'
    tags = ['satori']
    
    application = Application(
        cover = cover,
        custom_install_url = custom_install_url,
        description = description,
        flags = flags,
        icon = icon,
        install_parameters = install_parameters,
        interaction_endpoint_url = interaction_endpoint_url,
        role_connection_verification_url = role_connection_verification_url,
        tags = tags,
    )
    
    with catch_warnings(record = True) as warnings:
        apply_simple_filter('always')
        
        data = application.to_data(defaults = True)
        
        vampytest.assert_eq(len(warnings), 0)
    
    
    expected_data = {
        'cover_image': 'data:image/png;base64,iVBORw0KGgpheWF5YQ==',
        'custom_install_url': custom_install_url,
        'description': description,
        'flags': int(flags),
        'icon': 'data:image/png;base64,iVBORw0KGgpheWF5YQ==',
        'install_params': install_parameters.to_data(defaults = True),
        'interactions_endpoint_url': interaction_endpoint_url,
        'role_connections_verification_url': role_connection_verification_url,
        'tags': tags,
    }
    
    vampytest.assert_eq(
        data,
        expected_data,
    )


def test__Application__to_data_ready():
    """
    Tests whether `Application.to_data`` works as intended.
    
    Case: defaults & internals
    """
    application_id = 202211290040
    flags = ApplicationFlag(96)
    
    application = Application.precreate(
        application_id,
        flags = flags,
    )
    
    expected_data = {
        'id': str(application_id),
        'flags': int(flags),
    }
    
    vampytest.assert_eq(
        application.to_data_ready(defaults = True, include_internals = True),
        expected_data,
    )


def test__Application__to_data_own():
    """
    Tests whether `Application.to_data`` works as intended.
    
    Case: defaults & internals
    """
    application_id = 202211290041
    
    approximate_guild_count = 11
    approximate_user_install_count = 13
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    description = 'dancing'
    flags = ApplicationFlag(96)
    hook = True
    icon = Icon(IconType.static, 12)
    name = 'Kaenbyou Rin'
    privacy_policy_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    splash = Icon(IconType.static, 66)
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    application_type = ApplicationType.game
    verify_key = 'hell'
    
    creator_monetization_state = ApplicationMonetizationState.disabled
    custom_install_url = 'https://orindance.party/'
    developers = [ApplicationEntity.precreate(202312030001, name = 'BrainDead')]
    discoverability_state = ApplicationDiscoverabilityState.blocked
    discovery_eligibility_flags = ApplicationDiscoveryEligibilityFlags(9)
    event_webhook_event_types = [
        ApplicationEventWebhookEventType.application_authorization,
        ApplicationEventWebhookEventType.entitlement_create
    ]
    event_webhook_state = ApplicationEventWebhookState.enabled
    event_webhook_url = 'https://orindance.party/event-webhook'
    explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    guild_id = 202211290042
    install_parameters = ApplicationInstallParameters(permissions = 8)
    integration_public = True
    integration_requires_code_grant = True
    integration_types = [ApplicationIntegrationType.user_install]
    integration_types_configuration = {
        ApplicationIntegrationType.user_install: ApplicationIntegrationTypeConfiguration(
            install_parameters = ApplicationInstallParameters(permissions = 8),
        ),
        ApplicationIntegrationType.guild_install: ApplicationIntegrationTypeConfiguration(
            install_parameters = ApplicationInstallParameters(permissions = 123),
        ),
    }
    interaction_endpoint_url = 'https://orindance.party/'
    interaction_event_types = [ApplicationInteractionEventType.none]
    interaction_version = ApplicationInteractionVersion.selective
    internal_guild_restriction = ApplicationInternalGuildRestriction.restricted
    monetization_eligibility_flags = ApplicationMonetizationEligibilityFlags(17)
    monetization_state = ApplicationMonetizationState.disabled
    monetized = True
    owner = User.precreate(202211290043)
    primary_sku_id = 202211290044
    publishers = [ApplicationEntity.precreate(202312040001, name = 'Brain')]
    redirect_urls = ['https://orindance.party/']
    role_connection_verification_url = 'https://orindance.party/'
    rpc_state = ApplicationRPCState.approved
    slug = 'https://orindance.party/'
    store_state = ApplicationStoreState.approved
    verification_state = ApplicationVerificationState.approved
    
    application = Application.precreate(
        application_id,
        approximate_guild_count = approximate_guild_count,
        approximate_user_install_count = approximate_user_install_count,
        bot_public = bot_public,
        bot_requires_code_grant = bot_requires_code_grant,
        cover = cover,
        creator_monetization_state = creator_monetization_state,
        custom_install_url = custom_install_url,
        discoverability_state = discoverability_state,
        discovery_eligibility_flags = discovery_eligibility_flags,
        description = description,
        developers = developers,
        event_webhook_event_types = event_webhook_event_types,
        event_webhook_state = event_webhook_state,
        event_webhook_url = event_webhook_url,
        explicit_content_filter_level = explicit_content_filter_level,
        flags = flags,
        guild_id = guild_id,
        hook = hook,
        icon = icon,
        install_parameters = install_parameters,
        integration_public = integration_public,
        integration_requires_code_grant = integration_requires_code_grant,
        integration_types = integration_types,
        integration_types_configuration = integration_types_configuration,
        interaction_endpoint_url = interaction_endpoint_url,
        interaction_event_types = interaction_event_types,
        interaction_version = interaction_version,
        internal_guild_restriction = internal_guild_restriction,
        monetization_eligibility_flags = monetization_eligibility_flags,
        monetization_state = monetization_state,
        monetized = monetized,
        name = name,
        owner = owner,
        primary_sku_id = primary_sku_id,
        privacy_policy_url = privacy_policy_url,
        publishers = publishers,
        redirect_urls = redirect_urls,
        role_connection_verification_url = role_connection_verification_url,
        rpc_origins = rpc_origins,
        rpc_state = rpc_state,
        slug = slug,
        splash = splash,
        store_state = store_state,
        tags = tags,
        terms_of_service_url = terms_of_service_url,
        application_type = application_type,
        verification_state = verification_state,
        verify_key = verify_key,
    )
    
    expected_data = {
        'id': str(application_id),
        'approximate_guild_count': approximate_guild_count,
        'approximate_user_install_count': approximate_user_install_count,
        'bot_public': bot_public,
        'bot_require_code_grant': bot_requires_code_grant,
        'cover_image': cover.as_base_16_hash,
        'description': description,
        'flags': int(flags),
        'hook': hook,
        'icon': icon.as_base_16_hash,
        'name': name,
        'privacy_policy_url': privacy_policy_url,
        'rpc_origins': rpc_origins,
        'splash': splash.as_base_16_hash,
        'tags': tags,
        'terms_of_service_url': terms_of_service_url,
        'type': application_type.value,
        'verify_key': verify_key,
        
        'creator_monetization_state': creator_monetization_state.value,
        'custom_install_url': custom_install_url,
        'developers': [developer.to_data(defaults = True, include_internals = True) for developer in developers],
        'discoverability_state': discoverability_state.value,
        'discovery_eligibility_flags': int(discovery_eligibility_flags),
        'event_webhooks_types': [
            event_webhook_event_type.value for event_webhook_event_type in event_webhook_event_types
        ], 
        'event_webhooks_status': event_webhook_state.value,
        'event_webhooks_url': event_webhook_url,
        'explicit_content_filter': explicit_content_filter_level.value,
        'guild_id': str(guild_id),
        'install_params': install_parameters.to_data(defaults = True),
        'integration_public': integration_public,
        'integration_require_code_grant': integration_requires_code_grant,
        'integration_types': [integration_type.value for integration_type in integration_types],
        'integration_types_config': {
            str(integration_type.value) : integration_type_configuration.to_data(defaults = True)
            for integration_type, integration_type_configuration
            in integration_types_configuration.items()
        },
        'interactions_endpoint_url': interaction_endpoint_url,
        'interactions_event_types': [
            interaction_event_type.value for interaction_event_type in interaction_event_types
        ],
        'interactions_version': interaction_version.value,
        'internal_guild_restriction': internal_guild_restriction.value,
        'monetization_eligibility_flags': int(monetization_eligibility_flags),
        'monetization_state': monetization_state.value,
        'is_monetized': monetized,
        'owner': owner.to_data(defaults = True, include_internals = True),
        'team': None,
        'primary_sku_id': str(primary_sku_id),
        'publishers': [publisher.to_data(defaults = True, include_internals = True) for publisher in publishers],
        'redirect_uris': redirect_urls,
        'role_connections_verification_url': role_connection_verification_url,
        'rpc_application_state': rpc_state.value,
        'slug': slug,
        'store_application_state': store_state.value,
        'verification_state': verification_state.value,
    }
    
    vampytest.assert_eq(
        application.to_data_own(defaults = True, include_internals = True),
        expected_data,
    )


def test__Application__to_data_invite():
    """
    Tests whether `Application.to_data`` works as intended.
    
    Case: defaults & internals
    """
    application_id = 202211290045
    
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    description = 'dancing'
    flags = ApplicationFlag(96)
    hook = True
    icon = Icon(IconType.static, 12)
    name = 'Kaenbyou Rin'
    privacy_policy_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    splash = Icon(IconType.static, 66)
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    application_type = ApplicationType.game
    verify_key = 'hell'
    
    embedded_activity_configuration = EmbeddedActivityConfiguration(position = 6)
    max_participants = 23
    monetized = True
    
    application = Application.precreate(
        application_id,
        bot_public = bot_public,
        bot_requires_code_grant = bot_requires_code_grant,
        cover = cover,
        description = description,
        embedded_activity_configuration = embedded_activity_configuration,
        flags = flags,
        hook = hook,
        icon = icon,
        max_participants = max_participants,
        monetized = monetized,
        name = name,
        privacy_policy_url = privacy_policy_url,
        rpc_origins = rpc_origins,
        splash = splash,
        tags = tags,
        terms_of_service_url = terms_of_service_url,
        application_type = application_type,
        verify_key = verify_key,
    )
    
    expected_data = {
        'id': str(application_id),
        'bot_public': bot_public,
        'bot_require_code_grant': bot_requires_code_grant,
        'cover_image': cover.as_base_16_hash,
        'description': description,
        'flags': int(flags),
        'hook': hook,
        'icon': icon.as_base_16_hash,
        'name': name,
        'privacy_policy_url': privacy_policy_url,
        'rpc_origins': rpc_origins,
        'splash': splash.as_base_16_hash,
        'tags': tags,
        'terms_of_service_url': terms_of_service_url,
        'type': application_type.value,
        'verify_key': verify_key,
        
        'embedded_activity_config': embedded_activity_configuration.to_data(defaults = True),
        'max_participants': max_participants,
        'is_monetized': monetized,
    }
    
    vampytest.assert_eq(
        application.to_data_invite(defaults = True, include_internals = True),
        expected_data,
    )


def test__Application__to_data_detectable():
    """
    Tests whether `Application.to_data`` works as intended.
    
    Case: defaults & internals
    """
    application_id = 202211290046
    
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    description = 'dancing'
    flags = ApplicationFlag(96)
    hook = True
    icon = Icon(IconType.static, 12)
    name = 'Kaenbyou Rin'
    privacy_policy_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    splash = Icon(IconType.static, 66)
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    application_type = ApplicationType.game
    verify_key = 'hell'
    
    aliases = ['orin', 'rin']
    deeplink_url = 'https://orindance.party/'
    developers = [ApplicationEntity.precreate(202211290047, name = 'BrainDead')]
    eula_id = 202211290048
    executables = [ApplicationExecutable(name = 'Okuu')]
    guild_id = 202211290049
    overlay = True
    overlay_compatibility_hook = True
    overlay_method_flags = ApplicationOverlayMethodFlags(26)
    primary_sku_id = 202211290050
    publishers = [ApplicationEntity.precreate(202211290051, name = 'Brain')]
    slug = 'https://orindance.party/'
    third_party_skus = [ThirdPartySKU(distributor = 'Dead')]
    application_id = 202211290052
    flags = ApplicationFlag(96)
    
    application = Application.precreate(
        application_id,
        aliases = aliases,
        bot_public = bot_public,
        bot_requires_code_grant = bot_requires_code_grant,
        cover = cover,
        deeplink_url = deeplink_url,
        description = description,
        developers = developers,
        eula_id = eula_id,
        executables = executables,
        flags = flags,
        guild_id = guild_id,
        hook = hook,
        icon = icon,
        name = name,
        overlay = overlay,
        overlay_compatibility_hook = overlay_compatibility_hook,
        overlay_method_flags = overlay_method_flags,
        primary_sku_id = primary_sku_id,
        privacy_policy_url = privacy_policy_url,
        publishers = publishers,
        rpc_origins = rpc_origins,
        slug = slug,
        splash = splash,
        tags = tags,
        terms_of_service_url = terms_of_service_url,
        third_party_skus = third_party_skus,
        application_type = application_type,
        verify_key = verify_key,
    )
    
    expected_data = {
        'id': str(application_id),
        'bot_public': bot_public,
        'bot_require_code_grant': bot_requires_code_grant,
        'cover_image': cover.as_base_16_hash,
        'description': description,
        'flags': int(flags),
        'hook': hook,
        'icon': icon.as_base_16_hash,
        'name': name,
        'privacy_policy_url': privacy_policy_url,
        'rpc_origins': rpc_origins,
        'splash': splash.as_base_16_hash,
        'tags': tags,
        'terms_of_service_url': terms_of_service_url,
        'type': application_type.value,
        'verify_key': verify_key,
        
        'aliases': aliases,
        'deeplink_uri': deeplink_url,
        'developers': [developer.to_data(defaults = True, include_internals = True) for developer in developers],
        'eula_id': str(eula_id),
        'executables': [executable.to_data(defaults = True) for executable in executables],
        'guild_id': str(guild_id),
        'overlay': overlay,
        'overlay_compatibility_hook': overlay_compatibility_hook,
        'overlay_methods': int(overlay_method_flags),
        'primary_sku_id': str(primary_sku_id),
        'publishers': [publisher.to_data(defaults = True, include_internals = True) for publisher in publishers],
        'slug': slug,
        'third_party_skus': [third_party_sku.to_data(defaults = True) for third_party_sku in third_party_skus]
    }
    
    vampytest.assert_eq(
        application.to_data_detectable(defaults = True, include_internals = True),
        expected_data,
    )
