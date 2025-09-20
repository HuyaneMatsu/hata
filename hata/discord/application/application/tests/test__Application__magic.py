import vampytest

from ....bases import Icon, IconType
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


def test__Application__repr():
    """
    Tests whether ``Application.__repr__`` works as intended.
    """
    application_id = 202211290051
    
    aliases = ['orin', 'rin']
    approximate_guild_count = 11
    approximate_user_authorization_count = 21
    approximate_user_install_count = 13
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    creator_monetization_state = ApplicationMonetizationState.disabled
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290071, name = 'BrainDead')]
    discoverability_state = ApplicationDiscoverabilityState.blocked
    discovery_eligibility_flags = ApplicationDiscoveryEligibilityFlags(9)
    embedded_activity_configuration = EmbeddedActivityConfiguration(position = 6)
    eula_id = 202211290052
    event_webhook_event_types = [
        ApplicationEventWebhookEventType.application_authorization,
        ApplicationEventWebhookEventType.entitlement_create
    ]
    event_webhook_state = ApplicationEventWebhookState.enabled
    event_webhook_url = 'https://orindance.party/event-webhook'
    executables = [ApplicationExecutable(name = 'Okuu')]
    explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    flags = ApplicationFlag(96)
    guild_id = 202211290053
    hook = True
    icon = Icon(IconType.static, 12)
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
    max_participants = 23
    monetization_eligibility_flags = ApplicationMonetizationEligibilityFlags(17)
    monetization_state = ApplicationMonetizationState.disabled
    monetized = True
    name = 'Kaenbyou Rin'
    overlay = True
    overlay_compatibility_hook = True
    overlay_method_flags = ApplicationOverlayMethodFlags(26)
    owner = User.precreate(202211290054)
    primary_sku_id = 202211290055
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290056, name = 'Brain')]
    redirect_urls = ['https://orindance.party/']
    role_connection_verification_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    rpc_state = ApplicationRPCState.approved
    slug = 'https://orindance.party/'
    splash = Icon(IconType.static, 66)
    store_state = ApplicationStoreState.approved
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    third_party_skus = [ThirdPartySKU(distributor = 'Dead')]
    application_type = ApplicationType.game
    verification_state = ApplicationVerificationState.approved
    verify_key = 'hell'
    
    application = Application.precreate(
        application_id,
        aliases = aliases,
        approximate_guild_count = approximate_guild_count,
        approximate_user_authorization_count = approximate_user_authorization_count,
        approximate_user_install_count = approximate_user_install_count,
        bot_public = bot_public,
        bot_requires_code_grant = bot_requires_code_grant,
        cover = cover,
        creator_monetization_state = creator_monetization_state,
        custom_install_url = custom_install_url,
        deeplink_url = deeplink_url,
        description = description,
        developers = developers,
        discoverability_state = discoverability_state,
        discovery_eligibility_flags = discovery_eligibility_flags,
        embedded_activity_configuration = embedded_activity_configuration,
        eula_id = eula_id,
        event_webhook_event_types = event_webhook_event_types,
        event_webhook_state = event_webhook_state,
        event_webhook_url = event_webhook_url,
        executables = executables,
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
        max_participants = max_participants,
        monetization_eligibility_flags = monetization_eligibility_flags,
        monetization_state = monetization_state,
        monetized = monetized,
        name = name,
        overlay = overlay,
        overlay_compatibility_hook = overlay_compatibility_hook,
        overlay_method_flags = overlay_method_flags,
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
        third_party_skus = third_party_skus,
        application_type = application_type,
        verification_state = verification_state,
        verify_key = verify_key,
    )
    
    vampytest.assert_instance(repr(application), str)
    
    application = Application(
        aliases = aliases,
        approximate_guild_count = approximate_guild_count,
        approximate_user_authorization_count = approximate_user_authorization_count,
        approximate_user_install_count = approximate_user_install_count,
        bot_public = bot_public,
        bot_requires_code_grant = bot_requires_code_grant,
        cover = cover,
        creator_monetization_state = creator_monetization_state,
        custom_install_url = custom_install_url,
        deeplink_url = deeplink_url,
        description = description,
        developers = developers,
        discoverability_state = discoverability_state,
        discovery_eligibility_flags = discovery_eligibility_flags,
        embedded_activity_configuration = embedded_activity_configuration,
        eula_id = eula_id,
        event_webhook_event_types = event_webhook_event_types,
        event_webhook_state = event_webhook_state,
        event_webhook_url = event_webhook_url,
        executables = executables,
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
        max_participants = max_participants,
        monetization_eligibility_flags = monetization_eligibility_flags,
        monetization_state = monetization_state,
        monetized = monetized,
        name = name,
        overlay = overlay,
        overlay_compatibility_hook = overlay_compatibility_hook,
        overlay_method_flags = overlay_method_flags,
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
        third_party_skus = third_party_skus,
        application_type = application_type,
        verification_state = verification_state,
        verify_key = verify_key,
    )
    
    vampytest.assert_instance(repr(application), str)


