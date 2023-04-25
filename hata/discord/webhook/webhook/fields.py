__all__ = ()

from ...field_parsers import (
    default_entity_parser_factory, entity_id_parser_factory, force_string_parser_factory,
    nullable_entity_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    default_entity_putter_factory, entity_id_optional_putter_factory, force_string_putter_factory,
    nullable_entity_optional_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    default_entity_validator, entity_id_validator_factory, force_string_validator_factory,
    nullable_entity_validator_factory, preinstanced_validator_factory
)
from ...user import ClientUserBase, User, ZEROUSER

from ..webhook_source_channel import WebhookSourceChannel
from ..webhook_source_guild import WebhookSourceGuild

from .preinstanced import WebhookType

# application_id

parse_application_id = entity_id_parser_factory('application_id')
put_application_id_into = entity_id_optional_putter_factory('application_id')
validate_application_id = entity_id_validator_factory('application_id', NotImplemented, include = 'Application')

# channel_id

parse_channel_id = entity_id_parser_factory('channel_id')
put_channel_id_into = entity_id_optional_putter_factory('channel_id')
validate_channel_id = entity_id_validator_factory('channel_id', NotImplemented, include = 'Channel')

# source_channel

parse_source_channel = nullable_entity_parser_factory('source_channel', WebhookSourceChannel)
put_source_channel_into = nullable_entity_optional_putter_factory('source_channel', WebhookSourceChannel)
validate_source_channel = nullable_entity_validator_factory('source_channel', WebhookSourceChannel)

# source_guild

parse_source_guild = nullable_entity_parser_factory('source_guild', WebhookSourceGuild)
put_source_guild_into = nullable_entity_optional_putter_factory('source_guild', WebhookSourceGuild)
validate_source_guild = nullable_entity_validator_factory('source_guild', WebhookSourceGuild)

# token

parse_token = force_string_parser_factory('token')
put_token_into = force_string_putter_factory('token')
validate_token = force_string_validator_factory('token', 0, 4096)

# type

parse_type = preinstanced_parser_factory('type', WebhookType, WebhookType.none)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('webhook_type', WebhookType)

# user

parse_user = default_entity_parser_factory('user', User, default = ZEROUSER)
put_user_into = default_entity_putter_factory('user', ClientUserBase, ZEROUSER)
validate_user = default_entity_validator('user', ClientUserBase, default = ZEROUSER)
