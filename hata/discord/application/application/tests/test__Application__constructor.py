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


def _assert_is_every_attribute_set(application):
    """
    Asserts whether every attributes are set of the given application.
    
    Parameters
    ----------
    application : ``Application``
        The application to check.
    """
    vampytest.assert_instance(application, Application)
    vampytest.assert_instance(application.aliases, tuple, nullable = True)
    vampytest.assert_instance(application.bot_public, bool)
    vampytest.assert_instance(application.bot_require_code_grant, bool)
    vampytest.assert_instance(application.cover, Icon)
    vampytest.assert_instance(application.custom_install_url, str, nullable = True)
    vampytest.assert_instance(application.deeplink_url, str, nullable = True)
    vampytest.assert_instance(application.description, str, nullable = True)
    vampytest.assert_instance(application.developers, tuple, nullable = True)
    vampytest.assert_instance(application.eula_id, int)
    vampytest.assert_instance(application.executables, tuple, nullable = True)
    vampytest.assert_instance(application.flags, ApplicationFlag)
    vampytest.assert_instance(application.guild_id, int)
    vampytest.assert_instance(application.hook, bool)
    vampytest.assert_instance(application.install_parameters, ApplicationInstallParameters, nullable = True)
    vampytest.assert_instance(application.icon, Icon)
    vampytest.assert_instance(application.id, int)
    vampytest.assert_instance(application.max_participants, int)
    vampytest.assert_instance(application.name, str)
    vampytest.assert_instance(application.overlay, bool)
    vampytest.assert_instance(application.overlay_compatibility_hook, bool)
    vampytest.assert_instance(application.owner, object)
    vampytest.assert_instance(application.primary_sku_id, int)
    vampytest.assert_instance(application.privacy_policy_url, str, nullable = True)
    vampytest.assert_instance(application.publishers, tuple, nullable = True)
    vampytest.assert_instance(application.role_connection_verification_url, str, nullable = True)
    vampytest.assert_instance(application.rpc_origins, tuple, nullable = True)
    vampytest.assert_instance(application.slug, str, nullable = True)
    vampytest.assert_instance(application.splash, Icon)
    vampytest.assert_instance(application.tags, tuple, nullable = True)
    vampytest.assert_instance(application.terms_of_service_url, str, nullable = True)
    vampytest.assert_instance(application.third_party_skus, tuple, nullable = True)
    vampytest.assert_instance(application.type, ApplicationType)
    vampytest.assert_instance(application.verify_key, str, nullable = True)


def test__Application__new__0():
    """
    Tests whether ``Application.__new__`` works as intended.
    
    Case: No parameters.
    """
    application = Application()
    _assert_is_every_attribute_set(application)


def test__Application__new__1():
    """
    Tests whether ``Application.__new__`` works as intended.
    
    Case: All parameters.
    """
    aliases = ['orin', 'rin']
    bot_public = True
    bot_require_code_grant = True
    cover = Icon(IconType.static, 23)
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290000, name = 'BrainDead')]
    eula_id = 202211290001
    executables = [ApplicationExecutable(name = 'Okuu')]
    flags = ApplicationFlag(96)
    guild_id = 202211290002
    hook = True
    install_parameters = ApplicationInstallParameters(permissions = 8)
    icon = Icon(IconType.static, 12)
    max_participants = 23
    name = 'Kaenbyou Rin'
    overlay = True
    overlay_compatibility_hook = True
    owner = User.precreate(202211290003)
    primary_sku_id = 202211290004
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290005, name = 'Brain')]
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
    _assert_is_every_attribute_set(application)
    
    vampytest.assert_eq(application.aliases, tuple(aliases))
    vampytest.assert_eq(application.bot_public, bot_public)
    vampytest.assert_eq(application.bot_require_code_grant, bot_require_code_grant)
    vampytest.assert_eq(application.cover, cover)
    vampytest.assert_eq(application.custom_install_url, custom_install_url)
    vampytest.assert_eq(application.deeplink_url, deeplink_url)
    vampytest.assert_eq(application.description, description)
    vampytest.assert_eq(application.developers, tuple(developers))
    vampytest.assert_eq(application.eula_id, eula_id)
    vampytest.assert_eq(application.executables, tuple(executables))
    vampytest.assert_eq(application.flags, flags)
    vampytest.assert_eq(application.guild_id, guild_id)
    vampytest.assert_eq(application.hook, hook)
    vampytest.assert_eq(application.install_parameters, install_parameters)
    vampytest.assert_eq(application.icon, icon)
    vampytest.assert_eq(application.max_participants, max_participants)
    vampytest.assert_eq(application.name, name)
    vampytest.assert_eq(application.overlay, overlay)
    vampytest.assert_eq(application.overlay_compatibility_hook, overlay_compatibility_hook)
    vampytest.assert_eq(application.owner, owner)
    vampytest.assert_eq(application.primary_sku_id, primary_sku_id)
    vampytest.assert_eq(application.privacy_policy_url, privacy_policy_url)
    vampytest.assert_eq(application.publishers, tuple(publishers))
    vampytest.assert_eq(application.role_connection_verification_url, role_connection_verification_url)
    vampytest.assert_eq(application.rpc_origins, tuple(rpc_origins))
    vampytest.assert_eq(application.slug, slug)
    vampytest.assert_eq(application.splash, splash)
    vampytest.assert_eq(application.tags, tuple(tags))
    vampytest.assert_eq(application.terms_of_service_url, terms_of_service_url)
    vampytest.assert_eq(application.third_party_skus, tuple(third_party_skus))
    vampytest.assert_is(application.type, application_type)
    vampytest.assert_eq(application.verify_key, verify_key)


