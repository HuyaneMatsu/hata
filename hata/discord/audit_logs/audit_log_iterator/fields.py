__all__ = ()


from ...field_validators import entity_id_validator_factory, preinstanced_validator_factory
from ...user import ClientUserBase

from ..audit_log.fields import validate_guild_id
from ..audit_log_entry import AuditLogEntryType


# user_id

validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)


# entry_type

validate_entry_type = preinstanced_validator_factory('entry_type', AuditLogEntryType)
