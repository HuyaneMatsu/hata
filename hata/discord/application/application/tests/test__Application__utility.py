import vampytest

from ....bases import Icon, IconType
from ....guild import Guild
from ....user import User

from ...application_entity import ApplicationEntity
from ...application_executable import ApplicationExecutable
from ...application_install_parameters import ApplicationInstallParameters
from ...embedded_activity_configuration import EmbeddedActivityConfiguration
from ...third_party_sku import ThirdPartySKU

from ..application import Application
from ..flags import (
    ApplicationDiscoveryEligibilityFlags, ApplicationFlag, ApplicationMonetizationEligibilityFlags,
    ApplicationOverlayMethodFlags
)
from ..preinstanced import (
    ApplicationDiscoverabilityState, ApplicationExplicitContentFilterLevel, ApplicationInteractionEventType,
    ApplicationInteractionVersion, ApplicationInternalGuildRestriction, ApplicationMonetizationState,
    ApplicationRPCState, ApplicationStoreState, ApplicationType, ApplicationVerificationState
)

from .test__Application__constructor import _assert_fields_set


def test__Application__copy():
    """
    Tests whether ``Application.copy`` works as intended.
    """
    aliases = ['orin', 'rin']
    approximate_guild_count = 11
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    creator_monetization_state = ApplicationMonetizationState.disabled
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290072, name = 'BrainDead')]
    discoverability_state = ApplicationDiscoverabilityState.blocked
    discovery_eligibility_flags = ApplicationDiscoveryEligibilityFlags(9)
    embedded_activity_configuration = EmbeddedActivityConfiguration(position = 6)
    eula_id = 202211290073
    executables = [ApplicationExecutable(name = 'Okuu')]
    explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    flags = ApplicationFlag(96)
    guild_id = 202211290074
    hook = True
    install_parameters = ApplicationInstallParameters(permissions = 8)
    integration_public = True
    integration_requires_code_grant = True
    interaction_endpoint_url = 'https://orindance.party/'
    interaction_event_types = [ApplicationInteractionEventType.none]
    interaction_version = ApplicationInteractionVersion.every
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
    owner = User.precreate(202211290075)
    primary_sku_id = 202211290076
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290077, name = 'Brain')]
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
    
    copy = application.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(application, copy)


def test__Application__copy_with__no_fields():
    """
    Tests whether ``Application.copy_with`` works as intended.
    
    Case: No parameters.
    """
    aliases = ['orin', 'rin']
    approximate_guild_count = 11
    bot_public = True
    bot_requires_code_grant = True
    cover = Icon(IconType.static, 23)
    creator_monetization_state = ApplicationMonetizationState.disabled
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290077, name = 'BrainDead')]
    discoverability_state = ApplicationDiscoverabilityState.blocked
    discovery_eligibility_flags = ApplicationDiscoveryEligibilityFlags(9)
    embedded_activity_configuration = EmbeddedActivityConfiguration(position = 6)
    eula_id = 202211290078
    executables = [ApplicationExecutable(name = 'Okuu')]
    explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    flags = ApplicationFlag(96)
    guild_id = 202211290079
    hook = True
    install_parameters = ApplicationInstallParameters(permissions = 8)
    integration_public = True
    integration_requires_code_grant = True
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
    owner = User.precreate(202211290080)
    primary_sku_id = 202211290081
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290082, name = 'Brain')]
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
    
    copy = application.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(application, copy)
    vampytest.assert_eq(application, copy)


