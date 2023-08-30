import vampytest

from ....bases import Icon, IconType
from ....user import User

from ...application_entity import ApplicationEntity
from ...application_executable import ApplicationExecutable
from ...application_install_parameters import ApplicationInstallParameters
from ...third_party_sku import ThirdPartySKU

from ..application import Application
from ..flags import ApplicationFlag
from ..preinstanced import ApplicationType

from .test__Application__constructor import _assert_fields_set


def test__Application__copy():
    """
    Tests whether ``Application.copy`` works as intended.
    """
    aliases = ['orin', 'rin']
    bot_public = True
    bot_require_code_grant = True
    cover = Icon(IconType.static, 23)
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290072, name = 'BrainDead')]
    eula_id = 202211290073
    executables = [ApplicationExecutable(name = 'Okuu')]
    flags = ApplicationFlag(96)
    guild_id = 202211290074
    hook = True
    install_parameters = ApplicationInstallParameters(permissions = 8)
    icon = Icon(IconType.static, 12)
    max_participants = 23
    name = 'Kaenbyou Rin'
    overlay = True
    overlay_compatibility_hook = True
    owner = User.precreate(202211290075)
    primary_sku_id = 202211290076
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290077, name = 'Brain')]
    role_connection_verification_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    slug = 'https://orindance.party/'
    splash = Icon(IconType.static, 66)
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    third_party_skus = [ThirdPartySKU(distributor = 'Dead')]
    application_type = ApplicationType.game
    verify_key = 'hell'
    
    application = Application(
        aliases = aliases,
        bot_public = bot_public,
        bot_require_code_grant = bot_require_code_grant,
        cover = cover,
        custom_install_url = custom_install_url,
        deeplink_url = deeplink_url,
        description = description,
        developers = developers,
        eula_id = eula_id,
        executables = executables,
        flags = flags,
        guild_id = guild_id,
        hook = hook,
        install_parameters = install_parameters,
        icon = icon,
        max_participants = max_participants,
        name = name,
        overlay = overlay,
        overlay_compatibility_hook = overlay_compatibility_hook,
        owner = owner,
        primary_sku_id = primary_sku_id,
        privacy_policy_url = privacy_policy_url,
        publishers = publishers,
        role_connection_verification_url = role_connection_verification_url,
        rpc_origins = rpc_origins,
        slug = slug,
        splash = splash,
        tags = tags,
        terms_of_service_url = terms_of_service_url,
        third_party_skus = third_party_skus,
        application_type = application_type,
        verify_key = verify_key,
    )
    
    copy = application.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(application, copy)


def test__Application__copy_with__0():
    """
    Tests whether ``Application.copy_with`` works as intended.
    
    Case: No parameters.
    """
    aliases = ['orin', 'rin']
    bot_public = True
    bot_require_code_grant = True
    cover = Icon(IconType.static, 23)
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290077, name = 'BrainDead')]
    eula_id = 202211290078
    executables = [ApplicationExecutable(name = 'Okuu')]
    flags = ApplicationFlag(96)
    guild_id = 202211290079
    hook = True
    install_parameters = ApplicationInstallParameters(permissions = 8)
    icon = Icon(IconType.static, 12)
    max_participants = 23
    name = 'Kaenbyou Rin'
    overlay = True
    overlay_compatibility_hook = True
    owner = User.precreate(202211290080)
    primary_sku_id = 202211290081
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290082, name = 'Brain')]
    role_connection_verification_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    slug = 'https://orindance.party/'
    splash = Icon(IconType.static, 66)
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    third_party_skus = [ThirdPartySKU(distributor = 'Dead')]
    application_type = ApplicationType.game
    verify_key = 'hell'
    
    application = Application(
        aliases = aliases,
        bot_public = bot_public,
        bot_require_code_grant = bot_require_code_grant,
        cover = cover,
        custom_install_url = custom_install_url,
        deeplink_url = deeplink_url,
        description = description,
        developers = developers,
        eula_id = eula_id,
        executables = executables,
        flags = flags,
        guild_id = guild_id,
        hook = hook,
        install_parameters = install_parameters,
        icon = icon,
        max_participants = max_participants,
        name = name,
        overlay = overlay,
        overlay_compatibility_hook = overlay_compatibility_hook,
        owner = owner,
        primary_sku_id = primary_sku_id,
        privacy_policy_url = privacy_policy_url,
        publishers = publishers,
        role_connection_verification_url = role_connection_verification_url,
        rpc_origins = rpc_origins,
        slug = slug,
        splash = splash,
        tags = tags,
        terms_of_service_url = terms_of_service_url,
        third_party_skus = third_party_skus,
        application_type = application_type,
        verify_key = verify_key,
    )
    
    copy = application.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(application, copy)
    vampytest.assert_eq(application, copy)


