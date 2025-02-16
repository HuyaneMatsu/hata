__all__ = ()

from functools import partial as partial_func

from .fields import (
    put_allow, put_deny, put_target_id, put_target, put_target_type, validate_allow,
    validate_deny, validate_target, validate_target_id, validate_target_type
)


PERMISSION_OVERWRITE_PERMISSION_FIELD_CONVERTERS = {
    'allow': (validate_allow, put_allow),
    'deny': (validate_deny, put_deny),
}


PERMISSION_OVERWRITE_FIELD_CONVERTERS = {
    **PERMISSION_OVERWRITE_PERMISSION_FIELD_CONVERTERS,
    'target': (validate_target, partial_func(put_target, include_internals = True)),
    'target_id': (validate_target_id, put_target_id),
    'target_type': (validate_target_type, put_target_type),
}
