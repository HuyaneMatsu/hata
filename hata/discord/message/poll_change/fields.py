__all__ = ()

from ...field_validators import nullable_entity_validator_factory
from ...poll import Poll

from ..poll_update import PollUpdate


# added

validate_added = nullable_entity_validator_factory('added', Poll)


# updated

validate_updated = nullable_entity_validator_factory('updated', PollUpdate)


# removed

validate_removed = nullable_entity_validator_factory('removed', Poll)