def test__Application__copy_with__all_fields():
    """
    Tests whether ``Application.copy_with`` works as intended.
    
    Case: All parameters.
    """
    old_aliases = ['orin', 'rin']
    old_approximate_guild_count = 12
    old_bot_requires_code_grant = True
    old_bot_public = True
    old_cover = Icon(IconType.static, 23)
    old_creator_monetization_state = ApplicationMonetizationState.disabled
    old_custom_install_url = 'https://orindance.party/'
    old_deeplink_url = 'https://orindance.party/'
    old_description = 'dancing'
    old_developers = [ApplicationEntity.precreate(202211290083, name = 'BrainDead')]
    old_discoverability_state = ApplicationDiscoverabilityState.blocked
    old_discovery_eligibility_flags = ApplicationDiscoveryEligibilityFlags(9)
    old_embedded_activity_configuration = EmbeddedActivityConfiguration(position = 6)
    old_eula_id = 202211290085
    old_executables = [ApplicationExecutable(name = 'Okuu')]
    old_explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    old_flags = ApplicationFlag(96)
    old_guild_id = 202211290087
    old_hook = True
    old_icon = Icon(IconType.static, 12)
    old_install_parameters = ApplicationInstallParameters(permissions = 8)
    old_integration_public = True
    old_integration_requires_code_grant = True
    old_interaction_endpoint_url = 'https://orindance.party/'
    old_interaction_event_types = None
    old_interaction_version = ApplicationInteractionVersion.selective
    old_internal_guild_restriction = ApplicationInternalGuildRestriction.restricted
    old_max_participants = 23
    old_monetization_eligibility_flags = ApplicationMonetizationEligibilityFlags(17)
    old_monetization_state = ApplicationMonetizationState.disabled
    old_monetized = True
    old_name = 'Kaenbyou Rin'
    old_overlay = True
    old_overlay_compatibility_hook = True
    old_overlay_method_flags = ApplicationOverlayMethodFlags(26)
    old_owner = User.precreate(202211290089)
    old_primary_sku_id = 202211290091
    old_privacy_policy_url = 'https://orindance.party/'
    old_publishers = [ApplicationEntity.precreate(202211290093, name = 'Brain')]
    old_redirect_urls = ['https://orindance.party/']
    old_role_connection_verification_url = 'https://orindance.party/'
    old_rpc_origins = ['https://orindance.party/']
    old_rpc_state = ApplicationRPCState.approved
    old_slug = 'https://orindance.party/'
    old_splash = Icon(IconType.static, 66)
    old_store_state = ApplicationStoreState.approved
    old_tags = ['cat']
    old_terms_of_service_url = 'https://orindance.party/'
    old_third_party_skus = [ThirdPartySKU(distributor = 'Dead')]
    old_application_type = ApplicationType.game
    old_verification_state = ApplicationVerificationState.approved
    old_verify_key = 'hell'
    
    new_aliases = ['nue']
    new_approximate_guild_count = 15
    new_bot_public = False
    new_bot_requires_code_grant = False
    new_cover = Icon(IconType.static, 33)
    new_creator_monetization_state = ApplicationMonetizationState.approved
    new_custom_install_url = 'https://www.astil.dev/project/hata/'
    new_deeplink_url = 'https://www.astil.dev/project/hata/'
    new_description = 'flying'
    new_developers = [ApplicationEntity.precreate(202211290084, name = 'Nekosia')]
    new_discoverability_state = ApplicationDiscoverabilityState.featurable
    new_discovery_eligibility_flags = ApplicationDiscoveryEligibilityFlags(10)
    new_embedded_activity_configuration = EmbeddedActivityConfiguration(position = 6)
    new_eula_id = 202211290086
    new_executables = [ApplicationExecutable(name = 'Nue')]
    new_explicit_content_filter_level = ApplicationExplicitContentFilterLevel.none
    new_flags = ApplicationFlag(2)
    new_guild_id = 202211290088
    new_hook = False
    new_icon = Icon(IconType.static, 99)
    new_install_parameters = ApplicationInstallParameters(permissions = 16)
    new_integration_public = False
    new_integration_requires_code_grant = False
    new_interaction_endpoint_url = 'https://www.astil.dev/project/hata/'
    new_interaction_event_types = [ApplicationInteractionEventType.none]
    new_interaction_version = ApplicationInteractionVersion.every
    new_internal_guild_restriction = ApplicationInternalGuildRestriction.none
    new_max_participants = 11
    new_monetization_eligibility_flags = ApplicationMonetizationEligibilityFlags(18)
    new_monetization_state = ApplicationMonetizationState.approved
    new_monetized = False
    new_name = 'Houjuu Nue'
    new_overlay = False
    new_overlay_compatibility_hook = False
    new_overlay_method_flags = ApplicationOverlayMethodFlags(27)
    new_owner = User.precreate(202211290090)
    new_primary_sku_id = 202211290092
    new_privacy_policy_url = 'https://www.astil.dev/project/hata/'
    new_publishers = [ApplicationEntity.precreate(202211290094, name = 'Neko')]
    new_redirect_urls = ['https://www.astil.dev/project/hata/']
    new_role_connection_verification_url = 'https://www.astil.dev/project/hata/'
    new_rpc_origins = ['https://www.astil.dev/project/hata/']
    new_rpc_state = ApplicationRPCState.submitted
    new_slug = 'https://www.astil.dev/project/hata/'
    new_splash = Icon(IconType.animated, 66)
    new_store_state = ApplicationStoreState.submitted
    new_tags = ['alien', 'lovely']
    new_terms_of_service_url = 'https://www.astil.dev/project/hata/'
    new_third_party_skus = [ThirdPartySKU(distributor = 'Sia')]
    new_application_type = ApplicationType.music
    new_verification_state = ApplicationVerificationState.submitted
    new_verify_key = 'space'
    
    application = Application(
        aliases = old_aliases,
        approximate_guild_count = old_approximate_guild_count,
        bot_public = old_bot_public,
        bot_requires_code_grant = old_bot_requires_code_grant,
        cover = old_cover,
        creator_monetization_state = old_creator_monetization_state,
        custom_install_url = old_custom_install_url,
        deeplink_url = old_deeplink_url,
        description = old_description,
        developers = old_developers,
        discoverability_state = old_discoverability_state,
        discovery_eligibility_flags = old_discovery_eligibility_flags,
        embedded_activity_configuration = old_embedded_activity_configuration,
        eula_id = old_eula_id,
        executables = old_executables,
        explicit_content_filter_level = old_explicit_content_filter_level,
        flags = old_flags,
        guild_id = old_guild_id,
        hook = old_hook,
        icon = old_icon,
        install_parameters = old_install_parameters,
        integration_public = old_integration_public,
        integration_requires_code_grant = old_integration_requires_code_grant,
        interaction_endpoint_url = old_interaction_endpoint_url,
        interaction_event_types = old_interaction_event_types,
        interaction_version = old_interaction_version,
        internal_guild_restriction = old_internal_guild_restriction,
        max_participants = old_max_participants,
        monetization_eligibility_flags = old_monetization_eligibility_flags,
        monetization_state = old_monetization_state,
        monetized = old_monetized,
        name = old_name,
        overlay = old_overlay,
        overlay_compatibility_hook = old_overlay_compatibility_hook,
        overlay_method_flags = old_overlay_method_flags,
        owner = old_owner,
        primary_sku_id = old_primary_sku_id,
        privacy_policy_url = old_privacy_policy_url,
        publishers = old_publishers,
        redirect_urls = old_redirect_urls,
        role_connection_verification_url = old_role_connection_verification_url,
        rpc_origins = old_rpc_origins,
        rpc_state = old_rpc_state,
        slug = old_slug,
        splash = old_splash,
        store_state = old_store_state,
        tags = old_tags,
        terms_of_service_url = old_terms_of_service_url,
        third_party_skus = old_third_party_skus,
        application_type = old_application_type,
        verification_state = old_verification_state,
        verify_key = old_verify_key,
    )
    
    copy = application.copy_with(
        aliases = new_aliases,
        approximate_guild_count = new_approximate_guild_count,
        bot_public = new_bot_public,
        bot_requires_code_grant = new_bot_requires_code_grant,
        cover = new_cover,
        creator_monetization_state = new_creator_monetization_state,
        custom_install_url = new_custom_install_url,
        deeplink_url = new_deeplink_url,
        description = new_description,
        developers = new_developers,
        discoverability_state = new_discoverability_state,
        discovery_eligibility_flags = new_discovery_eligibility_flags,
        embedded_activity_configuration = new_embedded_activity_configuration,
        eula_id = new_eula_id,
        executables = new_executables,
        explicit_content_filter_level = new_explicit_content_filter_level,
        flags = new_flags,
        guild_id = new_guild_id,
        hook = new_hook,
        icon = new_icon,
        install_parameters = new_install_parameters,
        integration_public = new_integration_public,
        integration_requires_code_grant = new_integration_requires_code_grant,
        interaction_endpoint_url = new_interaction_endpoint_url,
        interaction_event_types = new_interaction_event_types,
        interaction_version = new_interaction_version,
        internal_guild_restriction = new_internal_guild_restriction,
        max_participants = new_max_participants,
        monetization_eligibility_flags = new_monetization_eligibility_flags,
        monetization_state = new_monetization_state,
        monetized = new_monetized,
        name = new_name,
        overlay = new_overlay,
        overlay_compatibility_hook = new_overlay_compatibility_hook,
        overlay_method_flags = new_overlay_method_flags,
        owner = new_owner,
        primary_sku_id = new_primary_sku_id,
        privacy_policy_url = new_privacy_policy_url,
        publishers = new_publishers,
        redirect_urls = new_redirect_urls,
        role_connection_verification_url = new_role_connection_verification_url,
        rpc_origins = new_rpc_origins,
        rpc_state = new_rpc_state,
        slug = new_slug,
        splash = new_splash,
        store_state = new_store_state,
        tags = new_tags,
        terms_of_service_url = new_terms_of_service_url,
        third_party_skus = new_third_party_skus,
        application_type = new_application_type,
        verification_state = new_verification_state,
        verify_key = new_verify_key,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(application, copy)
    
    vampytest.assert_eq(copy.aliases, tuple(new_aliases))
    vampytest.assert_eq(copy.approximate_guild_count, new_approximate_guild_count)
    vampytest.assert_eq(copy.bot_public, new_bot_public)
    vampytest.assert_eq(copy.bot_requires_code_grant, new_bot_requires_code_grant)
    vampytest.assert_eq(copy.cover, new_cover)
    vampytest.assert_eq(copy.creator_monetization_state, new_creator_monetization_state)
    vampytest.assert_eq(copy.custom_install_url, new_custom_install_url)
    vampytest.assert_eq(copy.deeplink_url, new_deeplink_url)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.developers, tuple(new_developers))
    vampytest.assert_is(copy.discoverability_state, new_discoverability_state)
    vampytest.assert_eq(copy.discovery_eligibility_flags, new_discovery_eligibility_flags)
    vampytest.assert_eq(copy.embedded_activity_configuration, new_embedded_activity_configuration)
    vampytest.assert_eq(copy.eula_id, new_eula_id)
    vampytest.assert_eq(copy.executables, tuple(new_executables))
    vampytest.assert_is(copy.explicit_content_filter_level, new_explicit_content_filter_level)
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.hook, new_hook)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.install_parameters, new_install_parameters)
    vampytest.assert_eq(copy.integration_public, new_integration_public)
    vampytest.assert_eq(copy.integration_requires_code_grant, new_integration_requires_code_grant)
    vampytest.assert_eq(copy.interaction_endpoint_url, new_interaction_endpoint_url)
    vampytest.assert_eq(copy.interaction_event_types, tuple(new_interaction_event_types))
    vampytest.assert_is(copy.interaction_version, new_interaction_version)
    vampytest.assert_is(copy.internal_guild_restriction, new_internal_guild_restriction)
    vampytest.assert_eq(copy.max_participants, new_max_participants)
    vampytest.assert_eq(copy.monetization_eligibility_flags, new_monetization_eligibility_flags)
    vampytest.assert_is(copy.monetization_state, new_monetization_state)
    vampytest.assert_eq(copy.monetized, new_monetized)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.overlay, new_overlay)
    vampytest.assert_eq(copy.overlay_compatibility_hook, new_overlay_compatibility_hook)
    vampytest.assert_eq(copy.overlay_method_flags, new_overlay_method_flags)
    vampytest.assert_eq(copy.owner, new_owner)
    vampytest.assert_eq(copy.primary_sku_id, new_primary_sku_id)
    vampytest.assert_eq(copy.privacy_policy_url, new_privacy_policy_url)
    vampytest.assert_eq(copy.publishers, tuple(new_publishers))
    vampytest.assert_eq(copy.redirect_urls, tuple(new_redirect_urls))
    vampytest.assert_eq(copy.role_connection_verification_url, new_role_connection_verification_url)
    vampytest.assert_eq(copy.rpc_origins, tuple(new_rpc_origins))
    vampytest.assert_eq(copy.slug, new_slug)
    vampytest.assert_eq(copy.splash, new_splash)
    vampytest.assert_is(copy.store_state, new_store_state)
    vampytest.assert_eq(copy.tags, tuple(new_tags))
    vampytest.assert_eq(copy.terms_of_service_url, new_terms_of_service_url)
    vampytest.assert_eq(copy.third_party_skus, tuple(new_third_party_skus))
    vampytest.assert_is(copy.type, new_application_type)
    vampytest.assert_is(copy.verification_state, new_verification_state)
    vampytest.assert_eq(copy.verify_key, new_verify_key)