def test__Application__copy_with__1():
    """
    Tests whether ``Application.copy_with`` works as intended.
    
    Case: All parameters.
    """
    old_aliases = ['orin', 'rin']
    new_aliases = ['nue']
    old_bot_public = True
    new_bot_public = False
    old_bot_require_code_grant = True
    new_bot_require_code_grant = False
    old_cover = Icon(IconType.static, 23)
    new_cover = Icon(IconType.static, 33)
    old_custom_install_url = 'https://orindance.party/'
    new_custom_install_url = 'https://www.astil.dev/project/hata/'
    old_deeplink_url = 'https://orindance.party/'
    new_deeplink_url = 'https://www.astil.dev/project/hata/'
    old_description = 'dancing'
    new_description = 'flying'
    old_developers = [ApplicationEntity.precreate(202211290083, name = 'BrainDead')]
    new_developers = [ApplicationEntity.precreate(202211290084, name = 'Nekosia')]
    old_eula_id = 202211290085
    new_eula_id = 202211290086
    old_executables = [ApplicationExecutable(name = 'Okuu')]
    new_executables = [ApplicationExecutable(name = 'Nue')]
    old_flags = ApplicationFlag(96)
    new_flags = ApplicationFlag(2)
    old_guild_id = 202211290087
    new_guild_id = 202211290088
    old_hook = True
    new_hook = False
    old_install_parameters = ApplicationInstallParameters(permissions = 8)
    new_install_parameters = ApplicationInstallParameters(permissions = 16)
    old_icon = Icon(IconType.static, 12)
    new_icon = Icon(IconType.static, 99)
    old_max_participants = 23
    new_max_participants = 11
    old_name = 'Kaenbyou Rin'
    new_name = 'Houjuu Nue'
    old_overlay = True
    new_overlay = False
    old_overlay_compatibility_hook = True
    new_overlay_compatibility_hook = False
    old_owner = User.precreate(202211290089)
    new_owner = User.precreate(202211290090)
    old_primary_sku_id = 202211290091
    new_primary_sku_id = 202211290092
    old_privacy_policy_url = 'https://orindance.party/'
    new_privacy_policy_url = 'https://www.astil.dev/project/hata/'
    old_publishers = [ApplicationEntity.precreate(202211290093, name = 'Brain')]
    new_publishers = [ApplicationEntity.precreate(202211290094, name = 'Neko')]
    old_role_connection_verification_url = 'https://orindance.party/'
    new_role_connection_verification_url = 'https://www.astil.dev/project/hata/'
    old_rpc_origins = ['https://orindance.party/']
    new_rpc_origins = ['https://www.astil.dev/project/hata/']
    old_slug = 'https://orindance.party/'
    new_slug = 'https://www.astil.dev/project/hata/'
    old_splash = Icon(IconType.static, 66)
    new_splash = Icon(IconType.animated, 66)
    old_tags = ['cat']
    new_tags = ['alien', 'lovely']
    old_terms_of_service_url = 'https://orindance.party/'
    new_terms_of_service_url = 'https://www.astil.dev/project/hata/'
    old_third_party_skus = [ThirdPartySKU(distributor = 'Dead')]
    new_third_party_skus = [ThirdPartySKU(distributor = 'Sia')]
    old_application_type = ApplicationType.game
    new_application_type = ApplicationType.music
    old_verify_key = 'hell'
    new_verify_key = 'space'
    
    application = Application(
        aliases = old_aliases,
        bot_public = old_bot_public,
        bot_require_code_grant = old_bot_require_code_grant,
        cover = old_cover,
        custom_install_url = old_custom_install_url,
        deeplink_url = old_deeplink_url,
        description = old_description,
        developers = old_developers,
        eula_id = old_eula_id,
        executables = old_executables,
        flags = old_flags,
        guild_id = old_guild_id,
        hook = old_hook,
        install_parameters = old_install_parameters,
        icon = old_icon,
        max_participants = old_max_participants,
        name = old_name,
        overlay = old_overlay,
        overlay_compatibility_hook = old_overlay_compatibility_hook,
        owner = old_owner,
        primary_sku_id = old_primary_sku_id,
        privacy_policy_url = old_privacy_policy_url,
        publishers = old_publishers,
        role_connection_verification_url = old_role_connection_verification_url,
        rpc_origins = old_rpc_origins,
        slug = old_slug,
        splash = old_splash,
        tags = old_tags,
        terms_of_service_url = old_terms_of_service_url,
        third_party_skus = old_third_party_skus,
        application_type = old_application_type,
        verify_key = old_verify_key,
    )
    
    copy = application.copy_with(
        aliases = new_aliases,
        bot_public = new_bot_public,
        bot_require_code_grant = new_bot_require_code_grant,
        cover = new_cover,
        custom_install_url = new_custom_install_url,
        deeplink_url = new_deeplink_url,
        description = new_description,
        developers = new_developers,
        eula_id = new_eula_id,
        executables = new_executables,
        flags = new_flags,
        guild_id = new_guild_id,
        hook = new_hook,
        install_parameters = new_install_parameters,
        icon = new_icon,
        max_participants = new_max_participants,
        name = new_name,
        overlay = new_overlay,
        overlay_compatibility_hook = new_overlay_compatibility_hook,
        owner = new_owner,
        primary_sku_id = new_primary_sku_id,
        privacy_policy_url = new_privacy_policy_url,
        publishers = new_publishers,
        role_connection_verification_url = new_role_connection_verification_url,
        rpc_origins = new_rpc_origins,
        slug = new_slug,
        splash = new_splash,
        tags = new_tags,
        terms_of_service_url = new_terms_of_service_url,
        third_party_skus = new_third_party_skus,
        application_type = new_application_type,
        verify_key = new_verify_key,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(application, copy)
    
    vampytest.assert_eq(copy.aliases, tuple(new_aliases))
    vampytest.assert_eq(copy.bot_public, new_bot_public)
    vampytest.assert_eq(copy.bot_require_code_grant, new_bot_require_code_grant)
    vampytest.assert_eq(copy.cover, new_cover)
    vampytest.assert_eq(copy.custom_install_url, new_custom_install_url)
    vampytest.assert_eq(copy.deeplink_url, new_deeplink_url)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.developers, tuple(new_developers))
    vampytest.assert_eq(copy.eula_id, new_eula_id)
    vampytest.assert_eq(copy.executables, tuple(new_executables))
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.hook, new_hook)
    vampytest.assert_eq(copy.install_parameters, new_install_parameters)
    vampytest.assert_eq(copy.icon, new_icon)
    vampytest.assert_eq(copy.max_participants, new_max_participants)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.overlay, new_overlay)
    vampytest.assert_eq(copy.overlay_compatibility_hook, new_overlay_compatibility_hook)
    vampytest.assert_eq(copy.owner, new_owner)
    vampytest.assert_eq(copy.primary_sku_id, new_primary_sku_id)
    vampytest.assert_eq(copy.privacy_policy_url, new_privacy_policy_url)
    vampytest.assert_eq(copy.publishers, tuple(new_publishers))
    vampytest.assert_eq(copy.role_connection_verification_url, new_role_connection_verification_url)
    vampytest.assert_eq(copy.rpc_origins, tuple(new_rpc_origins))
    vampytest.assert_eq(copy.slug, new_slug)
    vampytest.assert_eq(copy.splash, new_splash)
    vampytest.assert_eq(copy.tags, tuple(new_tags))
    vampytest.assert_eq(copy.terms_of_service_url, new_terms_of_service_url)
    vampytest.assert_eq(copy.third_party_skus, tuple(new_third_party_skus))
    vampytest.assert_is(copy.type, new_application_type)
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
    
    
def test__Application__iter_aliases():
    """
    Tests whether ``Application.iter_aliases`` works as intended.
    """
    alias_0 = 'Koishi'
    alias_1 = 'Komeiji'
    
    for input_value, expected_output in (
        (None, []),
        ([alias_0], [alias_0]),
        ([alias_0, alias_1], [alias_0, alias_1]),
    ):
        application = Application(aliases = input_value)
        vampytest.assert_eq([*application.iter_aliases()], expected_output)


