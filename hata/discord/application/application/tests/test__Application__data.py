import warnings as module_warnings

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

from .test__Application__constructor import _assert_is_every_attribute_set


def test__Application__from_data__0():
    """
    Tests whether `Application.from_data`` works as intended.
    
    Case: Warning & attributes.
    """
    application_id = 202211290015
    
    data = {
        'id': str(application_id),
    }
    
    with module_warnings.catch_warnings(record = True) as warnings:
        module_warnings.simplefilter('always')
        
        application = Application.from_data(data)
        _assert_is_every_attribute_set(application)
        vampytest.assert_eq(application.id, application_id)
        
        vampytest.assert_eq(len(warnings), 1)


def test__Application__from_data__1():
    """
    Tests whether `Application.from_data`` works as intended.
    
    Case: Caching.
    """
    application_id = 202211290016
    
    data = {
        'id': application_id,
    }
    
    with module_warnings.catch_warnings():
        module_warnings.simplefilter('ignore')
        
        application = Application.from_data(data)
        test_application = Application.from_data(data)
        
        vampytest.assert_is(application, test_application)


def test__Application__from_data_ready__0():
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
    _assert_is_every_attribute_set(application)
    vampytest.assert_eq(application.id, application_id)
    
    vampytest.assert_eq(application.flags, flags)


def test__Application__from_data_ready__1():
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


def test__Application__from_data_ready__2():
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


def test__Application__from_data_ready__3():
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


def test__Application__from_data_own__0():
    """
    Tests whether ``Application.from_data_own`` works as intended.
    
    Case: Attributes.
    """
    application_id = 202211290019
    
    bot_public = True
    bot_require_code_grant = True
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
    
    custom_install_url = 'https://orindance.party/'
    guild_id = 202211290020
    install_parameters = ApplicationInstallParameters(permissions = 8)
    owner = User.precreate(202211290021)
    primary_sku_id = 202211290022
    role_connection_verification_url = 'https://orindance.party/'
    slug = 'https://orindance.party/'
    
    data = {
        'id': str(application_id),
        'bot_public': bot_public,
        'bot_require_code_grant': bot_require_code_grant,
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
        
        'custom_install_url': custom_install_url,
        'guild_id': str(guild_id),
        'install_params': install_parameters.to_data(defaults = True),
        'owner': owner.to_data(defaults = True, include_internals = True),
        'team': None,
        'primary_sku_id': str(primary_sku_id),
        'role_connections_verification_url': role_connection_verification_url,
        'slug': slug,
    }
    
    application = Application.from_data_own(data)
    _assert_is_every_attribute_set(application)
    vampytest.assert_eq(application.id, application_id)
    
    vampytest.assert_eq(application.bot_public, bot_public)
    vampytest.assert_eq(application.bot_require_code_grant, bot_require_code_grant)
    vampytest.assert_eq(application.cover, cover)
    vampytest.assert_eq(application.custom_install_url, custom_install_url)
    vampytest.assert_eq(application.description, description)
    vampytest.assert_eq(application.flags, flags)
    vampytest.assert_eq(application.guild_id, guild_id)
    vampytest.assert_eq(application.hook, hook)
    vampytest.assert_eq(application.install_parameters, install_parameters)
    vampytest.assert_eq(application.icon, icon)
    vampytest.assert_eq(application.name, name)
    vampytest.assert_eq(application.owner, owner)
    vampytest.assert_eq(application.primary_sku_id, primary_sku_id)
    vampytest.assert_eq(application.privacy_policy_url, privacy_policy_url)
    vampytest.assert_eq(application.role_connection_verification_url, role_connection_verification_url)
    vampytest.assert_eq(application.rpc_origins, tuple(rpc_origins))
    vampytest.assert_eq(application.slug, slug)
    vampytest.assert_eq(application.splash, splash)
    vampytest.assert_eq(application.tags, tuple(tags))
    vampytest.assert_eq(application.terms_of_service_url, terms_of_service_url)
    vampytest.assert_is(application.type, application_type)
    vampytest.assert_eq(application.verify_key, verify_key)


def test__Application__from_data_own__1():
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


def test__Application__from_data_own__2():
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


def test__Application__from_data_own__3():
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


def test__Application__from_data_invite__0():
    """
    Tests whether ``Application.from_data_invite`` works as intended.
    
    Case: Attributes.
    """
    application_id = 202211290024
    
    bot_public = True
    bot_require_code_grant = True
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
    
    max_participants = 23
    
    data = {
        'id': str(application_id),
        'bot_public': bot_public,
        'bot_require_code_grant': bot_require_code_grant,
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
        
        'max_participants': max_participants,
    }
    
    application = Application.from_data_invite(data)
    _assert_is_every_attribute_set(application)
    vampytest.assert_eq(application.id, application_id)
    
    vampytest.assert_eq(application.bot_public, bot_public)
    vampytest.assert_eq(application.bot_require_code_grant, bot_require_code_grant)
    vampytest.assert_eq(application.cover, cover)
    vampytest.assert_eq(application.description, description)
    vampytest.assert_eq(application.flags, flags)
    vampytest.assert_eq(application.hook, hook)
    vampytest.assert_eq(application.icon, icon)
    vampytest.assert_eq(application.max_participants, max_participants)
    vampytest.assert_eq(application.name, name)
    vampytest.assert_eq(application.privacy_policy_url, privacy_policy_url)
    vampytest.assert_eq(application.rpc_origins, tuple(rpc_origins))
    vampytest.assert_eq(application.splash, splash)
    vampytest.assert_eq(application.tags, tuple(tags))
    vampytest.assert_eq(application.terms_of_service_url, terms_of_service_url)
    vampytest.assert_is(application.type, application_type)
    vampytest.assert_eq(application.verify_key, verify_key)