def test__Application__partial():
    """
    Tests whether ``Application.partial`` works as intended.
    """
    # we only check partial since we are lazy
    application = Application()
    vampytest.assert_true(application.partial)
    
    application = Application.precreate(202211290093)
    vampytest.assert_true(application.partial)


def _iter_options__iter_aliases():
    alias_0 = 'Koishi'
    alias_1 = 'Komeiji'
    
    yield None, []
    yield [alias_0], [alias_0]
    yield [alias_0, alias_1], [alias_0, alias_1]


@vampytest._(vampytest.call_from(_iter_options__iter_aliases()).returning_last())
def test__Application__iter_aliases(input_value):
    """
    Tests whether ``Application.iter_aliases`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<str>`
        Aliases to create the application with.
    
    Returns
    -------
    output : `list<str>`
    """
    application = Application(aliases = input_value)
    return [*application.iter_aliases()]


def _iter_options__iter_developers():
    developer_0 = ApplicationEntity.precreate(202211290096, name = 'Suika')
    developer_1 = ApplicationEntity.precreate(202211290097, name = 'Yuugi')

    yield None, []
    yield [developer_0], [developer_0]
    yield [developer_0, developer_1], [developer_0, developer_1]


@vampytest._(vampytest.call_from(_iter_options__iter_developers()).returning_last())
def test__Application__iter_developers(input_value):
    """
    Tests whether ``Application.iter_developers`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<ApplicationEntity>`
        Developers to create the application with.
    
    Returns
    -------
    output : `list<ApplicationEntity>`
    """
    application = Application(developers = input_value)
    return [*application.iter_developers()]


