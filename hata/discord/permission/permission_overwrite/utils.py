__all__ = ()

from .fields.allow import validate_allow, put_allow_into
from .fields.deny import validate_deny, put_deny_into
from .fields.target import validate_target, put_target_into
from .fields.target_id import validate_target_id, put_target_id_into
from .fields.target_type import validate_target_type, put_target_type_into


PERMISSION_OVERWRITE_PERMISSION_FIELD_CONVERTERS = {
    'allow': (validate_allow, put_allow_into),
    'deny': (validate_deny, put_deny_into),
}


PERMISSION_OVERWRITE_FIELD_CONVERTERS = {
    **PERMISSION_OVERWRITE_PERMISSION_FIELD_CONVERTERS,
    'target': (validate_target, put_target_into),
    'target_id': (validate_target_id, put_target_id_into),
    'target_type': (validate_target_type, put_target_type_into),
}
