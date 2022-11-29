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


def test__Application__repr():
    """
    Tests whether ``Application.__repr__`` works as intended.
    """
    application_id = 202211290051
    
    aliases = ['orin', 'rin']
    bot_public = True
    bot_require_code_grant = True
    cover = Icon(IconType.static, 23)
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290071, name = 'BrainDead')]
    eula_id = 202211290052
    executables = [ApplicationExecutable(name = 'Okuu')]
    flags = ApplicationFlag(96)
    guild_id = 202211290053
    hook = True
    install_parameters = ApplicationInstallParameters(permissions = 8)
    icon = Icon(IconType.static, 12)
    max_participants = 23
    name = 'Kaenbyou Rin'
    overlay = True
    overlay_compatibility_hook = True
    owner = User.precreate(202211290054)
    primary_sku_id = 202211290055
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290056, name = 'Brain')]
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
    
    vampytest.assert_instance(repr(application), str)
    
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
    
    vampytest.assert_instance(repr(application), str)


def test__Application__hash():
    """
    Tests whether ``Application.__hash__`` works as intended.
    """
    application_id = 202211290057
    
    aliases = ['orin', 'rin']
    bot_public = True
    bot_require_code_grant = True
    cover = Icon(IconType.static, 23)
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290058, name = 'BrainDead')]
    eula_id = 202211290059
    executables = [ApplicationExecutable(name = 'Okuu')]
    flags = ApplicationFlag(96)
    guild_id = 202211290060
    hook = True
    install_parameters = ApplicationInstallParameters(permissions = 8)
    icon = Icon(IconType.static, 12)
    max_participants = 23
    name = 'Kaenbyou Rin'
    overlay = True
    overlay_compatibility_hook = True
    owner = User.precreate(202211290061)
    primary_sku_id = 202211290062
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290063, name = 'Brain')]
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
    
    vampytest.assert_instance(hash(application), int)
    
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
    
    vampytest.assert_instance(hash(application), int)


def test__Application__eq():
    """
    Tests whether ``Application.__eq__`` works as intended.
    """
    application_id = 202211290064
    
    aliases = ['orin', 'rin']
    bot_public = True
    bot_require_code_grant = True
    cover = Icon(IconType.static, 23)
    custom_install_url = 'https://orindance.party/'
    deeplink_url = 'https://orindance.party/'
    description = 'dancing'
    developers = [ApplicationEntity.precreate(202211290065, name = 'BrainDead')]
    eula_id = 202211290066
    executables = [ApplicationExecutable(name = 'Okuu')]
    flags = ApplicationFlag(96)
    guild_id = 202211290067
    hook = True
    install_parameters = ApplicationInstallParameters(permissions = 8)
    icon = Icon(IconType.static, 12)
    max_participants = 23
    name = 'Kaenbyou Rin'
    overlay = True
    overlay_compatibility_hook = True
    owner = User.precreate(202211290068)
    primary_sku_id = 202211290069
    privacy_policy_url = 'https://orindance.party/'
    publishers = [ApplicationEntity.precreate(202211290070, name = 'Brain')]
    role_connection_verification_url = 'https://orindance.party/'
    rpc_origins = ['https://orindance.party/']
    slug = 'https://orindance.party/'
    splash = Icon(IconType.static, 66)
    tags = ['cat']
    terms_of_service_url = 'https://orindance.party/'
    third_party_skus = [ThirdPartySKU(distributor = 'Dead')]
    application_type = ApplicationType.game
    verify_key = 'hell'
    
    keyword_parameters = {
        'aliases': aliases,
        'bot_public': bot_public,
        'bot_require_code_grant': bot_require_code_grant,
        'cover': cover,
        'custom_install_url': custom_install_url,
        'deeplink_url': deeplink_url,
        'description': description,
        'developers': developers,
        'eula_id': eula_id,
        'executables': executables,
        'flags': flags,
        'guild_id': guild_id,
        'hook': hook,
        'install_parameters': install_parameters,
        'icon': icon,
        'max_participants': max_participants,
        'name': name,
        'overlay': overlay,
        'overlay_compatibility_hook': overlay_compatibility_hook,
        'owner': owner,
        'primary_sku_id': primary_sku_id,
        'privacy_policy_url': privacy_policy_url,
        'publishers': publishers,
        'role_connection_verification_url': role_connection_verification_url,
        'rpc_origins': rpc_origins,
        'slug': slug,
        'splash': splash,
        'tags': tags,
        'terms_of_service_url': terms_of_service_url,
        'third_party_skus': third_party_skus,
        'application_type': application_type,
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
        ('bot_public', False),
        ('bot_require_code_grant', False),
        ('cover', None),
        ('custom_install_url', None),
        ('deeplink_url', None),
        ('description', None),
        ('developers', None),
        ('eula_id', 0),
        ('executables', None),
        ('flags', ApplicationFlag(2)),
        ('guild_id', 0),
        ('hook', False),
        ('install_parameters', None),
        ('icon', None),
        ('max_participants', 0),
        ('name', 'Kagerou'),
        ('overlay', False),
        ('overlay_compatibility_hook', False),
        ('owner', None),
        ('primary_sku_id', 0),
        ('privacy_policy_url', None),
        ('publishers', None),
        ('role_connection_verification_url', None),
        ('rpc_origins', None),
        ('slug', None),
        ('splash', None),
        ('tags', None),
        ('terms_of_service_url', None),
        ('third_party_skus', None),
        ('application_type', ApplicationType.music),
        ('verify_key', None),
    ):
        test_application = Application(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(application, test_application)