def test__Application__from_data_invite__1():
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


def test__Application__from_data_detectable__0():
    """
    Tests whether ``Application.from_data_detectable`` works as intended.
    
    Case: Attributes.
    """
    application_id = 202211290032
    
    bot_public = True
    bot_require_code_grant = True
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
    primary_sku_id = 202211290036
    publishers = [ApplicationEntity.precreate(202211290037, name = 'Brain')]
    slug = 'https://orindance.party/'
    third_party_skus = [ThirdPartySKU(distributor = 'Dead')]
    
    data = {
        'id': str(application_id),
        'bot_public': bot_public,
        'bot_require_code_grant': bot_require_code_grant,
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
        'primary_sku_id': str(primary_sku_id),
        'publishers': [publisher.to_data(defaults = True, include_internals = True) for publisher in publishers],
        'slug': slug,
        'third_party_skus': [third_party_sku.to_data(defaults = True) for third_party_sku in third_party_skus]
    }
    
    application = Application.from_data_detectable(data)
    _assert_is_every_attribute_set(application)
    vampytest.assert_eq(application.id, application_id)
    
    vampytest.assert_eq(application.aliases, tuple(aliases))
    vampytest.assert_eq(application.bot_public, bot_public)
    vampytest.assert_eq(application.bot_require_code_grant, bot_require_code_grant)
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


def test__Application__from_data_detectable__1():
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


def test__Application__to_data():
    """
    Tests whether `Application.to_data`` works as intended.
    
    Case: warning & defaults & internals
    """
    application_id = 202211290039
    
    application = Application.precreate(
        application_id
    )
    
    with module_warnings.catch_warnings(record = True) as warnings:
        module_warnings.simplefilter('always')
        
        data = application.to_data(defaults = True, include_internals = True)
        
        vampytest.assert_eq(len(warnings), 1)
    
    vampytest.assert_in('id', data)
    vampytest.assert_eq(data['id'], str(application_id))


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
    
    bot_public = True
    bot_require_code_grant = True
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
    
    custom_install_url = 'https://orindance.party/'
    guild_id = 202211290042
    install_parameters = ApplicationInstallParameters(permissions = 8)
    owner = User.precreate(202211290043)
    primary_sku_id = 202211290044
    role_connection_verification_url = 'https://orindance.party/'
    slug = 'https://orindance.party/'
    
    application = Application.precreate(
        application_id,
        bot_public = bot_public,
        bot_require_code_grant = bot_require_code_grant,
        cover = cover,
        custom_install_url = custom_install_url,
        description = description,
        flags = flags,
        guild_id = guild_id,
        hook = hook,
        install_parameters = install_parameters,
        icon = icon,
        name = name,
        owner = owner,
        primary_sku_id = primary_sku_id,
        privacy_policy_url = privacy_policy_url,
        role_connection_verification_url = role_connection_verification_url,
        rpc_origins = rpc_origins,
        slug = slug,
        splash = splash,
        tags = tags,
        terms_of_service_url = terms_of_service_url,
        application_type = application_type,
        verify_key = verify_key,
    )
    
    expected_data = {
        'id': str(application_id),
        'bot_public': bot_public,
        'bot_require_code_grant': bot_require_code_grant,
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
        
        'custom_install_url': custom_install_url,
        'guild_id': str(guild_id),
        'install_params': install_parameters.to_data(defaults = True),
        'owner': owner.to_data(defaults = True, include_internals = True),
        'team': None,
        'primary_sku_id': str(primary_sku_id),
        'role_connections_verification_url': role_connection_verification_url,
        'slug': slug,
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
    bot_require_code_grant = True
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
    
    max_participants = 23
    
    application = Application.precreate(
        application_id,
        bot_public = bot_public,
        bot_require_code_grant = bot_require_code_grant,
        cover = cover,
        description = description,
        flags = flags,
        hook = hook,
        icon = icon,
        max_participants = max_participants,
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
        'bot_require_code_grant': bot_require_code_grant,
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
        
        'max_participants': max_participants,
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
    bot_require_code_grant = True
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
        bot_require_code_grant = bot_require_code_grant,
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
        'bot_require_code_grant': bot_require_code_grant,
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
        'primary_sku_id': str(primary_sku_id),
        'publishers': [publisher.to_data(defaults = True, include_internals = True) for publisher in publishers],
        'slug': slug,
        'third_party_skus': [third_party_sku.to_data(defaults = True) for third_party_sku in third_party_skus]
    }
    
    vampytest.assert_eq(
        application.to_data_detectable(defaults = True, include_internals = True),
        expected_data,
    )
