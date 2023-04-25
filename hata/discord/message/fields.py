__all__ = ()

from ..field_parsers import nullable_entity_parser_factory
from ..field_putters import nullable_entity_optional_putter_factory
from ..field_validators import nullable_entity_validator_factory

from .message_role_subscription import MessageRoleSubscription

# role_subscription

parse_role_subscription = nullable_entity_parser_factory('role_subscription_data', MessageRoleSubscription)
put_role_subscription_into = nullable_entity_optional_putter_factory(
    'role_subscription_data', MessageRoleSubscription
)
validate_role_subscription = nullable_entity_validator_factory('role_subscription', MessageRoleSubscription)