def _iter_options__iter_executables():
    executable_0 = ApplicationExecutable(name = 'pudding', launcher = False)
    executable_1 = ApplicationExecutable(name = 'pudding', launcher = True)
    
    yield None, []
    yield [executable_0], [executable_0]
    yield [executable_0, executable_1], [executable_0, executable_1]


@vampytest._(vampytest.call_from(_iter_options__iter_executables()).returning_last())
def test__Application__iter_executables(input_value):
    """
    Tests whether ``Application.iter_executables`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<ApplicationExecutable>`
        Executables to create the application with.
    
    Returns
    -------
    output : `list<ApplicationExecutable>`
    """
    application = Application(executables = input_value)
    return [*application.iter_executables()]


def _iter_options__iter_publishers():
    publisher_0 = ApplicationEntity.precreate(202211290098, name = 'Suika')
    publisher_1 = ApplicationEntity.precreate(202211290099, name = 'Yuugi')
    
    yield None, []
    yield [publisher_0], [publisher_0]
    yield [publisher_0, publisher_1], [publisher_0, publisher_1]


@vampytest._(vampytest.call_from(_iter_options__iter_publishers()).returning_last())
def test__Application__iter_publishers(input_value):
    """
    Tests whether ``Application.iter_publishers`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<ApplicationEntity>`
        Publishers to create the application with.
    
    Returns
    -------
    output : `list<ApplicationEntity>`
    """
    application = Application(publishers = input_value)
    return [*application.iter_publishers()]