def test__Application__hash():
    """
    Tests whether ``Application.__hash__`` works as intended.
    """
    application_id = 202211290057
    
    aliases = ['orin', 'rin']
    approximate_guild_count = 11
    approximate_user_authorization_count = 21
    approximate_user_install_count = 13
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    creator_monetization_state = ApplicationMonetizationState.disabled
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290058, name = 'BrainDead')]
    discoverability_state = ApplicationDiscoverabilityState.blocked
    discovery_eligibility_flags = ApplicationDiscoveryEligibilityFlags(9)
    embedded_activity_configuration = EmbeddedActivityConfiguration(position = 6)
    eula_id = 202211290059
    event_webhook_event_types = [
        ApplicationEventWebhookEventType.application_authorization,
        ApplicationEventWebhookEventType.entitlement_create
    ]
    event_webhook_state = ApplicationEventWebhookState.enabled
    event_webhook_url = 'https://orindance.party/event-webhook'
    executables = [ApplicationExecutable(name = 'Okuu')]
    explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    flags = ApplicationFlag(96)
    guild_id = 202211290060
    hook = True
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
    icon = Icon(IconType.static, 12)
    max_participants = 23
    monetization_eligibility_flags = ApplicationMonetizationEligibilityFlags(17)
    monetization_state = ApplicationMonetizationState.disabled
    monetized = True
    name = 'Kaenbyou Rin'
    overlay = True
    overlay_compatibility_hook = True
    overlay_method_flags = ApplicationOverlayMethodFlags(26)
    owner = User.precreate(202211290061)
    primary_sku_id = 202211290062
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290063, name = 'Brain')]
    redirect_urls = ['https://orindance.party/']
    role_connection_verification_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    rpc_state = ApplicationRPCState.approved
    slug = 'https://orindance.party/'
    splash = Icon(IconType.static, 66)
    store_state = ApplicationStoreState.approved
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    third_party_skus = [ThirdPartySKU(distributor = 'Dead')]
    application_type = ApplicationType.game
    verification_state = ApplicationVerificationState.approved
    verify_key = 'hell'
    
    application = Application.precreate(
        application_id,
        aliases = aliases,
        approximate_guild_count = approximate_guild_count,
        approximate_user_authorization_count = approximate_user_authorization_count,
        approximate_user_install_count = approximate_user_install_count,
        bot_public = bot_public,
        bot_requires_code_grant = bot_requires_code_grant,
        cover = cover,
        creator_monetization_state = creator_monetization_state,
        custom_install_url = custom_install_url,
        deeplink_url = deeplink_url,
        description = description,
        developers = developers,
        discoverability_state = discoverability_state,
        discovery_eligibility_flags = discovery_eligibility_flags,
        embedded_activity_configuration = embedded_activity_configuration,
        eula_id = eula_id,
        event_webhook_event_types = event_webhook_event_types,
        event_webhook_state = event_webhook_state,
        event_webhook_url = event_webhook_url,
        executables = executables,
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
        max_participants = max_participants,
        monetization_eligibility_flags = monetization_eligibility_flags,
        monetization_state = monetization_state,
        monetized = monetized,
        name = name,
        overlay = overlay,
        overlay_compatibility_hook = overlay_compatibility_hook,
        overlay_method_flags = overlay_method_flags,
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
        third_party_skus = third_party_skus,
        application_type = application_type,
        verification_state = verification_state,
        verify_key = verify_key,
    )
    
    vampytest.assert_instance(hash(application), int)
    
    application = Application(
        aliases = aliases,
        approximate_guild_count = approximate_guild_count,
        approximate_user_authorization_count = approximate_user_authorization_count,
        approximate_user_install_count = approximate_user_install_count,
        bot_public = bot_public,
        bot_requires_code_grant = bot_requires_code_grant,
        cover = cover,
        creator_monetization_state = creator_monetization_state,
        custom_install_url = custom_install_url,
        deeplink_url = deeplink_url,
        description = description,
        developers = developers,
        discoverability_state = discoverability_state,
        discovery_eligibility_flags = discovery_eligibility_flags,
        embedded_activity_configuration = embedded_activity_configuration,
        eula_id = eula_id,
        event_webhook_event_types = event_webhook_event_types,
        event_webhook_state = event_webhook_state,
        event_webhook_url = event_webhook_url,
        executables = executables,
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
        max_participants = max_participants,
        monetization_eligibility_flags = monetization_eligibility_flags,
        monetization_state = monetization_state,
        monetized = monetized,
        name = name,
        overlay = overlay,
        overlay_compatibility_hook = overlay_compatibility_hook,
        overlay_method_flags = overlay_method_flags,
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
        third_party_skus = third_party_skus,
        application_type = application_type,
        verification_state = verification_state,
        verify_key = verify_key,
    )
    
    vampytest.assert_instance(hash(application), int)



