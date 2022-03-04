__all__ = ()

from .....env import API_VERSION

from ....permission import PermissionOverwriteTargetType

from .shared import _convert_preinstanced, convert_deprecated, convert_permission, convert_snowflake


def convert_permission_overwrite_target_type(name, data):
    return _convert_preinstanced('target_type', data, PermissionOverwriteTargetType)


def convert_snowflake__target_id(name, data):
    return convert_snowflake('target_id', data)


CHANNEL_PERMISSION_OVERWRITE_CONVERTERS = {
    'allow': convert_deprecated if API_VERSION in (6, 7) else convert_permission,
    'allow_new': convert_permission if API_VERSION in (6, 7) else convert_deprecated,
    'deny': convert_deprecated if API_VERSION in (6, 7) else convert_permission,
    'deny_new': convert_permission if API_VERSION in (6, 7) else convert_deprecated,
    'id': convert_snowflake__target_id,
    'type': convert_permission_overwrite_target_type,
}