def _iter_options__iter_rpc_origins():
    rpc_origin_0 = 'https://orindance.party/'
    rpc_origin_1 = 'https://www.astil.dev/project/hata/'
    
    yield None, []
    yield [rpc_origin_0], [rpc_origin_0]
    yield [rpc_origin_0, rpc_origin_1], [rpc_origin_0, rpc_origin_1]


@vampytest._(vampytest.call_from(_iter_options__iter_rpc_origins()).returning_last())
def test__Application__iter_rpc_origins(input_value):
    """
    Tests whether ``Application.iter_rpc_origins`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<str>`
        Rpc origins to create the application with.
    
    Returns
    -------
    output : `list<str>`
    """
    application = Application(rpc_origins = input_value)
    return [*application.iter_rpc_origins()]


def _iter_options__iter_rpc_origins():
    tag_0 = 'Koishi'
    tag_1 = 'Komeiji'
    
    yield None, []
    yield [tag_0], [tag_0]
    yield [tag_0, tag_1], [tag_0, tag_1]


@vampytest._(vampytest.call_from(_iter_options__iter_rpc_origins()).returning_last())
def test__Application__iter_tags(input_value):
    """
    Tests whether ``Application.iter_tags`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<str>`
        Tags origins to create the application with.
    
    Returns
    -------
    output : `list<str>`
    """
    application = Application(tags = input_value)
    return [*application.iter_tags()]


