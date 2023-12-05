import vampytest

from ....bases import Icon, IconType
from ....user import User

from ...application_entity import ApplicationEntity
from ...application_executable import ApplicationExecutable
from ...application_install_parameters import ApplicationInstallParameters
from ...embedded_activity_configuration import EmbeddedActivityConfiguration
from ...third_party_sku import ThirdPartySKU

from ..application import Application
from ..flags import ApplicationFlag, ApplicationDiscoveryEligibilityFlags, ApplicationMonetizationEligibilityFlags, \
    ApplicationOverlayMethodFlags
from ..preinstanced import ApplicationMonetizationState, ApplicationType, ApplicationDiscoverabilityState, \
    ApplicationExplicitContentFilterLevel, ApplicationInteractionEventType, ApplicationInteractionVersion, \
    ApplicationInternalGuildRestriction, ApplicationRPCState, ApplicationStoreState, ApplicationVerificationState


def test__Application__repr():
    """
    Tests whether ``Application.__repr__`` works as intended.
    """
    application_id = 202211290051
    
    aliases = ['orin', 'rin']
    approximate_guild_count = 11
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
    executables = [ApplicationExecutable(name = 'Okuu')]
    explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    flags = ApplicationFlag(96)
    guild_id = 202211290053
    hook = True
    icon = Icon(IconType.static, 12)
    install_parameters = ApplicationInstallParameters(permissions = 8)
    integration_public = True
    integration_requires_code_grant = True
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
    
    vampytest.assert_instance(repr(application), str)
    
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
    
    vampytest.assert_instance(repr(application), str)


def test__Application__hash():
    """
    Tests whether ``Application.__hash__`` works as intended.
    """
    application_id = 202211290057
    
    aliases = ['orin', 'rin']
    approximate_guild_count = 11
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
    executables = [ApplicationExecutable(name = 'Okuu')]
    explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    flags = ApplicationFlag(96)
    guild_id = 202211290060
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
    
    vampytest.assert_instance(hash(application), int)
    
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
    
    vampytest.assert_instance(hash(application), int)


def test__Application__eq():
    """
    Tests whether ``Application.__eq__`` works as intended.
    """
    application_id = 202211290064
    
    aliases = ['orin', 'rin']
    approximate_guild_count = 11
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
    executables = [ApplicationExecutable(name = 'Okuu')]
    explicit_content_filter_level = ApplicationExplicitContentFilterLevel.filtered
    flags = ApplicationFlag(96)
    guild_id = 202211290067
    hook = True
    icon = Icon(IconType.static, 12)
    install_parameters = ApplicationInstallParameters(permissions = 8)
    integration_public = True
    integration_requires_code_grant = True
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
        'executables': executables,
        'explicit_content_filter_level': explicit_content_filter_level,
        'flags': flags,
        'guild_id': guild_id,
        'hook': hook,
        'icon': icon,
        'install_parameters': install_parameters,
        'integration_public': integration_public,
        'integration_requires_code_grant': integration_requires_code_grant,
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
    
    application = Application.precreate(application_id, **keyword_parameters,)
    vampytest.assert_eq(application, application)
    vampytest.assert_ne(application, object())
    
    test_application = Application(**keyword_parameters)
    vampytest.assert_eq(application, test_application)
    vampytest.assert_eq(application, application)
    
    for field_name, field_value in (
        ('aliases', None),
        ('approximate_guild_count', 26),
        ('bot_public', False),
        ('bot_requires_code_grant', False),
        ('cover', None),
        ('creator_monetization_state', ApplicationMonetizationState.approved),
        ('custom_install_url', None),
        ('deeplink_url', None),
        ('description', None),
        ('developers', None),
        ('discoverability_state', ApplicationDiscoverabilityState.featurable),
        ('discovery_eligibility_flags', ApplicationDiscoveryEligibilityFlags(10)),
        ('embedded_activity_configuration', None),
        ('eula_id', 0),
        ('executables', None),
        ('explicit_content_filter_level', ApplicationExplicitContentFilterLevel.none),
        ('flags', ApplicationFlag(2)),
        ('guild_id', 0),
        ('hook', False),
        ('icon', None),
        ('install_parameters', None),
        ('integration_public', False),
        ('integration_requires_code_grant', False),
        ('interaction_endpoint_url', None),
        ('interaction_event_types', None),
        ('interaction_version', ApplicationInteractionVersion.every),
        ('internal_guild_restriction', ApplicationInternalGuildRestriction.none),
        ('max_participants', 0),
        ('monetization_eligibility_flags', ApplicationMonetizationEligibilityFlags(18)),
        ('monetization_state', ApplicationMonetizationState.approved),
        ('monetized', False),
        ('name', 'Kagerou'),
        ('overlay', False),
        ('overlay_compatibility_hook', False),
        ('overlay_method_flags', ApplicationOverlayMethodFlags(27)),
        ('owner', None),
        ('primary_sku_id', 0),
        ('privacy_policy_url', None),
        ('publishers', None),
        ('redirect_urls', None),
        ('role_connection_verification_url', None),
        ('rpc_origins', None),
        ('rpc_state', ApplicationRPCState.submitted),
        ('slug', None),
        ('splash', None),
        ('store_state', ApplicationStoreState.submitted),
        ('tags', None),
        ('terms_of_service_url', None),
        ('third_party_skus', None),
        ('application_type', ApplicationType.music),
        ('verification_state', ApplicationVerificationState.submitted),
        ('verify_key', None),
    ):
        test_application = Application(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(application, test_application)
