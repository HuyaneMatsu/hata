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
    ApplicationDiscoverabilityState, ApplicationExplicitContentFilterLevel, ApplicationIntegrationType,
    ApplicationInteractionEventType, ApplicationInteractionVersion, ApplicationInternalGuildRestriction,
    ApplicationMonetizationState, ApplicationRPCState, ApplicationStoreState, ApplicationType,
    ApplicationVerificationState
)

def _assert_fields_set(application):
    """
    Asserts whether every attributes are set of the given application.
    
    Parameters
    ----------
    application : ``Application``
        The application to check.
    """
    vampytest.assert_instance(application, Application)
    vampytest.assert_instance(application._cache_emojis, dict, nullable = True)
    vampytest.assert_instance(application.aliases, tuple, nullable = True)
    vampytest.assert_instance(application.approximate_guild_count, int)
    vampytest.assert_instance(application.approximate_user_install_count, int)
    vampytest.assert_instance(application.bot_public, bool)
    vampytest.assert_instance(application.bot_requires_code_grant, bool)
    vampytest.assert_instance(application.cover, Icon)
    vampytest.assert_instance(application.creator_monetization_state, ApplicationMonetizationState)
    vampytest.assert_instance(application.custom_install_url, str, nullable = True)
    vampytest.assert_instance(application.deeplink_url, str, nullable = True)
    vampytest.assert_instance(application.description, str, nullable = True)
    vampytest.assert_instance(application.developers, tuple, nullable = True)
    vampytest.assert_instance(application.discoverability_state, ApplicationDiscoverabilityState)
    vampytest.assert_instance(application.discovery_eligibility_flags, ApplicationDiscoveryEligibilityFlags)
    vampytest.assert_instance(
        application.embedded_activity_configuration, EmbeddedActivityConfiguration, nullable = True
    )
    vampytest.assert_instance(application.eula_id, int)
    vampytest.assert_instance(application.executables, tuple, nullable = True)
    vampytest.assert_instance(application.explicit_content_filter_level, ApplicationExplicitContentFilterLevel)
    vampytest.assert_instance(application.flags, ApplicationFlag)
    vampytest.assert_instance(application.guild_id, int)
    vampytest.assert_instance(application.hook, bool)
    vampytest.assert_instance(application.icon, Icon)
    vampytest.assert_instance(application.id, int)
    vampytest.assert_instance(application.install_parameters, ApplicationInstallParameters, nullable = True)
    vampytest.assert_instance(application.integration_public, bool)
    vampytest.assert_instance(application.integration_requires_code_grant, bool)
    vampytest.assert_instance(application.integration_types, tuple, nullable = True)
    vampytest.assert_instance(application.integration_types_configuration, dict, nullable = True)
    vampytest.assert_instance(application.interaction_endpoint_url, str, nullable = True)
    vampytest.assert_instance(application.interaction_event_types, tuple, nullable = True)
    vampytest.assert_instance(application.interaction_version, ApplicationInteractionVersion)
    vampytest.assert_instance(application.internal_guild_restriction, ApplicationInternalGuildRestriction)
    vampytest.assert_instance(application.max_participants, int)
    vampytest.assert_instance(application.monetization_eligibility_flags, ApplicationMonetizationEligibilityFlags)
    vampytest.assert_instance(application.monetization_state, ApplicationMonetizationState)
    vampytest.assert_instance(application.monetized, bool)
    vampytest.assert_instance(application.name, str)
    vampytest.assert_instance(application.overlay, bool)
    vampytest.assert_instance(application.overlay_compatibility_hook, bool)
    vampytest.assert_instance(application.overlay_method_flags, ApplicationOverlayMethodFlags)
    vampytest.assert_instance(application.owner, object)
    vampytest.assert_instance(application.primary_sku_id, int)
    vampytest.assert_instance(application.privacy_policy_url, str, nullable = True)
    vampytest.assert_instance(application.publishers, tuple, nullable = True)
    vampytest.assert_instance(application.redirect_urls, tuple, nullable = True)
    vampytest.assert_instance(application.role_connection_verification_url, str, nullable = True)
    vampytest.assert_instance(application.rpc_origins, tuple, nullable = True)
    vampytest.assert_instance(application.rpc_state, ApplicationRPCState)
    vampytest.assert_instance(application.slug, str, nullable = True)
    vampytest.assert_instance(application.splash, Icon)
    vampytest.assert_instance(application.store_state, ApplicationStoreState)
    vampytest.assert_instance(application.tags, tuple, nullable = True)
    vampytest.assert_instance(application.terms_of_service_url, str, nullable = True)
    vampytest.assert_instance(application.third_party_skus, tuple, nullable = True)
    vampytest.assert_instance(application.type, ApplicationType)
    vampytest.assert_instance(application.verification_state, ApplicationVerificationState)
    vampytest.assert_instance(application.verify_key, str, nullable = True)