def _iter_options__iter_third_party_skus():
    third_party_sku_0 = ThirdPartySKU(distributor = 'Suika')
    third_party_sku_1 = ThirdPartySKU(distributor = 'Yuugi')
    
    yield None, []
    yield [third_party_sku_0], [third_party_sku_0]
    yield [third_party_sku_0, third_party_sku_1], [third_party_sku_0, third_party_sku_1]


@vampytest._(vampytest.call_from(_iter_options__iter_third_party_skus()).returning_last())
def test__Application__iter_third_party_skus(input_value):
    """
    Tests whether ``Application.iter_third_party_skus`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<ThirdPartySKU>`
        Third party stock keeping units origins to create the application with.
    
    Returns
    -------
    output : `list<ThirdPartySKU>`
    """
    application = Application(third_party_skus = input_value)
    return [*application.iter_third_party_skus()]


def _iter_options__guild():
    yield Application.precreate(202311270002), None
    yield Application.precreate(202311270003, guild_id = 202311270004), None
    
    guild_id = 202311270005
    yield Application.precreate(202311270006, guild_id = guild_id), Guild.precreate(guild_id)


@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__Application__guild(application):
    """
    Tests whether ``Application.guild`` works as intended.
    
    Parameters
    ----------
    input_value : ``Application```
        Application to test with.
    
    Returns
    -------
    output : `None | Guild`
    """
    return application.guild


def _iter_options__iter_interaction_event_types():
    interaction_event_type_0 = ApplicationInteractionEventType.none
    
    yield None, []
    yield [interaction_event_type_0], [interaction_event_type_0]


@vampytest._(vampytest.call_from(_iter_options__iter_interaction_event_types()).returning_last())
def test__Application__iter_interaction_event_types(input_value):
    """
    Tests whether ``Application.iter_interaction_event_types`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<ApplicationInteractionEventType>`
        Application interaction event types to create the application with.
    
    Returns
    -------
    output : `list<ApplicationInteractionEventType>`
    """
    application = Application(interaction_event_types = input_value)
    return [*application.iter_interaction_event_types()]


def _iter_options__iter_redirect_urls():
    redirect_url_0 = 'https://orindance.party/'
    redirect_url_1 = 'https://www.astil.dev/project/hata/'
    
    yield None, []
    yield [redirect_url_0], [redirect_url_0]
    yield [redirect_url_0, redirect_url_1], [redirect_url_0, redirect_url_1]


@vampytest._(vampytest.call_from(_iter_options__iter_redirect_urls()).returning_last())
def test__Application__iter_redirect_urls(input_value):
    """
    Tests whether ``Application.iter_redirect_urls`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<str>`
        Rpc origins to create the application with.
    
    Returns
    -------
    output : `list<str>`
    """
    application = Application(redirect_urls = input_value)
    return [*application.iter_redirect_urls()]