def _iter_options__eq():
    aliases = ['orin', 'rin']
    approximate_guild_count = 11
    approximate_user_authorization_count = 21
    approximate_user_install_count = 13
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    creator_monetization_state = ApplicationMonetizationState.disabled
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290065, name = 'BrainDead')]
    discoverability_state = ApplicationDiscoverabilityState.blocked
    discovery_eligibility_flags = ApplicationDiscoveryEligibilityFlags(9)
    embedded_activity_configuration = EmbeddedActivityConfiguration(position = 6)
    eula_id = 202211290066
    event_webhook_event_types = [
        ApplicationEventWebhookEventType.application_authorization,
        ApplicationEventWebhookEventType.entitlement_create
    ]
    event_webhook_state = ApplicationEventWebhookState.enabled
    event_webhook_url = 'https://orindance.party/event-webhook'
    executables = [ApplicationExecutable(name = 'Okuu')]
    explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    flags = ApplicationFlag(96)
    guild_id = 202211290067
    hook = True
    icon = Icon(IconType.static, 12)
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
    max_participants = 23
    monetization_eligibility_flags = ApplicationMonetizationEligibilityFlags(17)
    monetization_state = ApplicationMonetizationState.disabled
    monetized = True
    name = 'Kaenbyou Rin'
    overlay = True
    overlay_compatibility_hook = True
    overlay_method_flags = ApplicationOverlayMethodFlags(26)
    owner = User.precreate(202211290068)
    primary_sku_id = 202211290069
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290070, name = 'Brain')]
    redirect_urls = ['https://orindance.party/']
    role_connection_verification_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    rpc_state = ApplicationRPCState.approved
    slug = 'https://orindance.party/'
    splash = Icon(IconType.static, 66)
    store_state = ApplicationStoreState.approved
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    third_party_skus = [ThirdPartySKU(distributor = 'Dead')]
    application_type = ApplicationType.game
    verification_state = ApplicationVerificationState.approved
    verify_key = 'hell'
    
    keyword_parameters = {
        'aliases': aliases,
        'approximate_guild_count': approximate_guild_count,
        'approximate_user_authorization_count': approximate_user_authorization_count,
        'approximate_user_install_count': approximate_user_install_count,
        'bot_public': bot_public,
        'bot_requires_code_grant': bot_requires_code_grant,
        'cover': cover,
        'creator_monetization_state': creator_monetization_state,
        'custom_install_url': custom_install_url,
        'deeplink_url': deeplink_url,
        'description': description,
        'developers': developers,
        'discoverability_state': discoverability_state,
        'discovery_eligibility_flags': discovery_eligibility_flags,
        'embedded_activity_configuration': embedded_activity_configuration,
        'eula_id': eula_id,
        'event_webhook_event_types': event_webhook_event_types,
        'event_webhook_state': event_webhook_state,
        'event_webhook_url': event_webhook_url,
        'executables': executables,
        'explicit_content_filter_level': explicit_content_filter_level,
        'flags': flags,
        'guild_id': guild_id,
        'hook': hook,
        'icon': icon,
        'install_parameters': install_parameters,
        'integration_public': integration_public,
        'integration_requires_code_grant': integration_requires_code_grant,
        'integration_types': integration_types,
        'integration_types_configuration': integration_types_configuration,
        'interaction_endpoint_url': interaction_endpoint_url,
        'interaction_event_types': interaction_event_types,
        'interaction_version': interaction_version,
        'internal_guild_restriction': internal_guild_restriction,
        'max_participants': max_participants,
        'monetization_eligibility_flags': monetization_eligibility_flags,
        'monetization_state': monetization_state,
        'monetized': monetized,
        'name': name,
        'overlay': overlay,
        'overlay_compatibility_hook': overlay_compatibility_hook,
        'overlay_method_flags': overlay_method_flags,
        'owner': owner,
        'primary_sku_id': primary_sku_id,
        'privacy_policy_url': privacy_policy_url,
        'publishers': publishers,
        'redirect_urls': redirect_urls,
        'role_connection_verification_url': role_connection_verification_url,
        'rpc_origins': rpc_origins,
        'rpc_state': rpc_state,
        'slug': slug,
        'splash': splash,
        'store_state': store_state,
        'tags': tags,
        'terms_of_service_url': terms_of_service_url,
        'third_party_skus': third_party_skus,
        'application_type': application_type,
        'verification_state': verification_state,
        'verify_key': verify_key,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'aliases': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'approximate_guild_count': 26,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'approximate_user_authorization_count': 23,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'approximate_user_install_count': 14,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'bot_public': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'bot_requires_code_grant': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'cover': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'creator_monetization_state': ApplicationMonetizationState.approved,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'custom_install_url': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'deeplink_url': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'developers': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'discoverability_state': ApplicationDiscoverabilityState.featurable,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'discovery_eligibility_flags': ApplicationDiscoveryEligibilityFlags(10),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'embedded_activity_configuration': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'eula_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'event_webhook_event_types': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'event_webhook_state': ApplicationEventWebhookState.disabled,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'event_webhook_url': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'executables': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'explicit_content_filter_level': ApplicationExplicitContentFilterLevel.none,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flags': ApplicationFlag(2),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'guild_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'hook': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'icon': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'install_parameters': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'integration_public': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'integration_requires_code_grant': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'integration_types': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'integration_types_configuration': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'interaction_endpoint_url': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'interaction_event_types': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'interaction_version': ApplicationInteractionVersion.every,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'internal_guild_restriction': ApplicationInternalGuildRestriction.none,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'max_participants': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'monetization_eligibility_flags': ApplicationMonetizationEligibilityFlags(18),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'monetization_state': ApplicationMonetizationState.approved,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'monetized': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'Kagerou',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'overlay': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'overlay_compatibility_hook': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'overlay_method_flags': ApplicationOverlayMethodFlags(27),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'owner': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'primary_sku_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'privacy_policy_url': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'publishers': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'redirect_urls': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'role_connection_verification_url': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'rpc_origins': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'rpc_state': ApplicationRPCState.submitted,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'slug': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'splash': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'store_state': ApplicationStoreState.submitted,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'tags': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'terms_of_service_url': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'third_party_skus': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application_type': ApplicationType.music,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'verification_state': ApplicationVerificationState.submitted,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'verify_key': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Application__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Application.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    application_0 = Application(**keyword_parameters_0)
    application_1 = Application(**keyword_parameters_1)
    output = application_0 == application_1
    vampytest.assert_instance(output, bool)
    return output


def test__Application__eq__various():
    """
    Tests whether ``Application.__eq__`` works as intended.
    
    Case: other various cases.
    """
    application_id = 202211290064
    
    application = Application.precreate(application_id, name = 'hey mister')
    vampytest.assert_eq(application, application)
    vampytest.assert_ne(application, object())
    
    test_application = Application(name = 'hey mister')
    vampytest.assert_eq(application, test_application)
    vampytest.assert_eq(application, application)