def test__Application__new__no_fields():
    """
    Tests whether ``Application.__new__`` works as intended.
    
    Case: No parameters.
    """
    application = Application()
    _assert_fields_set(application)


def test__Application__new__all_fields():
    """
    Tests whether ``Application.__new__`` works as intended.
    
    Case: All parameters.
    """
    aliases = ['orin', 'rin']
    approximate_guild_count = 11
    approximate_user_install_count = 13
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    creator_monetization_state = ApplicationMonetizationState.disabled
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290000, name = 'BrainDead')]
    discoverability_state = ApplicationDiscoverabilityState.blocked
    discovery_eligibility_flags = ApplicationDiscoveryEligibilityFlags(9)
    embedded_activity_configuration = EmbeddedActivityConfiguration(position = 6)
    eula_id = 202211290001
    executables = [ApplicationExecutable(name = 'Okuu')]
    explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    flags = ApplicationFlag(96)
    guild_id = 202211290002
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
    owner = User.precreate(202211290003)
    primary_sku_id = 202211290004
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290005, name = 'Brain')]
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
    
    application = Application(
        aliases = aliases,
        approximate_guild_count = approximate_guild_count,
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
    _assert_fields_set(application)
    
    vampytest.assert_eq(application.aliases, tuple(aliases))
    vampytest.assert_eq(application.approximate_guild_count, approximate_guild_count)
    vampytest.assert_eq(application.approximate_user_install_count, approximate_user_install_count)
    vampytest.assert_eq(application.bot_public, bot_public)
    vampytest.assert_eq(application.bot_requires_code_grant, bot_requires_code_grant)
    vampytest.assert_eq(application.cover, cover)
    vampytest.assert_is(application.creator_monetization_state, creator_monetization_state)
    vampytest.assert_eq(application.custom_install_url, custom_install_url)
    vampytest.assert_eq(application.deeplink_url, deeplink_url)
    vampytest.assert_eq(application.description, description)
    vampytest.assert_eq(application.developers, tuple(developers))
    vampytest.assert_is(application.discoverability_state, discoverability_state)
    vampytest.assert_eq(application.discovery_eligibility_flags, discovery_eligibility_flags)
    vampytest.assert_eq(application.embedded_activity_configuration, embedded_activity_configuration)
    vampytest.assert_eq(application.eula_id, eula_id)
    vampytest.assert_eq(application.executables, tuple(executables))
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
    vampytest.assert_eq(application.max_participants, max_participants)
    vampytest.assert_eq(application.monetization_eligibility_flags, monetization_eligibility_flags)
    vampytest.assert_is(application.monetization_state, monetization_state)
    vampytest.assert_eq(application.monetized, monetized)
    vampytest.assert_eq(application.name, name)
    vampytest.assert_eq(application.overlay, overlay)
    vampytest.assert_eq(application.overlay_compatibility_hook, overlay_compatibility_hook)
    vampytest.assert_eq(application.overlay_method_flags, overlay_method_flags)
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
    vampytest.assert_eq(application.third_party_skus, tuple(third_party_skus))
    vampytest.assert_is(application.type, application_type)
    vampytest.assert_is(application.verification_state, verification_state)
    vampytest.assert_eq(application.verify_key, verify_key)


def test__Application__precreate__no_fields():
    """
    Tests whether ``Application.precreate`` works as intended.
    
    Case: No parameters.
    """
    application_id = 202211290006
    application = Application.precreate(application_id)
    _assert_fields_set(application)
    vampytest.assert_eq(application.id, application_id)


def test__Application__precreate__all_fields():
    """
    Tests whether ``Application.precreate`` works as intended.
    
    Case: All parameters.
    """
    application_id = 202211290007
    
    aliases = ['orin', 'rin']
    approximate_guild_count = 11
    approximate_user_install_count = 13
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    creator_monetization_state = ApplicationMonetizationState.disabled
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290008, name = 'BrainDead')]
    discoverability_state = ApplicationDiscoverabilityState.blocked
    discovery_eligibility_flags = ApplicationDiscoveryEligibilityFlags(9)
    embedded_activity_configuration = EmbeddedActivityConfiguration(position = 6)
    eula_id = 202211290009
    executables = [ApplicationExecutable(name = 'Okuu')]
    explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    flags = ApplicationFlag(96)
    guild_id = 202211290010
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
    owner = User.precreate(202211290011)
    primary_sku_id = 202211290004
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290012, name = 'Brain')]
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
        monetization_state = ApplicationMonetizationState.disabled,
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
    _assert_fields_set(application)
    vampytest.assert_eq(application.id, application_id)
    
    vampytest.assert_eq(application.aliases, tuple(aliases))
    vampytest.assert_eq(application.approximate_guild_count, approximate_guild_count)
    vampytest.assert_eq(application.approximate_user_install_count, approximate_user_install_count)
    vampytest.assert_eq(application.bot_public, bot_public)
    vampytest.assert_eq(application.bot_requires_code_grant, bot_requires_code_grant)
    vampytest.assert_eq(application.cover, cover)
    vampytest.assert_is(application.creator_monetization_state, creator_monetization_state)
    vampytest.assert_eq(application.custom_install_url, custom_install_url)
    vampytest.assert_eq(application.deeplink_url, deeplink_url)
    vampytest.assert_eq(application.description, description)
    vampytest.assert_eq(application.developers, tuple(developers))
    vampytest.assert_is(application.discoverability_state, discoverability_state)
    vampytest.assert_eq(application.discovery_eligibility_flags, discovery_eligibility_flags)
    vampytest.assert_eq(application.embedded_activity_configuration, embedded_activity_configuration)
    vampytest.assert_eq(application.eula_id, eula_id)
    vampytest.assert_eq(application.executables, tuple(executables))
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
    vampytest.assert_eq(application.max_participants, max_participants)
    vampytest.assert_eq(application.monetization_eligibility_flags, monetization_eligibility_flags)
    vampytest.assert_is(application.monetization_state, monetization_state)
    vampytest.assert_eq(application.monetized, monetized)
    vampytest.assert_eq(application.name, name)
    vampytest.assert_eq(application.overlay, overlay)
    vampytest.assert_eq(application.overlay_compatibility_hook, overlay_compatibility_hook)
    vampytest.assert_eq(application.overlay_method_flags, overlay_method_flags)
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
    vampytest.assert_eq(application.third_party_skus, tuple(third_party_skus))
    vampytest.assert_is(application.type, application_type)
    vampytest.assert_is(application.verification_state, verification_state)
    vampytest.assert_eq(application.verify_key, verify_key)


def test__Application__precreate__caching():
    """
    Tests whether ``Application.precreate`` works as intended.
    
    Case: Caching.
    """
    application_id = 202211290013
    application = Application.precreate(application_id)
    test_application = Application.precreate(application_id)
    vampytest.assert_is(application, test_application)


def test__Application__create_empty():
    """
    Tests whether ``Application._create_empty`` works as intended.
    
    Case: No parameters.
    """
    application_id = 202211290014
    application = Application._create_empty(application_id)
    _assert_fields_set(application)
    vampytest.assert_eq(application.id, application_id)
