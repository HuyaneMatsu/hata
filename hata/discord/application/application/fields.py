__all__ = ()

from ...field_parsers import (
    bool_parser_factory, default_entity_parser_factory, entity_id_parser_factory, flag_parser_factory,
    force_string_parser_factory, int_postprocess_parser_factory, nullable_entity_array_parser_factory,
    nullable_string_array_parser_factory, nullable_string_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, entity_id_putter_factory,
    flag_optional_putter_factory, force_string_putter_factory, int_optional_postprocess_putter_factory,
    nullable_entity_array_putter_factory, nullable_entity_optional_putter_factory,
    nullable_string_array_optional_putter_factory, nullable_string_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, default_entity_validator, entity_id_validator_factory, flag_validator_factory,
    force_string_validator_factory, int_conditional_validator_factory, nullable_entity_array_validator_factory,
    nullable_string_array_validator_factory, nullable_string_validator_factory, preinstanced_validator_factory,
    url_array_optional_validator_factory, url_optional_validator_factory
)
from ...guild import Guild
from ...user import ClientUserBase, User, ZEROUSER

from ..application_entity import ApplicationEntity
from ..application_executable import ApplicationExecutable
from ..application_install_parameters import ApplicationInstallParameters
from ..eula import EULA
from ..team import Team
from ..third_party_sku import ThirdPartySKU

from .constants import (
    BOT_PUBLIC_DEFAULT, BOT_REQUIRE_CODE_GRANT_DEFAULT, DESCRIPTION_LENGTH_MAX, HOOK_DEFAULT, MAX_PARTICIPANTS_DEFAULT,
    NAME_LENGTH_MAX, NAME_LENGTH_MIN, OVERLAY_COMPATIBILITY_HOOK_DEFAULT, OVERLAY_DEFAULT
)
from .flags import ApplicationFlag
from .preinstanced import ApplicationType

# aliases

parse_aliases = nullable_string_array_parser_factory('aliases')
put_aliases_into = nullable_string_array_optional_putter_factory('aliases')
validate_aliases = nullable_string_array_validator_factory('aliases')

# bot_public

parse_bot_public = bool_parser_factory('bot_public', BOT_PUBLIC_DEFAULT)
put_bot_public_into = bool_optional_putter_factory('bot_public', BOT_PUBLIC_DEFAULT)
validate_bot_public = bool_validator_factory('bot_public')

# bot_require_code_grant

parse_bot_require_code_grant = bool_parser_factory('bot_require_code_grant', BOT_REQUIRE_CODE_GRANT_DEFAULT)
put_bot_require_code_grant_into = bool_optional_putter_factory('bot_require_code_grant', BOT_REQUIRE_CODE_GRANT_DEFAULT)
validate_bot_require_code_grant = bool_validator_factory('bot_require_code_grant')

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

# eula_id

parse_eula_id = entity_id_parser_factory('eula_id')
put_eula_id_into = entity_id_optional_putter_factory('eula_id')
validate_eula_id = entity_id_validator_factory('eula_id', EULA)

# executables

parse_executables = nullable_entity_array_parser_factory('executables', ApplicationExecutable)
put_executables_into = nullable_entity_array_putter_factory('executables', ApplicationExecutable)
validate_executables = nullable_entity_array_validator_factory('executables', ApplicationExecutable)

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
validate_hook = bool_validator_factory('hook')

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('application_id')

# install_parameters

parse_install_parameters = default_entity_parser_factory('install_params', ApplicationInstallParameters, None)
put_install_parameters_into = nullable_entity_optional_putter_factory('install_params', ApplicationInstallParameters)
validate_install_parameters = default_entity_validator('install_parameters', ApplicationInstallParameters, None)

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

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

# overlay

parse_overlay = bool_parser_factory('overlay', OVERLAY_DEFAULT)
put_overlay_into = bool_optional_putter_factory('overlay', OVERLAY_DEFAULT)
validate_overlay = bool_validator_factory('overlay')

# overlay_compatibility_hook

parse_overlay_compatibility_hook = bool_parser_factory('overlay_compatibility_hook', OVERLAY_COMPATIBILITY_HOOK_DEFAULT)
put_overlay_compatibility_hook_into = bool_optional_putter_factory(
    'overlay_compatibility_hook', OVERLAY_COMPATIBILITY_HOOK_DEFAULT
)
validate_overlay_compatibility_hook = bool_validator_factory('overlay_compatibility_hook')

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
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
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
            f'got {owner.__class__.__name__}; {owner!r}'
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

# role_connection_verification_url

parse_role_connection_verification_url = nullable_string_parser_factory('role_connections_verification_url')
put_role_connection_verification_url_into = url_optional_putter_factory('role_connections_verification_url')
validate_role_connection_verification_url = url_optional_validator_factory('role_connection_verification_url')

# rpc_origins

parse_rpc_origins = nullable_string_array_parser_factory('rpc_origins')
put_rpc_origins_into = nullable_string_array_optional_putter_factory('rpc_origins')
validate_rpc_origins = url_array_optional_validator_factory('rpc_origins')

# slug

parse_slug = nullable_string_parser_factory('slug')
put_slug_into = url_optional_putter_factory('slug')
validate_slug = url_optional_validator_factory('slug')

# tags

parse_tags = nullable_string_array_parser_factory('tags')
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
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if application_type is ApplicationType.none:
        value = None
    else:
        value = application_type.value
    
    data['type'] = value
    return data


validate_type = preinstanced_validator_factory('application_type', ApplicationType)

# verify_key

parse_verify_key = nullable_string_parser_factory('verify_key')
put_verify_key_into = nullable_string_putter_factory('verify_key')
validate_verify_key = nullable_string_validator_factory('verify_key', 0, 1024)