def test__Application__iter_developers():
    """
    Tests whether ``Application.iter_developers`` works as intended.
    """
    developer_0 = ApplicationEntity.precreate(202211290096, name = 'Suika')
    developer_1 = ApplicationEntity.precreate(202211290097, name = 'Yuugi')
    
    for input_value, expected_output in (
        (None, []),
        ([developer_0], [developer_0]),
        ([developer_0, developer_1], [developer_0, developer_1]),
    ):
        application = Application(developers = input_value)
        vampytest.assert_eq([*application.iter_developers()], expected_output)


def test__Application__iter_executables():
    """
    Tests whether ``Application.iter_executables`` works as intended.
    """
    executable_0 = ApplicationExecutable(name = 'pudding', launcher = False)
    executable_1 = ApplicationExecutable(name = 'pudding', launcher = True)
    
    for input_value, expected_output in (
        (None, []),
        ([executable_0], [executable_0]),
        ([executable_0, executable_1], [executable_0, executable_1]),
    ):
        application = Application(executables = input_value)
        vampytest.assert_eq([*application.iter_executables()], expected_output)


def test__Application__iter_publishers():
    """
    Tests whether ``Application.iter_publishers`` works as intended.
    """
    publisher_0 = ApplicationEntity.precreate(202211290098, name = 'Suika')
    publisher_1 = ApplicationEntity.precreate(202211290099, name = 'Yuugi')
    
    for input_value, expected_output in (
        (None, []),
        ([publisher_0], [publisher_0]),
        ([publisher_0, publisher_1], [publisher_0, publisher_1]),
    ):
        application = Application(publishers = input_value)
        vampytest.assert_eq([*application.iter_publishers()], expected_output)