def test__Application__precreate__0():
    """
    Tests whether ``Application.precreate`` works as intended.
    
    Case: No parameters.
    """
    application_id = 202211290006
    application = Application.precreate(application_id)
    _assert_is_every_attribute_set(application)
    vampytest.assert_eq(application.id, application_id)


def test__Application__precreate__1():
    """
    Tests whether ``Application.precreate`` works as intended.
    
    Case: All parameters.
    """
    application_id = 202211290007
    
    aliases = ['orin', 'rin']
    bot_public = True
    bot_require_code_grant = True
    cover = Icon(IconType.static, 23)
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290008, name = 'BrainDead')]
    eula_id = 202211290009
    executables = [ApplicationExecutable(name = 'Okuu')]
    flags = ApplicationFlag(96)
    guild_id = 202211290010
    hook = True
    install_parameters = ApplicationInstallParameters(permissions = 8)
    icon = Icon(IconType.static, 12)
    max_participants = 23
    name = 'Kaenbyou Rin'
    overlay = True
    overlay_compatibility_hook = True
    owner = User.precreate(202211290011)
    primary_sku_id = 202211290004
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290012, name = 'Brain')]
    role_connection_verification_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    slug = 'https://orindance.party/'
    splash = Icon(IconType.static, 66)
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    third_party_skus = [ThirdPartySKU(distributor = 'Dead')]
    application_type = ApplicationType.game
    verify_key = 'hell'
    
    application = Application.precreate(
        application_id,
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
    _assert_is_every_attribute_set(application)
    vampytest.assert_eq(application.id, application_id)
    
    vampytest.assert_eq(application.aliases, tuple(aliases))
    vampytest.assert_eq(application.bot_public, bot_public)
    vampytest.assert_eq(application.bot_require_code_grant, bot_require_code_grant)
    vampytest.assert_eq(application.cover, cover)
    vampytest.assert_eq(application.custom_install_url, custom_install_url)
    vampytest.assert_eq(application.deeplink_url, deeplink_url)
    vampytest.assert_eq(application.description, description)
    vampytest.assert_eq(application.developers, tuple(developers))
    vampytest.assert_eq(application.eula_id, eula_id)
    vampytest.assert_eq(application.executables, tuple(executables))
    vampytest.assert_eq(application.flags, flags)
    vampytest.assert_eq(application.guild_id, guild_id)
    vampytest.assert_eq(application.hook, hook)
    vampytest.assert_eq(application.install_parameters, install_parameters)
    vampytest.assert_eq(application.icon, icon)
    vampytest.assert_eq(application.max_participants, max_participants)
    vampytest.assert_eq(application.name, name)
    vampytest.assert_eq(application.overlay, overlay)
    vampytest.assert_eq(application.overlay_compatibility_hook, overlay_compatibility_hook)
    vampytest.assert_eq(application.owner, owner)
    vampytest.assert_eq(application.primary_sku_id, primary_sku_id)
    vampytest.assert_eq(application.privacy_policy_url, privacy_policy_url)
    vampytest.assert_eq(application.publishers, tuple(publishers))
    vampytest.assert_eq(application.role_connection_verification_url, role_connection_verification_url)
    vampytest.assert_eq(application.rpc_origins, tuple(rpc_origins))
    vampytest.assert_eq(application.slug, slug)
    vampytest.assert_eq(application.splash, splash)
    vampytest.assert_eq(application.tags, tuple(tags))
    vampytest.assert_eq(application.terms_of_service_url, terms_of_service_url)
    vampytest.assert_eq(application.third_party_skus, tuple(third_party_skus))
    vampytest.assert_is(application.type, application_type)
    vampytest.assert_eq(application.verify_key, verify_key)


def test__Application__precreate__2():
    """
    Tests whether ``Application.precreate`` works as intended.
    
    Case: No parameters.
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
    _assert_is_every_attribute_set(application)
    vampytest.assert_eq(application.id, application_id)