def test__Application__iter_rpc_origins():
    """
    Tests whether ``Application.iter_rpc_origins`` works as intended.
    """
    rpc_origin_0 = 'https://orindance.party/'
    rpc_origin_1 = 'https://www.astil.dev/project/hata/'
    
    for input_value, expected_output in (
        (None, []),
        ([rpc_origin_0], [rpc_origin_0]),
        ([rpc_origin_0, rpc_origin_1], [rpc_origin_0, rpc_origin_1]),
    ):
        application = Application(rpc_origins = input_value)
        vampytest.assert_eq([*application.iter_rpc_origins()], expected_output)


def test__Application__iter_tags():
    """
    Tests whether ``Application.iter_tags`` works as intended.
    """
    tag_0 = 'Koishi'
    tag_1 = 'Komeiji'
    
    for input_value, expected_output in (
        (None, []),
        ([tag_0], [tag_0]),
        ([tag_0, tag_1], [tag_0, tag_1]),
    ):
        application = Application(tags = input_value)
        vampytest.assert_eq([*application.iter_tags()], expected_output)


def test__Application__iter_third_party_skus():
    """
    Tests whether ``Application.iter_third_party_skus`` works as intended.
    """
    third_party_sku_0 = ThirdPartySKU(distributor = 'Suika')
    third_party_sku_1 = ThirdPartySKU(distributor = 'Yuugi')
    
    for input_value, expected_output in (
        (None, []),
        ([third_party_sku_0], [third_party_sku_0]),
        ([third_party_sku_0, third_party_sku_1], [third_party_sku_0, third_party_sku_1]),
    ):
        application = Application(third_party_skus = input_value)
        vampytest.assert_eq([*application.iter_third_party_skus()], expected_output)
